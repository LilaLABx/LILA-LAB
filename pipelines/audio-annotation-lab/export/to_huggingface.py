"""Export to HuggingFace Datasets-compatible format.

The exported directory can be loaded with::

    from datasets import load_dataset
    ds = load_dataset("json", data_files="<output_dir>/data.jsonl")

No HuggingFace ``datasets`` library is required for the export itself;
the output is standard JSONL that the ``datasets`` library can consume.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pipelines.audio_annotation_lab.database.store import Store


def export_to_hf(
    store: Store,
    output_dir: str | Path,
    session_ids: list[str] | None = None,
    push_to_hub: bool = False,
    repo_id: str | None = None,
) -> int:
    """Export annotated audio data to HuggingFace Datasets format.

    Creates a directory containing ``data.jsonl`` (one flat JSON object per
    segment, with annotation labels embedded) and ``dataset_info.json`` with
    metadata.

    If ``push_to_hub`` is ``True``, the user must have the ``datasets``
    library installed and be authenticated with ``huggingface-cli login``.

    Each exported record has a flat structure::

        {
          "session_id": "ses_001",
          "file_name": "interview.mp3",
          "file_path": "/data/interview.mp3",
          "duration": 360.5,
          "sample_rate": 16000,
          "channels": 1,
          "format": "mp3",
          "segment_id": "seg_abc123",
          "segment_index": 3,
          "start_time": 142.5,
          "end_time": 148.3,
          "segment_duration": 5.8,
          "speaker": "economist_1",
          "text": "The central bank raised interest rates...",
          "language": "bn",
          "asr_confidence": 0.92,
          "segment_type": "utterance",
          "annotator": "claude-3-opus",
          "annotator_type": "llm",
          "schema_name": "narrative",
          "annotation_confidence": 0.95,
          "economic_relevance": "relevant",
          "sentiment": "negative",
          "topic": "finance_banking",
          "created_at": "2024-01-15T10:30:00",
          "session_created_at": "2024-01-15T10:00:00"
        }

    Args:
        store: A ``Store`` instance.
        output_dir: Destination directory for the HuggingFace dataset.
        session_ids: Optional filter — only these session IDs.
        push_to_hub: If ``True``, also push to HuggingFace Hub (requires
            ``datasets`` library and authentication).
        repo_id: HuggingFace repository ID (e.g. ``"lilalab/bengali-audio"``).
            Required when ``push_to_hub`` is ``True``.

    Returns:
        Number of records (annotated segments) written.
    """
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    data_path = out_dir / "data.jsonl"
    count = 0

    records: list[dict[str, Any]] = []
    sessions = store.list_sessions()

    for session in sessions:
        if session_ids is not None and session.id not in session_ids:
            continue
        segments = store.load_segments(session.id)
        for seg in segments:
            annotations = store.load_annotations(seg.id)

            # If no annotations, still export the segment with empty fields
            if not annotations:
                record = _build_hf_record(session, seg, None)
                records.append(record)
                count += 1
                continue

            # One output row per annotation (enables multi-annotator analysis)
            for ann in annotations:
                record = _build_hf_record(session, seg, ann)
                records.append(record)
                count += 1

    with open(data_path, "w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")

    # Write dataset metadata
    dataset_info_path = out_dir / "dataset_info.json"
    dataset_info = {
        "description": (
            "Audio Annotation Lab — annotated speech segments from "
            "low-resource languages."
        ),
        "citation": "",
        "homepage": "",
        "license": "",
        "features": _infer_features(records),
    }
    with open(dataset_info_path, "w", encoding="utf-8") as f:
        json.dump(dataset_info, f, indent=2, ensure_ascii=False)

    # Optional push to HuggingFace Hub
    if push_to_hub:
        _push_to_hub(out_dir, repo_id)

    return count


def _build_hf_record(
    session: Any,
    segment: Any,
    annotation: Any | None,
) -> dict[str, Any]:
    """Build a flat dictionary for one (segment, annotation) pair."""
    rec: dict[str, Any] = {
        # Session fields
        "session_id": session.id,
        "file_name": session.file_name,
        "file_path": session.file_path,
        "duration": session.duration,
        "sample_rate": session.sample_rate,
        "channels": session.channels,
        "format": session.format,
        "session_created_at": session.created_at,
        # Segment fields
        "segment_id": segment.id,
        "segment_index": segment.index,
        "start_time": segment.start_time,
        "end_time": segment.end_time,
        "segment_duration": segment.duration,
        "speaker": segment.speaker,
        "text": segment.text,
        "language": segment.language,
        "asr_confidence": segment.confidence,
        "segment_type": segment.segment_type,
    }

    if annotation is not None:
        rec["annotator"] = annotation.annotator
        rec["annotator_type"] = annotation.annotator_type
        rec["schema_name"] = annotation.schema_name
        rec["annotation_confidence"] = annotation.confidence
        rec["annotation_created_at"] = annotation.created_at
        # Flatten labels as top-level columns
        for k, v in (annotation.labels or {}).items():
            if k not in rec:  # don't overwrite base fields
                rec[k] = v
    else:
        rec["annotator"] = ""
        rec["annotator_type"] = ""
        rec["schema_name"] = ""
        rec["annotation_confidence"] = 0.0
        rec["annotation_created_at"] = ""

    return rec


def _infer_features(records: list[dict[str, Any]]) -> dict[str, dict[str, str]]:
    """Infer HuggingFace feature types from a sample of records.

    Returns a dict mapping field names to ``{"_type": "..."}`` descriptors.
    """
    type_map: dict[str, str] = {}
    for rec in records:
        for k, v in rec.items():
            if k in type_map:
                continue
            if isinstance(v, bool):
                type_map[k] = "bool"
            elif isinstance(v, int):
                type_map[k] = "int64"
            elif isinstance(v, float):
                type_map[k] = "float32"
            elif isinstance(v, str):
                type_map[k] = "string"
            elif v is None:
                type_map[k] = "null"
            else:
                type_map[k] = "string"
    return {k: {"_type": v} for k, v in type_map.items()}


def _push_to_hub(out_dir: Path, repo_id: str | None) -> None:
    """Push the exported dataset to HuggingFace Hub.

    Requires the ``datasets`` package and ``huggingface-cli`` authentication.

    Args:
        out_dir: Directory containing ``data.jsonl``.
        repo_id: HuggingFace dataset repository ID.

    Raises:
        ImportError: If the ``datasets`` library is not installed.
        ValueError: If ``repo_id`` is ``None``.
    """
    if repo_id is None:
        raise ValueError("repo_id is required when push_to_hub=True")
    try:
        import datasets  # type: ignore[import-untyped]
    except ImportError as err:
        raise ImportError(
            "The 'datasets' library is required to push to the Hub. "
            "Install it with: pip install datasets"
        ) from err

    ds = datasets.load_dataset("json", data_files=str(out_dir / "data.jsonl"))
    ds.push_to_hub(repo_id)
