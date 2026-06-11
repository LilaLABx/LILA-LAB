#!/usr/bin/env python3
"""Phase 1 — Corpus profile.

Computes descriptive statistics: article counts per year/source/category,
text length distributions, quality metrics, date coverage.

Usage::

    python run_phase1.py [--config config.yaml]
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
logger = logging.getLogger("phase1")

_HERE = Path(__file__).resolve().parent
_PIPELINES = _HERE.parents[1]
sys.path.insert(0, str(_PIPELINES))

from shared.analysis.profiler import run_profile  # noqa: E402
from shared.io import read_zst_csv  # noqa: E402


def run_phase1(config: dict) -> Path:
    corpus_cfg = config["corpus"]
    profile_cfg = config["profile"]
    out_base = Path(config["output"]["base_dir"])
    out_dir = out_base / config["output"]["phases"]["profile"]
    out_dir.mkdir(parents=True, exist_ok=True)
    fn = corpus_cfg["fieldnames"]

    corpus_path = _HERE / corpus_cfg["path"]
    if not corpus_path.exists():
        fallback = _HERE / corpus_cfg["fallback"]
        if fallback.exists():
            corpus_path = fallback
        else:
            raise FileNotFoundError(f"Corpus not found: {corpus_path}")

    logger.info("Phase 1 — Corpus profile")
    logger.info("Corpus: %s", corpus_path)
    logger.info("Loading corpus into DataFrame...")

    df = read_zst_csv(corpus_path)
    logger.info("Loaded %s rows, %s columns", len(df), len(df.columns))

    cfg = {
        "text_column": fn.get("text", "text_clean"),
        "date_column": fn.get("date", "publication_date"),
        "category_column": fn.get("category", "category_harmonised"),
        "source_column": fn.get("source", "dataset_source"),
        "sample_size": profile_cfg.get("sample_n", 200_000),
    }
    result = run_profile(df, output_dir=out_dir, config=cfg)
    logger.info("Profile written to %s", out_dir)
    return result


def main():
    parser = argparse.ArgumentParser(description="Phase 1 — Corpus profile")
    parser.add_argument("--config", default="config.yaml")
    args = parser.parse_args()

    import yaml
    config_path = _HERE / args.config
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    run_phase1(config)


if __name__ == "__main__":
    main()
