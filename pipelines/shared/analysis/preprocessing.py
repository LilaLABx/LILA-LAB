"""Text preprocessing utilities for XENI pipeline corpora.

Provides stop word filtering, tokenization, text cleaning, and a
:class:`PreprocessingPipeline` factory that builds method-specific
preprocessing pipelines for the four BENI index construction methods:

- ``"bbd"`` — minimal: whitespace split, no stop words, no stemming
- ``"classical_ml"`` — TF-IDF ready: stop words, punctuation cleaned, bigrams
- ``"deep_learning"`` — subword tokens (BPE), entity-preserved
- ``"llm"`` — clean text, entity-preserved, full context preserved

Usage::

    from shared.analysis.preprocessing import PreprocessingPipeline

    # Preset pipeline
    pipe = PreprocessingPipeline.preset("classical_ml", language="bengali")
    tokens = pipe("এটি একটি বাংলা বাক্য")

    # Custom pipeline
    from shared.analysis.preprocessing import PreprocessingPipeline
    pipe = PreprocessingPipeline.from_config({
        "tokenizer": "whitespace",
        "stopwords": True,
        "language": "bengali",
    })
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar, Callable

logger = logging.getLogger(__name__)

# Path to shared data files
_HERE = Path(__file__).resolve().parent.parent  # pipelines/shared/
_DATA_DIR = _HERE / "data"


# ═════════════════════════════════════════════════════════════════════
#  Sentinels & helpers
# ═════════════════════════════════════════════════════════════════════

# Unicode range for ASCII punctuation (without hyphen/apostrophe)
_ASCII_PUNCT_RE = re.compile(
    r"""[!\"#$%&()*,./:;<=>?@[\]^_`{|}~।‹›""''«»–—‐·…]"""
)


# ═════════════════════════════════════════════════════════════════════
#  Stop Words  (unchanged from original)
# ═════════════════════════════════════════════════════════════════════


def load_stopwords(language: str = "bengali") -> set[str]:
    """Load stop words for a given language from ``shared/data/``.

    Expects a file named ``<language>_stopwords.txt`` in the shared
    data directory. The file should have one word per line, with
    ``#`` for comments.

    Parameters
    ----------
    language:
        Language identifier (e.g., ``"bengali"``, ``"hindi"``).
        Maps to ``shared/data/<language>_stopwords.txt``.

    Returns
    -------
    set[str]
        Set of stop words (lowercased, stripped).

    Raises
    ------
    FileNotFoundError
        If no stop word file exists for the given language.
    """
    file_path = _DATA_DIR / f"{language}_stopwords.txt"
    if not file_path.exists():
        raise FileNotFoundError(
            f"Stop word file not found: {file_path}\n"
            f"Create one at pipelines/shared/data/{language}_stopwords.txt"
        )

    stopwords: set[str] = set()
    text = file_path.read_text(encoding="utf-8")
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        stopwords.add(line.lower())

    logger.info("Loaded %d stop words from %s", len(stopwords), file_path)
    return stopwords


# ═════════════════════════════════════════════════════════════════════
#  Tokenizers  (unchanged from original)
# ═════════════════════════════════════════════════════════════════════


def simple_tokenizer(text: str) -> list[str]:
    """Split text on whitespace and strip basic punctuation.

    This is the default tokenizer used by the vocabulary profiler.
    Works with Latin, Devanagari, Arabic, and Bangla scripts.

    Unlike a ``\\W``-based strip, this only removes specific ASCII
    punctuation so that Unicode combining marks (e.g. Bengali vowel
    signs ি া ে, Devanagari matras) are preserved.

    For language-specific tokenization, use
    :func:`stopword_filtered_tokenizer` with stop words.

    Parameters
    ----------
    text:
        Raw text string.

    Returns
    -------
    list[str]
        Lowercased tokens.
    """
    if not isinstance(text, str) or not text.strip():
        return []
    text = text.lower()
    text = _ASCII_PUNCT_RE.sub("", text)
    return text.split()


def stopword_filtered_tokenizer(
    stopwords: set[str],
    base_tokenizer: Callable[[str], list[str]] | None = None,
) -> Callable[[str], list[str]]:
    """Create a tokenizer that removes stop words after tokenizing.

    The returned tokenizer function:
    1. Tokenizes using the base tokenizer (default: :func:`simple_tokenizer`)
    2. Filters out any token present in the stop word set

    Parameters
    ----------
    stopwords:
        Set of stop words to filter out.
    base_tokenizer:
        Tokenizer to use before filtering. Defaults to
        :func:`simple_tokenizer`.

    Returns
    -------
    Callable[[str], list[str]]
        A tokenizer function that filters stop words.

    Example
    -------
    >>> stopwords = {"এবং", "ও", "এই"}
    >>> tokenizer = stopword_filtered_tokenizer(stopwords)
    >>> tokenizer("এই ও একটি বাংলা বাক্য")
    ['একটি', 'বাংলা', 'বাক্য']
    """
    if base_tokenizer is None:
        base_tokenizer = simple_tokenizer

    def tokenizer(text: str) -> list[str]:
        tokens = base_tokenizer(text)
        return [t for t in tokens if t not in stopwords]

    return tokenizer


# ═════════════════════════════════════════════════════════════════════
#  Text Cleaning  (unchanged from original)
# ═════════════════════════════════════════════════════════════════════


def clean_text(
    text: str,
    min_token_length: int = 2,
    strip_digits: bool = True,
    strip_urls: bool = True,
) -> str:
    """Clean and normalize text for analysis or LLM annotation.

    Applies the following cleaning steps:
    1. Strip URLs (``http://...``, ``https://...``)
    2. Strip digits (optional, default on)
    3. Remove tokens shorter than ``min_token_length``
    4. Collapse whitespace

    This is a lightweight cleaner — does NOT remove stop words.
    Use :func:`stopword_filtered_tokenizer` for that.

    Parameters
    ----------
    text:
        Raw text string.
    min_token_length:
        Minimum character length for tokens to keep. Set to 1 to
        keep all tokens. Default 2 (filters single characters).
    strip_digits:
        If True, removes digit-only tokens.
    strip_urls:
        If True, removes URL tokens.

    Returns
    -------
    str
        Cleaned text.
    """
    if not isinstance(text, str) or not text.strip():
        return ""

    cleaned = text

    # Strip URLs
    if strip_urls:
        cleaned = re.sub(r"https?://\S+", "", cleaned)

    # Strip digits
    if strip_digits:
        cleaned = re.sub(r"\b\d+\b", "", cleaned)

    # Tokenize, filter by length, and rejoin
    tokens = cleaned.split()
    tokens = [t for t in tokens if len(t) >= min_token_length]

    return " ".join(tokens).strip()


# ═════════════════════════════════════════════════════════════════════
#  Convenience: create a tokenizer for a known XENI language
# ═════════════════════════════════════════════════════════════════════


_LANGUAGE_MAP: dict[str, str] = {
    "BENI": "bengali",
    "AENI": "assamese",
    "NENI": "nepali",
    "SENI": "sylheti",
    "CENI": "chittagonian",
    "HENI": "hausa",
    "KIENI": "swahili",
    "VIENI": "vietnamese",
    "TIENI": "tagalog",
    "IDENI": "indonesian",
}


def tokenizer_for_pipeline(
    pipeline_code: str,
    stopwords: set[str] | None = None,
) -> Callable[[str], list[str]]:
    """Get an appropriate tokenizer for a XENI pipeline language.

    If stop words are provided (or can be loaded), returns a
    stop-word-filtered tokenizer. Otherwise falls back to the
    simple whitespace tokenizer.

    Parameters
    ----------
    pipeline_code:
        Three- or four-letter pipeline code like ``"BENI"``, ``"HENI"``.
    stopwords:
        Optional pre-loaded stop word set. If None, attempts to load
        from ``shared/data/<language>_stopwords.txt``.

    Returns
    -------
    Callable[[str], list[str]]
        Tokenizer function appropriate for the language.
    """
    if stopwords is None:
        lang = _LANGUAGE_MAP.get(pipeline_code.upper())
        if lang:
            try:
                stopwords = load_stopwords(lang)
            except FileNotFoundError:
                logger.warning(
                    "No stop words for %s (%s), using simple tokenizer",
                    pipeline_code, lang,
                )
                return simple_tokenizer
        else:
            logger.warning(
                "Unknown pipeline code %s, using simple tokenizer",
                pipeline_code,
            )
            return simple_tokenizer

    return stopword_filtered_tokenizer(stopwords)


# ═════════════════════════════════════════════════════════════════════
#  PreprocessingPipeline — method-aware pipeline factory
# ═════════════════════════════════════════════════════════════════════


@dataclass
class PreprocessingPipeline:
    """Configurable preprocessing pipeline for economic index construction.

    Each preset configures tokenization, stop word filtering, and text
    cleaning appropriate for a specific index construction method.

    Parameters
    ----------
    config:
        Pipeline configuration dict. See ``PRESETS`` for the 4 built-in
        configurations.
    stopwords:
        Pre-loaded stop word set (optional).
    """

    config: dict = field(default_factory=dict)
    stopwords: set[str] | None = None

    # ── Built-in presets ──────────────────────────────────────────────

    PRESETS: ClassVar[dict[str, dict]] = {
        "bbd": {
            "description": "BBD-style keyword counting — minimal preprocessing",
            "tokenizer": "raw",            # whitespace split only, no lowercasing
            "stopwords": False,
            "stemming": False,
            "ngrams": False,
            "strip_punct": False,
            "strip_digits": False,
            "min_token_length": 1,
        },
        "classical_ml": {
            "description": "TF-IDF + shallow models — stop words, punctuation clean, bigrams",
            "tokenizer": "whitespace",
            "stopwords": True,
            "stemming": False,
            "ngrams": "bigram",            # extract unigrams + bigrams
            "strip_punct": True,
            "strip_digits": True,
            "min_token_length": 2,
        },
        "deep_learning": {
            "description": "Subword embeddings + LSTM/transformer — BPE tokens, entity-preserved",
            "tokenizer": "bpe",             # subword tokenisation
            "stopwords": False,             # attention handles function words
            "stemming": False,
            "ngrams": False,
            "strip_punct": False,
            "strip_digits": False,
            "min_token_length": 1,
            "preserve_entities": True,       # keep multi-word names
            "max_seq_length": 256,
        },
        "llm": {
            "description": "LLM annotation — clean text, full context, entity-preserved",
            "tokenizer": "whitespace",      # return *text*, not tokens
            "stopwords": False,             # LLM handles function words
            "stemming": False,
            "ngrams": False,
            "strip_punct": False,
            "strip_digits": False,
            "min_token_length": 1,
            "preserve_entities": True,
            "return_text": True,            # pipeline returns str, not list[str]
        },
    }

    # ── Factory methods ───────────────────────────────────────────────

    @classmethod
    def preset(cls, name: str, language: str = "bengali") -> "PreprocessingPipeline":
        """Create a pipeline from a built-in preset.

        Parameters
        ----------
        name:
            Preset name: ``"bbd"``, ``"classical_ml"``, ``"deep_learning"``,
            or ``"llm"``.
        language:
            Language identifier for stop words (e.g. ``"bengali"``).

        Returns
        -------
        PreprocessingPipeline
        """
        config = cls.PRESETS.get(name)
        if config is None:
            raise ValueError(
                f"Unknown preset: {name}. "
                f"Choose from {set(cls.PRESETS)}"
            )

        # Load stop words if the preset uses them
        stopwords = None
        if config.get("stopwords", False):
            try:
                stopwords = load_stopwords(language)
            except FileNotFoundError:
                logger.warning(
                    "No stop words for %s, proceeding without", language
                )

        return cls(config=config, stopwords=stopwords)

    @classmethod
    def from_config(
        cls,
        config: dict,
        language: str | None = None,
    ) -> "PreprocessingPipeline":
        """Create a pipeline from an arbitrary config dict.

        Accepts the same keys as the preset dicts.  If ``config``
        contains a ``"preset"`` key, delegates to :meth:`preset`.
        """
        if "preset" in config:
            return cls.preset(config["preset"], language or "bengali")

        stopwords = None
        if config.get("stopwords", False):
            lang = language or config.get("language", "bengali")
            try:
                stopwords = load_stopwords(lang)
            except FileNotFoundError:
                logger.warning(
                    "No stop words for %s, proceeding without", lang
                )

        return cls(config=config, stopwords=stopwords)

    # ── Processing ────────────────────────────────────────────────────

    def process(self, text: str) -> list[str] | str:
        """Run the full preprocessing pipeline on a single text.

        Returns tokenized text (``list[str]``), or plain text
        (``str``) if the pipeline is configured for LLM input.
        """
        if not isinstance(text, str) or not text.strip():
            return [] if not self.config.get("return_text") else ""

        t = text

        # 1. Lowercase (unless BBD raw mode)
        if self.config.get("tokenizer") != "raw":
            t = t.lower()

        # 2. Strip punctuation (classical_ml only)
        if self.config.get("strip_punct", False):
            t = _ASCII_PUNCT_RE.sub("", t)

        # 3. Clean URLs / digits
        if self.config.get("strip_digits", False):
            t = re.sub(r"\b\d+\b", "", t)
        t = re.sub(r"https?://\S+", "", t)

        # 4. Tokenize
        tok_type = self.config.get("tokenizer", "whitespace")
        if tok_type == "raw":
            tokens = t.split()
        elif tok_type == "whitespace":
            tokens = t.split()
        elif tok_type == "bpe":
            # BPE placeholder — requires a separate subword tokeniser.
            # Falls back to whitespace split for now.
            tokens = t.split()
        else:
            tokens = t.split()

        # 5. Filter by min length
        min_len = self.config.get("min_token_length", 1)
        if min_len > 1:
            tokens = [tk for tk in tokens if len(tk) >= min_len]

        # 6. Filter stop words
        if self.config.get("stopwords", False) and self.stopwords:
            tokens = [tk for tk in tokens if tk not in self.stopwords]

        # 7. Return
        if self.config.get("return_text", False):
            return " ".join(tokens)

        return tokens

    def __call__(self, text: str) -> list[str] | str:
        """Convenience alias for :meth:`process`."""
        return self.process(text)

    # ── Batch processing ──────────────────────────────────────────────

    def process_batch(
        self,
        texts: list[str],
        show_progress: bool = False,
    ) -> list[list[str] | str]:
        """Process a batch of texts through the pipeline.

        Parameters
        ----------
        texts:
            List of raw text strings.
        show_progress:
            If True, log progress at 10% intervals.

        Returns
        -------
        list[list[str] | str]
            Processed outputs (tokens or text, matching the preset).
        """
        results: list[list[str] | str] = []
        total = len(texts)
        for i, t in enumerate(texts):
            results.append(self.process(t))
            if show_progress and total > 1000:
                if i % max(1, total // 10) == 0:
                    logger.info("  preprocessing %d / %d", i, total)
        return results

    # ── Introspection ─────────────────────────────────────────────────

    @property
    def name(self) -> str:
        """Return the preset name if this pipeline was built from one."""
        for name, cfg in self.PRESETS.items():
            if self.config.get("tokenizer") == cfg.get("tokenizer") and \
               self.config.get("stopwords") == cfg.get("stopwords"):
                return name
        return "custom"

    def describe(self) -> str:
        """Return a human-readable description of this pipeline."""
        name = self.name
        desc = self.PRESETS[name]["description"] if name != "custom" else "Custom configuration"
        parts = [
            f"Pipeline: {name}",
            f"  {desc}",
            f"  tokenizer={self.config.get('tokenizer')}",
            f"  stopwords={self.config.get('stopwords')}",
            f"  strip_punct={self.config.get('strip_punct')}",
            f"  ngrams={self.config.get('ngrams')}",
            f"  return_text={self.config.get('return_text')}",
        ]
        if self.stopwords:
            parts.append(f"  stopword_count={len(self.stopwords)}")
        return "\n".join(parts)
