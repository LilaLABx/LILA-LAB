"""
Visualisation utilities for Audio Annotation Lab.

All functions make ``matplotlib`` an optional dependency — plots are
generated only when ``matplotlib`` is installed.  Without it, the
functions print a warning and return ``None``.

Functions
---------
plot_waveform
    Waveform with optional segment-boundary overlays.
plot_confidence_histogram
    Histogram of segment confidence scores.
plot_agreement_heatmap
    Heatmap of pairwise annotator agreement.
plot_timeline
    Segment timeline coloured by a label field.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def _check_matplotlib() -> bool:
    """Return ``True`` if ``matplotlib`` is importable."""
    try:
        import matplotlib  # noqa: F401

        return True
    except ImportError:
        return False


# ── Public API ─────────────────────────────────────────────────────────


def plot_waveform(
    audio_path: str | Path,
    segments: list[dict] | None = None,
    output_path: str | Path | None = None,
    figsize: tuple[float, float] = (12, 4),
) -> None:
    """Plot an audio waveform with optional segment-boundary overlays.

    Parameters
    ----------
    audio_path : str | Path
        Path to the audio file.
    segments : list[dict] | None
        Optional list of segment dicts, each containing ``start_time``
        and optionally ``end_time`` and ``label``.
    output_path : str | Path | None
        If provided, save the figure to this path.
    figsize : tuple[float, float]
        Figure size in inches ``(width, height)``.
    """
    if not _check_matplotlib():
        import warnings

        warnings.warn("matplotlib not installed; skipping plot_waveform()", stacklevel=2)
        return

    import matplotlib.patches as mpatches
    import matplotlib.pyplot as plt

    try:
        import soundfile as sf  # type: ignore[import-untyped]
    except ImportError:
        import warnings

        warnings.warn("soundfile not installed; skipping plot_waveform()", stacklevel=2)
        return

    try:
        data, sr = sf.read(str(audio_path))
    except Exception as exc:
        import warnings

        warnings.warn(f"Failed to read audio: {exc}", stacklevel=2)
        return

    # Convert to mono for plotting
    if data.ndim > 1:
        import numpy as np  # type: ignore[import-untyped]

        data = np.mean(data, axis=1)

    duration = len(data) / sr
    time = [i / sr for i in range(len(data))]

    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(time, data, color="steelblue", linewidth=0.5, alpha=0.8)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    ax.set_title("Waveform")
    ax.set_xlim(0, duration)

    # Overlay segment boundaries
    if segments:
        colors = ["coral", "limegreen", "gold", "mediumpurple", "deepskyblue"]
        legend_patches = []
        for i, seg in enumerate(segments):
            start = seg.get("start_time", 0)
            end = seg.get("end_time", start + 1)
            label = seg.get("label", f"seg_{i}")

            color = colors[i % len(colors)]
            ax.axvline(x=start, color=color, linestyle="--", linewidth=0.8)
            ax.axvline(x=end, color=color, linestyle="--", linewidth=0.8)
            ax.axvspan(start, end, alpha=0.08, color=color)
            legend_patches.append(mpatches.Patch(color=color, label=label))

        ax.legend(handles=legend_patches, fontsize="small", loc="upper right")

    fig.tight_layout()

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(str(output_path), dpi=150)
        plt.close(fig)
    else:
        plt.show()


def plot_confidence_histogram(
    segments: list[dict],
    output_path: str | Path | None = None,
) -> None:
    """Plot a histogram of confidence scores from segments.

    Parameters
    ----------
    segments : list[dict]
        Segment records, each containing a ``confidence`` key or an
        ``annotation`` key with label confidence.
    output_path : str | Path | None
        If provided, save the figure to this path.
    """
    if not _check_matplotlib():
        import warnings

        warnings.warn(
            "matplotlib not installed; skipping plot_confidence_histogram()", stacklevel=2
        )
        return

    import matplotlib.pyplot as plt

    from .confidence import segment_confidence

    scores: list[float] = []
    for seg in segments:
        annotation = seg.get("annotation")
        conf = segment_confidence(seg, annotation) if annotation else seg.get("confidence", 0.0)
        scores.append(conf)

    if not scores:
        import warnings

        warnings.warn("No confidence scores to plot", stacklevel=2)
        return

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(scores, bins=20, color="steelblue", edgecolor="white", alpha=0.85)
    ax.axvline(x=0.7, color="coral", linestyle="--", linewidth=1.5, label="Threshold (0.7)")
    ax.axvline(x=0.8, color="limegreen", linestyle="--", linewidth=1.5, label="Auto-accept (0.8)")
    ax.set_xlabel("Confidence")
    ax.set_ylabel("Count")
    ax.set_title("Confidence Score Distribution")
    ax.legend()
    fig.tight_layout()

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(str(output_path), dpi=150)
        plt.close(fig)
    else:
        plt.show()


def plot_agreement_heatmap(
    matrix: pd.DataFrame,
    output_path: str | Path | None = None,
) -> None:
    """Plot a heatmap of pairwise annotator agreement.

    Parameters
    ----------
    matrix : pd.DataFrame
        Symmetric agreement matrix (annotators as both index and columns),
        as produced by :func:`~quality.agreement.pairwise_agreement_matrix`.
    output_path : str | Path | None
        If provided, save the figure to this path.
    """
    if not _check_matplotlib():
        import warnings

        warnings.warn("matplotlib not installed; skipping plot_agreement_heatmap()", stacklevel=2)
        return

    import matplotlib.pyplot as plt

    if matrix.empty:
        import warnings

        warnings.warn("Empty agreement matrix; nothing to plot", stacklevel=2)
        return

    fig, ax = plt.subplots(figsize=(8, 6))

    # Simple heatmap via imshow (no seaborn dependency)
    data = matrix.to_numpy(dtype=float)
    annotators = list(matrix.index)

    im = ax.imshow(data, cmap="YlOrRd", vmin=0.0, vmax=1.0)

    # Annotate cells
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            val = data[i, j]
            color = "white" if val < 0.5 else "black"
            ax.text(j, i, f"{val:.2f}", ha="center", va="center", color=color, fontsize=9)

    ax.set_xticks(range(len(annotators)))
    ax.set_yticks(range(len(annotators)))
    ax.set_xticklabels(annotators, rotation=45, ha="right", fontsize=9)
    ax.set_yticklabels(annotators, fontsize=9)
    ax.set_title("Pairwise Annotator Agreement")

    fig.colorbar(im, ax=ax, shrink=0.8)
    fig.tight_layout()

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(str(output_path), dpi=150)
        plt.close(fig)
    else:
        plt.show()


def plot_timeline(
    segments: list[dict],
    output_path: str | Path | None = None,
    color_by: str = "speaker",
) -> None:
    """Plot a horizontal timeline of segments coloured by a label field.

    Parameters
    ----------
    segments : list[dict]
        Segment records, each containing at least ``start_time`` and
        ``end_time``, plus the field named by ``color_by``.
    output_path : str | Path | None
        If provided, save the figure to this path.
    color_by : str
        Field to colour segments by (default ``"speaker"``).
    """
    if not _check_matplotlib():
        import warnings

        warnings.warn("matplotlib not installed; skipping plot_timeline()", stacklevel=2)
        return

    import matplotlib.patches as mpatches
    import matplotlib.pyplot as plt

    if not segments:
        import warnings

        warnings.warn("No segments to plot", stacklevel=2)
        return

    # Collect unique categories for colour assignment
    categories: list[str] = []
    for seg in segments:
        val = seg.get(color_by, "unknown")
        if val not in categories:
            categories.append(val)

    cat_to_color = {
        cat: plt.cm.tab10(i % 10)  # type: ignore[attr-defined]
        for i, cat in enumerate(categories)
    }

    fig, ax = plt.subplots(figsize=(14, max(3, len(segments) * 0.3 + 1)))

    for i, seg in enumerate(segments):
        start = seg.get("start_time", 0.0)
        end = seg.get("end_time", start + 1.0)
        label = seg.get(color_by, "unknown")
        color = cat_to_color.get(label, "gray")
        seg_label = seg.get("label", seg.get("transcript", ""))

        ax.barh(
            i,
            width=end - start,
            left=start,
            height=0.6,
            color=color,
            edgecolor="white",
            linewidth=0.5,
        )

        # Add text label when segment is wide enough
        if end - start > 1.0 and seg_label:
            ax.text(
                (start + end) / 2,
                i,
                seg_label[:40],
                ha="center",
                va="center",
                fontsize=7,
                color="black",
            )

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Segment Index")
    ax.set_title(f"Segment Timeline (coloured by {color_by})")
    ax.set_xlim(
        min(s.get("start_time", 0) for s in segments),
        max(s.get("end_time", 1) for s in segments),
    )
    ax.set_ylim(-0.5, len(segments) - 0.5)

    # Legend
    legend_patches = [mpatches.Patch(color=cat_to_color[cat], label=cat) for cat in categories]
    ax.legend(handles=legend_patches, fontsize="small", loc="upper right")

    fig.tight_layout()

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(str(output_path), dpi=150)
        plt.close(fig)
    else:
        plt.show()
