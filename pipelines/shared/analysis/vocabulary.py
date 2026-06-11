"""Vocabulary profiler — lexical analysis for any XENI corpus.

Computes type-token ratio, hapax legomena, top-N words, log-odds ratio
keywords, and n-gram frequencies. Language-agnostic — accepts a custom
tokenizer function so it works with Bangla, Arabic, Vietnamese, etc.

Typical usage::

    from shared.analysis.vocabulary import vocabulary_profile

    profile = vocabulary_profile(
        df["content"],
        config={"language": "beni", "top_n": 50, "ngram_n": 2},
    )
"""

from __future__ import annotations

import logging
import re
from collections import Counter
from pathlib import Path
from typing import Any, Callable

import numpy as np
import pandas as pd

from ..io import write_json

logger = logging.getLogger(__name__)

# ── Default tokenizer ─────────────────────────────────────────────────


def default_tokenizer(text: str) -> list[str]:
    """Split text on whitespace and strip basic ASCII punctuation.

    Works with Latin, Devanagari, Arabic, and Bangla scripts by
    stripping only ASCII punctuation instead of ``[^\\w\\s]`` —
    the latter strips Unicode combining marks (e.g. Bengali vowel
    signs ি া ে) and corrupts non-Latin text.

    For language-specific tokenization, pass a custom tokenizer
    via the config.
    """
    if not isinstance(text, str) or not text.strip():
        return []
    text = text.lower()
    # Strip punctuation including Indic/Bengali marks (। ‹ › “ ” ‘ ’ « »)
    # but keep intra-word hyphens/apostrophes.
    text = re.sub(r"""[!\"#$%&()*,./:;<=>?@[\]^_`{|}~।‹›""''«»–—‐·…]""", "", text)
    return text.split()


# ── Log-odds ratio ────────────────────────────────────────────────────


def log_odds_ratio(
    target_counts: Counter,
    background_counts: Counter,
    total_target: int,
    total_background: int,
    *,
    prior_strength: float = 0.01,
) -> list[tuple[str, float]]:
    """Compute log-odds ratio with informative Dirichlet prior (Monroe et al. 2008).

    Parameters
    ----------
    target_counts:
        Word frequencies in the target category.
    background_counts:
        Word frequencies in the background (rest of corpus).
    total_target:
        Total tokens in target category.
    total_background:
        Total tokens in background.
    prior_strength:
        Pseudocount for the Dirichlet prior (default 0.01).

    Returns
    -------
    list[tuple[str, float]]
        Words ranked by log-odds ratio (highest = most distinctive).
    """
    vocab = set(target_counts) | set(background_counts)
    prior: dict[str, float] = {}

    for w in vocab:
        prior[w] = (target_counts.get(w, 0) + background_counts.get(w, 0)) / (
            total_target + total_background
        )

    alpha = prior_strength
    result: list[tuple[str, float]] = []
    for w in vocab:
        y_w = target_counts.get(w, 0)
        n_w = background_counts.get(w, 0)
        # Log-odds with prior smoothing
        delta = np.log(
            (y_w + alpha * prior[w]) / (total_target + alpha - (y_w + alpha * prior[w]))
        ) - np.log(
            (n_w + alpha * prior[w]) / (total_background + alpha - (n_w + alpha * prior[w]))
        )
        # Variance estimate (inverse weighting)
        var = 1 / (y_w + alpha * prior[w]) + 1 / (n_w + alpha * prior[w])
        z = delta / np.sqrt(var) if var > 0 else 0.0
        result.append((w, float(z)))

    result.sort(key=lambda x: -x[1])
    return result


# ── Core vocabulary profile ──────────────────────────────────────────


def vocabulary_profile(
    texts: pd.Series,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Compute lexical statistics for a corpus.

    Parameters
    ----------
    texts:
        Series of article texts.
    config:
        Optional dictionary with keys:
        - ``tokenizer``: callable ``str -> list[str]`` (default: :func:`default_tokenizer`).
        - ``stopwords``: set of stop words to filter out. If provided, wraps
          the default (or given) tokenizer with stop word filtering.
        - ``top_n``: number of top words to report (default 50).
        - ``ngram_n``: n-gram size (1 = unigram, 2 = bigram; default 1).
        - ``per_category`` : if an array of labels is passed here, per-category
          stats are also computed.  Pass ``{"labels": series}``.
        - ``sample_size``: max texts to process for expensive stats (default 20000).

    Returns
    -------
    dict
        Keys: ``tokens``, ``types``, ``ttr``, ``hapax_count``,
        ``hapax_percentage``, ``top_n_words``, ``per_category`` (optional),
        ``log_odds_keywords`` (optional).
    """
    cfg = config or {}
    tokenizer: Callable = cfg.get("tokenizer", default_tokenizer)
    top_n = cfg.get("top_n", 50)

    # Apply stop word filtering if configured
    stopwords: set[str] | None = cfg.get("stopwords")
    if stopwords is not None:
        from .preprocessing import stopword_filtered_tokenizer
        tokenizer = stopword_filtered_tokenizer(stopwords, base_tokenizer=tokenizer)

    ngram_n = cfg.get("ngram_n", 1)
    ngram_n = cfg.get("ngram_n", 1)
    sample_size = cfg.get("sample_size", 20_000)

    # Sample if corpus is very large (vocab stats converge quickly)
    if len(texts) > sample_size:
        texts = texts.sample(n=sample_size, random_state=42)
        logger.info("Vocabulary sampling %d texts (from %d)", sample_size, len(texts))

    # Tokenize all texts
    all_tokens: list[str] = []
    doc_lengths: list[int] = []
    for t in texts:
        toks = tokenizer(str(t)) if pd.notna(t) else []
        if ngram_n > 1:
            toks = ["_".join(toks[i:i + ngram_n]) for i in range(len(toks) - ngram_n + 1)]
        all_tokens.extend(toks)
        doc_lengths.append(len(toks))

    total_tokens = len(all_tokens)
    if total_tokens == 0:
        return {"tokens": 0, "types": 0, "ttr": 0.0, "hapax_count": 0,
                "hapax_percentage": 0.0, "top_n_words": []}

    word_counts = Counter(all_tokens)
    types = len(word_counts)
    ttr = types / total_tokens
    hapax = sum(1 for c in word_counts.values() if c == 1)

    # Top N words
    top = word_counts.most_common(top_n)

    result: dict[str, Any] = {
        "tokens": total_tokens,
        "types": types,
        "ttr": round(ttr, 4),
        "hapax_count": hapax,
        "hapax_percentage": round(hapax / types * 100, 2) if types else 0.0,
        "mean_doc_length_tokens": round(float(np.mean(doc_lengths)), 1) if doc_lengths else 0,
        "top_n_words": [
            {"word": w, "frequency": f, "proportion": round(f / total_tokens, 4)}
            for w, f in top
        ],
    }

    # ── Per-category vocabulary ─────────────────────────────────────
    labels = cfg.get("per_category", {}).get("labels") if isinstance(cfg.get("per_category"), dict) else cfg.get("per_category")
    if labels is not None and len(labels) == len(texts):
        logger.info("Computing per-category vocabulary...")
        categories = pd.Series(labels, index=texts.index)
        cat_stats: dict[str, dict] = {}
        background_counts: Counter = Counter()
        background_total: int = 0

        for cat in sorted(categories.unique()):
            mask = categories == cat
            cat_tokens: list[str] = []
            for t in texts[mask]:
                toks = tokenizer(str(t)) if pd.notna(t) else []
                if ngram_n > 1:
                    toks = ["_".join(toks[i:i + ngram_n]) for i in range(len(toks) - ngram_n + 1)]
                cat_tokens.extend(toks)
            cat_counts = Counter(cat_tokens)
            cat_total = len(cat_tokens)
            cat_types = len(cat_counts)
            cat_ttr = cat_types / cat_total if cat_total else 0
            cat_top = cat_counts.most_common(min(top_n, len(cat_counts)))
            cat_stats[str(cat)] = {
                "tokens": cat_total,
                "types": cat_types,
                "ttr": round(cat_ttr, 4),
                "top_n_words": [
                    {"word": w, "frequency": f} for w, f in cat_top
                ],
            }
            background_counts.update(cat_counts)
            background_total += cat_total

        # Log-odds keywords per category
        for cat in cat_stats:
            mask = categories == cat
            cat_tokens_list: list[str] = []
            for t in texts[mask]:
                toks = tokenizer(str(t)) if pd.notna(t) else []
                if ngram_n > 1:
                    toks = ["_".join(toks[i:i + ngram_n]) for i in range(len(toks) - ngram_n + 1)]
                cat_tokens_list.extend(toks)
            cat_counts = Counter(cat_tokens_list)
            cat_total = len(cat_tokens_list)

            # Background = everything NOT this category
            bg_counts = Counter(background_counts)
            for w, c in cat_counts.items():
                bg_counts[w] -= c
                if bg_counts[w] <= 0:
                    del bg_counts[w]
            bg_total = background_total - cat_total

            if bg_total > 0 and cat_total > 0:
                keywords = log_odds_ratio(cat_counts, bg_counts, cat_total, bg_total)
                cat_stats[cat]["log_odds_keywords"] = [
                    {"word": w, "z_score": round(z, 2)}
                    for w, z in keywords[:top_n]
                ]

        result["per_category"] = cat_stats

    logger.info("Vocabulary profile: %d tokens, %d types, TTR=%.4f, hapax=%d (%.1f%%)",
                total_tokens, types, ttr, hapax, result["hapax_percentage"])
    return result


def run_vocabulary(
    df: pd.DataFrame,
    output_dir: str | Path,
    text_column: str = "text",
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Compute vocabulary profile and write to *output_dir*.

    Returns the profile dict.
    """
    from pathlib import Path

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    # Attach category labels if column exists
    cfg = dict(config or {})
    cat_col = cfg.get("category_column") or "category"
    if cat_col in df.columns and "per_category" not in cfg:
        cfg["per_category"] = df[cat_col]

    texts = df[text_column]
    profile = vocabulary_profile(texts, cfg)
    write_json(out / "vocabulary_summary.json", profile)

    # Human-readable summary
    lines = [
        "═" * 60,
        "VOCABULARY PROFILE",
        "═" * 60,
        f"  Tokens:       {profile['tokens']:,}",
        f"  Types:        {profile['types']:,}",
        f"  TTR:          {profile['ttr']}",
        f"  Hapax:        {profile['hapax_count']:,} ({profile['hapax_percentage']}% of types)",
    ]
    if profile.get("top_n_words"):
        lines.append("")
        lines.append("  Top 20 words:")
        for w in profile["top_n_words"][:20]:
            lines.append(f"    {w['word']:<25} {w['frequency']:>8,}  ({w['proportion']:.2%})")
    if profile.get("per_category"):
        lines.append("")
        lines.append("  Per-category TTR:")
        for cat, stats in profile["per_category"].items():
            lines.append(f"    {cat:<20} TTR={stats['ttr']}  types={stats['types']:,}")
    lines.append("═" * 60)
    out.joinpath("vocabulary_report.md").write_text("\n".join(lines) + "\n")

    logger.info("Vocabulary profile written to %s", out)
    return profile
