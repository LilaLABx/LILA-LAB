"""Data models for the Audio Annotation Lab.

Defines the core dataclass-based ORM models:
    AudioSession — A single audio file/session.
    AudioSegment — A time-bounded segment within a session.
    Annotation   — A label set applied to a segment by an annotator.

All models use pure Python ``@dataclass`` with no external dependencies.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class AudioSession:
    """A single audio recording session.

    Each AudioSession represents one audio file that has been (or will be)
    transcribed, segmented, and annotated.

    Attributes:
        id: Unique session identifier (UUID).
        file_path: Absolute or relative path to the original audio file.
        file_name: Base name of the audio file (e.g. ``interview.mp3``).
        duration: Total duration in seconds.
        sample_rate: Audio sample rate in Hz (e.g. 16000, 44100).
        channels: Number of audio channels (1 = mono, 2 = stereo).
        format: File format extension (e.g. ``mp3``, ``wav``, ``ogg``, ``flac``).
        file_size: File size in bytes.
        metadata: Arbitrary user-defined key-value metadata.
        created_at: ISO-8601 timestamp of creation.
        updated_at: ISO-8601 timestamp of last update.
    """

    id: str
    file_path: str
    file_name: str
    duration: float
    sample_rate: int
    channels: int
    format: str
    file_size: int
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AudioSession:
        """Deserialize from a dictionary."""
        return cls(**data)


@dataclass
class AudioSegment:
    """A time-bounded segment within an audio session.

    Segments form the primary unit of transcription and annotation. Each
    segment covers a contiguous time range and can represent an utterance,
    sentence, word, or custom boundary.

    Attributes:
        id: Unique segment identifier (UUID).
        session_id: Foreign key referencing the parent ``AudioSession.id``.
        index: Ordinal position of this segment within the session (0-based).
        start_time: Start time in seconds relative to the audio file.
        end_time: End time in seconds relative to the audio file.
        duration: Duration in seconds (end_time - start_time).
        speaker: Speaker label or identifier.
        text: Transcribed text content.
        language: BCP-47 language code (e.g. ``bn``, ``ha``, ``en``).
        confidence: ASR confidence score in [0.0, 1.0].
        segment_type: Semantic type — ``utterance``, ``sentence``, ``word``, or ``custom``.
        metadata: Arbitrary user-defined key-value metadata.
    """

    id: str
    session_id: str
    index: int
    start_time: float
    end_time: float
    duration: float
    speaker: str = ""
    text: str = ""
    language: str = ""
    confidence: float = 0.0
    segment_type: str = "utterance"
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AudioSegment:
        """Deserialize from a dictionary."""
        return cls(**data)


@dataclass
class Annotation:
    """A set of labels applied to a segment by an annotator.

    Annotations are the output of the annotation layer — whether from an
    LLM or a human annotator. Each annotation references a single segment
    and carries labels structured according to a named schema.

    Attributes:
        id: Unique annotation identifier (UUID).
        segment_id: Foreign key referencing the ``AudioSegment.id``.
        annotator: Model name (e.g. ``claude-3-opus``) or human annotator ID.
        annotator_type: ``"llm"`` or ``"human"``.
        schema_name: Name of the annotation schema used (e.g. ``"narrative"``).
        labels: Annotation labels keyed by field name (e.g. ``{"sentiment": "positive"}``).
        confidence: Overall annotation confidence in [0.0, 1.0].
        created_at: ISO-8601 timestamp of creation.
        metadata: Optional ancillary data (raw LLM response, latency, etc.).
    """

    id: str
    segment_id: str
    annotator: str = ""
    annotator_type: str = "llm"
    schema_name: str = ""
    labels: dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.0
    created_at: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-compatible dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Annotation:
        """Deserialize from a dictionary."""
        return cls(**data)
