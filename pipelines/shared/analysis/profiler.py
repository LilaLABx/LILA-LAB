"""Dataset profiler — descriptive statistics for any XENI corpus.

Computes article counts, text length distributions, category/source/temporal
coverage, and data quality metrics. Language-agnostic — works with any
DataFrame that has text, date, category, and source columns.

Typical usage::

    from shared.analysis.profiler import corpus_profile

    df = pd.read_csv("articles.csv")
    config = {"text_column": "content", "date_column": "date",
              "category_column": "category", "source_column": "newspaper"}
    profile = corpus_profile(df, config)
"""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from ..io import write_json

logger = logging.getLogger(__name__)

# ── Config helpers ────────────────────────────────────────────────────


def _resolve_column(df: pd.DataFrame, candidates: list[str]) -> str | None:
    """Return the first column name from *candidates* that exists in *df*."""
    return next((c for c in candidates if c in df.columns), None)


def _normalise_text_col(col: str, config: dict) -> str:
    """Return the effective text column — honour config override, else guess."""
    return config.get("text_column") or _resolve_column(
        df := pd.DataFrame(),  # placeholder, unused here
        []  # caller handles fallback
    ) or col


# ── Core profile ──────────────────────────────────────────────────────


def corpus_profile(
    df: pd.DataFrame,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Compute a full descriptive profile of a corpus DataFrame.

    Parameters
    ----------
    df:
        Corpus DataFrame with at least a text column.
    config:
        Dictionary with optional keys:
        - ``text_column``: name of the column containing article text.
        - ``date_column``: name of the date column (auto-detected if omitted).
        - ``category_column``: name of the category column.
        - ``source_column``: name of the source / newspaper column.
        - ``sample_size``: max rows to load for expensive stats (default 50000).

    Returns
    -------
    dict
        Nested dictionary with keys: ``n_articles``, ``date_range``,
        ``by_year``, ``by_source``, ``by_category``, ``text_length``,
        ``quality``, ``date_coverage``, ``source_overlap``.
    """
    cfg = config or {}
    text_col = (
        cfg.get("text_column")
        or _resolve_column(df, ["text", "content", "article", "body", "article_text", "headline", "Title", "Content", "News"])
        or df.columns[0]
    )
    date_col = cfg.get("date_column") or _resolve_column(
        df, ["date", "Date", "Time", "publication_date", "month", "year_month", "timestamp"]
    )
    cat_col = cfg.get("category_column") or _resolve_column(
        df, ["category", "Category", "class", "label", "topic", "section"]
    )
    src_col = cfg.get("source_column") or _resolve_column(
        df, ["source", "Source", "newspaper", "Newspaper", "publication", "outlet"]
    )

    sample_size = cfg.get("sample_size", 50_000)
    total = len(df)
    logger.info("Profiling %s rows — text_col=%s date_col=%s cat_col=%s src_col=%s",
                total, text_col, date_col, cat_col, src_col)

    # ── 1. Basic counts ────────────────────────────────────────────
    result: dict[str, Any] = {"n_articles": total}

    # ── 2. Text length ─────────────────────────────────────────────
    lengths = df[text_col].dropna().apply(
        lambda t: len(str(t).split()) if isinstance(t, str) else 0
    )
    result["text_length"] = {
        "mean_words": round(float(lengths.mean()), 1) if len(lengths) else None,
        "median_words": float(lengths.median()) if len(lengths) else None,
        "std_words": round(float(lengths.std()), 1) if len(lengths) else None,
        "min_words": int(lengths.min()) if len(lengths) else None,
        "max_words": int(lengths.max()) if len(lengths) else None,
        "q25_words": float(lengths.quantile(0.25)) if len(lengths) else None,
        "q75_words": float(lengths.quantile(0.75)) if len(lengths) else None,
    }

    # ── 3. Quality flags ────────────────────────────────────────────
    empty_texts = df[text_col].apply(
        lambda t: not (isinstance(t, str) and t.strip())
    ).sum()
    missing_dates = df[date_col].isna().sum() if date_col else 0
    result["quality"] = {
        "empty_texts": int(empty_texts),
        "empty_texts_pct": round(float(empty_texts / total * 100), 2) if total else 0.0,
        "missing_dates": int(missing_dates) if date_col else None,
        "missing_dates_pct": round(float(missing_dates / total * 100), 2) if date_col and total else None,
    }

    # ── 4. Date range & temporal coverage ──────────────────────────
    if date_col:
        dates = pd.to_datetime(df[date_col], errors="coerce")
        valid_dates = dates.dropna()
        result["date_range"] = {
            "start": str(valid_dates.min().date()) if len(valid_dates) else None,
            "end": str(valid_dates.max().date()) if len(valid_dates) else None,
            "n_days": (valid_dates.max() - valid_dates.min()).days if len(valid_dates) else None,
        }

        # Per-year breakdown
        years = valid_dates.dt.year.value_counts().sort_index()
        result["by_year"] = [
            {"year": int(k), "n_articles": int(v)} for k, v in years.items()
        ]

        # Monthly coverage — detect gaps
        monthly = valid_dates.dt.to_period("M").value_counts().sort_index()
        if len(monthly) > 0:
            all_months = pd.period_range(
                start=monthly.index.min(), end=monthly.index.max(), freq="M"
            )
            gaps = [str(m) for m in all_months if m not in monthly.index]
            result["date_coverage"] = {
                "n_months": len(monthly),
                "n_gaps": len(gaps),
                "gaps": gaps[:20],  # cap display
                "mean_articles_per_month": round(float(monthly.mean()), 1),
            }
        else:
            result["date_coverage"] = {"n_months": 0, "n_gaps": 0, "gaps": []}
    else:
        result["date_range"] = None
        result["by_year"] = []
        result["date_coverage"] = {"n_months": 0, "n_gaps": 0, "gaps": []}

    # ── 5. Per-source breakdown ─────────────────────────────────────
    if src_col and src_col in df.columns:
        src_counts = df[src_col].value_counts()
        result["by_source"] = [
            {"source": str(k), "n_articles": int(v)}
            for k, v in src_counts.items()
        ]
        result["n_sources"] = len(src_counts)
    else:
        result["by_source"] = []
        result["n_sources"] = 0

    # ── 6. Per-category breakdown ───────────────────────────────────
    if cat_col and cat_col in df.columns:
        cat_counts = df[cat_col].value_counts()
        result["by_category"] = [
            {"category": str(k), "n_articles": int(v)}
            for k, v in cat_counts.items()
        ]
        result["n_categories"] = len(cat_counts)
    else:
        result["by_category"] = []
        result["n_categories"] = 0

    # ── 7. Source overlap (multi-year source coverage) ──────────────
    if date_col and src_col and src_col in df.columns and date_col in df.columns:
        dates_valid = pd.to_datetime(df[date_col], errors="coerce")
        df_temp = df.assign(_year=dates_valid.dt.year).dropna(subset=["_year"])
        if len(df_temp):
            cross = df_temp.pivot_table(
                index="_year", columns=src_col, aggfunc="size", fill_value=0
            )
            result["source_overlap"] = {
                "years_covered": [int(y) for y in cross.index],
                "sources_per_year": [int((cross > 0).sum(axis=1)[y]) for y in cross.index],
            }
        else:
            result["source_overlap"] = None
    else:
        result["source_overlap"] = None

    logger.info("Profile complete — %d articles, %d sources, %d categories",
                total, result.get("n_sources", 0), result.get("n_categories", 0))
    return result


def run_profile(
    df: pd.DataFrame,
    output_dir: str | Path,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Compute corpus profile and write result to *output_dir* as JSON.

    Returns the profile dict (same as :func:`corpus_profile`).
    """
    from pathlib import Path

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    profile = corpus_profile(df, config)
    write_json(out / "profile_summary.json", profile)

    # Human-readable text summary
    lines = [
        "═" * 60,
        "CORPUS PROFILE",
        "═" * 60,
        f"  Articles:     {profile['n_articles']:,}",
    ]
    if profile.get("date_range") and profile["date_range"].get("start"):
        lines.append(f"  Period:       {profile['date_range']['start']} → {profile['date_range']['end']}")
        lines.append(f"  Span:         {profile['date_range']['n_days']} days")
    if profile.get("n_sources"):
        lines.append(f"  Sources:      {profile['n_sources']}")
    if profile.get("n_categories"):
        lines.append(f"  Categories:   {profile['n_categories']}")
    if profile.get("text_length"):
        tl = profile["text_length"]
        lines.append(f"  Words/art:    mean={tl.get('mean_words')} median={tl.get('median_words')}")
    if profile.get("quality"):
        q = profile["quality"]
        lines.append(f"  Empty texts:  {q.get('empty_texts')} ({q.get('empty_texts_pct')}%)")
        if q.get("missing_dates") is not None:
            lines.append(f"  Missing dates: {q.get('missing_dates')} ({q.get('missing_dates_pct')}%)")
    lines.append(f"  Output:       {out / 'profile_summary.json'}")
    lines.append("═" * 60)
    out.joinpath("profile_report.md").write_text("\n".join(lines) + "\n")

    logger.info("Profile written to %s", out)
    return profile
