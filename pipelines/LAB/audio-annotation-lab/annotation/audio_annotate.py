#!/usr/bin/env python3
"""
Audio Annotation Lab — Audio-segment-specific annotation helpers.

Provides utility functions for working with transcribed audio segments:
merging adjacent segments, splitting long segments, building context
windows, and formatting segments for LLM prompts.

Usage:
    from pipelines.audio_annotation_lab.annotation.audio_annotate import (
        merge_adjacent_segments,
        split_long_segment,
        context_window,
        format_segment_for_llm,
    )
"""

import logging
import re
from typing import Any

logger = logging.getLogger(__name__)


# ── Segment helpers ────────────────────────────────────────────────────


def merge_adjacent_segments(
    segments: list[dict[str, Any]],
    max_gap: float = 1.0,
) -> list[dict[str, Any]]:
    """Merge adjacent segments from the same speaker.

    When two consecutive segments share the same ``speaker`` label and
    the gap between them (``next.start_time - current.end_time``) is at
    most ``max_gap`` seconds, they are merged into a single segment.

    Args:
        segments: List of segment dicts. Each must contain ``speaker``,
                  ``start_time``, ``end_time``, and ``text``.
        max_gap: Maximum silence gap (seconds) allowed between segments
                 to consider them mergeable.

    Returns:
        New list with merged segments. Non-adjacent or different-speaker
        segments are left unchanged.
    """
    if not segments:
        return []

    # Sort by start_time to ensure correct ordering
    sorted_segs = sorted(segments, key=lambda s: float(s.get("start_time", 0)))

    merged: list[dict[str, Any]] = []
    current = dict(sorted_segs[0])

    for i in range(1, len(sorted_segs)):
        seg = sorted_segs[i]

        same_speaker = str(seg.get("speaker", "")) == str(current.get("speaker", ""))
        gap = float(seg.get("start_time", 0)) - float(current.get("end_time", 0))

        if same_speaker and 0 <= gap <= max_gap:
            # Merge: extend end_time, concatenate text
            current["end_time"] = seg["end_time"]
            current_text = str(current.get("text", "")).strip()
            seg_text = str(seg.get("text", "")).strip()
            current["text"] = f"{current_text} {seg_text}" if current_text else seg_text
        else:
            merged.append(current)
            current = dict(seg)

    merged.append(current)
    return merged


def split_long_segment(
    segment: dict[str, Any],
    max_duration: float = 30.0,
) -> list[dict[str, Any]]:
    """Split a long audio segment at sentence boundaries.

    If the segment's duration exceeds ``max_duration`` seconds, it is
    split at sentence-ending punctuation (``.``, ``!``, ``?``).
    Timestamps are interpolated proportionally across the text.

    Args:
        segment: A single segment dict with ``text``, ``start_time``,
                 ``end_time``, and optional ``speaker``.
        max_duration: Maximum segment duration in seconds before splitting.

    Returns:
        List of segment dicts. If the segment is within the duration
        limit, returns ``[segment]`` unchanged.
    """
    duration = float(segment.get("end_time", 0)) - float(segment.get("start_time", 0))
    if duration <= max_duration:
        return [segment]

    text = str(segment.get("text", "")).strip()
    if not text:
        return [segment]

    # Split at sentence boundaries
    sentences = re.split(r"(?<=[.!?])\s+", text)
    if len(sentences) <= 1:
        # Fall back to clause boundaries
        sentences = re.split(r"(?<=[,;:])\s+", text)

    if len(sentences) <= 1:
        # Cannot split meaningfully — return as-is
        return [segment]

    start_time = float(segment.get("start_time", 0))
    total_chars = len(text)
    total_duration = duration

    sub_segments: list[dict[str, Any]] = []
    char_offset = 0

    for sent in sentences:
        sent = sent.strip()
        if not sent:
            continue

        sent_length = len(sent)
        if total_chars > 0:
            fraction = sent_length / total_chars
            seg_start = start_time + (total_duration * char_offset / total_chars)
            seg_end = seg_start + (total_duration * fraction)
        else:
            seg_start = start_time
            seg_end = start_time + total_duration

        sub_segments.append(
            {
                "text": sent,
                "start_time": round(seg_start, 3),
                "end_time": round(seg_end, 3),
                "speaker": segment.get("speaker", ""),
            }
        )

        char_offset += sent_length

    return sub_segments


def context_window(
    segments: list[dict[str, Any]],
    segment_id: str,
    window_size: int = 2,
) -> list[dict[str, Any]]:
    """Get surrounding context segments for a given segment.

    Returns a window of up to ``window_size`` segments before and after
    the target segment (identified by its ``id`` field).

    Args:
        segments: Full ordered list of segment dicts.
        segment_id: The ``id`` value of the target segment.
        window_size: Number of segments to include on each side.

    Returns:
        List of context segment dicts, including the target. Segments
        are returned in chronological order.
    """
    sorted_segs = sorted(segments, key=lambda s: float(s.get("start_time", 0)))

    for idx, seg in enumerate(sorted_segs):
        if str(seg.get("id", "")) == segment_id:
            start = max(0, idx - window_size)
            end = min(len(sorted_segs), idx + window_size + 1)
            return sorted_segs[start:end]

    logger.warning("Segment %s not found in segments list", segment_id)
    return []


def format_segment_for_llm(
    segment: dict[str, Any],
    include_context: bool = True,
    context_segments: list[dict[str, Any]] | None = None,
) -> str:
    """Format an audio segment for inclusion in an LLM prompt.

    Produces a human-readable block containing the segment's metadata
    and transcript text, with optional surrounding context.

    Args:
        segment: Segment dict with ``text``, ``start_time``, ``end_time``,
                 ``speaker``, and optionally ``id``.
        include_context: If ``True`` and ``context_segments`` is provided,
                         prepend surrounding context.
        context_segments: Optional list of context segment dicts (as
                          returned by :func:`context_window`).

    Returns:
        Formatted string suitable for an LLM prompt.
    """
    seg_id = segment.get("id", "unknown")
    speaker = segment.get("speaker", "unknown")
    start = segment.get("start_time", 0)
    end = segment.get("end_time", 0)
    text = str(segment.get("text", "")).strip()

    parts: list[str] = []

    if include_context and context_segments:
        parts.append("--- Surrounding Context ---")
        for ctx in context_segments:
            ctx_id = str(ctx.get("id", ""))
            ctx_speaker = ctx.get("speaker", "unknown")
            ctx_start = ctx.get("start_time", 0)
            ctx_end = ctx.get("end_time", 0)
            ctx_text = str(ctx.get("text", "")).strip()
            marker = ">>>" if str(ctx.get("id", "")) == seg_id else "   "
            parts.append(
                f"{marker} [{ctx_id}] {ctx_speaker} ({ctx_start:.1f}s–{ctx_end:.1f}s): {ctx_text}"
            )
        parts.append("--- End Context ---\n")

    parts.append(
        f"SEGMENT ID: {seg_id}\n"
        f"SPEAKER: {speaker}\n"
        f"TIMESTAMP: {start:.1f}s – {end:.1f}s\n"
        f"TEXT: {text}"
    )

    return "\n".join(parts)
