"""JSONL export functions for the Audio Annotation Lab.

Two export modes are provided:

- **XENI-compatible** — Each line matches the XENI article schema, making
  the output directly ingestible by XENI pipelines (``index/``,
  ``experiment/``).
- **Raw** — Full data dump that includes all annotations per segment,
  suitable for archival or manual inspection.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pipelines.audio_annotation_lab.database.store import Store


def _iter_segments(
    store: Store,
    session_ids: list[str] | None,
    min_confidence: float = 0.0,
) -> Any:
    """Yield ``(session_dict, segment_obj, annotations_list)`` tuples.

    Iterates over the requested sessions (or all if ``session_ids`` is
    ``None``) and their segments, loading annotations for each segment.

    Args:
        store: A ``Store`` instance.
        session_ids: Optional filter — only these session IDs.
        min_confidence: Minimum annotation confidence to include.

    Yields:
        ``(session_dict, segment_obj, annotations)`` where
        ``annotations`` is filtered by confidence.
    """
    sessions = store.list_sessions()
    for session in sessions:
        if session_ids is not None and session.id not in session_ids:
            continue
        sdict = session.to_dict()
        segments = store.load_segments(session.id)
        for seg in segments:
            annotations = store.load_annotations(seg.id)
            annotations = [a for a in annotations if a.confidence >= min_confidence]
            yield sdict, seg, annotations


def export_xeni_compatible(
    store: Store,
    output_path: str | Path,
    session_ids: list[str] | None = None,
    min_confidence: float = 0.0,
) -> int:
    """Export annotated segments as XENI-compatible JSONL.

    Each output line is a flat dictionary matching the XENI article schema
    used by downstream ``index/`` and ``experiment/`` pipelines.

    For each segment the **highest-confidence annotation** is folded into
    the output as the ``annotation`` key.  If no annotation meets the
    confidence threshold the segment is still exported with an empty
    ``annotation`` dict.

    Example output line::

        {
          "id": "seg_abc123",
          "text": "The central bank raised interest rates...",
          "source": "community_radio_interview",
          "date": "2024-01-15",
          "audio_file": "interview.mp3",
          "start_time": 142.5,
          "end_time": 148.3,
          "speaker": "economist_1",
          "language": "bn",
          "session_id": "ses_001",
          "segment_index": 5,
          "asr_confidence": 0.92,
          "annotation": {
            "economic_relevance": "relevant",
            "sentiment": "negative"
          }
        }

    Args:
        store: A ``Store`` instance with data to export.
        output_path: Destination path for the JSONL file.
        session_ids: If provided, only export these session IDs.
        min_confidence: Minimum annotation confidence threshold (0.0‑1.0).
            Annotations below this value are ignored.

    Returns:
        Number of lines (segments) written.
    """
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    count = 0

    with open(out, "w", encoding="utf-8") as f:
        for sdict, seg, annotations in _iter_segments(store, session_ids, 0.0):
            # Best annotation (highest confidence) that meets threshold
            best_annotation: dict[str, Any] = {}
            best_conf = -1.0
            for ann in annotations:
                if ann.confidence > best_conf:
                    best_conf = ann.confidence
                    best_annotation = ann.labels if ann.labels else {}

            # If best doesn't meet threshold, set empty
            if best_conf < min_confidence:
                best_annotation = {}

            line = {
                "id": seg.id,
                "text": seg.text,
                "source": sdict.get("file_name", ""),
                "date": sdict.get("created_at", ""),
                "audio_file": sdict.get("file_name", ""),
                "start_time": seg.start_time,
                "end_time": seg.end_time,
                "duration": seg.duration,
                "speaker": seg.speaker,
                "language": seg.language,
                "session_id": sdict.get("id", ""),
                "segment_index": seg.index,
                "asr_confidence": seg.confidence,
                "annotation": best_annotation,
            }
            f.write(json.dumps(line, ensure_ascii=False, default=str) + "\n")
            count += 1

    return count


def export_raw(
    store: Store,
    output_path: str | Path,
    session_ids: list[str] | None = None,
) -> int:
    """Export full raw data including all annotations per segment.

    Unlike ``export_xeni_compatible``, this function includes **every**
    annotation for each segment (not just the best one).  Each output line
    represents one segment with its session context and all annotations
    embedded.

    Example output line::

        {
          "_type": "annotated_segment",
          "session": {
            "id": "ses_001",
            "file_name": "interview.mp3",
            ...
          },
          "segment": {
            "id": "seg_abc123",
            "text": "...",
            ...
          },
          "annotations": [
            {
              "id": "ann_001",
              "annotator": "claude-3-opus",
              "annotator_type": "llm",
              "labels": {"sentiment": "positive"},
              ...
            }
          ]
        }

    Args:
        store: A ``Store`` instance.
        output_path: Destination path for the JSONL file.
        session_ids: Optional filter — only these session IDs.

    Returns:
        Number of lines (segments) written.
    """
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    count = 0

    with open(out, "w", encoding="utf-8") as f:
        for sdict, seg, annotations in _iter_segments(store, session_ids, 0.0):
            line: dict[str, Any] = {
                "_type": "annotated_segment",
                "session": sdict,
                "segment": seg.to_dict(),
                "annotations": [a.to_dict() for a in annotations],
            }
            f.write(json.dumps(line, ensure_ascii=False, default=str) + "\n")
            count += 1

    return count
