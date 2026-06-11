#!/usr/bin/env python3
"""
ASR Model Configuration Registry for the Audio Annotation Lab.

Maps model names to their configuration metadata (backend, size, quality tier, etc.).
Supports both ``openai-whisper`` and ``faster-whisper`` backends.

Usage:
    >>> from pipelines.audio_annotation_lab.asr.models import get_model_config, list_available_models
    >>> cfg = get_model_config("whisper-small")
    >>> cfg["backend"]
    'openai-whisper'
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)

# ── Model Registry ──────────────────────────────────────────────────────

MODEL_REGISTRY: dict[str, dict[str, Any]] = {
    # ── openai-whisper variants ──────────────────────────────────────
    "whisper-tiny": {
        "backend": "openai-whisper",
        "model_name": "tiny",
        "params": 39_000_000,
        "quality": "basic",
        "language_support": "multilingual",
        "use_case": "Quick testing, low-resource environments",
        "recommended_device": "cpu",
    },
    "whisper-base": {
        "backend": "openai-whisper",
        "model_name": "base",
        "params": 74_000_000,
        "quality": "fair",
        "language_support": "multilingual",
        "use_case": "Lightweight transcription",
        "recommended_device": "cpu",
    },
    "whisper-small": {
        "backend": "openai-whisper",
        "model_name": "small",
        "params": 244_000_000,
        "quality": "good",
        "language_support": "multilingual",
        "use_case": "Balanced speed/accuracy",
        "recommended_device": "cpu",
    },
    "whisper-medium": {
        "backend": "openai-whisper",
        "model_name": "medium",
        "params": 769_000_000,
        "quality": "very good",
        "language_support": "multilingual",
        "use_case": "High-quality transcription with GPU",
        "recommended_device": "cuda",
    },
    "whisper-large-v3": {
        "backend": "openai-whisper",
        "model_name": "large-v3",
        "params": 1_550_000_000,
        "quality": "best",
        "language_support": "multilingual",
        "use_case": "Maximum accuracy, requires GPU",
        "recommended_device": "cuda",
    },
    # ── faster-whisper (CTranslate2) variants ───────────────────────
    "faster-whisper-tiny": {
        "backend": "faster-whisper",
        "model_name": "tiny",
        "params": 39_000_000,
        "quality": "basic",
        "language_support": "multilingual",
        "use_case": "Quick testing with CTranslate2 optimization",
        "recommended_device": "cpu",
    },
    "faster-whisper-base": {
        "backend": "faster-whisper",
        "model_name": "base",
        "params": 74_000_000,
        "quality": "fair",
        "language_support": "multilingual",
        "use_case": "Lightweight optimized transcription",
        "recommended_device": "cpu",
    },
    "faster-whisper-small": {
        "backend": "faster-whisper",
        "model_name": "small",
        "params": 244_000_000,
        "quality": "good",
        "language_support": "multilingual",
        "use_case": "Optimized balanced speed/accuracy",
        "recommended_device": "cpu",
    },
    "faster-whisper-medium": {
        "backend": "faster-whisper",
        "model_name": "medium",
        "params": 769_000_000,
        "quality": "very good",
        "language_support": "multilingual",
        "use_case": "Optimized high-quality transcription",
        "recommended_device": "cuda",
    },
    "faster-whisper-large-v3": {
        "backend": "faster-whisper",
        "model_name": "large-v3",
        "params": 1_550_000_000,
        "quality": "best",
        "language_support": "multilingual",
        "use_case": "Fastest maximum-accuracy transcription",
        "recommended_device": "cuda",
    },
}


def get_model_config(name: str) -> dict[str, Any]:
    """Return the configuration dictionary for a named model.

    Args:
        name: Model key from the registry (e.g. ``"whisper-small"``).

    Returns:
        A copy of the model's configuration dict.

    Raises:
        KeyError: If ``name`` is not in the registry.
    """
    if name not in MODEL_REGISTRY:
        available = list_available_models()
        raise KeyError(
            f"Unknown model '{name}'. Available models:\n"
            + "\n".join(f"  - {m}" for m in available)
        )
    return dict(MODEL_REGISTRY[name])


def list_available_models() -> list[str]:
    """Return a sorted list of all registered model names.

    Returns:
        Alphabetically sorted model name strings.
    """
    return sorted(MODEL_REGISTRY.keys())
