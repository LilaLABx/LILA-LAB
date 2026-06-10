"""CSV export functions for the Audio Annotation Lab.

Produces two output modes:

- **Segment-level CSV** — One row per segment, with annotation labels
  flattened from the highest-confidence annotation.
- **Session summary CSV** — One row per session with aggregate statistics.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from pipelines.audio_annotation_lab.database.store import Store


def export_csv(
    store: Store,
    output_path: str | Path,
    session_ids: list[str] | None = None,
) -> int:
    """Export segment-level data as a CSV file.

    Each row corresponds to one segment.  Annotation fields from the
    highest-confidence annotation are flattened into top-level columns
    prefixed with ``annotation_``.

    Columns include::

        session_id, segment_id, index, start_time, end_time, duration,
        speaker, text, language, asr_confidence, segment_type,
        annotator, annotation_confidence,
        annotation_<field1>, annotation_<field2>, ...

    Args:
        store: A ``Store`` instance.
        output_path: Destination path for the CSV file.
        session_ids: Optional filter — only these session IDs.

    Returns:
        Number of rows (segments) written.
    """
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    count = 0

    rows: list[dict[str, Any]] = []
    all_field_names: set[str] = set()

    sessions = store.list_sessions()
    for session in sessions:
        if session_ids is not None and session.id not in session_ids:
            continue
        segments = store.load_segments(session.id)
        for seg in segments:
            annotations = store.load_annotations(seg.id)
            # Pick best annotation (highest confidence)
            best = None
            best_conf = -1.0
            for ann in annotations:
                if ann.confidence > best_conf:
                    best_conf = ann.confidence
                    best = ann

            row: dict[str, Any] = {
                "session_id": session.id,
                "session_file": session.file_name,
                "segment_id": seg.id,
                "index": seg.index,
                "start_time": seg.start_time,
                "end_time": seg.end_time,
                "duration": seg.duration,
                "speaker": seg.speaker,
                "text": seg.text,
                "language": seg.language,
                "asr_confidence": seg.confidence,
                "segment_type": seg.segment_type,
            }

            if best is not None:
                row["annotator"] = best.annotator
                row["annotator_type"] = best.annotator_type
                row["schema_name"] = best.schema_name
                row["annotation_confidence"] = best.confidence
                for k, v in (best.labels or {}).items():
                    col = f"annotation_{k}"
                    row[col] = v
                    all_field_names.add(col)
            else:
                row["annotator"] = ""
                row["annotator_type"] = ""
                row["schema_name"] = ""
                row["annotation_confidence"] = ""

            rows.append(row)
            count += 1

    # Build column order
    base_cols = [
        "session_id",
        "session_file",
        "segment_id",
        "index",
        "start_time",
        "end_time",
        "duration",
        "speaker",
        "text",
        "language",
        "asr_confidence",
        "segment_type",
        "annotator",
        "annotator_type",
        "schema_name",
        "annotation_confidence",
    ]
    extra_cols = sorted(all_field_names)
    fieldnames = base_cols + extra_cols

    with open(out, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return count


def export_summary_csv(store: Store, output_path: str | Path) -> int:
    """Export session-level summary statistics as a CSV file.

    Each row corresponds to one session with aggregate statistics.

    Columns include::

        session_id, file_name, format, duration, sample_rate, channels,
        file_size, segment_count, total_annotation_count, avg_segment_duration,
        min_confidence, max_confidence, avg_asr_confidence, avg_annotation_confidence,
        speakers, languages, created_at, updated_at

    Args:
        store: A ``Store`` instance.
        output_path: Destination path for the CSV file.

    Returns:
        Number of rows (sessions) written.
    """
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    count = 0

    rows: list[dict[str, Any]] = []
    sessions = store.list_sessions()

    for session in sessions:
        segments = store.load_segments(session.id)
        seg_count = len(segments)
        if seg_count > 0:
            avg_dur = sum(s.duration for s in segments) / seg_count
            min_asr = min(s.confidence for s in segments)
            max_asr = max(s.confidence for s in segments)
            avg_asr = sum(s.confidence for s in segments) / seg_count
        else:
            avg_dur = 0.0
            min_asr = 0.0
            max_asr = 0.0
            avg_asr = 0.0

        speakers = sorted({s.speaker for s in segments if s.speaker})
        languages = sorted({s.language for s in segments if s.language})

        # Annotation counts and average confidence
        annotation_count = 0
        annotation_confs: list[float] = []
        for seg in segments:
            anns = store.load_annotations(seg.id)
            annotation_count += len(anns)
            annotation_confs.extend(a.confidence for a in anns)
        avg_ann_conf = (
            sum(annotation_confs) / len(annotation_confs)
            if annotation_confs
            else 0.0
        )

        row: dict[str, Any] = {
            "session_id": session.id,
            "file_name": session.file_name,
            "file_path": session.file_path,
            "format": session.format,
            "duration": session.duration,
            "sample_rate": session.sample_rate,
            "channels": session.channels,
            "file_size": session.file_size,
            "segment_count": seg_count,
            "total_annotation_count": annotation_count,
            "avg_segment_duration": round(avg_dur, 3),
            "min_asr_confidence": round(min_asr, 3),
            "max_asr_confidence": round(max_asr, 3),
            "avg_asr_confidence": round(avg_asr, 3),
            "avg_annotation_confidence": round(avg_ann_conf, 3),
            "speakers": ";".join(speakers),
            "languages": ";".join(languages),
            "created_at": session.created_at,
            "updated_at": session.updated_at,
        }
        rows.append(row)
        count += 1

    fieldnames = [
        "session_id",
        "file_name",
        "file_path",
        "format",
        "duration",
        "sample_rate",
        "channels",
        "file_size",
        "segment_count",
        "total_annotation_count",
        "avg_segment_duration",
        "min_asr_confidence",
        "max_asr_confidence",
        "avg_asr_confidence",
        "avg_annotation_confidence",
        "speakers",
        "languages",
        "created_at",
        "updated_at",
    ]

    with open(out, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return count
