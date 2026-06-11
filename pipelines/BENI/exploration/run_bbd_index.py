#!/usr/bin/env python3
"""BBD-style keyword index for BENI.

Counts articles per month that match the BBD triple categories
(Economy ∩ Policy ∩ Narrative), normalises per source, and
produces a monthly index standardised to mean=100.

Usage::

    python run_bbd_index.py                          # full corpus
    python run_bbd_index.py --sample 10000            # quick test
    python run_bbd_index.py --no-normalise            # raw shares only
    python run_bbd_index.py --output outputs/bbd_index
"""

from __future__ import annotations

import argparse
import logging
import sys
import time
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("bbd_index")

_HERE = Path(__file__).resolve().parent
_PIPELINES = _HERE.parents[1]
sys.path.insert(0, str(_PIPELINES))

import numpy as np
import pandas as pd

from shared.analysis.bengali_economic_keywords import (
    ECONOMY_KEYWORDS,
    POLICY_KEYWORDS,
    NARRATIVE_KEYWORDS,
    POSITIVE_SENTIMENT,
    NEGATIVE_SENTIMENT,
    make_category_regex,
)
from shared.io import read_zst_csv

# ═══════════════════════════════════════════════════════════════════════
#  Config
# ═══════════════════════════════════════════════════════════════════════

CORPUS_PATH = (
    _HERE
    / "../../../dataset/BENI/beni-v1/data/processed/"
    / "beni_unified_articles_deduped.csv.zst"
)

OUTPUT_DIR = _HERE / "outputs" / "06_bbd_index"

# Columns to load (keeps memory low)
USE_COLS = [
    "article_id",
    "dataset_source",
    "newspaper",
    "publication_date",
    "year_month",
    "text_clean",
    "text",
]

# ═══════════════════════════════════════════════════════════════════════
#  Pre-compiled category patterns
# ═══════════════════════════════════════════════════════════════════════

# Use word_boundary=False for Bangla (combining marks break \b)
_E_RE = make_category_regex(ECONOMY_KEYWORDS, word_boundary=False)
_P_RE = make_category_regex(POLICY_KEYWORDS, word_boundary=False)
_N_RE = make_category_regex(NARRATIVE_KEYWORDS, word_boundary=False)
_SP_RE = make_category_regex(POSITIVE_SENTIMENT, word_boundary=False)
_SN_RE = make_category_regex(NEGATIVE_SENTIMENT, word_boundary=False)


# ═══════════════════════════════════════════════════════════════════════
#  Classification
# ═══════════════════════════════════════════════════════════════════════


def classify_batch(df: pd.DataFrame, text_col: str = "text_clean") -> pd.DataFrame:
    """Vectorised BBD triple + sentiment classification.

    Uses ``pandas.Series.str.contains`` instead of row-by-row iteration
    for a 1000× speedup on the full 933K corpus.
    """
    n = len(df)
    logger.info("Classifying %d articles in BBD categories (vectorised) ...", n)

    t0 = time.time()
    t = df[text_col].fillna("").astype(str).str.lower()

    patterns = {
        "E": _E_RE,
        "P": _P_RE,
        "N": _N_RE,
        "Spos": _SP_RE,
        "Sneg": _SN_RE,
    }

    results: dict[str, pd.Series] = {}
    for label, regex in patterns.items():
        results[label] = t.str.contains(regex, regex=True, na=False)

    elapsed = time.time() - t0
    e_rate = results["E"].mean() * 100
    p_rate = results["P"].mean() * 100
    n_rate = results["N"].mean() * 100
    triple = (results["E"] & results["P"] & results["N"]).mean() * 100
    logger.info(
        "Classification done in %.1fs — E:%.1f%% P:%.1f%% N:%.1f%% E∩P∩N:%.1f%%",
        elapsed, e_rate, p_rate, n_rate, triple,
    )

    out = pd.DataFrame(results)
    out["year_month"] = df["year_month"].values
    out["dataset_source"] = df["dataset_source"].values
    out["newspaper"] = df["newspaper"].values
    out["article_id"] = df["article_id"].values
    return out


# ═══════════════════════════════════════════════════════════════════════
#  Monthly aggregation
# ═══════════════════════════════════════════════════════════════════════


def build_monthly_index(
    cls_df: pd.DataFrame,
    normalise: bool = True,
    method: str = "vw_share",
    min_articles_per_month: int = 10,
    base_period_years: tuple[int, int] | None = None,
) -> pd.DataFrame:
    """Aggregate article-level classifications into a monthly BBD index.

    Parameters
    ----------
    cls_df:
        DataFrame with year_month, dataset_source, and boolean
        category columns (E, P, N, Spos, Sneg).
    normalise:
        If True, standardise the final index to mean=100.
    method:
        ``"vw_share"`` — volume-weighted triple share (simple, robust).
        ``"zscore"`` — per-source z-score, then volume-weighted average
        (standard BBD approach, requires sufficient sources/months).
    min_articles_per_month:
        Minimum articles for a source-month to be included.
    base_period_years:
        (start, end) inclusive years for standardisation base.

    Returns
    -------
    index_df, source_summary
    """
    cls_df["is_triple"] = cls_df["E"] & cls_df["P"] & cls_df["N"]
    cls_df["sentiment_balance"] = (
        cls_df["Spos"].astype(int) - cls_df["Sneg"].astype(int)
    )

    monthly = (
        cls_df.groupby(["year_month", "dataset_source"], as_index=False)
        .agg(
            n_articles=("article_id", "count"),
            n_economic=("E", "sum"),
            n_triple=("is_triple", "sum"),
            sentiment_balance=("sentiment_balance", "sum"),
            pos_count=("Spos", "sum"),
            neg_count=("Sneg", "sum"),
        )
    )

    monthly["economic_share"] = monthly["n_economic"] / monthly["n_articles"]
    monthly["triple_share"] = monthly["n_triple"] / monthly["n_articles"]
    monthly["sentiment_per_article"] = (
        monthly["sentiment_balance"] / monthly["n_articles"]
    )

    before = len(monthly)
    monthly = monthly[monthly["n_articles"] >= min_articles_per_month].copy()
    logger.info(
        "Monthly aggregation: %d source-months (%d filtered, min=%d articles)",
        len(monthly), before - len(monthly), min_articles_per_month,
    )

    if not normalise:
        return monthly

    if method == "zscore":
        monthly = _per_source_zscore(monthly, base_period_years)
    # else (vw_share): use triple_share directly

    index = (
        monthly.groupby("year_month")
        .agg(
            n_articles=("n_articles", "sum"),
            n_economic=("n_economic", "sum"),
            n_triple=("n_triple", "sum"),
            economic_share=("economic_share", "mean"),
            triple_share=("triple_share", "mean"),
            sentiment_balance=("sentiment_balance", "sum"),
            beni_raw=("zscore" if method == "zscore" else "triple_share", "sum"
                       if method == "zscore" else "mean"),
        )
        .reset_index()
        .sort_values("year_month")
    )

    base = index
    if base_period_years:
        y1, y2 = base_period_years
        base = index[
            index["year_month"].str[:4].astype(int).between(y1, y2)
        ]

    mu = base["beni_raw"].mean()
    sigma = base["beni_raw"].std()
    index["beni_index"] = 100.0 + (index["beni_raw"] - mu) / sigma * 10.0

    source_summary = (
        monthly.groupby("dataset_source")
        .agg(
            n_months=("year_month", "count"),
            mean_share=("triple_share", "mean"),
            std_share=("triple_share", "std"),
        )
        .reset_index()
    )

    logger.info(
        "BENI index (method=%s): %d months, mean=%.1f, std=%.1f, "
        "min=%.1f, max=%.1f",
        method, len(index),
        index["beni_index"].mean(),
        index["beni_index"].std(),
        index["beni_index"].min(),
        index["beni_index"].max(),
    )

    return index, source_summary


def _per_source_zscore(
    monthly: pd.DataFrame,
    base_period_years: tuple[int, int] | None = None,
) -> pd.DataFrame:
    """Per-source z-score normalisation of triple_share (BBD standard)."""
    base = monthly
    if base_period_years:
        y1, y2 = base_period_years
        base = monthly[
            monthly["year_month"].str[:4].astype(int).between(y1, y2)
        ]

    source_stats = (
        base.groupby("dataset_source")["triple_share"]
        .agg(["mean", "std"])
        .rename(columns={"mean": "mu", "std": "sigma"})
    )
    global_std = base["triple_share"].std()
    min_std = max(0.005, global_std * 0.1)
    source_stats["sigma"] = source_stats["sigma"].clip(lower=min_std)

    monthly = monthly.merge(source_stats, on="dataset_source", how="left")
    monthly["zscore"] = (
        (monthly["triple_share"] - monthly["mu"]) / monthly["sigma"]
    ).clip(-3.0, 3.0)

    volume_weights = (
        monthly.groupby("year_month")["n_articles"].transform("sum")
    )
    monthly["zscore"] *= monthly["n_articles"] / volume_weights

    logger.info(
        "Per-source z-score: %d source-months, %d sources  "
        "(global_std=%.4f, min_std=%.4f)",
        len(base), len(source_stats), global_std, min_std,
    )
    return monthly


# ═══════════════════════════════════════════════════════════════════════
#  Main
# ═══════════════════════════════════════════════════════════════════════


def main():
    parser = argparse.ArgumentParser(description="BENI BBD index")
    parser.add_argument(
        "--sample", type=int, default=None,
        help="Process only N articles (for testing)",
    )
    parser.add_argument(
        "--method", default="vw_share", choices=["vw_share", "zscore"],
        help="Normalisation method: vw_share (simple, robust) or zscore (BBD standard)",
    )
    parser.add_argument(
        "--no-normalise", action="store_true",
        help="Skip normalisation, output raw shares only",
    )
    parser.add_argument(
        "--output", type=Path, default=OUTPUT_DIR,
        help="Output directory (default: outputs/06_bbd_index)",
    )
    parser.add_argument(
        "--text-col", default="text_clean",
        choices=["text_clean", "text"],
        help="Text column to classify (default: text_clean)",
    )
    parser.add_argument(
        "--base-period", type=str, default=None,
        help="Normalisation base as 'YYYY-YYYY' (default: entire series)",
    )
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # ── Load corpus ─────────────────────────────────────────────────
    logger.info("Loading corpus from %s", CORPUS_PATH)
    df = read_zst_csv(CORPUS_PATH, usecols=USE_COLS)
    original_n = len(df)

    # Drop rows without text
    before = len(df)
    df = df.dropna(subset=[args.text_col]).reset_index(drop=True)
    logger.info(
        "Loaded %d articles (%d dropped for missing text)",
        original_n, before - len(df),
    )
    logger.info(
        "Sources: %s  |  Date range: %s — %s",
        df["dataset_source"].unique(),
        df["publication_date"].min(),
        df["publication_date"].max(),
    )

    # Sample if requested
    if args.sample and args.sample < len(df):
        df = df.sample(n=args.sample, random_state=42).reset_index(drop=True)
        logger.info("Sampled %d articles", len(df))

    # ── Classify ────────────────────────────────────────────────────
    cls_df = classify_batch(df, text_col=args.text_col)

    # ── Aggregate ────────────────────────────────────────────────────
    base_period = None
    if args.base_period:
        parts = args.base_period.split("-")
        base_period = (int(parts[0]), int(parts[1]))

    result = build_monthly_index(
        cls_df,
        normalise=not args.no_normalise,
        method=args.method,
        base_period_years=base_period,
    )

    if args.no_normalise:
        result.to_csv(output_dir / "bbd_raw_shares.csv", index=False)
        logger.info("Raw shares → %s", output_dir / "bbd_raw_shares.csv")
        return

    index_df, source_summary = result

    # ── Save ─────────────────────────────────────────────────────────
    index_df.to_csv(output_dir / "beni_bbd_index.csv", index=False)
    source_summary.to_csv(output_dir / "bbd_source_stats.csv", index=False)

    # Quick summary
    summary = {
        "n_articles": len(df),
        "n_months": len(index_df),
        "date_range": {
            "start": index_df["year_month"].iloc[0],
            "end": index_df["year_month"].iloc[-1],
        },
        "mean_index": round(float(index_df["beni_index"].mean()), 1),
        "std_index": round(float(index_df["beni_index"].std()), 1),
        "mean_economic_share": round(float(index_df["economic_share"].mean()) * 100, 1),
        "n_sources": len(source_summary),
        "sources": source_summary.to_dict(orient="records"),
    }

    import json
    (output_dir / "bbd_index_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    logger.info("BENI BBD index written to %s", output_dir)
    logger.info("Summary: %d months, mean_index=%.1f, std=%.1f",
                 len(index_df), summary["mean_index"], summary["std_index"])
    logger.info("Sources: %s", [s["dataset_source"] for s in summary["sources"]])

    # Print top/bottom months
    print("\n═══ Top 5 BBD Index Months ═══")
    for _, row in index_df.nlargest(5, "beni_index").iterrows():
        print(f"  {row['year_month']}: {row['beni_index']:.1f}  "
              f"(share={row['triple_share']:.1%}, n={int(row['n_articles'])})")

    print("\n═══ Bottom 5 BBD Index Months ═══")
    for _, row in index_df.nsmallest(5, "beni_index").iterrows():
        print(f"  {row['year_month']}: {row['beni_index']:.1f}  "
              f"(share={row['triple_share']:.1%}, n={int(row['n_articles'])})")

    print()


if __name__ == "__main__":
    main()
