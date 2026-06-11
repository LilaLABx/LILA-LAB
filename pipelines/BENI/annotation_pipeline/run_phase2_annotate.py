#!/usr/bin/env python3
"""Phase 2 — Full Corpus Annotation.

Annotates the full BENI corpus using the validated schema and prompt from
Phase 1. Processes articles in batches with checkpointing for resilience.

This phase produces per-article predictions from the LLM ensemble and a
consensus label set that feeds into Phase 3 (index construction).

Usage::

    python run_phase2_annotate.py [--config config.yaml]

Expected outputs (under ``outputs/02_annotations/``):

    - ``full_predictions.parquet``  — Per-article, per-LLM predictions
    - ``consensus_labels.parquet``  — Consensus labels (one per article)
    - ``checkpoint.parquet``        — Checkpoint for resume on failure
    - ``annotation_summary.json``   — Coverage, cost, throughput stats
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
logger = logging.getLogger("phase2_annotate")

_HERE = Path(__file__).resolve().parent
_PIPELINES = _HERE.parents[1]
sys.path.insert(0, str(_PIPELINES))

# from shared.io import read_zst_csv, write_json                  # noqa: E402
# from shared.analysis.annotator import run_batch_annotation      # noqa: E402


def run_phase2(config: dict) -> Path:
    """Run full-corpus batch annotation.

    Steps:
        1. Load the full corpus
        2. Load the validated schema
        3. Run batched LLM annotation with checkpointing
        4. Compute consensus labels across LLMs
        5. Write predictions, consensus, and summary

    Parameters
    ----------
    config:
        Full pipeline configuration dict.

    Returns
    -------
    Path
        Path to the output directory.
    """
    corpus_cfg = config["corpus"]
    annotate_cfg = config["annotate"]
    schema_cfg = config["schema"]
    llm_cfg = config["llm"]
    out_base = Path(config["output"]["base_dir"])
    out_dir = out_base / config["output"]["phases"]["annotate"]
    out_dir.mkdir(parents=True, exist_ok=True)
    fn = corpus_cfg["fieldnames"]

    # ── 1. Resolve corpus path ──────────────────────────────────
    corpus_path = _HERE / corpus_cfg["path"]
    if not corpus_path.exists():
        fallback = _HERE / corpus_cfg["fallback"]
        if fallback.exists():
            corpus_path = fallback
        else:
            raise FileNotFoundError(f"Corpus not found: {corpus_path}")

    logger.info("Phase 2 — Full corpus annotation")
    logger.info("Corpus: %s", corpus_path)

    # ── 2. Load corpus ──────────────────────────────────────────
    logger.info("Loading corpus...")
    logger.info("  (read_zst_csv not yet called — placeholder)")
    # from shared.io import read_zst_csv
    # df = read_zst_csv(corpus_path)
    # logger.info("Loaded %d rows", len(df))

    # ── 3. Resolve schema path ──────────────────────────────────
    schema_path = _HERE / schema_cfg["path"]
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema not found: {schema_path}")

    # ── 4. Resolve checkpoint path ──────────────────────────────
    checkpoint_path = None
    if annotate_cfg.get("checkpoint_path"):
        checkpoint_path = _HERE / annotate_cfg["checkpoint_path"]
        if checkpoint_path.exists():
            logger.info("Found checkpoint — will resume: %s", checkpoint_path)

    # ── 5. Run batch annotation ─────────────────────────────────
    # TODO: Uncomment when annotator.run_batch_annotation is implemented:
    #   result = run_batch_annotation(
    #       df=df,
    #       schema_path=schema_path,
    #       output_dir=out_dir,
    #       llm_config=llm_cfg,
    #       checkpoint_path=checkpoint_path,
    #       checkpoint_every=annotate_cfg.get("checkpoint_every", 500),
    #       batch_size=annotate_cfg.get("batch_size", 100),
    #       max_articles=annotate_cfg.get("max_articles"),
    #       n_workers=annotate_cfg.get("n_workers", 1),
    #       consensus=annotate_cfg.get("consensus", "majority_vote"),
    #   )
    #   write_json(out_dir / "annotation_summary.json", {
    #       "n_annotated": result["n_annotated"],
    #       "predictions": result["predictions_path"],
    #       "consensus": result["consensus_path"],
    #   })
    logger.info("  (run_batch_annotation not yet called — placeholder)")

    summary = {
        "phase": "annotate",
        "status": "scaffold — not yet implemented",
        "corpus": str(corpus_path),
        "schema": str(schema_path),
        "batch_size": annotate_cfg.get("batch_size"),
        "max_articles": annotate_cfg.get("max_articles"),
        "next_steps": [
            "1. Implement read_zst_csv import",
            "2. Implement run_batch_annotation call",
            "3. Implement consensus computation",
        ],
    }
    # write_json(out_dir / "annotation_summary.json", summary)

    logger.info("Phase 2 complete — outputs in %s", out_dir)
    return out_dir


def main():
    parser = argparse.ArgumentParser(description="Phase 2 — Full corpus annotation")
    parser.add_argument("--config", default="config.yaml")
    args = parser.parse_args()

    import yaml

    config_path = _HERE / args.config
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    run_phase2(config)


if __name__ == "__main__":
    main()
