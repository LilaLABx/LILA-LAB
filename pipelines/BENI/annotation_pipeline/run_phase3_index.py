#!/usr/bin/env python3
"""Phase 3 — Index Construction.

Builds the BENI Economic Narrative Index from article-level predictions
(produced in Phase 2). Aggregates monthly proportions, applies LLM
calibration factors from Phase 1, and merges macroeconomic time series.

The core index is the **monthly economic narrative share**: the fraction of
articles classified as economically relevant in each month.

Usage::

    python run_phase3_index.py [--config config.yaml]

Expected outputs (under ``outputs/03_index/``):

    - ``narrative_index.csv``          — Monthly index (raw + calibrated)
    - ``narrative_index_enhanced.csv`` — Index merged with macro series
    - ``index_summary.json``           — Summary statistics
    - ``calibration_factors.json``     — Calibration factors used

Dependencies:
    - Phase 2 must have produced ``consensus_labels.parquet`` or similar
    - Phase 1 must have produced ``agreement_report.json`` (for calibration)
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
logger = logging.getLogger("phase3_index")

_HERE = Path(__file__).resolve().parent
_PIPELINES = _HERE.parents[1]
sys.path.insert(0, str(_PIPELINES))

# from shared.io import write_json, read_json                            # noqa: E402
# from shared.analysis.index_builder import build_monthly_index,          # noqa: E402
#     apply_calibration, merge_macro_data                                # noqa: E402


def run_phase3(config: dict) -> Path:
    """Build the monthly narrative index.

    Steps:
        1. Load article-level predictions from Phase 2
        2. Load calibration factors from Phase 1 (pilot agreement report)
        3. Build the raw monthly index via ``build_monthly_index``
        4. Apply LLM calibration via ``apply_calibration``
        5. Merge macroeconomic series via ``merge_macro_data``
        6. Write index CSV and summary JSON

    Parameters
    ----------
    config:
        Full pipeline configuration dict.

    Returns
    -------
    Path
        Path to the output directory.
    """
    index_cfg = config["index"]
    out_base = Path(config["output"]["base_dir"])
    out_dir = out_base / config["output"]["phases"]["index"]
    out_dir.mkdir(parents=True, exist_ok=True)

    # Paths from other phases
    pilot_dir = out_base / config["output"]["phases"]["pilot"]
    annotate_dir = out_base / config["output"]["phases"]["annotate"]

    logger.info("Phase 3 — Index construction")
    logger.info("Output: %s", out_dir)

    # ── 1. Load predictions from Phase 2 ────────────────────────
    predictions_path = annotate_dir / "consensus_labels.parquet"
    if predictions_path.exists():
        logger.info("Predictions found: %s", predictions_path)
    else:
        logger.warning(
            "Predictions not found at %s\n"
            "  Phase 2 must complete before Phase 3.\n"
            "  Using placeholder — replace with actual data loading.",
            predictions_path,
        )
    # TODO: df = pd.read_parquet(predictions_path)

    # ── 2. Load calibration factors from Phase 1 ────────────────
    calibration_factors = None
    agreement_path = pilot_dir / "agreement_report.json"
    if agreement_path.exists():
        logger.info("Calibration data found: %s", agreement_path)
        # TODO: pilot_results = read_json(agreement_path)
        # TODO: extract calibration factors from pilot results
    else:
        logger.info(
            "No pilot agreement found — running without calibration. "
            "Phase 1 must complete for calibration."
        )

    # ── 3. Build the raw monthly index ──────────────────────────
    # TODO: index = build_monthly_index(
    #     df=df,
    #     date_col="publication_date",
    #     prob_col="economic_prob",
    #     pred_col="economic_pred",
    #     output_dir=out_dir,
    #     min_articles_per_month=index_cfg.get("min_articles_per_month", 10),
    # )
    logger.info("  (build_monthly_index not yet called — placeholder)")

    # ── 4. Apply calibration ────────────────────────────────────
    # if calibration_factors:
    #     calibrated = apply_calibration(
    #         index["index"],
    #         calibration_factors=calibration_factors,
    #         method=index_cfg.get("calibration", "base_rate"),
    #     )
    # else:
    #     calibrated = index["index"]

    # ── 5. Merge macro data ─────────────────────────────────────
    # macro_series = index_cfg.get("macro_series", [])
    # macro_dir = _HERE / index_cfg.get("macro_dir", "../data/raw/macro")
    # enhanced = merge_macro_data(calibrated, macro_config=macro_series, macro_dir=macro_dir)

    # ── 6. Write outputs ────────────────────────────────────────
    # enhanced.to_csv(out_dir / "narrative_index_enhanced.csv", index=False)
    # write_json(out_dir / "index_summary.json", index.get("summary", {}))

    summary = {
        "phase": "index",
        "status": "scaffold — not yet implemented",
        "calibration_method": index_cfg.get("calibration"),
        "normalization": index_cfg.get("normalization"),
        "n_macro_series": len(index_cfg.get("macro_series", [])),
        "next_steps": [
            "1. Implement pd.read_parquet for predictions loading",
            "2. Implement build_monthly_index call",
            "3. Implement apply_calibration call",
            "4. Implement merge_macro_data call",
            "5. Write index CSV and summary JSON",
        ],
    }
    # write_json(out_dir / "index_summary.json", summary)

    logger.info("Phase 3 complete — outputs in %s", out_dir)
    return out_dir


def main():
    parser = argparse.ArgumentParser(description="Phase 3 — Index construction")
    parser.add_argument("--config", default="config.yaml")
    args = parser.parse_args()

    import yaml

    config_path = _HERE / args.config
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    run_phase3(config)


if __name__ == "__main__":
    main()
