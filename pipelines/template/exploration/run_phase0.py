#!/usr/bin/env python3
"""Phase 0 — Sample selection (template stub)."""

import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
logger = logging.getLogger("phase0")

_HERE = Path(__file__).resolve().parent

# ── Customise for your pipeline ───────────────────────────────────


def main():
    logger.info("Phase 0 — Sample selection (stub)")
    logger.info("Implement sample extraction logic for your corpus.")
    logger.info("See pipelines/BENI/exploration/run_phase0.py for reference.")


if __name__ == "__main__":
    main()
