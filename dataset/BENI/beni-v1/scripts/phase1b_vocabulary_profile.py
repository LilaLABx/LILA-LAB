#!/usr/bin/env python3
"""Phase 1B — Vocabulary Profiling of the BENI unified corpus.

Reads the deduped unified corpus and produces per-category and per-year
vocabulary analyses:

  1. Type-token ratio (TTR) per year (vocabulary richness over time)
  2. Hapax legomena proportion per year
  3. Most frequent words per category (raw frequency)
  4. Distinctive keywords per category (log-odds ratio)
  5. Most frequent bigrams/trigrams per category
  6. Collocations around key economic terms per year

Assumes Bangla text. Tokenises by splitting on whitespace after basic
cleaning (no stemming for now — we want surface forms).

Output: JSON with tables + PNG plots under docs/exploration/phase1b/
"""

from __future__ import annotations

import csv
import io
import json
import subprocess
import sys
import re
from collections import Counter, defaultdict
from pathlib import Path
from math import log

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "processed"
OUT_DIR = ROOT / "docs" / "exploration" / "phase1b"
SUMMARY_PATH = OUT_DIR / "vocabulary_summary.json"

# ── tokeniser ─────────────────────────────────────────────────────────────

# Basic Bangla + punctuation cleaning
BANGLA_UNICODE_RANGE = re.compile(r"[^\u0980-\u09FF\u0041-\u005A\u0061-\u007A\u0030-\u0039\s]")
MULTI_WS = re.compile(r"\s+")


def clean_and_tokenise(text: str) -> list[str]:
    """Clean text and return tokens."""
    text = text.replace("\ufeff", " ").replace("\xa0", " ")
    text = BANGLA_UNICODE_RANGE.sub(" ", text)
    text = MULTI_WS.sub(" ", text).strip()
    return text.lower().split()


def get_ngrams(tokens: list[str], n: int) -> list[str]:
    """Generate n-grams from token list."""
    return [" ".join(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]


# ── streaming reader ──────────────────────────────────────────────────────

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


# ── vocabulary analysis ──────────────────────────────────────────────────

ECONOMIC_SEED_TERMS = [
    "অর্থনীতি", "মুদ্রাস্ফীতি", "বাজেট", "রিজার্ভ",
    "জিডিপি", "বাণিজ্য", "বিনিয়োগ", "রপ্তানি",
    "আমদানি", "ব্যাংক", "মূল্যস্ফীতি", "অর্থ",
]


def compute_vocabulary_stats(corpus_path: Path, max_rows: int = 500_000) -> dict:
    """Compute vocabulary stats per category and per year.

    To keep memory manageable with 1.45M documents, we process a subset
    for detailed vocabulary work (500k rows = ~34%).
    """
    results = {
        "per_category": {},
        "per_year": {},
        "collocations": {},
    }

    # Accumulators
    cat_tokens: dict[str, list[Counter]] = defaultdict(list)  # cat -> list of Counters (per document)
    cat_doc_counts: dict[str, int] = Counter()
    year_tokens: dict[str, list[Counter]] = defaultdict(list)
    economy_year_tokens: dict[str, list[Counter]] = defaultdict(list)
    collocation_window: dict[str, list[list[str]]] = defaultdict(list)

    for i, row in enumerate(iter_zst_csv(corpus_path)):
        if i >= max_rows:
            break
        if i % 100_000 == 0 and i > 0:
            print(f"  Processed {i:,} rows...")

        text = row.get("text_clean") or row.get("text") or ""
        tokens = clean_and_tokenise(text)
        if not tokens:
            continue

        cat = row["category_harmonised"]
        year = row["publication_date"][:4]

        doc_counter = Counter(tokens)
        cat_tokens[cat].append(doc_counter)
        cat_doc_counts[cat] += 1
        year_tokens[year].append(doc_counter)

        if cat == "economy":
            economy_year_tokens[year].append(doc_counter)

        # Collocations: find windows around economic seed terms
        for seed in ECONOMIC_SEED_TERMS:
            if seed in tokens:
                idxs = [j for j, t in enumerate(tokens) if t == seed]
                for idx in idxs:
                    start = max(0, idx - 5)
                    end = min(len(tokens), idx + 6)
                    collocation_window[seed].append(tokens[start:end])

    print(f"  Finished processing {i+1:,} rows.")

    # Per-category: merge counters and compute stats
    for cat, doc_counters in cat_tokens.items():
        merged: Counter = sum(doc_counters, Counter())
        total_tokens = sum(merged.values())
        types = len(merged)
        hapax = sum(1 for v in merged.values() if v == 1)

        results["per_category"][cat] = {
            "documents": cat_doc_counts[cat],
            "total_tokens": total_tokens,
            "types": types,
            "ttr": types / total_tokens if total_tokens else 0,
            "hapax": hapax,
            "hapax_ratio": hapax / total_tokens if total_tokens else 0,
            "top_50_words": merged.most_common(50),
        }

    # Per-year vocabulary stats
    for year, doc_counters in year_tokens.items():
        merged: Counter = sum(doc_counters, Counter())
        total_tokens = sum(merged.values())
        types = len(merged)
        hapax = sum(1 for v in merged.values() if v == 1)
        results["per_year"][year] = {
            "total_tokens": total_tokens,
            "types": types,
            "ttr": types / total_tokens if total_tokens else 0,
            "hapax": hapax,
            "hapax_ratio": hapax / total_tokens if total_tokens else 0,
        }

    # Economy-only per-year
    for year, doc_counters in economy_year_tokens.items():
        merged: Counter = sum(doc_counters, Counter())
        results.setdefault("economy_per_year", {})
        results["economy_per_year"][year] = {
            "total_tokens": sum(merged.values()),
            "types": len(merged),
            "top_30_words": merged.most_common(30),
        }

    # Collocations: most frequent neighbours within ±5 of seed terms
    for seed, windows in collocation_window.items():
        neighbour_counts: Counter = Counter()
        for window in windows:
            neighbour_counts.update(window)
        # Remove the seed itself
        if seed in neighbour_counts:
            del neighbour_counts[seed]
        results["collocations"][seed] = neighbour_counts.most_common(30)

    return results


# ── log-odds ratio (distinctive keywords) ────────────────────────────────

def compute_log_odds(
    cat_freq: Counter, other_freq: Counter,
    cat_total: int, other_total: int,
    prior: float = 0.01,
    n: int = 50,
) -> list[tuple[str, float]]:
    """Compute log-odds ratio for words in cat_freq vs other_freq.

    Uses additive smoothing with a uniform `prior` to avoid division by zero.
    Positive = distinctive of `cat_freq`, negative = distinctive of `other_freq`.
    """
    vocab = set(cat_freq) | set(other_freq)
    scores: list[tuple[str, float]] = []
    for word in vocab:
        c_cat = cat_freq.get(word, 0) + prior
        c_other = other_freq.get(word, 0) + prior
        p_cat = c_cat / (cat_total + prior * len(vocab))
        p_other = c_other / (other_total + prior * len(vocab))
        lodds = log(p_cat / p_other)
        scores.append((word, lodds))
    scores.sort(key=lambda x: -x[1])
    return scores[:n]


def compute_keywords(vocab: dict) -> dict:
    """Compute distinctive keywords for each category vs all others."""
    cats = [c for c in vocab["per_category"] if c != "other_or_unknown"]
    keywords = {}
    for cat in cats:
        cat_freq = dict(vocab["per_category"][cat]["top_50_words"])
        cat_total = vocab["per_category"][cat]["total_tokens"]
        # Aggregate all other categories
        other_freq: Counter = Counter()
        other_total = 0
        for other_cat in cats:
            if other_cat == cat:
                continue
            for word, count in vocab["per_category"][other_cat]["top_50_words"]:
                other_freq[word] += count
            other_total += vocab["per_category"][other_cat]["total_tokens"]
        keywords[cat] = compute_log_odds(cat_freq, other_freq, cat_total, other_total)
    return keywords


# ── n-gram analysis ──────────────────────────────────────────────────────

def compute_ngrams(corpus_path: Path, max_rows: int = 200_000) -> dict:
    """Compute most frequent bigrams and trigrams per category."""
    ngram_counts: dict[str, tuple[Counter, Counter]] = defaultdict(
        lambda: (Counter(), Counter())
    )  # cat -> (bigrams, trigrams)

    for i, row in enumerate(iter_zst_csv(corpus_path)):
        if i >= max_rows:
            break
        if i % 50_000 == 0 and i > 0:
            print(f"  N-grams: processed {i:,} rows...")
        tokens = clean_and_tokenise(row.get("text_clean") or row.get("text") or "")
        cat = row["category_harmonised"]
        bigrams = get_ngrams(tokens, 2)
        trigrams = get_ngrams(tokens, 3)
        ngram_counts[cat][0].update(bigrams)
        ngram_counts[cat][1].update(trigrams)

    result = {}
    for cat, (big_counter, tri_counter) in ngram_counts.items():
        result[cat] = {
            "top_30_bigrams": big_counter.most_common(30),
            "top_30_trigrams": tri_counter.most_common(30),
        }
    return result


# ── plots ────────────────────────────────────────────────────────────────

def plot_ttr_per_year(vocab: dict, out_dir: Path):
    years = sorted(vocab["per_year"].keys())
    ttrs = [vocab["per_year"][y]["ttr"] for y in years]
    hapax_ratios = [vocab["per_year"][y]["hapax_ratio"] for y in years]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    ax1.plot(years, ttrs, marker="o", color="#4C72B0", linewidth=2)
    ax1.set_title("Type-Token Ratio per Year", fontsize=12)
    ax1.set_xlabel("Year")
    ax1.set_ylabel("TTR")

    ax2.plot(years, hapax_ratios, marker="s", color="#DD8452", linewidth=2)
    ax2.set_title("Hapax Legomena Ratio per Year", fontsize=12)
    ax2.set_xlabel("Year")
    ax2.set_ylabel("Hapax Ratio")

    fig.tight_layout()
    fig.savefig(out_dir / "ttr_per_year.png", bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"  → {out_dir / 'ttr_per_year.png'}")


def plot_top_words_per_category(vocab: dict, out_dir: Path):
    for cat, data in vocab["per_category"].items():
        if cat == "other_or_unknown":
            continue
        top_words = data["top_50_words"][:20]  # top 20
        words, counts = zip(*top_words) if top_words else ([], [])
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(range(len(words)), counts, color="#4C72B0")
        ax.set_yticks(range(len(words)))
        ax.set_yticklabels(words, fontsize=9)
        ax.invert_yaxis()
        ax.set_title(f"Top 20 Words — {cat}", fontsize=12)
        ax.set_xlabel("Frequency")
        fig.tight_layout()
        fig.savefig(out_dir / f"top_words_{cat}.png", bbox_inches="tight", dpi=150)
        plt.close(fig)
        print(f"  → top_words_{cat}.png")


# ── main ──────────────────────────────────────────────────────────────────

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    corpus_path = find_corpus()
    print(f"Corpus: {corpus_path}")

    # Phase 1B-1: Vocabulary stats (sampled: 500k rows for per-category vocab)
    print("\n[1B-1] Computing vocabulary statistics (500k rows)...")
    vocab = compute_vocabulary_stats(corpus_path, max_rows=500_000)
    print("  Categories:", list(vocab["per_category"].keys()))

    # Phase 1B-2: Distinctive keywords via log-odds
    print("\n[1B-2] Computing distinctive keywords (log-odds ratio)...")
    keywords = compute_keywords(vocab)
    vocab["keywords_log_odds"] = keywords
    for cat, kw in keywords.items():
        print(f"  {cat}: top word = '{kw[0][0]}' (log-odds={kw[0][1]:.2f})")

    # Phase 1B-3: N-grams (sampled: 200k rows)
    print("\n[1B-3] Computing bigrams and trigrams (200k rows)...")
    ngrams = compute_ngrams(corpus_path, max_rows=200_000)
    vocab["ngrams"] = ngrams

    # Generate plots
    print("\n[1B-4] Generating plots...")
    plot_ttr_per_year(vocab, OUT_DIR)
    plot_top_words_per_category(vocab, OUT_DIR)

    # Write summary JSON
    # Convert Counters and tuples to serializable lists
    def serialize(obj):
        if isinstance(obj, Counter):
            return dict(obj)
        if isinstance(obj, list) and obj and isinstance(obj[0], tuple):
            return [(str(k), int(v)) for k, v in obj]
        if isinstance(obj, dict):
            return {k: serialize(v) for k, v in obj.items()}
        return obj

    serializable = serialize(vocab)
    SUMMARY_PATH.write_text(json.dumps(serializable, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSummary written to {SUMMARY_PATH}")
    print("Phase 1B complete.")


if __name__ == "__main__":
    main()
