from __future__ import annotations

import argparse
from pathlib import Path
from typing import Final

from cli.validation import (
    ValidationReport,
    load_language_rows,
    validate_repository,
)

REPO_ROOT: Final = Path(__file__).resolve().parent.parent


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lila",
        description="LILA Lab repository status and validation tools.",
    )
    parser.add_argument(
        "--repo-root",
        default=str(REPO_ROOT),
        help="Repository root path. Defaults to the current checkout.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    status = subparsers.add_parser("status", help="Show pipeline status from registry.")
    status.add_argument(
        "--registry",
        default="registry/languages.json",
        help="Language registry path relative to repo root.",
    )

    validate = subparsers.add_parser("validate", help="Validate registry and pipeline structure.")
    validate.add_argument(
        "--registry",
        default="registry/languages.json",
        help="Language registry path relative to repo root.",
    )
    validate.add_argument(
        "--contract",
        default="registry/xeni_pipeline_contract.json",
        help="XENI contract path relative to repo root.",
    )
    return parser


def _resolve(root: Path, candidate: str) -> Path:
    path = Path(candidate)
    if path.is_absolute():
        return path
    return root / path


def _run_status(repo_root: Path, registry_arg: str) -> int:
    registry = _resolve(repo_root, registry_arg)
    rows = load_language_rows(registry)
    print("Pipeline | Language | Pipeline status | Dataset status | Seeking")
    print("--- | --- | --- | --- | ---")
    for row in rows:
        seeking = "yes" if row.seeking else "no"
        print(
            f"{row.pipeline_id} | {row.name} | {row.pipeline_status} | "
            f"{row.dataset_status} | {seeking}"
        )
    print(f"\nTotal pipelines: {len(rows)}")
    return 0


def _print_report(report: ValidationReport) -> None:
    for message in report.messages:
        print(f"OK: {message}")
    for error in report.errors:
        print(f"ERROR: {error}")


def _run_validate(repo_root: Path, registry_arg: str, contract_arg: str) -> int:
    registry = _resolve(repo_root, registry_arg)
    contract = _resolve(repo_root, contract_arg)
    report = validate_repository(
        repo_root=repo_root, registry_path=registry, contract_path=contract
    )
    _print_report(report)
    if report.errors:
        print(f"\nValidation failed: {len(report.errors)} error(s)")
        return 1
    print("\nValidation passed")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    repo_root = Path(args.repo_root).resolve()

    match args.command:
        case "status":
            return _run_status(repo_root, args.registry)
        case "validate":
            return _run_validate(repo_root, args.registry, args.contract)
        case unreachable:
            parser.error(f"unknown command: {unreachable}")
            return 2
