#!/usr/bin/env python3
"""Phase 3 — Temporal diagnostics.

Analyses temporal coverage, detects gaps, and runs the KS source-boundary
test between Potrika and BNAD periods.

Usage::

    python run_phase3.py [--config config.yaml]
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
logger = logging.getLogger("phase3")

_HERE = Path(__file__).resolve().parent
_PIPELINES = _HERE.parents[1]
sys.path.insert(0, str(_PIPELINES))

from shared.analysis.temporal import run_temporal  # noqa: E402
from shared.io import read_zst_csv  # noqa: E402


def run_phase3(config: dict) -> Path:
    corpus_cfg = config["corpus"]
    temporal_cfg = config["temporal"]
    out_base = Path(config["output"]["base_dir"])
    out_dir = out_base / config["output"]["phases"]["temporal"]
    out_dir.mkdir(parents=True, exist_ok=True)
    fn = corpus_cfg["fieldnames"]

    corpus_path = _HERE / corpus_cfg["path"]
    if not corpus_path.exists():
        fallback = _HERE / corpus_cfg["fallback"]
        if fallback.exists():
            corpus_path = fallback
        else:
            raise FileNotFoundError(f"Corpus not found: {corpus_path}")

    logger.info("Phase 3 — Temporal diagnostics")
    logger.info("Corpus: %s", corpus_path)
    logger.info("Loading corpus...")

    df = read_zst_csv(corpus_path)
    logger.info("Loaded %s rows", len(df))

    result = run_temporal(
        df,
        output_dir=out_dir,
        date_col=fn.get("date", "publication_date"),
        source_col=fn.get("source", "dataset_source"),
        metric_col=None,
    )
    logger.info("Temporal diagnostics written to %s", out_dir)
    return result


def main():
    parser = argparse.ArgumentParser(description="Phase 3 — Temporal diagnostics")
    parser.add_argument("--config", default="config.yaml")
    args = parser.parse_args()

    import yaml
    config_path = _HERE / args.config
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    run_phase3(config)


if __name__ == "__main__":
    main()
