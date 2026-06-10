"""
Review workflow for Audio Annotation Lab.

Manages the queue of low-confidence / disputed segments that require
human review before they can be accepted into the final annotation set.

Classes
-------
ReviewItem
    Immutable data container for a single review entry.

Functions
---------
create_review_queue
    Build a review queue from segments and annotations.
priority_sort
    Sort a review queue by configurable priority strategy.
review_stats
    Aggregate statistics over a review queue.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from .confidence import threshold_filter

# ── Data class ────────────────────────────────────────────────────────


@dataclass
class ReviewItem:
    """A single item in the review queue.

    Attributes
    ----------
    segment_id : str
        Unique identifier of the audio segment.
    session_id : str
        Session the segment belongs to.
    reason : str
        Why this item was flagged (e.g. ``"low_confidence"``).
    confidence : float
        Current confidence score in [0, 1].
    current_labels : dict
        Labels assigned so far (from LLM or previous annotation).
    proposed_corrections : list[dict] | None
        Suggested label changes, if any.
    reviewed : bool
        Whether this item has been reviewed.
    reviewed_by : str | None
        Annotator who performed the review.
    reviewed_at : str | None
        ISO-8601 timestamp of the review.
    """

    segment_id: str
    session_id: str
    reason: str
    confidence: float
    current_labels: dict
    proposed_corrections: list[dict] | None = None
    reviewed: bool = False
    reviewed_by: str | None = None
    reviewed_at: str | None = None


# ── Public API ────────────────────────────────────────────────────────


def create_review_queue(
    segments: list[dict],
    annotations: list[dict],
    min_confidence: float = 0.7,
) -> list[ReviewItem]:
    """Build a review queue from segments that fall below the confidence threshold.

    Segments whose combined :func:`~quality.confidence.segment_confidence`
    is below ``min_confidence`` are wrapped in ``ReviewItem`` instances.

    Parameters
    ----------
    segments : list[dict]
        Segment records (must contain ``id``, ``session_id``).
    annotations : list[dict]
        Annotation records keyed to segments (must contain ``segment_id``).
    min_confidence : float
        Minimum acceptable confidence (default 0.7).

    Returns
    -------
    list[ReviewItem]
        Ordered list of items needing review.
    """
    # Index annotations by segment_id
    ann_by_seg: dict[str, list[dict]] = {}
    for ann in annotations:
        seg_id = ann.get("segment_id", "")
        ann_by_seg.setdefault(seg_id, []).append(ann)

    # Build annotation lookup for each segment
    segments_with_annotation: list[dict] = []
    for seg in segments:
        seg_id = seg.get("id", "")
        seg_anns = ann_by_seg.get(seg_id, [])

        if seg_anns:
            # Use the most recent annotation for confidence
            latest = max(seg_anns, key=lambda a: a.get("created_at", ""))
            seg_copy = dict(seg)
            seg_copy["annotation"] = latest
            segments_with_annotation.append(seg_copy)
        else:
            segments_with_annotation.append(seg)

    _, review_segments = threshold_filter(segments_with_annotation, min_confidence)

    queue: list[ReviewItem] = []
    for seg in review_segments:
        seg_id = seg.get("id", "")
        annotation = seg.get("annotation", {})
        labels: dict = annotation.get("labels", {}) if isinstance(annotation, dict) else {}

        conf: float = seg.get("confidence", 0.0)

        queue.append(
            ReviewItem(
                segment_id=seg_id,
                session_id=seg.get("session_id", ""),
                reason="low_confidence",
                confidence=conf,
                current_labels=labels,
            )
        )

    return queue


def priority_sort(
    queue: list[ReviewItem],
    strategy: str = "confidence_ascending",
) -> list[ReviewItem]:
    """Sort a review queue by the given priority strategy.

    Parameters
    ----------
    queue : list[ReviewItem]
        Review queue to sort.
    strategy : str
        One of:

        - ``"confidence_ascending"`` — lowest confidence first (default)
        - ``"confidence_descending"`` — highest confidence first
        - ``"unreviewed_first"`` — unreviewed items before reviewed

    Returns
    -------
    list[ReviewItem]
        New sorted list (original is unchanged).

    Raises
    ------
    ValueError
        If the strategy is not recognised.
    """
    strategies: dict[str, Callable[[ReviewItem], Any]] = {
        "confidence_ascending": lambda item: item.confidence,
        "confidence_descending": lambda item: -item.confidence,
        "unreviewed_first": lambda item: (item.reviewed, item.confidence),
    }

    key_fn = strategies.get(strategy)
    if key_fn is None:
        msg = f"Unknown strategy '{strategy}'. Choose from: {', '.join(sorted(strategies))}"
        raise ValueError(msg)

    reverse = strategy == "confidence_descending"
    if strategy == "unreviewed_first":
        # False (not reviewed) sorts before True (reviewed)
        return sorted(queue, key=key_fn)

    return sorted(queue, key=key_fn, reverse=reverse)


def review_stats(queue: list[ReviewItem]) -> dict[str, Any]:
    """Compute aggregate statistics over a review queue.

    Parameters
    ----------
    queue : list[ReviewItem]
        The review queue.

    Returns
    -------
    dict
        With keys:

        - ``total`` — total items
        - ``reviewed`` — number of reviewed items
        - ``unreviewed`` — number of unreviewed items
        - ``review_pct`` — percentage reviewed
        - ``mean_confidence`` — mean confidence across items
        - ``min_confidence`` — minimum confidence
        - ``max_confidence`` — maximum confidence
        - ``reasons`` — dict mapping reason → count
    """
    total = len(queue)
    if total == 0:
        return {
            "total": 0,
            "reviewed": 0,
            "unreviewed": 0,
            "review_pct": 0.0,
            "mean_confidence": 0.0,
            "min_confidence": 0.0,
            "max_confidence": 0.0,
            "reasons": {},
        }

    n_reviewed = sum(1 for item in queue if item.reviewed)
    confidences = [item.confidence for item in queue]
    reasons: dict[str, int] = {}
    for item in queue:
        reasons[item.reason] = reasons.get(item.reason, 0) + 1

    return {
        "total": total,
        "reviewed": n_reviewed,
        "unreviewed": total - n_reviewed,
        "review_pct": round(n_reviewed / total * 100, 2),
        "mean_confidence": round(sum(confidences) / total, 4),
        "min_confidence": round(min(confidences), 4),
        "max_confidence": round(max(confidences), 4),
        "reasons": dict(sorted(reasons.items())),
    }
