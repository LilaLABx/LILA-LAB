#!/usr/bin/env python3
"""BENI — Run all 5 exploration phases sequentially.

Orchestrates Phase 0→4 in dependency order, then generates the
diagnostic report.  Each phase is a separate subprocess so partial
failures are visible.

Usage::

    python run_all.py [--force] [--skip PHASE [PHASE ...]]
        --force    Re-run phases even if output exists
        --skip     Skip one or more phases by name
                   (sample, profile, vocabulary, temporal, schema)

Environment variables:
    N_WORKERS   Number of parallel phase processes (default: 1, run sequentially)
"""

from __future__ import annotations

import argparse
import logging
import os
import subprocess
import sys
import time
from pathlib import Path

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("run_all")

_HERE = Path(__file__).resolve().parent

PHASES = [
    ("sample", "run_phase0.py"),
    ("profile", "run_phase1.py"),
    ("vocabulary", "run_phase2.py"),
    ("temporal", "run_phase3.py"),
    ("schema", "run_phase4.py"),
]

PHASE_DEPENDENCIES: dict[str, list[str]] = {
    "sample": [],
    "profile": ["sample"],
    "vocabulary": ["sample"],
    "temporal": ["sample"],
    "schema": ["sample"],
}


def _phase_output_exists(phase_name: str) -> bool:
    """Check if a phase's output already exists."""
    import yaml
    config_path = _HERE / "config.yaml"
    if not config_path.exists():
        return False
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    out_base = Path(config["output"]["base_dir"])
    phase_dir = out_base / config["output"]["phases"].get(phase_name, phase_name)
    # Phase dir exists and has at least one json file
    if phase_dir.exists():
        json_files = list(phase_dir.glob("*.json"))
        return len(json_files) > 0
    return False


def run_phase(script_name: str, force: bool = False) -> bool:
    """Run one phase script. Returns True on success."""
    script_path = _HERE / script_name
    if not script_path.exists():
        logger.error("Script not found: %s", script_path)
        return False

    logger.info("=" * 60)
    logger.info("Running: %s", script_name)
    logger.info("=" * 60)

    start = time.time()
    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=_HERE,
        capture_output=False,
    )
    elapsed = time.time() - start

    if result.returncode == 0:
        logger.info("✅ %s completed in %.1fs", script_name, elapsed)
        return True
    else:
        logger.error("❌ %s failed (exit code %d) in %.1fs",
                      script_name, result.returncode, elapsed)
        return False


def generate_report(force: bool = False) -> bool:
    """Generate diagnostic report from phase outputs."""
    import yaml
    sys.path.insert(0, str(_HERE.parents[1]))
    from shared.analysis.reporter import generate_report

    config_path = _HERE / "config.yaml"
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    out_base = Path(config["output"]["base_dir"])
    report_dir = out_base / config["output"]["phases"]["report"]

    phases = {}
    for phase_name, _ in PHASES:
        phase_dir = out_base / config["output"]["phases"].get(phase_name, phase_name)
        json_files = sorted(phase_dir.glob("*_summary.json")) + sorted(phase_dir.glob("*.json"))
        # Find the main output file
        main_file = phase_dir / f"{phase_name}_summary.json"
        if main_file.exists():
            phases[phase_name] = str(main_file.resolve())
        elif json_files:
            phases[phase_name] = str(json_files[0].resolve())
        else:
            phases[phase_name] = None

    report_path = generate_report(
        language="BENI",
        output_dir=str(report_dir.resolve()),
        phases=phases,
    )
    logger.info("Diagnostic report → %s", report_path)
    return True


def main():
    parser = argparse.ArgumentParser(description="Run all BENI exploration phases")
    parser.add_argument("--force", action="store_true", help="Re-run phases even if output exists")
    parser.add_argument("--skip", nargs="*", default=[], help="Phases to skip")
    parser.add_argument("--until", choices=[p[0] for p in PHASES], default=None,
                        help="Run phases up to and including this one")
    args = parser.parse_args()

    skip_set = set(args.skip)

    # Determine which phases to run
    active_phases = PHASES
    if args.until:
        idx = next(i for i, (n, _) in enumerate(PHASES) if n == args.until)
        active_phases = PHASES[:idx + 1]

    # Filter skipped and already-completed (unless --force)
    to_run = []
    for phase_name, script_name in active_phases:
        if phase_name in skip_set:
            logger.info("Skipping %s (--skip)", phase_name)
            continue
        if not args.force and _phase_output_exists(phase_name):
            logger.info("Skipping %s (output exists, use --force to re-run)", phase_name)
            continue
        to_run.append((phase_name, script_name))

    if not to_run:
        logger.info("Nothing to run.")
        # Still generate report
        generate_report(force=args.force)
        return

    # Check dependencies
    phase_names = {p[0] for p in to_run}
    for phase_name, _ in to_run:
        for dep in PHASE_DEPENDENCIES.get(phase_name, []):
            if dep not in phase_names and not _phase_output_exists(dep):
                logger.warning("Dependency not met: %s depends on %s", phase_name, dep)

    # Run phases sequentially
    success = True
    for phase_name, script_name in to_run:
        ok = run_phase(script_name, force=args.force)
        if not ok:
            logger.error("Pipeline halted at %s", phase_name)
            success = False
            break

    if success:
        generate_report(force=args.force)
        logger.info("✅ All phases complete. Report generated.")
    else:
        logger.error("❌ Pipeline incomplete.")


if __name__ == "__main__":
    main()
