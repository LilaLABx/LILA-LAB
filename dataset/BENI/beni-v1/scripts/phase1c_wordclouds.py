#!/usr/bin/env python3
"""Phase 1C — Word Cloud Generation for the BENI unified corpus.

Generates word clouds for:
  1. Per harmonised category (Economy, National, Politics, International, etc.)
  2. Per year — Economy category only (2014→2024)
  3. Per newspaper (Jugantor, Ittefaq, Kaler Kontho, etc.)

Uses a sample of 200k rows for efficiency.
Masks are not used — clean rectangular wordclouds are easier to compare.

Output: PNG files under docs/exploration/phase1c/
"""

from __future__ import annotations

import csv
import io
import json
import subprocess
import re
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from wordcloud import WordCloud

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "processed"
OUT_DIR = ROOT / "docs" / "exploration" / "phase1c"
SUMMARY_PATH = OUT_DIR / "wordcloud_data.json"

BANGLA_KEEP = re.compile(r"[^\u0980-\u09FF\s]")
MULTI_WS = re.compile(r"\s+")

WC_DEFAULTS = dict(
    width=1200,
    height=600,
    background_color="white",
    max_words=200,
    collocations=False,
    random_state=42,
    prefer_horizontal=1.0,
)


def iter_zst_csv(path: Path):
    proc = subprocess.Popen(["zstd", "-q", "-dc", str(path)], stdout=subprocess.PIPE)
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


def find_corpus() -> Path:
    candidates = [
        DATA_DIR / "beni_unified_articles_deduped.csv.zst",
        DATA_DIR / "beni_unified_articles.csv.zst",
    ]
    for p in candidates:
        if p.exists():
            return p
    raise FileNotFoundError(f"No corpus zst found in {DATA_DIR}")


def clean_text(text: str) -> str:
    """Remove non-Bangla characters, collapse whitespace."""
    text = text.replace("\ufeff", " ").replace("\xa0", " ")
    text = BANGLA_KEEP.sub(" ", text)
    text = MULTI_WS.sub(" ", text).strip()
    return text.lower()


def make_wordcloud(text_data: str, title: str, filename: str):
    """Generate and save a word cloud."""
    wc = WordCloud(**WC_DEFAULTS)
    wc.generate(text_data)
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    ax.set_title(title, fontsize=14, pad=12)
    fig.tight_layout(pad=0)
    path = OUT_DIR / filename
    fig.savefig(path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"  → {path}")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    corpus_path = find_corpus()
    print(f"Corpus: {corpus_path}")

    # Accumulate text per dimension
    cat_texts: dict[str, list[str]] = defaultdict(list)
    economy_year_texts: dict[str, list[str]] = defaultdict(list)
    newspaper_texts: dict[str, list[str]] = defaultdict(list)

    for i, row in enumerate(iter_zst_csv(corpus_path)):
        if i >= 200_000:
            break
        if i % 50_000 == 0 and i > 0:
            print(f"  Processed {i:,} rows...")

        text = clean_text(row.get("text_clean") or row.get("text") or "")
        if len(text) < 50:
            continue

        cat = row["category_harmonised"]
        year = row["publication_date"][:4]
        paper = row["newspaper"]

        cat_texts[cat].append(text)
        if cat == "economy":
            economy_year_texts[year].append(text)
        newspaper_texts[paper].append(text)

    print(f"  Processed {i+1:,} rows total.")

    # ── 1. Per-category word clouds ──
    print("\n[1C-1] Per-category word clouds...")
    for cat, texts in sorted(cat_texts.items()):
        if cat == "other_or_unknown":
            continue
        combined = " ".join(texts)
        make_wordcloud(combined, f"Category: {cat}", f"wordcloud_category_{cat}.png")

    # ── 2. Economy per-year word clouds ──
    print("\n[1C-2] Economy per-year word clouds...")
    for year in sorted(economy_year_texts.keys()):
        combined = " ".join(economy_year_texts[year])
        make_wordcloud(combined, f"Economy — {year}", f"wordcloud_economy_{year}.png")

    # ── 3. Per-newspaper word clouds ──
    print("\n[1C-3] Per-newspaper word clouds...")
    for paper, texts in sorted(newspaper_texts.items()):
        combined = " ".join(texts)
        safe_name = paper.replace(" ", "_").replace("-", "_")
        make_wordcloud(combined, f"Newspaper: {paper}", f"wordcloud_newspaper_{safe_name}.png")

    # ── Summary ──
    summary = {
        "per_category": {cat: len(texts) for cat, texts in cat_texts.items()},
        "economy_per_year": {year: len(texts) for year, texts in economy_year_texts.items()},
        "per_newspaper": {paper: len(texts) for paper, texts in newspaper_texts.items()},
    }
    SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSummary written to {SUMMARY_PATH}")
    print("Phase 1C complete.")


if __name__ == "__main__":
    main()
