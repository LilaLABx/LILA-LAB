"""JSONL-based storage backend for the Audio Annotation Lab.

Storage layout on disk::

    <base_dir>/
    ├── sessions.jsonl              # All AudioSession records
    └── <session_id>/
        ├── segments.jsonl           # All AudioSegment records for this session
        └── annotations.jsonl        # All Annotation records for this session

No external database is required — the entire store is built on JSONL files
under a single directory tree.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from pipelines.audio_annotation_lab.database.models import Annotation, AudioSegment, AudioSession


class Store:
    """JSONL-based persistent store for audio annotation data.

    Each store maps to a directory on disk.  Sessions, segments, and
    annotations are stored as newline-delimited JSON (JSONL) files.

    Args:
        base_dir: Root directory for all stored data.  Created if it does
            not exist.

    Attributes:
        base_dir: Resolved ``Path`` to the storage root.
    """

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def __init__(self, base_dir: str | Path) -> None:
        self.base_dir = Path(base_dir).resolve()
        self.base_dir.mkdir(parents=True, exist_ok=True)

    # -- Path helpers ---------------------------------------------------

    @property
    def _sessions_path(self) -> Path:
        return self.base_dir / "sessions.jsonl"

    def _session_dir(self, session_id: str) -> Path:
        return self.base_dir / session_id

    def _segments_path(self, session_id: str) -> Path:
        return self._session_dir(session_id) / "segments.jsonl"

    def _annotations_path(self, session_id: str) -> Path:
        return self._session_dir(session_id) / "annotations.jsonl"

    # -- JSONL I/O ------------------------------------------------------

    @staticmethod
    def _read_jsonl(path: Path) -> list[dict[str, Any]]:
        """Read all records from a JSONL file.

        Returns an empty list if the file does not exist.
        """
        if not path.exists():
            return []
        records: list[dict[str, Any]] = []
        with open(path, encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if stripped:
                    records.append(json.loads(stripped))
        return records

    @staticmethod
    def _write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
        """Overwrite a JSONL file with the given records."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            for record in records:
                f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")

    @staticmethod
    def _append_jsonl(path: Path, record: dict[str, Any]) -> None:
        """Append a single record to a JSONL file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")

    # -- Session helpers ------------------------------------------------

    def _rewrite_sessions(self, sessions: list[AudioSession]) -> None:
        """Replace the sessions.jsonl with a new list of sessions."""
        self._write_jsonl(self._sessions_path, [s.to_dict() for s in sessions])

    # ------------------------------------------------------------------
    # Public API — Session CRUD
    # ------------------------------------------------------------------

    def save_session(self, session: AudioSession) -> str:
        """Persist a new audio session.

        The session is appended to ``sessions.jsonl``.  If a session with
        the same ``id`` already exists, a ``ValueError`` is raised.

        Args:
            session: The ``AudioSession`` to persist.

        Returns:
            The session's ``id``.

        Raises:
            ValueError: A session with this ``id`` already exists.
        """
        existing = self.load_session(session.id)
        if existing is not None:
            raise ValueError(f"Session '{session.id}' already exists.")
        self._append_jsonl(self._sessions_path, session.to_dict())
        return session.id

    def load_session(self, session_id: str) -> AudioSession | None:
        """Retrieve a single session by ID.

        Args:
            session_id: The session UUID to look up.

        Returns:
            The matching ``AudioSession``, or ``None`` if not found.
        """
        for record in self._read_jsonl(self._sessions_path):
            if record["id"] == session_id:
                return AudioSession.from_dict(record)
        return None

    def list_sessions(self) -> list[AudioSession]:
        """List all stored sessions.

        Returns:
            A list of ``AudioSession`` objects in insertion order (oldest
            first).
        """
        return [AudioSession.from_dict(r) for r in self._read_jsonl(self._sessions_path)]

    def delete_session(self, session_id: str) -> bool:
        """Delete a session and all its associated data.

        Removes the session from ``sessions.jsonl`` and recursively deletes
        the ``<session_id>/`` directory (including segments and annotations).

        Args:
            session_id: The session UUID to delete.

        Returns:
            ``True`` if the session was found and deleted, ``False`` if no
            session with that ID existed.
        """
        sessions = self._read_jsonl(self._sessions_path)
        filtered = [r for r in sessions if r["id"] != session_id]
        if len(filtered) == len(sessions):
            return False  # nothing removed
        self._write_jsonl(self._sessions_path, filtered)

        # Remove session directory tree
        sdir = self._session_dir(session_id)
        if sdir.exists():
            shutil.rmtree(sdir)
        return True

    # ------------------------------------------------------------------
    # Public API — Segment CRUD
    # ------------------------------------------------------------------

    def save_segments(self, session_id: str, segments: list[AudioSegment]) -> int:
        """Save (overwrite) all segments for a session.

        This replaces any previously stored segments for the given session
        with the provided list.  Use this after re-transcription or when
        importing a fresh set of segments.

            Args:
                session_id: The parent session UUID.
                segments: One or more ``AudioSegment`` objects.

            Returns:
                The number of segments written.
        """
        # Ensure session directory exists
        self._session_dir(session_id).mkdir(parents=True, exist_ok=True)
        self._write_jsonl(
            self._segments_path(session_id),
            [s.to_dict() for s in segments],
        )
        return len(segments)

    def load_segments(self, session_id: str) -> list[AudioSegment]:
        """Load all segments for a session.

        Args:
            session_id: The parent session UUID.

        Returns:
            A list of ``AudioSegment`` objects ordered by insertion.
            Empty list if the session has no segments.
        """
        return [
            AudioSegment.from_dict(r) for r in self._read_jsonl(self._segments_path(session_id))
        ]

    def get_segment(self, segment_id: str) -> AudioSegment | None:
        """Find a single segment by ID across all sessions.

        Args:
            segment_id: The segment UUID to look up.

        Returns:
            The matching ``AudioSegment``, or ``None``.
        """
        # Iterate session directories and search each segments file
        for child in self.base_dir.iterdir():
            if not child.is_dir():
                continue
            seg_path = child / "segments.jsonl"
            for record in self._read_jsonl(seg_path):
                if record["id"] == segment_id:
                    return AudioSegment.from_dict(record)
        return None

    def update_segment(self, segment: AudioSegment) -> bool:
        """Update an existing segment in-place.

        Locates the segment by ID within its session's segments file and
        replaces it.  Raises ``ValueError`` if the session directory or
        segments file is missing.

        Args:
            segment: The ``AudioSegment`` with updated fields.

        Returns:
            ``True`` if the segment was found and updated.
        """
        session_id = segment.session_id
        seg_path = self._segments_path(session_id)
        if not seg_path.exists():
            return False
        records = self._read_jsonl(seg_path)
        updated = False
        for i, rec in enumerate(records):
            if rec["id"] == segment.id:
                records[i] = segment.to_dict()
                updated = True
                break
        if not updated:
            return False
        self._write_jsonl(seg_path, records)
        return True

    # ------------------------------------------------------------------
    # Public API — Annotation CRUD
    # ------------------------------------------------------------------

    def save_annotation(self, annotation: Annotation) -> str:
        """Persist a new annotation.

        The annotation is appended to the appropriate session's
        ``annotations.jsonl`` file.

        Args:
            annotation: The ``Annotation`` to persist.

        Returns:
            The annotation's ``id``.
        """
        session_id = self._resolve_session_for_segment(annotation.segment_id)
        self._append_jsonl(
            self._annotations_path(session_id),
            annotation.to_dict(),
        )
        return annotation.id

    def load_annotations(self, segment_id: str) -> list[Annotation]:
        """Retrieve all annotations for a given segment.

        Searches all session directories for annotations referencing the
        provided segment ID.

        Args:
            segment_id: The segment UUID to look up.

        Returns:
            A list of ``Annotation`` objects (newest-first by file order).
        """
        results: list[Annotation] = []
        for child in self.base_dir.iterdir():
            if not child.is_dir():
                continue
            ann_path = child / "annotations.jsonl"
            if not ann_path.exists():
                continue
            for record in self._read_jsonl(ann_path):
                if record["segment_id"] == segment_id:
                    results.append(Annotation.from_dict(record))
        return results

    def get_annotations_by_annotator(self, annotator: str) -> list[Annotation]:
        """Retrieve all annotations created by a specific annotator.

        Args:
            annotator: The annotator identifier (model name or human ID).

        Returns:
            A list of matching ``Annotation`` objects.
        """
        results: list[Annotation] = []
        for child in self.base_dir.iterdir():
            if not child.is_dir():
                continue
            ann_path = child / "annotations.jsonl"
            if not ann_path.exists():
                continue
            for record in self._read_jsonl(ann_path):
                if record["annotator"] == annotator:
                    results.append(Annotation.from_dict(record))
        return results

    def delete_annotation(self, annotation_id: str) -> bool:
        """Delete a single annotation by ID.

        Searches all session annotation files and removes the matching
        record.

        Args:
            annotation_id: The annotation UUID to delete.

        Returns:
            ``True`` if found and deleted, ``False`` otherwise.
        """
        for child in self.base_dir.iterdir():
            if not child.is_dir():
                continue
            ann_path = child / "annotations.jsonl"
            if not ann_path.exists():
                continue
            records = self._read_jsonl(ann_path)
            filtered = [r for r in records if r["id"] != annotation_id]
            if len(filtered) < len(records):
                self._write_jsonl(ann_path, filtered)
                return True
        return False

    # ------------------------------------------------------------------
    # Bulk operations
    # ------------------------------------------------------------------

    def export_all(self, output_path: str | Path) -> int:
        """Export every record across all sessions to a single JSONL file.

        Each exported line is a flat dictionary with a ``_type`` key that
        is one of ``"session"``, ``"segment"``, or ``"annotation"``.

        Args:
            output_path: Destination file path for the combined JSONL.

        Returns:
            Total number of records written.
        """
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        count = 0
        with open(out, "w", encoding="utf-8") as f:
            # Sessions
            for rec in self._read_jsonl(self._sessions_path):
                rec["_type"] = "session"
                f.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")
                count += 1
            # Segments and annotations per session
            for child in sorted(self.base_dir.iterdir()):
                if not child.is_dir():
                    continue
                for rec in self._read_jsonl(child / "segments.jsonl"):
                    rec["_type"] = "segment"
                    f.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")
                    count += 1
                for rec in self._read_jsonl(child / "annotations.jsonl"):
                    rec["_type"] = "annotation"
                    f.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")
                    count += 1
        return count

    def import_from_jsonl(self, input_path: str | Path) -> int:
        """Import records from a JSONL file produced by ``export_all``.

        Lines with ``_type`` equal to ``"session"``, ``"segment"``, or
        ``"annotation"`` are routed to the correct internal storage.

        Args:
            input_path: Path to the JSONL file to import.

        Returns:
            Number of records successfully imported.
        """
        count = 0
        with open(Path(input_path), encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if not stripped:
                    continue
                record = json.loads(stripped)
                record_type = record.pop("_type", None)
                if record_type == "session":
                    self.save_session(AudioSession.from_dict(record))
                    count += 1
                elif record_type == "segment":
                    sid = record["session_id"]
                    seg = AudioSegment.from_dict(record)
                    self._append_jsonl(self._segments_path(sid), seg.to_dict())
                    count += 1
                elif record_type == "annotation":
                    sid = self._resolve_session_for_segment(record["segment_id"])
                    ann = Annotation.from_dict(record)
                    self._append_jsonl(self._annotations_path(sid), ann.to_dict())
                    count += 1
                else:
                    # Skip unknown type (e.g. raw export lines without _type)
                    continue
        return count

    def stats(self) -> dict[str, Any]:
        """Compute aggregate statistics for the store.

        Returns:
            A dictionary with keys ``sessions``, ``segments``, and
            ``annotations``, each mapping to a count.
        """
        sessions = len(self._read_jsonl(self._sessions_path))
        segments = 0
        annotations = 0
        for child in self.base_dir.iterdir():
            if not child.is_dir():
                continue
            segments += len(self._read_jsonl(child / "segments.jsonl"))
            annotations += len(self._read_jsonl(child / "annotations.jsonl"))
        return {
            "sessions": sessions,
            "segments": segments,
            "annotations": annotations,
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _resolve_session_for_segment(self, segment_id: str) -> str:
        """Find the session ID that owns a given segment.

        Scans all session directories.  Raises ``ValueError`` if no
        segment is found.

        Returns:
            The session ID string.
        """
        for child in self.base_dir.iterdir():
            if not child.is_dir():
                continue
            seg_path = child / "segments.jsonl"
            if not seg_path.exists():
                continue
            for record in self._read_jsonl(seg_path):
                if record["id"] == segment_id:
                    return child.name
        raise ValueError(f"Segment '{segment_id}' not found in any session.")
