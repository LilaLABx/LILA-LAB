#!/usr/bin/env python3
"""
Main ASR transcription pipeline for the Audio Annotation Lab.

Supports ``openai-whisper`` and ``faster-whisper`` backends.  Processes
single audio files or batches of files from a directory, and writes
JSONL output with full segment structure.

CLI Usage::

    # Single file
    python transcribe.py --input audio.mp3 --output data/processed/ \\
        --model whisper-small --language bengali --device cpu

    # Batch directory
    python transcribe.py --input data/raw/ --batch --output data/processed/ \\
        --model faster-whisper-large-v3 --device cuda

Programmatic usage::

    >>> from pipelines.audio_annotation_lab.asr.transcribe import transcribe_file
    >>> session = transcribe_file("audio.mp3", "data/processed/")
"""

import argparse
import json
import logging
import uuid
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Supported audio extensions (lowercase, without dot)
AUDIO_EXTENSIONS: set[str] = {".mp3", ".wav", ".ogg", ".flac", ".m4a", ".aac", ".wma"}

# ── Internal helpers ───────────────────────────────────────────────────


def _get_audio_duration(audio_path: Path) -> float:
    """Return the duration of an audio file in seconds.

    Uses ``librosa.get_duration()`` (lazy import).

    Args:
        audio_path: Path to the audio file.

    Returns:
        Duration in seconds, or ``0.0`` on failure.
    """
    try:
        import librosa
        return float(librosa.get_duration(path=str(audio_path)))
    except Exception as exc:
        logger.warning("Could not get duration for '%s': %s", audio_path, exc)
        return 0.0


def _is_audio_file(path: Path) -> bool:
    """Check whether a path is a supported audio file (not a directory)."""
    return path.is_file() and path.suffix.lower() in AUDIO_EXTENSIONS


def _find_audio_files(directory: Path) -> list[Path]:
    """Recursively collect all supported audio files from a directory.

    Args:
        directory: Directory to scan.

    Returns:
        Sorted list of audio file paths.
    """
    files: list[Path] = []
    for ext in AUDIO_EXTENSIONS:
        files.extend(directory.rglob(f"*{ext}"))
    return sorted(files)


def _save_session_jsonl(session: dict, output_path: Path) -> None:
    """Append one JSON line to a JSONL file.

    Args:
        session: Session dict to serialize.
        output_path: Path to the output JSONL file.
    """
    with open(str(output_path), "a", encoding="utf-8") as f:
        f.write(json.dumps(session, ensure_ascii=False, default=str) + "\n")


# ── Backend-specific transcription ─────────────────────────────────────


def _transcribe_openai_whisper(
    audio_path: Path,
    model_name: str,
    language: str | None,
    device: str,
) -> tuple[list[dict[str, Any]], str]:
    """Transcribe using ``openai-whisper``.

    Returns:
        Tuple of (segments_list, detected_language).
    """
    import whisper  # type: ignore[import-untyped]

    logger.info(
        "Loading openai-whisper model '%s' on %s …",
        model_name, device,
    )
    model = whisper.load_model(model_name, device=device)

    logger.info("Transcribing '%s' …", audio_path.name)
    result = model.transcribe(
        str(audio_path),
        language=language,
        temperature=0.0,
        compression_ratio_threshold=2.4,
        logprob_threshold=-1.0,
        no_speech_threshold=0.6,
        condition_on_previous_text=False,
    )

    detected_language: str = result.get("language", language or "unknown")

    segments: list[dict[str, Any]] = []
    for seg in result.get("segments", []):
        seg_id = str(uuid.uuid4())
        segments.append({
            "id": seg_id,
            "start_time": round(float(seg.get("start", 0.0)), 3),
            "end_time": round(float(seg.get("end", 0.0)), 3),
            "speaker": "SPEAKER_00",
            "text": seg.get("text", "").strip(),
            "confidence": round(float(seg.get("confidence", 0.0)), 4),
            "language": detected_language,
        })

    return segments, detected_language


def _transcribe_faster_whisper(
    audio_path: Path,
    model_name: str,
    language: str | None,
    device: str,
) -> tuple[list[dict[str, Any]], str]:
    """Transcribe using ``faster-whisper`` (CTranslate2).

    Returns:
        Tuple of (segments_list, detected_language).
    """
    from faster_whisper import WhisperModel  # type: ignore[import-untyped]

    compute_type = "float16" if device == "cuda" else "int8"
    logger.info(
        "Loading faster-whisper model '%s' on %s (compute_type=%s) …",
        model_name, device, compute_type,
    )
    model = WhisperModel(model_name, device=device, compute_type=compute_type)

    logger.info("Transcribing '%s' …", audio_path.name)
    seg_generator, info = model.transcribe(
        str(audio_path),
        language=language,
        beam_size=5,
        vad_filter=True,
        vad_parameters=dict(
            min_silence_duration_ms=500,
            threshold=0.5,
        ),
    )

    detected_language: str = info.language if info.language else (language or "unknown")

    segments: list[dict[str, Any]] = []
    for seg in seg_generator:
        seg_id = str(uuid.uuid4())
        segments.append({
            "id": seg_id,
            "start_time": round(float(seg.start), 3),
            "end_time": round(float(seg.end), 3),
            "speaker": "SPEAKER_00",
            "text": seg.text.strip(),
            "confidence": round(float(seg.avg_logprob if hasattr(seg, "avg_logprob") else seg.no_speech_prob), 4),
            "language": detected_language,
        })

    return segments, detected_language


# ── Public API ─────────────────────────────────────────────────────────


def transcribe_file(
    audio_path: Path | str,
    output_dir: Path | str,
    model_name: str = "whisper-small",
    language: str | None = None,
    device: str = "cpu",
) -> dict[str, Any]:
    """Transcribe a single audio file and write its JSONL output.

    Args:
        audio_path: Path to the input audio file.
        output_dir: Directory for output files (created if missing).
        model_name: ASR model name from ``models.MODEL_REGISTRY``.
        language: Language code (e.g. ``"bn"`` for Bengali) or ``None``
                  for auto-detection.
        device: ``"cpu"`` or ``"cuda"``.

    Returns:
        Session dict with the transcription result (also written to disk).

    Raises:
        FileNotFoundError: If ``audio_path`` does not exist.
        KeyError: If ``model_name`` is unknown.
        RuntimeError: If transcription fails.
    """
    audio_path = Path(audio_path).resolve()
    output_dir = Path(output_dir).resolve()

    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    # Lazy-import model registry to avoid circular dependencies
    from pipelines.audio_annotation_lab.asr.models import get_model_config

    config = get_model_config(model_name)
    backend: str = config["backend"]
    whisper_model_name: str = config["model_name"]

    output_dir.mkdir(parents=True, exist_ok=True)

    # Duration
    duration = _get_audio_duration(audio_path)

    # Transcribe
    try:
        if backend == "openai-whisper":
            segments, detected_lang = _transcribe_openai_whisper(
                audio_path, whisper_model_name, language, device,
            )
        elif backend == "faster-whisper":
            segments, detected_lang = _transcribe_faster_whisper(
                audio_path, whisper_model_name, language, device,
            )
        else:
            raise RuntimeError(f"Unsupported backend: {backend}")
    except Exception as exc:
        raise RuntimeError(
            f"Transcription failed for '{audio_path.name}': {exc}"
        ) from exc

    # Build session record
    session_id = str(uuid.uuid4())
    session: dict[str, Any] = {
        "session_id": session_id,
        "file_path": str(audio_path),
        "duration": duration,
        "segments": segments,
    }

    # Write output
    output_file = output_dir / f"{audio_path.stem}.jsonl"
    _save_session_jsonl(session, output_file)
    logger.info(
        "Transcribed '%s' → '%s' (%d segments, %s)",
        audio_path.name,
        output_file.name,
        len(segments),
        detected_lang,
    )

    return session


def transcribe_batch(
    input_dir: Path | str,
    output_dir: Path | str,
    model_name: str = "whisper-small",
    language: str | None = None,
    device: str = "cpu",
    intermediate_save_interval: int = 10,
) -> list[dict[str, Any]]:
    """Transcribe all audio files in a directory.

    Processes every supported audio file found in ``input_dir``
    (recursive).  Saves an intermediate checkpoint every
    ``intermediate_save_interval`` files so partial progress is not lost.

    Args:
        input_dir: Directory containing audio files.
        output_dir: Directory for output JSONL files.
        model_name: ASR model name.
        language: Language code or ``None`` for auto-detect.
        device: ``"cpu"`` or ``"cuda"``.
        intermediate_save_interval: Number of files between checkpoint saves.

    Returns:
        List of session dicts, one per successfully transcribed file.
    """
    input_dir = Path(input_dir).resolve()
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    audio_files = _find_audio_files(input_dir)
    if not audio_files:
        logger.warning("No audio files found in '%s'", input_dir)
        return []

    logger.info(
        "Batch processing %d audio files from '%s' …",
        len(audio_files), input_dir,
    )

    sessions: list[dict[str, Any]] = []
    total = len(audio_files)
    checkpoint_file = output_dir / "transcriptions.jsonl"

    for i, audio_path in enumerate(audio_files, 1):
        try:
            session = transcribe_file(
                audio_path=audio_path,
                output_dir=output_dir,
                model_name=model_name,
                language=language,
                device=device,
            )
            sessions.append(session)

            # Also write to the combined JSONL
            _save_session_jsonl(session, checkpoint_file)

            logger.info("  [%d/%d] ✓ %s", i, total, audio_path.name)

        except Exception as exc:
            logger.error(
                "  [%d/%d] ✗ %s — %s",
                i, total, audio_path.name, exc,
            )
            # Continue with next file
            continue

        # Intermediate checkpoint
        if i % intermediate_save_interval == 0:
            ckpt = output_dir / f"checkpoint_{i:04d}.jsonl"
            for s in sessions:
                _save_session_jsonl(s, ckpt)
            logger.info("  Checkpoint saved: %s (%d sessions)", ckpt.name, len(sessions))

    logger.info(
        "Batch complete: %d / %d files transcribed successfully",
        len(sessions), total,
    )
    return sessions


# ── CLI ────────────────────────────────────────────────────────────────


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    parser = argparse.ArgumentParser(
        description="ASR Transcription Pipeline — Audio Annotation Lab",
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Input audio file or directory (use --batch for directories)",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output directory for transcription JSONL files",
    )
    parser.add_argument(
        "--model",
        default="whisper-small",
        help="ASR model name (see models.list_available_models())",
    )
    parser.add_argument(
        "--language",
        default=None,
        help="Language code (e.g. 'bn' for Bengali). Auto-detect if omitted.",
    )
    parser.add_argument(
        "--device",
        default="cpu",
        choices=["cpu", "cuda"],
        help="Device to run inference on (default: cpu)",
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Process all audio files in the input directory",
    )
    parser.add_argument(
        "--checkpoint-interval",
        type=int,
        default=10,
        help="Number of files between intermediate saves in batch mode (default: 10)",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output)

    if args.batch:
        if not input_path.is_dir():
            parser.error("--batch requires --input to be a directory")
        transcribe_batch(
            input_dir=input_path,
            output_dir=output_dir,
            model_name=args.model,
            language=args.language,
            device=args.device,
            intermediate_save_interval=args.checkpoint_interval,
        )
    else:
        if not input_path.is_file():
            parser.error(
                f"Input file not found: {input_path}. "
                "Use --batch for directories."
            )
        transcribe_file(
            audio_path=input_path,
            output_dir=output_dir,
            model_name=args.model,
            language=args.language,
            device=args.device,
        )


if __name__ == "__main__":
    main()
