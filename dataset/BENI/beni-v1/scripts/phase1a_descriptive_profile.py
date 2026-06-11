#!/usr/bin/env python3
"""Phase 1A — Descriptive Profiling of the BENI unified corpus.

Reads the deduped unified corpus (beni_unified_articles_deduped.csv.zst) and
produces:

  1. Article counts per year (table + bar chart)
  2. Articles per newspaper over time (stacked area)
  3. Articles per harmonised category over time
  4. Source stability at the 2020/2021 Potrika→BNAD boundary
  5. Text length distribution per category/year/source (boxplot + outlier count)

Outputs go to dataset/beni-v1/docs/exploration/phase1a/
"""

from __future__ import annotations

import gzip
import io
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "processed"
OUT_DIR = ROOT / "docs" / "exploration" / "phase1a"
SUMMARY_PATH = OUT_DIR / "summary.json"

FIELDNAMES = [
    "article_id", "dataset_source", "source_file", "newspaper",
    "publication_date", "year_month", "category_original", "category_harmonised",
    "headline", "text", "text_clean", "tags", "meta", "language",
    "text_hash", "headline_date_hash", "is_duplicate", "duplicate_group_id",
    "economic_seed_label", "economic_probability", "economic_prediction",
    "model_version", "release_version",
]

# ── helpers ──────────────────────────────────────────────────────────────

def find_corpus() -> Path:
    """Find the deduped corpus .zst file."""
    candidates = [
        DATA_DIR / "beni_unified_articles_deduped.csv.zst",
        DATA_DIR / "beni_unified_articles.csv.zst",
    ]
    for p in candidates:
        if p.exists():
            return p
    raise FileNotFoundError(
        f"No corpus zst found in {DATA_DIR}. "
        "Run build_beni_v1_articles.py first."
    )


def iter_zst_csv(path: Path) -> Iterable[dict]:
    """Yield rows from a zstd-compressed CSV."""
    proc = subprocess.Popen(
        ["zstd", "-q", "-dc", str(path)],
        stdout=subprocess.PIPE,
    )
    if proc.stdout is None:
        raise RuntimeError(f"Failed to open zstd stdout for {path}")
    try:
        text_stream = io.TextIOWrapper(proc.stdout, encoding="utf-8", newline="")
        reader = csv.DictReader(text_stream)
        yield from reader
    finally:
        if proc.stdout is not None:
            proc.stdout.close()
        proc.wait()


def load_sample(path: Path, n: int = 200_000) -> pd.DataFrame:
    """Load a sample of rows into a DataFrame for rapid iteration,
    then we stream the rest for counts we cannot sample.
    
    For 1.45M rows, sampling 200k gives ~14% coverage which is fine for
    most distribution plots.  We use full streaming for total counts.
    """
    # Read first N rows for quick stats
    rows = []
    for i, row in enumerate(iter_zst_csv(path)):
        if i >= n:
            break
        rows.append(row)
    df = pd.DataFrame(rows)
    # Parse dates
    df["publication_date"] = pd.to_datetime(df["publication_date"], errors="coerce")
    df["year"] = df["publication_date"].dt.year.astype("Int64")
    df["text_len"] = df["text"].fillna("").str.len()
    df["headline_len"] = df["headline"].fillna("").str.len()
    return df


def full_counts(path: Path) -> dict:
    """Stream the entire corpus and count dimensions we need."""
    counts = {
        "year": Counter(),
        "newspaper_year": Counter(),
        "category_year": Counter(),
        "source_year": Counter(),
        "category_newspaper_year": Counter(),
        "total_rows": 0,
    }
    for row in iter_zst_csv(path):
        year = row["publication_date"][:4]
        cat = row["category_harmonised"]
        src = row["dataset_source"]
        paper = row["newspaper"]
        counts["year"][year] += 1
        counts["newspaper_year"][f"{paper}|{year}"] += 1
        counts["category_year"][f"{cat}|{year}"] += 1
        counts["source_year"][f"{src}|{year}"] += 1
        counts["category_newspaper_year"][f"{cat}|{paper}|{year}"] += 1
        counts["total_rows"] += 1
    return counts


def savefig(fig, name: str):
    path = OUT_DIR / name
    fig.savefig(path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"  → {path}")


# ── plots ──────────────────────────────────────────────────────────────────

def plot_articles_per_year(year_counts: dict):
    years = sorted(year_counts.keys())
    counts = [year_counts[y] for y in years]
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ["#4C72B0" if int(y) <= 2020 else "#DD8452" for y in years]
    bars = ax.bar(years, counts, color=colors, edgecolor="white", linewidth=0.5)
    ax.set_title("Articles per Year (blue = Potrika, orange = BNAD)", fontsize=13)
    ax.set_ylabel("Article Count")
    ax.set_xlabel("Year")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    # Add value labels on bars
    for bar, count in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(counts)*0.01,
                f"{count:,}", ha="center", va="bottom", fontsize=8, rotation=45)
    fig.tight_layout()
    savefig(fig, "articles_per_year.png")


def plot_newspapers_over_time(newspaper_year_counts: dict):
    """Stacked area chart: articles per newspaper per year."""
    # Parse the compound key
    paper_years: dict[str, dict[str, int]] = {}
    for key, count in newspaper_year_counts.items():
        paper, year = key.split("|", 1)
        if paper not in paper_years:
            paper_years[paper] = {}
        paper_years[paper][year] = count

    years = sorted({y for py in paper_years.values() for y in py})
    papers = sorted(paper_years.keys())

    # Build matrix
    data = {}
    for paper in papers:
        data[paper] = [paper_years[paper].get(y, 0) for y in years]

    fig, ax = plt.subplots(figsize=(12, 6))
    bottom = np.zeros(len(years))
    colors = plt.cm.tab20(np.linspace(0, 1, len(papers)))
    for paper, color in zip(papers, colors):
        vals = data[paper]
        ax.bar(years, vals, bottom=bottom, label=paper, color=color, width=0.6)
        bottom += vals

    ax.set_title("Articles per Newspaper per Year", fontsize=13)
    ax.set_ylabel("Article Count")
    ax.set_xlabel("Year")
    ax.legend(fontsize=7, loc="upper left", ncol=2)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    fig.tight_layout()
    savefig(fig, "newspapers_per_year.png")


def plot_categories_over_time(category_year_counts: dict):
    """Stacked bar: articles per harmonised category per year."""
    cat_year_data: dict[str, dict[str, int]] = {}
    for key, count in category_year_counts.items():
        cat, year = key.split("|", 1)
        if cat not in cat_year_data:
            cat_year_data[cat] = {}
        cat_year_data[cat][year] = count

    years = sorted({y for cy in cat_year_data.values() for y in cy})
    # Exclude "other_or_unknown" from the main plot, show it separately
    main_cats = sorted(c for c in cat_year_data if c != "other_or_unknown")
    other_cat = "other_or_unknown"

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    for ax, cats, title in [
        (ax1, main_cats, "Articles per Category per Year (Known)"),
        (ax2, [other_cat], "Articles per Year (Other / Unknown Category)"),
    ]:
        bottom = np.zeros(len(years))
        colors = plt.cm.Set2(np.linspace(0, 1, len(cats))) if len(cats) > 1 else ["#999999"]
        for cat, color in zip(cats, colors):
            vals = [cat_year_data[cat].get(y, 0) for y in years]
            ax.bar(years, vals, bottom=bottom, label=cat, color=color, width=0.6)
            bottom += vals
        ax.set_title(title, fontsize=12)
        ax.set_ylabel("Article Count")
        ax.set_xlabel("Year")
        ax.legend(fontsize=8)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))

    fig.tight_layout()
    savefig(fig, "categories_per_year.png")


def plot_source_boundary(source_year_counts: dict):
    """Potrika vs BNAD article share per year — highlight the 2020/2021 break."""
    src_year: dict[str, dict[str, int]] = {}
    for key, count in source_year_counts.items():
        src, year = key.split("|", 1)
        if src not in src_year:
            src_year[src] = {}
        src_year[src][year] = count

    years = sorted({y for sy in src_year.values() for y in sy})
    sources = sorted(src_year.keys())

    fig, ax = plt.subplots(figsize=(10, 5))
    bottom = np.zeros(len(years))
    colors = {"potrika": "#4C72B0", "bnad": "#DD8452"}
    for src in sources:
        vals = [src_year[src].get(y, 0) for y in years]
        ax.bar(years, vals, bottom=bottom, label=src, color=colors.get(src, "#999999"), width=0.6)
        bottom += vals

    # Highlight the boundary
    ax.axvline(x="2020.5", color="red", linestyle="--", linewidth=1.5, label="Potrika→BNAD boundary")
    ax.set_title("Potrika vs BNAD Coverage per Year", fontsize=13)
    ax.set_ylabel("Article Count")
    ax.set_xlabel("Year")
    ax.legend()
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    fig.tight_layout()
    savefig(fig, "source_boundary.png")


def plot_text_length_distribution(df: pd.DataFrame):
    """Boxplot of text length per category, per year (sampled)."""
    # Per category
    fig, ax = plt.subplots(figsize=(10, 5))
    categories = df["category_harmonised"].value_counts().index.tolist()
    data_by_cat = [df[df["category_harmonised"] == c]["text_len"].dropna().values for c in categories]
    bp = ax.boxplot(data_by_cat, labels=categories, patch_artist=True, showfliers=False)
    for patch, color in zip(bp["boxes"], plt.cm.Set3(np.linspace(0, 1, len(categories)))):
        patch.set_facecolor(color)
    ax.set_title("Text Length Distribution by Category (sampled, outliers hidden)", fontsize=12)
    ax.set_ylabel("Character Count")
    ax.set_yscale("log")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    savefig(fig, "text_length_by_category.png")

    # Per year — economy only
    eco = df[df["category_harmonised"] == "economy"].copy()
    if not eco.empty:
        fig, ax = plt.subplots(figsize=(12, 5))
        years = sorted(eco["year"].dropna().unique())
        data_by_year = [eco[eco["year"] == y]["text_len"].dropna().values for y in years]
        bp = ax.boxplot(data_by_year, labels=[str(int(y)) for y in years], patch_artist=True, showfliers=False)
        for patch in bp["boxes"]:
            patch.set_facecolor("#4C72B0")
        ax.set_title("Economy Article Text Length by Year (sampled, outliers hidden)", fontsize=12)
        ax.set_ylabel("Character Count")
        ax.set_yscale("log")
        fig.tight_layout()
        savefig(fig, "text_length_economy_by_year.png")


def count_empty_texts(path: Path) -> dict:
    """Stream the corpus and count empty/short texts."""
    counts = {"total": 0, "empty_text": 0, "empty_headline": 0, "short_text_under_50": 0, "short_text_under_100": 0}
    for row in iter_zst_csv(path):
        counts["total"] += 1
        if not row.get("text", "").strip():
            counts["empty_text"] += 1
        if not row.get("headline", "").strip():
            counts["empty_headline"] += 1
        if len(row.get("text", "").strip()) < 50:
            counts["short_text_under_50"] += 1
        if len(row.get("text", "").strip()) < 100:
            counts["short_text_under_100"] += 1
    return counts


# ── main ──────────────────────────────────────────────────────────────────

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    corpus_path = find_corpus()
    print(f"Corpus: {corpus_path} ({corpus_path.stat().st_size / 1e9:.2f} GB)")

    # 1. Stream full corpus for counts
    print("Counting full corpus...")
    full = full_counts(corpus_path)
    print(f"  Total rows: {full['total_rows']:,}")

    # 2. Load sample for text length analysis
    print("Loading sample (200k rows) for text length analysis...")
    df_sample = load_sample(corpus_path, n=200_000)
    print(f"  Sampled {len(df_sample):,} rows")

    # 3. Generate plots
    print("Generating plots...")
    plot_articles_per_year(full["year"])
    plot_newspapers_over_time(full["newspaper_year"])
    plot_categories_over_time(full["category_year"])
    plot_source_boundary(full["source_year"])
    plot_text_length_distribution(df_sample)

    # 4. Empty text counts
    print("Counting empty/short texts...")
    empty_counts = count_empty_texts(corpus_path)
    print(f"  Empty text: {empty_counts['empty_text']:,}")
    print(f"  Empty headline: {empty_counts['empty_headline']:,}")
    print(f"  Text < 50 chars: {empty_counts['short_text_under_50']:,}")
    print(f"  Text < 100 chars: {empty_counts['short_text_under_100']:,}")

    # 5. Write summary JSON
    summary = {
        "corpus": str(corpus_path),
        "total_rows": full["total_rows"],
        "years": dict(sorted(full["year"].items())),
        "newspapers": {
            year: dict(sorted(
                (k.split("|", 1)[0], v) for k, v in full["newspaper_year"].items()
                if k.endswith(f"|{year}")
            ))
            for year in sorted(full["year"].keys())
        },
        "categories": {
            year: dict(sorted(
                (k.split("|", 1)[0], v) for k, v in full["category_year"].items()
                if k.endswith(f"|{year}")
            ))
            for year in sorted(full["year"].keys())
        },
        "source_breakdown": {
            year: dict(sorted(
                (k.split("|", 1)[0], v) for k, v in full["source_year"].items()
                if k.endswith(f"|{year}")
            ))
            for year in sorted(full["year"].keys())
        },
        "text_quality": empty_counts,
        "sample_size": len(df_sample),
        "sample_text_length_stats": {
            "mean": float(df_sample["text_len"].mean()),
            "median": float(df_sample["text_len"].median()),
            "std": float(df_sample["text_len"].std()),
            "p1": float(df_sample["text_len"].quantile(0.01)),
            "p99": float(df_sample["text_len"].quantile(0.99)),
        },
    }
    SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSummary written to {SUMMARY_PATH}")
    print("Phase 1A complete.")


if __name__ == "__main__":
    import csv
    from collections.abc import Iterable
    main()
