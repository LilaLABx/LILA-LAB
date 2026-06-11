#!/usr/bin/env python3
"""Phase 4 — Schema validation.

Validates annotation schema coverage against the corpus sample. Checks
whether keyword-based field matching meets the coverage threshold.

Usage::

    python run_phase4.py [--config config.yaml]
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
logger = logging.getLogger("phase4")

_HERE = Path(__file__).resolve().parent
_PIPELINES = _HERE.parents[1]
sys.path.insert(0, str(_PIPELINES))

from shared.analysis.schema_validator import run_schema_validation  # noqa: E402
from shared.io import read_zst_csv  # noqa: E402


def run_phase4(config: dict) -> Path:
    corpus_cfg = config["corpus"]
    schema_cfg = config["schema"]
    out_base = Path(config["output"]["base_dir"])
    out_dir = out_base / config["output"]["phases"]["schema"]
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

    schema_path = _HERE / schema_cfg["schema_path"]
    if not schema_path.exists():
        logger.warning("Schema not found at %s — skipping schema validation", schema_path)
        return out_dir / "schema_coverage.json"

    logger.info("Phase 4 — Schema validation")
    logger.info("Schema: %s", schema_path)
    logger.info("Loading corpus sample...")

    df = read_zst_csv(corpus_path)
    sample_size = schema_cfg.get("sample_size", 10_000)
    if len(df) > sample_size:
        df = df.sample(n=sample_size, random_state=42)
    logger.info("Using %s rows", len(df))

    min_cov = schema_cfg.get("coverage_threshold_pct", 50.0) / 100.0
    result = run_schema_validation(
        df,
        output_dir=out_dir,
        schema_path=schema_path,
        text_column=text_col,
        sample_size=sample_size,
        min_coverage=min_cov,
    )
    logger.info("Schema validation written to %s", out_dir)
    return result


def main():
    parser = argparse.ArgumentParser(description="Phase 4 — Schema validation")
    parser.add_argument("--config", default="config.yaml")
    args = parser.parse_args()

    import yaml
    config_path = _HERE / args.config
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    run_phase4(config)


if __name__ == "__main__":
    main()
