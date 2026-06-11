#!/usr/bin/env python3
"""
Audio preprocessing for ASR pipelines.

Converts any audio format to 16 kHz mono WAV, applies noise reduction via
spectral gating, and strips leading / trailing silence using energy-based
Voice Activity Detection (VAD).

All heavy imports (librosa, soundfile, numpy) are lazy — they are loaded
only when the ``preprocess()`` function is called.

Usage:
    >>> from pipelines.audio_annotation_lab.asr.preprocess import preprocess
    >>> wav_path = preprocess("interview.mp3", "data/processed/")
"""

from __future__ import annotations

import logging
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import numpy as np

logger = logging.getLogger(__name__)


def _ffmpeg_convert_to_wav(
    input_path: Path,
    output_path: Path,
    target_sr: int = 16000,
) -> None:
    """Convert any audio file to a mono WAV at the target sample rate.

    Uses ffmpeg under the hood.  Raises ``RuntimeError`` on failure.

    Args:
        input_path: Source audio file path.
        output_path: Destination WAV path.
        target_sr: Target sample rate in Hz.
    """
    cmd = [
        "ffmpeg",
        "-y",  # overwrite output without asking
        "-i",
        str(input_path),
        "-ac",
        "1",  # mono
        "-ar",
        str(target_sr),
        "-sample_fmt",
        "s16",
        "-loglevel",
        "error",
        str(output_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg conversion failed for '{input_path}': {result.stderr.strip()}")


def _spectral_gate_noise_reduction(
    audio: np.ndarray,
    sr: int,
    noise_fraction: float = 0.05,
) -> np.ndarray:
    """Apply simple spectral-gating noise reduction.

    Estimates the noise profile from the first ``noise_fraction`` of the
    signal and suppresses stationary noise components.

    Args:
        audio: 1-D audio signal.
        sr: Sample rate of the audio.
        noise_fraction: Fraction of the signal start to use for noise profiling.

    Returns:
        Noise-reduced 1-D audio signal.
    """
    import librosa
    import numpy as np

    # Compute STFT
    D = librosa.stft(audio)
    magnitude, phase = librosa.magphase(D)

    # Estimate noise profile from the first portion
    n_frames = magnitude.shape[1]
    noise_frames_count = max(1, int(n_frames * noise_fraction))
    noise_profile = np.mean(magnitude[:, :noise_frames_count] ** 2, axis=1, keepdims=True)

    # Spectral subtraction (half-wave rectification)
    magnitude_denoised = np.maximum(magnitude**2 - noise_profile, 0.0) ** 0.5
    D_denoised = magnitude_denoised * phase
    return librosa.istft(D_denoised)


def _strip_silence_vad(
    audio: np.ndarray,
    sr: int,
    frame_duration_ms: float = 30.0,
    silence_percentile: float = 10.0,
    min_silence_ms: float = 200.0,
) -> np.ndarray:
    """Strip leading / trailing silence using energy-based VAD.

    Computes RMS energy over sliding frames and thresholds at the given
    percentile.  Silence shorter than ``min_silence_ms`` inside speech is
    preserved.

    Args:
        audio: 1-D audio signal.
        sr: Sample rate.
        frame_duration_ms: Frame length in milliseconds.
        silence_percentile: Bottom percentile of frame energy considered silence.
        min_silence_ms: Minimum silence duration (ms) to be trimmed.

    Returns:
        Audio with leading/trailing silence removed.
    """
    import librosa
    import numpy as np

    frame_length = int(sr * frame_duration_ms / 1000)
    hop_length = frame_length // 2

    # Frame energy
    energy = librosa.feature.rms(y=audio, frame_length=frame_length, hop_length=hop_length)[0]

    threshold = float(np.percentile(energy, silence_percentile))
    is_speech = energy > threshold

    # Convert frame-level mask to sample indices
    # Each frame covers hop_length samples
    speech_samples = np.repeat(is_speech, hop_length)
    # Trim to audio length
    speech_samples = speech_samples[: len(audio)]

    # Find first and last speech sample
    indices = np.where(speech_samples)[0]
    if len(indices) == 0:
        logger.warning("VAD detected no speech — returning original audio unchanged")
        return audio

    start = int(indices[0])
    end = int(indices[-1])

    # Ensure we don't cut shorter than min_silence_ms of actual silence
    silence_pad = int(sr * min_silence_ms / 1000)
    start = max(0, start - silence_pad)
    end = min(len(audio), end + silence_pad)

    return audio[start:end]


def preprocess(
    input_path: Path | str,
    output_dir: Path | str,
    target_sr: int = 16000,
    apply_noise_reduction: bool = True,
    apply_vad: bool = True,
) -> Path:
    """Preprocess an audio file for ASR transcription.

    Pipeline:
        1. Convert to 16 kHz mono WAV via ffmpeg.
        2. Apply spectral-gating noise reduction (optional).
        3. Strip leading/trailing silence via VAD (optional).

    All heavy dependencies (``librosa``, ``soundfile``, ``numpy``) are
    imported lazily at call time.

    Args:
        input_path: Path to the input audio file (any format).
        output_dir: Directory where the preprocessed WAV is written.
        target_sr: Target sample rate (default 16 000 Hz — standard for ASR).
        apply_noise_reduction: Whether to apply spectral-gate denoising.
        apply_vad: Whether to strip leading/trailing silence.

    Returns:
        Absolute ``Path`` to the preprocessed WAV file.

    Raises:
        FileNotFoundError: If ``input_path`` does not exist.
        RuntimeError: If ffmpeg conversion or audio processing fails.
    """
    import soundfile as sf

    input_path = Path(input_path).resolve()
    output_dir = Path(output_dir).resolve()

    if not input_path.exists():
        raise FileNotFoundError(f"Input audio not found: {input_path}")

    output_dir.mkdir(parents=True, exist_ok=True)
    intermediate_wav = output_dir / f"{input_path.stem}_raw.wav"
    output_wav = output_dir / f"{input_path.stem}_preprocessed.wav"

    # Step 1: Convert to 16 kHz mono WAV
    logger.info("Converting '%s' → %d Hz mono WAV …", input_path.name, target_sr)
    try:
        _ffmpeg_convert_to_wav(input_path, intermediate_wav, target_sr=target_sr)
    except RuntimeError:
        # Clean up partial output
        if intermediate_wav.exists():
            intermediate_wav.unlink()
        raise

    # Step 2: Load audio for further processing
    audio, sr = sf.read(str(intermediate_wav))
    if audio.ndim > 1:
        # Already mono from ffmpeg, but be safe
        audio = audio.mean(axis=1)

    # Step 3: Noise reduction
    if apply_noise_reduction:
        logger.info("Applying spectral-gate noise reduction …")
        try:
            audio = _spectral_gate_noise_reduction(audio, sr)
        except Exception as exc:
            logger.warning("Noise reduction failed (%s), continuing with original", exc)

    # Step 4: VAD silence stripping
    if apply_vad:
        logger.info("Stripping leading/trailing silence via VAD …")
        try:
            audio = _strip_silence_vad(audio, sr)
        except Exception as exc:
            logger.warning("VAD failed (%s), continuing with original", exc)

    # Step 5: Write preprocessed WAV
    sf.write(str(output_wav), audio, sr)
    logger.info(
        "Preprocessed audio saved: '%s' (%.1f s, %d Hz)",
        output_wav.name,
        len(audio) / sr,
        sr,
    )

    # Clean up intermediate
    if intermediate_wav.exists():
        intermediate_wav.unlink()

    return output_wav
