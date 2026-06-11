"""Standardized visualizations for dataset exploration.

Generates publication-quality figures: word clouds, category/ source
distributions, text length histograms, and time-series coverage plots.
All functions save to disk and return the output path.

Typical usage::

    from shared.analysis.visualizer import (
        plot_category_distribution,
        plot_temporal_coverage,
        plot_wordcloud,
    )

    plot_category_distribution(df, cat_col="category", output_dir="outputs/figures/")
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")  # non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# Global style
plt.rcParams.update({
    "figure.dpi": 150,
    "figure.figsize": (10, 6),
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "savefig.bbox": "tight",
    "savefig.dpi": 200,
})

FONT_PATH = Path(__file__).resolve().parent / "fonts"


def _ensure_output_dir(path: str | Path) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


# ── Category distribution ─────────────────────────────────────────────


def plot_category_distribution(
    df: pd.DataFrame,
    cat_col: str = "category",
    *,
    output_dir: str | Path = "outputs/figures",
    top_n: int = 20,
    figsize: tuple[int, int] = (10, 8),
) -> Path:
    """Horizontal bar chart of category frequencies."""
    out = _ensure_output_dir(output_dir)
    counts = df[cat_col].value_counts().head(top_n)

    fig, ax = plt.subplots(figsize=figsize)
    colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(counts)))
    bars = ax.barh(range(len(counts)), counts.values, color=colors)
    ax.set_yticks(range(len(counts)))
    ax.set_yticklabels(counts.index, fontsize=10)
    ax.set_xlabel("Article count")
    ax.set_title(f"Article distribution by {cat_col}")
    for bar, val in zip(bars, counts.values):
        ax.text(bar.get_width() + max(counts.values) * 0.01,
                bar.get_y() + bar.get_height() / 2,
                f"{val:,}", va="center", fontsize=9)
    ax.invert_yaxis()
    ax.margins(x=0.15)
    fig.tight_layout()

    path = out / f"category_distribution_{cat_col}.png"
    fig.savefig(path)
    plt.close(fig)
    logger.info("Saved %s", path)
    return path


# ── Source distribution ───────────────────────────────────────────────


def plot_source_distribution(
    df: pd.DataFrame,
    source_col: str = "source",
    *,
    output_dir: str | Path = "outputs/figures",
    top_n: int = 15,
    figsize: tuple[int, int] = (10, 7),
) -> Path:
    """Horizontal bar chart of source/newspaper frequencies."""
    return plot_category_distribution(
        df, cat_col=source_col, output_dir=output_dir,
        top_n=top_n, figsize=figsize,
    )


# ── Text length distribution ──────────────────────────────────────────


def plot_text_length_distribution(
    df: pd.DataFrame,
    text_column: str = "text",
    *,
    output_dir: str | Path = "outputs/figures",
    bins: int = 50,
    max_words: int = 500,
    figsize: tuple[int, int] = (10, 5),
) -> Path:
    """Histogram of article word counts."""
    out = _ensure_output_dir(output_dir)
    lengths = df[text_column].dropna().apply(
        lambda t: len(str(t).split()) if isinstance(t, str) else 0
    )
    lengths = lengths[lengths < max_words]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    ax1.hist(lengths, bins=bins, color="steelblue", edgecolor="white", alpha=0.8)
    ax1.set_xlabel("Word count")
    ax1.set_ylabel("Frequency")
    ax1.set_title("Text length distribution")
    ax1.axvline(lengths.median(), color="red", linestyle="--",
                label=f"Median={lengths.median():.0f}")
    ax1.legend()

    # Log scale inset for the long tail
    ax2.hist(lengths, bins=bins, color="steelblue", edgecolor="white", alpha=0.8)
    ax2.set_yscale("log")
    ax2.set_xlabel("Word count")
    ax2.set_ylabel("Frequency (log)")
    ax2.set_title("Text length (log scale)")
    fig.tight_layout()

    path = out / "text_length_distribution.png"
    fig.savefig(path)
    plt.close(fig)
    logger.info("Saved %s", path)
    return path


# ── Temporal coverage ─────────────────────────────────────────────────


def plot_temporal_coverage(
    df: pd.DataFrame,
    date_col: str = "date",
    *,
    output_dir: str | Path = "outputs/figures",
    freq: str = "M",
    figsize: tuple[int, int] = (12, 5),
) -> Path:
    """Time series of article counts per time bucket."""
    out = _ensure_output_dir(output_dir)
    dates = pd.to_datetime(df[date_col], errors="coerce").dropna()
    series = dates.dt.to_period(freq).value_counts().sort_index()
    idx = series.index.to_timestamp()

    fig, ax = plt.subplots(figsize=figsize)
    ax.fill_between(idx, series.values, alpha=0.3, color="steelblue")
    ax.plot(idx, series.values, color="steelblue", linewidth=0.8)
    ax.set_xlabel("Time")
    ax.set_ylabel("Article count")
    ax.set_title("Temporal coverage")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()

    path = out / "temporal_coverage.png"
    fig.savefig(path)
    plt.close(fig)
    logger.info("Saved %s", path)
    return path


# ── Multi-source temporal coverage ────────────────────────────────────


def plot_source_temporal_coverage(
    df: pd.DataFrame,
    date_col: str = "date",
    source_col: str = "source",
    *,
    output_dir: str | Path = "outputs/figures",
    freq: str = "M",
    figsize: tuple[int, int] = (14, 6),
) -> Path:
    """Stacked area chart showing per-source contribution over time."""
    out = _ensure_output_dir(output_dir)
    dates = pd.to_datetime(df[date_col], errors="coerce")
    period = dates.dt.to_period(freq)
    pivot = df.assign(_period=period).pivot_table(
        index="_period", columns=source_col, aggfunc="size", fill_value=0
    )
    # Keep top N sources
    top = pivot.sum().nlargest(8).index
    pivot = pivot[top]
    idx = pivot.index.to_timestamp()

    fig, ax = plt.subplots(figsize=figsize)
    colors = plt.cm.Set2(np.linspace(0, 1, len(top)))
    ax.stackplot(idx, pivot.values.T, labels=top, colors=colors, alpha=0.85)
    ax.set_xlabel("Time")
    ax.set_ylabel("Article count")
    ax.set_title("Per-source temporal coverage")
    ax.legend(loc="upper left", framealpha=0.8, fontsize=8)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()

    path = out / "source_temporal_coverage.png"
    fig.savefig(path)
    plt.close(fig)
    logger.info("Saved %s", path)
    return path


# ── Word cloud ────────────────────────────────────────────────────────


def plot_wordcloud(
    texts: pd.Series,
    *,
    output_dir: str | Path = "outputs/figures",
    max_words: int = 100,
    width: int = 1200,
    height: int = 800,
    title: str = "Word cloud",
    background_color: str = "white",
    figsize: tuple[int, int] = (12, 8),
) -> Path | None:
    """Generate a word cloud from text series.

    Requires the ``wordcloud`` package.  Returns ``None`` if not installed.
    """
    try:
        from wordcloud import WordCloud
    except ImportError:
        logger.warning("wordcloud not installed — skipping word cloud. pip install wordcloud")
        return None

    out = _ensure_output_dir(output_dir)
    text = " ".join(
        str(t) for t in texts.dropna() if isinstance(t, str) and t.strip()
    )
    if not text.strip():
        logger.warning("No text to generate word cloud")
        return None

    wc = WordCloud(
        width=width, height=height,
        max_words=max_words,
        background_color=background_color,
        collocations=False,
    ).generate(text)

    fig, ax = plt.subplots(figsize=figsize)
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    ax.set_title(title, fontsize=14)
    fig.tight_layout()

    path = out / "wordcloud.png"
    fig.savefig(path)
    plt.close(fig)
    logger.info("Saved %s", path)
    return path


# ── Source transition diagnostic plot ─────────────────────────────────


def plot_source_transition_diagnostic(
    df: pd.DataFrame,
    date_col: str = "date",
    source_col: str = "source",
    metric_col: str = "article_length",
    *,
    output_dir: str | Path = "outputs/figures",
    figsize: tuple[int, int] = (12, 5),
) -> Path:
    """Box plot of metric per source per year — visual source-boundary check."""
    out = _ensure_output_dir(output_dir)
    metric_col = metric_col if metric_col in df.columns else (
        next(c for c in df.columns if pd.api.types.is_numeric_dtype(df[c]))
    )
    dates = pd.to_datetime(df[date_col], errors="coerce")
    years = dates.dt.year
    plot_df = df.assign(_year=years, _metric=df[metric_col]).dropna(subset=["_year", "_metric"])

    fig, ax = plt.subplots(figsize=figsize)
    # Group by source and year
    grouped = plot_df.groupby(["_year", source_col])["_metric"].mean().reset_index()
    for src in grouped[source_col].unique():
        src_data = grouped[grouped[source_col] == src]
        ax.plot(src_data["_year"], src_data["_metric"], marker="o", label=str(src), linewidth=1.5)

    ax.set_xlabel("Year")
    ax.set_ylabel(f"Mean {metric_col}")
    ax.set_title(f"Source-transition diagnostic: {metric_col} by source and year")
    ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()

    path = out / "source_transition_diagnostic.png"
    fig.savefig(path)
    plt.close(fig)
    logger.info("Saved %s", path)
    return path
