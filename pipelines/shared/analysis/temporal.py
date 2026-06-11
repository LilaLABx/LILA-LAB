"""Temporal coverage and source-boundary diagnostics.

Detects coverage gaps in monthly time series and uses Kolmogorov-Smirnov
tests to identify distribution shifts at source boundaries — critical for
multi-source corpora where a scraper/source change can create spurious
narrative signals.

Typical usage::

    from shared.analysis.temporal import coverage_diagnostics, detect_source_boundary

    diag = coverage_diagnostics(df, date_col="date", source_col="newspaper")
    boundary = detect_source_boundary(df, date_col="date", source_col="newspaper",
                                      metric_col="article_length")
"""

from __future__ import annotations

import logging
from collections import defaultdict
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import ks_2samp

from ..io import write_json

logger = logging.getLogger(__name__)


# ── Temporal coverage ─────────────────────────────────────────────────


def coverage_diagnostics(
    df: pd.DataFrame,
    date_col: str = "date",
    source_col: str | None = None,
    metrics: list[str] | None = None,
) -> dict[str, Any]:
    """Analyse temporal coverage of a corpus.

    Parameters
    ----------
    df:
        Corpus DataFrame with a date column.
    date_col:
        Name of the date column.
    source_col:
        Optional source/newspaper column for per-source coverage.
    metrics:
        Optional list of numeric column names to track over time
        (e.g. ``["article_length"]``).

    Returns
    -------
    dict
        Keys: ``date_range``, ``monthly_coverage``, ``gaps``,
        ``per_source_years`` (if source_col given),
        ``metric_trends`` (if metrics given).
    """
    dates = pd.to_datetime(df[date_col], errors="coerce").dropna()
    if len(dates) == 0:
        return {"error": "No valid dates found"}

    monthly = dates.dt.to_period("M").value_counts().sort_index()
    all_months = pd.period_range(monthly.index.min(), monthly.index.max(), freq="M")
    gaps = [str(m) for m in all_months if m not in monthly.index]

    result: dict[str, Any] = {
        "date_range": {
            "start": str(monthly.index.min()),
            "end": str(monthly.index.max()),
        },
        "n_months_total": len(all_months),
        "n_months_with_data": len(monthly),
        "coverage_pct": round(len(monthly) / len(all_months) * 100, 1),
        "n_gaps": len(gaps),
        "gaps": gaps[:30],  # cap reporting
        "max_gap_months": _max_consecutive_gap(gaps),
        "monthly_statistics": {
            "mean_articles_per_month": round(float(monthly.mean()), 1),
            "median_articles_per_month": float(monthly.median()),
            "std_articles_per_month": round(float(monthly.std()), 1),
            "min_articles_month": int(monthly.min()),
            "max_articles_month": int(monthly.max()),
        },
    }

    # Per-source coverage
    if source_col and source_col in df.columns:
        years = dates.dt.year
        cross = df.assign(_year=years).pivot_table(
            index="_year", columns=source_col, aggfunc="size", fill_value=0
        )
        result["per_source_coverage"] = {
            str(src): {
                "years_active": int((cross[src] > 0).sum()),
                "total_articles": int(cross[src].sum()),
                "first_year": int(cross[src][cross[src] > 0].index.min()) if (cross[src] > 0).any() else None,
                "last_year": int(cross[src][cross[src] > 0].index.max()) if (cross[src] > 0).any() else None,
            }
            for src in cross.columns
        }

    # Metric trends
    if metrics:
        year_month = dates.dt.to_period("M")
        trends = {}
        for m in metrics:
            if m in df.columns:
                grouped = df.assign(_ym=year_month).groupby("_ym")[m].agg(["mean", "std", "count"])
                trends[m] = {
                    "overall_mean": round(float(grouped["mean"].mean()), 2),
                    "overall_std": round(float(grouped["mean"].std()), 2),
                    "trend_direction": "increasing" if _is_trending(grouped["mean"]) else (
                        "decreasing" if _is_trending(-grouped["mean"]) else "stable"
                    ),
                }
        result["metric_trends"] = trends

    logger.info(
        "Coverage: %d/%d months (%.0f%%), %d gaps, max gap=%d months",
        result["n_months_with_data"],
        result["n_months_total"],
        result["coverage_pct"],
        result["n_gaps"],
        result["max_gap_months"],
    )
    return result


# ── Source-boundary diagnostic ───────────────────────────────────────


def detect_source_boundary(
    df: pd.DataFrame,
    date_col: str = "date",
    source_col: str = "source",
    metric_col: str = "article_length",
    *,
    alpha: float = 0.05,
    min_samples: int = 30,
) -> list[dict[str, Any]]:
    """Detect distribution shifts at source-transition boundaries.

    When a corpus switches from one source to another (e.g. Potrika→BNAD
    at 2020/2021), this test checks whether article-level metrics change
    significantly — which would create a spurious signal in downstream
    indices.

    Uses a two-sample Kolmogorov-Smirnov test.

    Parameters
    ----------
    df:
        Corpus DataFrame.
    date_col:
        Date column.
    source_col:
        Source/newspaper column.
    metric_col:
        Numeric column to test (e.g. article length, sentiment score).
    alpha:
        Significance threshold (default 0.05).
    min_samples:
        Minimum samples per source for a valid KS test.

    Returns
    -------
    list[dict]
        Each entry::

            {"source_a": str, "source_b": str,
             "transition_year": int,
             "ks_statistic": float, "p_value": float,
             "significant": bool,
             "n_a": int, "n_b": int,
             "mean_a": float, "mean_b": float}
    """
    if metric_col not in df.columns:
        logger.warning("Metric column '%s' not found — using article length heuristic", metric_col)
        metric_col = _resolve_metric(df)

    dates = pd.to_datetime(df[date_col], errors="coerce")
    years = dates.dt.year
    df_temp = df.assign(_year=years, _metric=df[metric_col]).dropna(subset=["_year", "_metric"])

    # Find year-over-year source transitions
    transitions: list[dict[str, Any]] = []
    sources_by_year = (
        df_temp.groupby("_year")[source_col]
        .apply(lambda x: set(x.dropna().unique()))
        .to_dict()
    )

    sorted_years = sorted(sources_by_year.keys())
    for i in range(len(sorted_years) - 1):
        y1, y2 = sorted_years[i], sorted_years[i + 1]
        srcs1 = sources_by_year[y1]
        srcs2 = sources_by_year[y2]
        leaving = srcs1 - srcs2
        entering = srcs2 - srcs1

        if not leaving and not entering:
            continue

        for s1 in leaving or srcs1:
            for s2 in entering or srcs2:
                data1 = df_temp[(df_temp["_year"] == y1) & (df_temp[source_col] == s1)]["_metric"]
                data2 = df_temp[(df_temp["_year"] == y2) & (df_temp[source_col] == s2)]["_metric"]
                if len(data1) < min_samples or len(data2) < min_samples:
                    continue
                stat, p = ks_2samp(data1, data2)
                transitions.append({
                    "source_a": str(s1),
                    "source_b": str(s2),
                    "transition_year": int(y2),
                    "ks_statistic": round(stat, 4),
                    "p_value": round(p, 6),
                    "significant": bool(p < alpha),
                    "n_a": int(len(data1)),
                    "n_b": int(len(data2)),
                    "mean_a": round(float(data1.mean()), 2),
                    "mean_b": round(float(data2.mean()), 2),
                })

    if transitions:
        n_sig = sum(1 for t in transitions if t["significant"])
        logger.info("Found %d source transitions, %d significant (p<%.2f)", len(transitions), n_sig, alpha)
    else:
        logger.info("No source transitions detected (check source_col='%s')", source_col)

    return transitions


# ── Helpers ───────────────────────────────────────────────────────────


def _max_consecutive_gap(gaps: list[str]) -> int:
    """Return the longest run of consecutive missing months."""
    if not gaps:
        return 0
    from datetime import datetime

    dates = sorted(datetime.strptime(g, "%Y-%m") for g in gaps)
    max_run = 1
    current = 1
    for i in range(1, len(dates)):
        diff = (dates[i].year - dates[i - 1].year) * 12 + (dates[i].month - dates[i - 1].month)
        if diff == 1:
            current += 1
        else:
            max_run = max(max_run, current)
            current = 1
    return max(max_run, current)


def _is_trending(series: pd.Series, threshold: float = 0.3) -> bool:
    """Simple linear trend detection via correlation with time index."""
    if len(series) < 3:
        return False
    x = np.arange(len(series))
    corr = np.corrcoef(x, series.values)[0, 1]
    return abs(corr) > threshold and corr > 0


def _resolve_metric(df: pd.DataFrame) -> str:
    """Find a reasonable numeric column for metric analysis."""
    candidates = ["article_length", "text_length", "length", "n_tokens",
                   "word_count", "words", "sentiment", "probability", "score"]
    for c in candidates:
        if c in df.columns and pd.api.types.is_numeric_dtype(df[c]):
            return c
    # Fallback: first float column
    for c in df.columns:
        if pd.api.types.is_float_dtype(df[c]):
            return c
    raise ValueError("No suitable numeric column found for source-boundary diagnostic")


def run_temporal(
    df: pd.DataFrame,
    output_dir: str | Path,
    date_col: str = "date",
    source_col: str | None = "source",
    metric_col: str | None = None,
) -> dict[str, Any]:
    """Run temporal diagnostics and write results to *output_dir*.

    Returns combined dict with ``coverage`` and ``source_boundaries`` keys.
    """
    from pathlib import Path

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    coverage = coverage_diagnostics(df, date_col=date_col, source_col=source_col)
    boundaries = detect_source_boundary(df, date_col=date_col, source_col=source_col or "",
                                        metric_col=metric_col or "article_length")

    result = {"coverage": coverage, "source_boundaries": boundaries}
    write_json(out / "temporal_diagnostics.json", result)

    # Report
    lines = [
        "═" * 60,
        "TEMPORAL DIAGNOSTICS",
        "═" * 60,
    ]
    cov = coverage
    lines.append(f"  Period:       {cov.get('date_range', {}).get('start')} → {cov.get('date_range', {}).get('end')}")
    lines.append(f"  Coverage:     {cov.get('n_months_with_data')}/{cov.get('n_months_total')} months ({cov.get('coverage_pct')}%)")
    lines.append(f"  Gaps:         {cov.get('n_gaps')} (max consecutive: {cov.get('max_gap_months')})")
    if boundaries:
        lines.append(f"  Source transitions: {len(boundaries)}")
        sig_count = sum(1 for b in boundaries if b["significant"])
        lines.append(f"  Significant shifts: {sig_count}")
        for b in boundaries[:5]:
            lines.append(f"    {b['source_a']}→{b['source_b']} ({b['transition_year']}): "
                         f"KS={b['ks_statistic']} p={b['p_value']} {'⚠️' if b['significant'] else '✓'}")
    lines.append("═" * 60)
    out.joinpath("temporal_report.md").write_text("\n".join(lines) + "\n")

    logger.info("Temporal diagnostics written to %s", out)
    return result
