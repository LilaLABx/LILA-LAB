"""
Confidence scoring for Audio Annotation Lab annotations.

Provides per-label, per-segment, and aggregate confidence measures to
drive the review workflow and auto-accept decisions.

Functions
---------
label_confidence
    Per-label confidence from annotation metadata.
segment_confidence
    Combined ASR + annotation confidence for a segment.
threshold_filter
    Split a segment list into accepted vs. review-needed.
confidence_distribution
    Histogram-ready distribution of confidence scores.
"""

from __future__ import annotations

import statistics
from typing import Any

# ── Public API ───────────────────────────────────────────────────────


def label_confidence(
    annotation: dict,
    base_confidence: float = 1.0,
) -> dict[str, float]:
    """Compute per-label confidence scores based on annotation source.

    Confidence assignment rules:

    - ``human`` annotator → full ``base_confidence`` (default 1.0).
    - ``llm`` annotator  → ``base_confidence * 0.85``.
    - ``asr`` (generated) → ``base_confidence * 0.65``.
    - Unknown source     → ``base_confidence * 0.50``.

    If the annotation carries an explicit ``confidence`` key, that value
    is used directly for all labels in the annotation.

    Parameters
    ----------
    annotation : dict
        Annotation record.  Expected keys:
        ``annotator_type`` (``"human"``, ``"llm"``, ``"asr"``),
        ``labels`` (dict), and optionally ``confidence`` (float).
    base_confidence : float
        Maximum confidence for a human annotator.

    Returns
    -------
    dict[str, float]
        Mapping from each label key to its confidence score.
    """
    labels: dict = annotation.get("labels", {})
    explicit_confidence = annotation.get("confidence")

    if explicit_confidence is not None:
        return {k: float(explicit_confidence) for k in labels}

    atype = annotation.get("annotator_type", "unknown")
    factor = {"human": 1.0, "llm": 0.85, "asr": 0.65}.get(atype, 0.50)

    per_label = base_confidence * factor
    return {k: per_label for k in labels}


def segment_confidence(
    segment: dict,
    annotation: dict,
    asr_weight: float = 0.3,
    annotation_weight: float = 0.7,
) -> float:
    """Combine ASR-level and annotation-level confidence for a segment.

    The segment's own ``confidence`` key (ASR transcription confidence)
    is weighted by ``asr_weight`` and combined with the annotation's
    mean label confidence weighted by ``annotation_weight``.

    Parameters
    ----------
    segment : dict
        Segment record, expected to contain ``confidence`` (ASR confidence).
    annotation : dict
        Annotation record (see :func:`label_confidence`).
    asr_weight : float
        Weight for ASR confidence in [0, 1].
    annotation_weight : float
        Weight for annotation confidence in [0, 1].

    Returns
    -------
    float
        Combined confidence score in [0, 1].

    Raises
    ------
    ValueError
        If weights do not sum to 1 (within floating tolerance).
    """
    if abs(asr_weight + annotation_weight - 1.0) > 1e-9:
        msg = (
            f"asr_weight ({asr_weight}) + annotation_weight ({annotation_weight}) "
            f"must sum to 1"
        )
        raise ValueError(msg)

    asr_conf: float = segment.get("confidence", 0.5) if isinstance(segment, dict) else 0.5
    label_scores = label_confidence(annotation)
    annotation_conf: float = (
        statistics.mean(list(label_scores.values())) if label_scores else 0.5
    )

    return asr_weight * asr_conf + annotation_weight * annotation_conf


def threshold_filter(
    segments: list[dict],
    min_confidence: float = 0.7,
) -> tuple[list[dict], list[dict]]:
    """Split a list of segments into accepted and review-queue buckets.

    Segments whose ``confidence`` key (or combined
    :func:`segment_confidence` when an ``annotation`` key is present) is
    at or above ``min_confidence`` go to the accepted list; the rest go
    to the review queue.

    Parameters
    ----------
    segments : list[dict]
        Segments, each optionally containing ``confidence`` and/or
        ``annotation``.
    min_confidence : float
        Threshold in [0, 1].

    Returns
    -------
    accepted : list[dict]
        Segments meeting the threshold.
    review_queue : list[dict]
        Segments requiring review.
    """
    accepted: list[dict] = []
    review_queue: list[dict] = []

    for seg in segments:
        annotation = seg.get("annotation")
        conf = segment_confidence(seg, annotation) if annotation else seg.get("confidence", 0.0)

        if conf >= min_confidence:
            accepted.append(seg)
        else:
            review_queue.append(seg)

    return accepted, review_queue


def confidence_distribution(
    segments: list[dict],
    bins: int = 10,
) -> dict[str, Any]:
    """Compute histogram data for confidence scores across segments.

    Parameters
    ----------
    segments : list[dict]
        Segments (see :func:`threshold_filter`).
    bins : int
        Number of equal-width bins in [0, 1].

    Returns
    -------
    dict
        With keys:

        - ``bins`` — list of bin edges (``bins + 1`` floats)
        - ``counts`` — list of counts per bin
        - ``mean`` — mean confidence
        - ``median`` — median confidence
        - ``std`` — standard deviation
        - ``total`` — total segments
    """
    scores: list[float] = []
    for seg in segments:
        annotation = seg.get("annotation")
        conf = segment_confidence(seg, annotation) if annotation else seg.get("confidence", 0.0)
        scores.append(conf)

    if not scores:
        return {
            "bins": [],
            "counts": [],
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "total": 0,
        }

    # Manual binning (no numpy dependency)
    bin_edges = [i / bins for i in range(bins + 1)]
    counts = [0] * bins

    for s in scores:
        # Clamp to [0, 1)
        s_clamped = max(0.0, min(s, 0.999999))
        idx = int(s_clamped * bins)
        counts[idx] += 1

    mean = statistics.mean(scores)
    std = statistics.stdev(scores) if len(scores) > 1 else 0.0
    try:
        median = statistics.median(scores)
    except statistics.StatisticsError:
        median = 0.0

    return {
        "bins": bin_edges,
        "counts": counts,
        "mean": round(mean, 4),
        "median": round(median, 4),
        "std": round(std, 4),
        "total": len(scores),
    }
