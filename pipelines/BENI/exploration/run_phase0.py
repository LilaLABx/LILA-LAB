#!/usr/bin/env python3
"""Phase 0 — Sample selection.

Extracts a representative sample from the compressed corpus for downstream
analysis. Supports random, stratified (by category), and temporal strategies.

Usage::

    python run_phase0.py [--config config.yaml] [--sample-size 200000]
"""

from __future__ import annotations

import argparse
import json
import logging
import random
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
logger = logging.getLogger("phase0")

# Add shared to path
_HERE = Path(__file__).resolve().parent
_PIPELINES = _HERE.parents[1]  # pipelines/
sys.path.insert(0, str(_PIPELINES))

from shared.io import read_json, save_jsonl, write_json  # noqa: E402


def _iter_corpus(corpus_path: Path, fieldnames: dict, compression: str):
    """Yield rows from corpus (zst CSV for now)."""
    import csv
    import io
    import subprocess

    if compression == "zst":
        proc = subprocess.Popen(
            ["zstd", "-q", "-dc", str(corpus_path)],
            stdout=subprocess.PIPE,
        )
        if proc.stdout is None:
            raise RuntimeError("Failed to open zstd stdout")
        text_stream = io.TextIOWrapper(proc.stdout, encoding="utf-8", newline="")
        reader = csv.DictReader(text_stream)
        yield from reader
        proc.wait()
    else:
        with open(corpus_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            yield from reader


def _select_stratified(rows, n: int, stratify_by: str, seed: int):
    """Select n rows via stratified sampling by a categorical column."""
    from collections import defaultdict

    groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        groups[row.get(stratify_by, "unknown")].append(row)

    rng = random.Random(seed)
    selected: list[dict] = []
    # Proportional allocation
    total = sum(len(v) for v in groups.values())
    for group_key, group_rows in groups.items():
        target = max(1, round(n * len(group_rows) / total))
        rng.shuffle(group_rows)
        selected.extend(group_rows[:target])

    # Trim or pad
    if len(selected) > n:
        rng.shuffle(selected)
        selected = selected[:n]
    return selected


def _select_temporal(rows, n: int, seed: int):
    """Select n rows evenly across years/months."""
    from collections import defaultdict

    buckets: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        buckets[row.get("year_month", "")[:7]].append(row)

    per_bucket = max(1, n // len(buckets))
    rng = random.Random(seed)
    selected: list[dict] = []
    for bucket_rows in buckets.values():
        rng.shuffle(bucket_rows)
        selected.extend(bucket_rows[:per_bucket])

    rng.shuffle(selected)
    return selected[:n]


def run_phase0(config: dict) -> Path:
    """Execute Phase 0 and return path to the sample file."""
    corpus_cfg = config["corpus"]
    sampling_cfg = config["sampling"]
    out_base = Path(config["output"]["base_dir"])
    sample_dir = out_base / config["output"]["phases"]["sample"]
    sample_dir.mkdir(parents=True, exist_ok=True)

    # Resolve corpus path
    corpus_path = _HERE / corpus_cfg["path"]
    if not corpus_path.exists():
        fallback = _HERE / corpus_cfg["fallback"]
        if fallback.exists():
            corpus_path = fallback
            logger.info("Using fallback corpus: %s", fallback)
        else:
            raise FileNotFoundError(f"Corpus not found: {corpus_path} or {fallback}")

    n = sampling_cfg["sample_size"]
    seed = sampling_cfg["seed"]
    strategy = sampling_cfg.get("strategy", "random")
    stratify_by = sampling_cfg.get("stratify_by", "category_harmonised")
    fieldnames = corpus_cfg["fieldnames"]

    logger.info("Phase 0 — Sampling strategy=%s, n=%s, seed=%s", strategy, n, seed)
    logger.info("Corpus: %s", corpus_path)

    rows = list(_iter_corpus(corpus_path, fieldnames, corpus_cfg["compression"]))
    logger.info("Total rows in corpus: %s", len(rows))

    if strategy == "stratified":
        selected = _select_stratified(rows, n, stratify_by, seed)
    elif strategy == "temporal":
        selected = _select_temporal(rows, n, seed)
    else:
        rng = random.Random(seed)
        selected = rows[:]  # copy
        rng.shuffle(selected)
        selected = selected[:n]

    logger.info("Selected %s rows", len(selected))

    # Write outputs
    sample_json = sample_dir / "sample.json"
    write_json(sample_json, {"n": len(selected), "strategy": strategy, "seed": seed})
    logger.info("Sample metadata → %s", sample_json)

    sample_jsonl = sample_dir / "sample.jsonl"
    save_jsonl(selected, sample_jsonl)
    logger.info("Sample data → %s", sample_jsonl)

    # Summary stats about the sample
    cat_counts: dict[str, int] = {}
    for row in selected:
        cat = row.get(fieldnames["category"], "unknown")
        cat_counts[cat] = cat_counts.get(cat, 0) + 1

    summary = {
        "total": len(selected),
        "strategy": strategy,
        "seed": seed,
        "corpus": str(corpus_path),
        "category_counts": dict(sorted(cat_counts.items(), key=lambda x: -x[1])),
    }
    summary_path = sample_dir / "sample_summary.json"
    write_json(summary_path, summary)
    logger.info("Summary → %s", summary_path)

    return sample_jsonl


def main():
    parser = argparse.ArgumentParser(description="Phase 0 — Sample selection")
    parser.add_argument("--config", default="config.yaml", help="Path to config YAML")
    parser.add_argument("--sample-size", type=int, default=None, help="Override sample size")
    args = parser.parse_args()

    import yaml
    config_path = _HERE / args.config
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))

    if args.sample_size:
        config["sampling"]["sample_size"] = args.sample_size

    run_phase0(config)


if __name__ == "__main__":
    main()
