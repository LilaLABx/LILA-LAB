#!/usr/bin/env python3
"""Phase 4 — Macroeconomic Validation.

Validates the BENI Economic Narrative Index against real-world macroeconomic
indicators: CPI (inflation), FX rate, and foreign exchange reserves.

Computes:
    - **Level correlations**: contemporaneous Pearson/Spearman with CPI, FX
    - **First-differenced correlations**: month-over-month change correlation
    - **Lead/lag analysis**: test if the narrative index leads macro by 1–6 months
    - **Annual correlation**: with reserves (only available yearly)

This phase produces a validation report and diagnostic plots.

Usage::

    python run_phase4_validate.py [--config config.yaml]

Expected outputs (under ``outputs/04_validation/``):

    - ``correlation_report.json``       — Full correlation results
    - ``validation_summary.json``       — Key findings
    - ``figures/``                      — Correlation scatter plots, time series overlays

Dependencies:
    - Phase 3 must have produced ``narrative_index_enhanced.csv``
    - Macro data must be downloaded (via ``download_macro.py``)
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
logger = logging.getLogger("phase4_validate")

_HERE = Path(__file__).resolve().parent
_PIPELINES = _HERE.parents[1]
sys.path.insert(0, str(_PIPELINES))

# from shared.io import write_json                                    # noqa: E402
# from shared.analysis.validator import correlate_with_macro,         # noqa: E402
#     lead_lag_analysis, generate_validation_report                   # noqa: E402


def run_phase4(config: dict) -> Path:
    """Run macroeconomic validation of the narrative index.

    Steps:
        1. Load the enhanced narrative index (with macro data) from Phase 3
        2. Compute level correlations (Pearson, Spearman) with CPI, FX
        3. Compute first-differenced correlations
        4. Run lead/lag analysis (narrative leads macro by 1, 3, 6 months)
        5. Compute annual correlation with reserves
        6. Write correlation report and generate diagnostic plots

    Parameters
    ----------
    config:
        Full pipeline configuration dict.

    Returns
    -------
    Path
        Path to the output directory.
    """
    val_cfg = config["validation"]
    out_base = Path(config["output"]["base_dir"])
    out_dir = out_base / config["output"]["phases"]["validate"]
    out_dir.mkdir(parents=True, exist_ok=True)

    index_dir = out_base / config["output"]["phases"]["index"]

    logger.info("Phase 4 — Macroeconomic validation")
    logger.info("Output: %s", out_dir)

    # ── 1. Load index with macro data ───────────────────────────
    index_path = index_dir / "narrative_index_enhanced.csv"
    if index_path.exists():
        logger.info("Index found: %s", index_path)
    else:
        logger.warning(
            "Enhanced index not found at %s\n"
            "  Phase 3 must complete before Phase 4.\n"
            "  Using placeholder — replace with actual data loading.",
            index_path,
        )
    # TODO: df = pd.read_csv(index_path, parse_dates=["year_month"])

    # ── 2. Compute correlations ────────────────────────────────
    # TODO:
    #   results = correlate_with_macro(
    #       df=df,
    #       index_col="economic_share",  # or "calibrated_share"
    #       macro_cols={
    #           "fx_bis": "FX (BIS)",
    #           "cpi": "CPI (IMF)",
    #           "reserves_usd": "Reserves (WB)",
    #       },
    #       methods=val_cfg.get("methods", ["pearson", "spearman"]),
    #   )

    # ── 3. Lead/lag analysis ───────────────────────────────────
    # TODO:
    #   lead_lag = {}
    #   for lag in val_cfg.get("lead_lags", [0, 1, 3, 6]):
    #       lead_lag[lag] = lead_lag_analysis(df, macro_col="cpi", lag=lag)

    # ── 4. Write report ────────────────────────────────────────
    # report = generate_validation_report(results, lead_lag, output_dir=out_dir)
    # write_json(out_dir / "correlation_report.json", results)
    logger.info("  (correlation computation not yet implemented — placeholder)")

    summary = {
        "phase": "validate",
        "status": "scaffold — not yet implemented",
        "methods": val_cfg.get("methods"),
        "lead_lags": val_cfg.get("lead_lags"),
        "alpha": val_cfg.get("alpha"),
        "next_steps": [
            "1. Implement pd.read_csv for index loading",
            "2. Implement correlate_with_macro call",
            "3. Implement lead_lag_analysis call",
            "4. Implement generate_validation_report call",
            "5. Generate diagnostic plots",
        ],
    }
    # write_json(out_dir / "validation_summary.json", summary)

    logger.info("Phase 4 complete — outputs in %s", out_dir)
    return out_dir


def main():
    parser = argparse.ArgumentParser(description="Phase 4 — Macroeconomic validation")
    parser.add_argument("--config", default="config.yaml")
    args = parser.parse_args()

    import yaml

    config_path = _HERE / args.config
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    run_phase4(config)


if __name__ == "__main__":
    main()
