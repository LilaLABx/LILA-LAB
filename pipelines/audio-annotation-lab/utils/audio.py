"""
Audio I/O and processing utilities for Audio Annotation Lab.

Lightweight wrappers around ``soundfile`` (when available) with
``ffprobe`` / ``ffmpeg`` fallback.  No ``torch`` dependency.

Functions
---------
get_audio_info
    Read metadata from an audio file.
convert_format
    Resample / re-encode audio to a standard format.
extract_segment
    Extract a time-range segment from an audio file.
normalize_audio
    Apply loudness normalisation (RMS-based).
validate_audio
    Check an audio file for usability.
"""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path
from typing import Any

# ── Helpers ────────────────────────────────────────────────────────────


def _has_soundfile() -> bool:
    """Check whether ``soundfile`` is installed."""
    try:
        import soundfile  # noqa: F401

        return True
    except ImportError:
        return False


def _has_ffmpeg() -> bool:
    """Check whether ``ffmpeg`` is on ``PATH``."""
    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            check=False,
        )
        return True
    except FileNotFoundError:
        return False


def _has_ffprobe() -> bool:
    """Check whether ``ffprobe`` is on ``PATH``."""
    try:
        subprocess.run(
            ["ffprobe", "-version"],
            capture_output=True,
            check=False,
        )
        return True
    except FileNotFoundError:
        return False


# ── Public API ─────────────────────────────────────────────────────────


def get_audio_info(path: str | Path) -> dict[str, Any]:
    """Read metadata from an audio file.

    Uses ``soundfile`` if available, otherwise falls back to ``ffprobe``.

    Parameters
    ----------
    path : str | Path
        Path to the audio file.

    Returns
    -------
    dict
        Metadata with keys: ``duration``, ``sample_rate``, ``channels``,
        ``format``, ``file_size`` (bytes).

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    RuntimeError
        If neither ``soundfile`` nor ``ffprobe`` can read the file.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Audio file not found: {path}")

    file_size = path.stat().st_size
    ext = path.suffix.lower().lstrip(".")

    info: dict[str, Any] = {
        "duration": 0.0,
        "sample_rate": 0,
        "channels": 0,
        "format": ext or "unknown",
        "file_size": file_size,
    }

    # Try soundfile first
    if _has_soundfile():
        try:
            import soundfile as sf  # type: ignore[import-untyped]

            sfinfo = sf.info(str(path))
            info["duration"] = round(float(sfinfo.duration), 3)
            info["sample_rate"] = int(sfinfo.samplerate)
            info["channels"] = int(sfinfo.channels)
            info["format"] = sfinfo.format or ext
            return info
        except Exception:
            pass

    # Fallback: ffprobe
    if _has_ffprobe():
        cmd = [
            "ffprobe",
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            str(path),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if result.returncode == 0:
            try:
                data = json.loads(result.stdout)
                streams = data.get("streams", [])
                fmt = data.get("format", {})

                # Prefer first audio stream
                for stream in streams:
                    if stream.get("codec_type") == "audio":
                        info["sample_rate"] = int(stream.get("sample_rate", 0))
                        info["channels"] = int(stream.get("channels", 0))
                        break

                duration_str = fmt.get("duration", "0")
                info["duration"] = round(float(duration_str), 3)
                format_name = fmt.get("format_name", ext)
                info["format"] = format_name
                return info
            except (json.JSONDecodeError, ValueError, KeyError):
                pass

    raise RuntimeError(
        f"Unable to read audio metadata for {path}. Install soundfile or ensure ffprobe is on PATH."
    )


def convert_format(
    input_path: str | Path,
    output_path: str | Path,
    target_sr: int = 16000,
    target_channels: int = 1,
    target_format: str = "wav",
) -> Path:
    """Convert an audio file to a standard format.

    Uses ``soundfile`` when possible, otherwise ``ffmpeg``.

    Parameters
    ----------
    input_path : str | Path
        Source audio file.
    output_path : str | Path
        Destination path (will be created / overwritten).
    target_sr : int
        Target sample rate (Hz, default 16000).
    target_channels : int
        Target number of channels (default 1 = mono).
    target_format : str
        Output format (default ``"wav"``).

    Returns
    -------
    Path
        Absolute path to the converted file.

    Raises
    ------
    RuntimeError
        If conversion fails.
    """
    input_path = Path(input_path)
    output_path = Path(output_path)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Try soundfile first (WAV only)
    if _has_soundfile() and target_format.lower() in ("wav", "flac"):
        try:
            import soundfile as sf  # type: ignore[import-untyped]

            data, sr = sf.read(str(input_path))
            # Resample if needed
            if sr != target_sr:
                data = _resample_numpy(data, sr, target_sr)
            # Convert channels
            if data.ndim == 1 and target_channels > 1:
                import numpy as np  # type: ignore[import-untyped]

                data = np.column_stack([data] * target_channels)
            elif data.ndim > 1 and target_channels == 1:
                import numpy as np  # type: ignore[import-untyped]

                data = np.mean(data, axis=1)

            sf.write(str(output_path), data, target_sr)
            return output_path.resolve()
        except Exception:
            pass

    # Fallback: ffmpeg
    if not _has_ffmpeg():
        raise RuntimeError("Neither soundfile nor ffmpeg is available for format conversion.")

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-ar",
        str(target_sr),
        "-ac",
        str(target_channels),
        "-f",
        target_format,
        str(output_path),
    ]
    result = subprocess.run(cmd, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg conversion failed:\n{result.stderr.decode(errors='replace')}")

    return output_path.resolve()


def extract_segment(
    input_path: str | Path,
    output_path: str | Path,
    start_time: float,
    end_time: float,
) -> Path:
    """Extract a time-range segment from an audio file.

    Parameters
    ----------
    input_path : str | Path
        Source audio file.
    output_path : str | Path
        Destination path.
    start_time : float
        Start time in seconds.
    end_time : float
        End time in seconds.

    Returns
    -------
    Path
        Absolute path to the extracted segment.

    Raises
    ------
    ValueError
        If ``start_time >= end_time``.
    RuntimeError
        If extraction fails.
    """
    if start_time >= end_time:
        msg = f"start_time ({start_time}) must be less than end_time ({end_time})"
        raise ValueError(msg)

    input_path = Path(input_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    duration = end_time - start_time

    if not _has_ffmpeg():
        raise RuntimeError("ffmpeg is required for segment extraction.")

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-ss",
        str(start_time),
        "-t",
        str(duration),
        "-c",
        "copy",
        str(output_path),
    ]
    result = subprocess.run(cmd, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(
            f"ffmpeg segment extraction failed:\n{result.stderr.decode(errors='replace')}"
        )

    return output_path.resolve()


def normalize_audio(
    input_path: str | Path,
    output_path: str | Path | None = None,
    target_level: float = -16.0,
) -> Path:
    """Normalise audio loudness using RMS-based adjustment.

    Uses ``soundfile`` if available, otherwise ``ffmpeg`` loudnorm filter.

    Parameters
    ----------
    input_path : str | Path
        Source audio file.
    output_path : str | Path | None
        Destination path.  If ``None``, ``{stem}_normalized{ext}`` is used.
    target_level : float
        Target RMS level in dB (default -16.0 dB).

    Returns
    -------
    Path
        Absolute path to the normalised file.
    """
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    if output_path is None:
        output_path = input_path.with_stem(input_path.stem + "_normalized")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Try soundfile-based RMS normalisation
    if _has_soundfile():
        try:
            import numpy as np  # type: ignore[import-untyped]
            import soundfile as sf  # type: ignore[import-untyped]

            data, sr = sf.read(str(input_path))
            # Current RMS in dB
            rms = math.sqrt(np.mean(data**2))
            if rms < 1e-10:
                # Silent file — just copy
                sf.write(str(output_path), data, sr)
                return output_path.resolve()

            current_db = 20.0 * math.log10(rms)
            gain_db = target_level - current_db
            gain_linear = 10.0 ** (gain_db / 20.0)
            data_normalized = data * gain_linear

            # Prevent clipping
            max_val = np.max(np.abs(data_normalized))
            if max_val > 0.99:
                data_normalized = data_normalized / max_val * 0.99

            sf.write(str(output_path), data_normalized, sr)
            return output_path.resolve()
        except Exception:
            pass

    # Fallback: ffmpeg loudnorm
    if not _has_ffmpeg():
        raise RuntimeError("Neither soundfile nor ffmpeg is available for loudness normalisation.")

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-af",
        f"loudnorm=I={target_level}:LRA=7:TP=-1.5",
        str(output_path),
    ]
    result = subprocess.run(cmd, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(
            f"ffmpeg loudness normalisation failed:\n{result.stderr.decode(errors='replace')}"
        )

    return output_path.resolve()


def validate_audio(
    input_path: str | Path,
    min_duration: float = 0.5,
    max_duration: float = 36000.0,
) -> tuple[bool, str]:
    """Validate an audio file for usability in the annotation pipeline.

    Checks performed:
    - File exists and is readable.
    - Duration is within ``[min_duration, max_duration]``.
    - Sample rate is ≥ 8000 Hz.
    - Has at least 1 channel.

    Parameters
    ----------
    input_path : str | Path
        Path to the audio file.
    min_duration : float
        Minimum acceptable duration in seconds.
    max_duration : float
        Maximum acceptable duration in seconds.

    Returns
    -------
    valid : bool
        ``True`` if the file passes all checks.
    message : str
        Human-readable validation message.
    """
    input_path = Path(input_path)

    if not input_path.exists():
        return False, f"File does not exist: {input_path}"

    if not input_path.is_file():
        return False, f"Path is not a file: {input_path}"

    if input_path.stat().st_size == 0:
        return False, f"File is empty: {input_path}"

    try:
        info = get_audio_info(str(input_path))
    except (RuntimeError, Exception) as exc:
        return False, f"Unable to read audio metadata: {exc}"

    dur = info["duration"]
    if dur < min_duration:
        return (
            False,
            f"Duration {dur:.2f}s is below minimum {min_duration:.2f}s",
        )
    if dur > max_duration:
        return (
            False,
            f"Duration {dur:.2f}s exceeds maximum {max_duration:.2f}s",
        )

    sr = info["sample_rate"]
    if sr < 8000:
        return (
            False,
            f"Sample rate {sr} Hz is below minimum 8000 Hz",
        )

    if info["channels"] < 1:
        return False, f"Invalid channel count: {info['channels']}"

    return True, f"Audio validated: {dur:.2f}s, {sr} Hz, {info['channels']} ch"


# ── Internal helpers ───────────────────────────────────────────────────


def _resample_numpy(
    data: Any,
    orig_sr: int,
    target_sr: int,
) -> Any:
    """Simple linear-interpolation resample using NumPy (no librosa).

    This is intentionally basic; for production use ``librosa.resample``
    or ``scipy.signal.resample``.
    """
    import numpy as np  # type: ignore[import-untyped]

    n_orig = data.shape[0] if hasattr(data, "shape") else len(data)
    n_target = int(round(n_orig * target_sr / orig_sr))
    indices = np.linspace(0, n_orig - 1, n_target)
    return np.interp(indices, np.arange(n_orig), data)
