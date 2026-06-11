#!/usr/bin/env python3
"""Phase 1 — Corpus profile (template stub)."""

import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
logger = logging.getLogger("phase1")

_HERE = Path(__file__).resolve().parent


def main():
    logger.info("Phase 1 — Corpus profile (stub)")
    logger.info("See pipelines/BENI/exploration/run_phase1.py for reference.")


if __name__ == "__main__":
    main()
