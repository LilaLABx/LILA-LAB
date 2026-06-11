#!/usr/bin/env python3
"""Run all exploration phases — template."""

import logging
import subprocess
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
logger = logging.getLogger("run_all")

_HERE = Path(__file__).resolve().parent

PHASES = [
    ("00_sample", "run_phase0.py"),
    ("01_profile", "run_phase1.py"),
    ("02_vocabulary", "run_phase2.py"),
    ("03_temporal", "run_phase3.py"),
    ("04_schema", "run_phase4.py"),
]


def main():
    for phase_name, script in PHASES:
        script_path = _HERE / script
        if not script_path.exists():
            logger.warning("Skipping %s — %s not found", phase_name, script)
            continue
        logger.info("Running %s...", phase_name)
        r = subprocess.run([sys.executable, str(script_path)], cwd=_HERE)
        if r.returncode != 0:
            logger.error("❌ %s failed", phase_name)
            sys.exit(1)
        logger.info("✅ %s complete", phase_name)

    logger.info("All phases complete.")


if __name__ == "__main__":
    main()
