#!/usr/bin/env python3
"""
Forced alignment: word-level timestamp generation for ASR transcripts.

Attempts to use ``whisper-timestamped`` for precise word-boundary alignment
when available, falling back to linear interpolation within segments.

Usage:
    >>> from pipelines.audio_annotation_lab.asr.align import align_words
    >>> segments = [{"start_time": 0.0, "end_time": 3.5, "text": "hello world"}]
    >>> word_timings = align_words("audio.wav", segments)
    >>> word_timings["words"]
    [{"word": "hello", "start": 0.1, "end": 0.6, "confidence": 0.98}, ...]
"""

import logging
import re
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def _tokenize_words(text: str) -> list[str]:
    """Split a text string into whitespace-delimited words.

    Args:
        text: Input text.

    Returns:
        List of word strings.
    """
    return re.split(r"\s+", text.strip()) if text.strip() else []


def _linear_interpolate_words(
    segment_text: str,
    start_time: float,
    end_time: float,
    avg_confidence: float,
) -> list[dict[str, Any]]:
    """Assign evenly-spaced timestamps to each word in a segment.

    Useful as a fallback when more precise alignment methods are unavailable.

    Args:
        segment_text: The transcribed text for the segment.
        start_time: Segment start time in seconds.
        end_time: Segment end time in seconds.
        avg_confidence: Average confidence for the segment.

    Returns:
        List of per-word dicts with keys ``word``, ``start``, ``end``,
        ``confidence``.
    """
    words = _tokenize_words(segment_text)
    n_words = len(words)
    if n_words == 0:
        return []

    duration = end_time - start_time
    word_duration = duration / n_words

    word_list: list[dict[str, Any]] = []
    for i, word in enumerate(words):
        w_start = start_time + i * word_duration
        w_end = w_start + word_duration
        word_list.append(
            {
                "word": word,
                "start": round(w_start, 3),
                "end": round(w_end, 3),
                "confidence": round(avg_confidence, 4),
            }
        )
    return word_list


def _try_whisper_timestamped(
    audio_path: Path,
) -> list[dict[str, Any]] | None:
    """Attempt word-level alignment using ``whisper-timestamped``.

    Returns ``None`` if the package is not installed or fails, signalling
    the caller to fall back.

    Args:
        audio_path: Path to the audio file.

    Returns:
        List of word dicts with at minimum ``word``, ``start``, ``end``
        keys, or ``None`` on failure.
    """
    try:
        import whisper_timestamped  # type: ignore[import-untyped]
    except ImportError:
        logger.debug("whisper-timestamped not available — will use linear interpolation")
        return None

    try:
        import whisper  # openai-whisper base model
    except ImportError:
        logger.debug("openai-whisper not available for whisper-timestamped")
        return None

    try:
        # Load model (use tiny for speed; alignment is the goal, not quality)
        model = whisper.load_model("tiny")
        audio = whisper_timestamped.load_audio(str(audio_path))
        result = whisper_timestamped.transcribe(model, audio, language=None)

        words: list[dict[str, Any]] = []
        for seg in result.get("segments", []):
            for w in seg.get("words", []):
                words.append(
                    {
                        "word": w.get("text", "").strip(),
                        "start": round(float(w.get("start", 0.0)), 3),
                        "end": round(float(w.get("end", 0.0)), 3),
                        "confidence": round(float(w.get("confidence", 0.0)), 4),
                    }
                )
        return words if words else None
    except Exception as exc:
        logger.warning("whisper-timestamped alignment failed: %s", exc)
        return None


def align_words(
    audio_path: Path | str,
    segments: list[dict[str, Any]],
) -> dict[str, Any]:
    """Generate word-level timestamps for each segment.

    Pipeline:
        1. Try ``whisper-timestamped`` for precise alignment.
        2. Fall back to linear interpolation per segment.

    Args:
        audio_path: Path to the audio file (used by whisper-timestamped).
        segments: List of segment dicts.  Each must contain ``start_time``,
                  ``end_time``, ``text``, and optionally ``confidence``.

    Returns:
        Dict with a ``words`` key containing a flat list of word-level
        annotations::

            {
                "words": [
                    {
                        "word": "rice",
                        "start": 142.5,
                        "end": 142.8,
                        "confidence": 0.97
                    },
                    ...
                ]
            }
    """
    audio_path = Path(audio_path)
    result_words: list[dict[str, Any]] = []

    # Attempt precise alignment with whisper-timestamped
    precise = _try_whisper_timestamped(audio_path)

    if precise is not None and len(precise) > 0:
        logger.info("Precise alignment produced %d word timestamps", len(precise))
        return {"words": precise}

    # Fall back: linear interpolation per segment
    logger.info("Falling back to linear interpolation for word timestamps")
    total_words = 0
    for seg in segments:
        text = seg.get("text", "").strip()
        if not text:
            continue

        start = float(seg.get("start_time", 0.0))
        end = float(seg.get("end_time", 0.0))
        confidence = float(seg.get("confidence", 0.9))

        word_list = _linear_interpolate_words(text, start, end, confidence)
        result_words.extend(word_list)
        total_words += len(word_list)

    logger.info("Linear interpolation produced %d word timestamps", total_words)
    return {"words": result_words}
