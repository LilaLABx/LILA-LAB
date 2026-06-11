#!/usr/bin/env python3
"""Phase 2 — Vocabulary analysis.

Computes TTR, hapax legomena, top words per category, log-odds ratio
for distinctive keywords, and n-gram frequencies.

Supports optional stop word filtering via ``vocabulary.stopwords``
in the config file.  When enabled, function words are excluded from
all vocabulary statistics.

Usage::

    python run_phase2.py [--config config.yaml]
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
logger = logging.getLogger("phase2")

_HERE = Path(__file__).resolve().parent
_PIPELINES = _HERE.parents[1]
sys.path.insert(0, str(_PIPELINES))

from shared.analysis.preprocessing import PreprocessingPipeline  # noqa: E402
from shared.analysis.vocabulary import run_vocabulary  # noqa: E402
from shared.io import read_zst_csv  # noqa: E402


def run_phase2(config: dict) -> Path:
    corpus_cfg = config["corpus"]
    vocab_cfg = config["vocabulary"]
    out_base = Path(config["output"]["base_dir"])
    out_dir = out_base / config["output"]["phases"]["vocabulary"]
    out_dir.mkdir(parents=True, exist_ok=True)
    fn = corpus_cfg["fieldnames"]
    text_col = fn.get("text", "text_clean")

    corpus_path = _HERE / corpus_cfg["path"]
    if not corpus_path.exists():
        fallback = _HERE / corpus_cfg["fallback"]
        if fallback.exists():
            corpus_path = fallback
        else:
            raise FileNotFoundError(f"Corpus not found: {corpus_path}")

    logger.info("Phase 2 — Vocabulary analysis")
    logger.info("Corpus: %s", corpus_path)
    logger.info("Loading %s rows...", vocab_cfg.get("max_rows", "all"))

    df = read_zst_csv(corpus_path)
    max_rows = vocab_cfg.get("max_rows", 500_000)
    if max_rows and len(df) > max_rows:
        df = df.sample(n=max_rows, random_state=42)
    logger.info("Using %s rows", len(df))

    # Build pipeline from config preset — provides tokenizer + stop words
    preproc_cfg = config.get("preprocessing", {})
    preset_name = preproc_cfg.get("pipeline_preset", "classical_ml")
    pipe = PreprocessingPipeline.preset(preset_name, language="bengali")
    logger.info("Pipeline preset: %s", pipe.describe())

    # Pass stop words + tokenizer to run_vocabulary via analysis_cfg
    analysis_cfg = dict(vocab_cfg)
    if pipe.stopwords:
        analysis_cfg["stopwords"] = pipe.stopwords

    result = run_vocabulary(
        df, output_dir=out_dir, text_column=text_col, config=analysis_cfg,
    )
    logger.info("Vocabulary analysis written to %s", out_dir)
    return result


def main():
    parser = argparse.ArgumentParser(description="Phase 2 — Vocabulary analysis")
    parser.add_argument("--config", default="config.yaml")
    args = parser.parse_args()

    import yaml

    config_path = _HERE / args.config
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    run_phase2(config)


if __name__ == "__main__":
    main()
