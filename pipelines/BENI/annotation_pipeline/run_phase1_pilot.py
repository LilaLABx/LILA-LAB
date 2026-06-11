#!/usr/bin/env python3
"""Phase 1 — Pilot Annotation.

Runs a small-scale LLM annotation on a stratified sample of the corpus,
measures inter-LLM agreement, and reports per-field reliability.

This phase validates the annotation schema before scaling up. If agreement
is below threshold, the schema or prompt should be revised before Phase 2.

Usage::

    python run_phase1_pilot.py [--config config.yaml]

Expected outputs (under ``outputs/01_pilot/``):

    - ``annotated_sample.json``     — Raw annotations per article per LLM
    - ``agreement_report.json``     — Cohen's κ, Fleiss' κ per field
    - ``reliability_report.json``   — Per-field reliability breakdown
    - ``pilot_summary.json``        — High-level summary
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
logger = logging.getLogger("phase1_pilot")

_HERE = Path(__file__).resolve().parent
_PIPELINES = _HERE.parents[1]
sys.path.insert(0, str(_PIPELINES))

# ── Shared imports (lazy — requires sys.path) ─────────────────────
# from shared.io import read_zst_csv, write_json        # noqa: E402
# from shared.analysis.annotator import run_pilot_annotation, compute_agreement  # noqa: E402


def run_phase1(config: dict) -> Path:
    """Run the pilot annotation phase.

    Steps:
        1. Load corpus (from config.corpus.path)
        2. Sample N articles (config.pilot.sample_size)
        3. Run multi-LLM annotation via ``shared.analysis.annotator.run_pilot_annotation``
        4. Compute inter-annotator agreement
        5. Report per-field reliability
        6. Write results to output directory

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
    pilot_cfg = config["pilot"]
    schema_cfg = config["schema"]
    llm_cfg = config["llm"]
    out_base = Path(config["output"]["base_dir"])
    out_dir = out_base / config["output"]["phases"]["pilot"]
    out_dir.mkdir(parents=True, exist_ok=True)
    fn = corpus_cfg["fieldnames"]

    # ── 1. Resolve corpus path ──────────────────────────────────
    corpus_path = _HERE / corpus_cfg["path"]
    if not corpus_path.exists():
        fallback = _HERE / corpus_cfg["fallback"]
        if fallback.exists():
            corpus_path = fallback
        else:
            raise FileNotFoundError(
                f"Corpus not found: {corpus_path}\n"
                f"  Fallback also missing: {fallback}\n"
                "  Download the BENI corpus and place it at the configured path."
            )

    logger.info("Phase 1 — Pilot annotation")
    logger.info("Corpus: %s", corpus_path)

    # ── 2. Load corpus ──────────────────────────────────────────
    # TODO: Replace with actual DataFrame loading:
    #   from shared.io import read_zst_csv
    #   df = read_zst_csv(corpus_path)
    logger.info("Loading corpus...")
    logger.info("  (read_zst_csv not yet called — placeholder)")
    # df = read_zst_csv(corpus_path)
    # text_col = fn.get("text", "text_clean")
    # logger.info("Loaded %d rows", len(df))

    # ── 3. Resolve schema path ──────────────────────────────────
    schema_path = _HERE / schema_cfg["path"]
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema not found: {schema_path}")
    logger.info("Schema: %s", schema_path)

    # ── 4. Run pilot annotation ─────────────────────────────────
    # TODO: Uncomment when annotator is implemented:
    #   result = run_pilot_annotation(
    #       df=df,
    #       schema_path=schema_path,
    #       output_dir=out_dir,
    #       sample_size=pilot_cfg["sample_size"],
    #       providers=llm_cfg.get("providers"),
    #       seed=pilot_cfg.get("seed", 42),
    #       strategy=pilot_cfg.get("strategy", "stratified"),
    #       stratify_by=fn.get("category", pilot_cfg.get("stratify_by")),
    #   )
    #   write_json(out_dir / "pilot_summary.json", result["summary"])
    #   write_json(out_dir / "agreement_report.json", result["agreement"])
    #   write_json(out_dir / "reliability_report.json", result["field_reliability"])
    logger.info("  (run_pilot_annotation not yet called — placeholder)")

    # Placeholder summary
    summary = {
        "phase": "pilot",
        "status": "scaffold — not yet implemented",
        "sample_size": pilot_cfg.get("sample_size"),
        "strategy": pilot_cfg.get("strategy"),
        "schema": str(schema_path),
        "corpus": str(corpus_path),
        "next_steps": [
            "1. Implement read_zst_csv import",
            "2. Implement run_pilot_annotation call",
            "3. Implement compute_agreement call",
        ],
    }
    # write_json(out_dir / "pilot_summary.json", summary)  # TODO: uncomment

    logger.info("Phase 1 complete — outputs in %s", out_dir)
    return out_dir


def main():
    parser = argparse.ArgumentParser(description="Phase 1 — Pilot annotation")
    parser.add_argument("--config", default="config.yaml")
    args = parser.parse_args()

    import yaml

    config_path = _HERE / args.config
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    run_phase1(config)


if __name__ == "__main__":
    main()
