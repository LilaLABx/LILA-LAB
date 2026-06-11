#!/usr/bin/env python3
"""BENI — Run all 4 annotation pipeline phases sequentially.

Orchestrates Phase 1→4 in dependency order.  Each phase is a separate
subprocess so partial failures are visible and can be retried.

Usage::

    python run_all.py [--force] [--skip PHASE [PHASE ...]] [--until PHASE]
        --force    Re-run phases even if output exists
        --skip     Skip one or more phases by name
        --until    Run phases up to and including this one

    python run_all.py --skip pilot               # skip pilot, run rest
    python run_all.py --until index              # run pilot → annotate → index
    python run_all.py --force                    # re-run everything

Environment variables::

    ANTHROPIC_API_KEY    Required for Claude annotation (Phase 1 & 2)
    OPENAI_API_KEY       Required for GPT-4o annotation (Phase 1 & 2)

Dependencies between phases:

    pilot ──► annotate ──► index ──► validate

Each phase depends on the previous one's output.

Community contribution guide:
    - This orchestrator is a proven pattern (see exploration/run_all.py)
    - Add new phases by appending to PHASES and PHASE_DEPENDENCIES
    - Each phase runs as a subprocess — keep run_phase*.py self-contained
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
    ("pilot", "run_phase1_pilot.py"),
    ("annotate", "run_phase2_annotate.py"),
    ("index", "run_phase3_index.py"),
    ("validate", "run_phase4_validate.py"),
]

PHASE_DEPENDENCIES: dict[str, list[str]] = {
    "pilot": [],
    "annotate": ["pilot"],
    "index": ["annotate"],
    "validate": ["index"],
}


# ── Helpers ─────────────────────────────────────────────────────────


def _phase_output_exists(phase_name: str) -> bool:
    """Check if a phase's output already exists by inspecting config."""
    import yaml

    config_path = _HERE / "config.yaml"
    if not config_path.exists():
        return False
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    out_base = Path(config["output"]["base_dir"])
    phase_dir = out_base / config["output"]["phases"].get(phase_name, phase_name)
    if phase_dir.exists():
        json_files = list(phase_dir.glob("*.json"))
        parquet_files = list(phase_dir.glob("*.parquet"))
        return len(json_files) > 0 or len(parquet_files) > 0
    return False


def run_phase(script_name: str, force: bool = False) -> bool:
    """Run one phase script as a subprocess. Returns True on success."""
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
        logger.error(
            "❌ %s failed (exit code %d) in %.1fs",
            script_name,
            result.returncode,
            elapsed,
        )
        return False


def generate_report(force: bool = False) -> bool:
    """Generate diagnostic report from all phase outputs.

    TODO: Implement report aggregation. For now this is a placeholder.
    The report should combine:
      - Phase 1: agreement metrics, field-level reliability
      - Phase 2: annotation coverage, consensus statistics
      - Phase 3: index summary, calibration factors
      - Phase 4: correlation table, significance tests
    """
    logger.info("Report generation — not yet implemented")
    logger.info("Phase outputs available in outputs/")
    return True


# ── Main ────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Run all BENI annotation → index → validation phases"
    )
    parser.add_argument(
        "--force", action="store_true", help="Re-run phases even if output exists"
    )
    parser.add_argument(
        "--skip", nargs="*", default=[], help="Phases to skip (pilot, annotate, index, validate)"
    )
    parser.add_argument(
        "--until",
        choices=[p[0] for p in PHASES],
        default=None,
        help="Run phases up to and including this one",
    )
    args = parser.parse_args()

    skip_set = set(args.skip)

    # Determine which phases to run
    active_phases = PHASES
    if args.until:
        idx = next(i for i, (n, _) in enumerate(PHASES) if n == args.until)
        active_phases = PHASES[: idx + 1]

    # Filter skipped and already-completed (unless --force)
    to_run = []
    for phase_name, script_name in active_phases:
        if phase_name in skip_set:
            logger.info("Skipping %s (--skip)", phase_name)
            continue
        if not args.force and _phase_output_exists(phase_name):
            logger.info(
                "Skipping %s (output exists, use --force to re-run)", phase_name
            )
            continue
        to_run.append((phase_name, script_name))

    if not to_run:
        logger.info("Nothing to run.")
        generate_report(force=args.force)
        return

    # Warn about missing env vars for LLM phases
    if any(p in ("pilot", "annotate") for p, _ in to_run):
        if not os.environ.get("ANTHROPIC_API_KEY"):
            logger.warning("ANTHROPIC_API_KEY not set — Claude annotation will fail")
        if not os.environ.get("OPENAI_API_KEY"):
            logger.warning("OPENAI_API_KEY not set — GPT-4o annotation will fail")

    # Check dependencies
    phase_names = {p[0] for p in to_run}
    for phase_name, _ in to_run:
        for dep in PHASE_DEPENDENCIES.get(phase_name, []):
            if dep not in phase_names and not _phase_output_exists(dep):
                logger.warning(
                    "Dependency not met: %s depends on %s", phase_name, dep
                )

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
