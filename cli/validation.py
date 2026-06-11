from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class LanguageRow:
    pipeline_id: str
    name: str
    pipeline_status: str
    dataset_status: str
    seeking: bool


@dataclass(frozen=True, slots=True)
class ValidationReport:
    messages: tuple[str, ...]
    errors: tuple[str, ...]


def _read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise TypeError(f"{path} must contain a JSON object")
    return payload


def _string_list(payload: dict[str, Any], key: str) -> list[str]:
    value = payload.get(key)
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise TypeError(f"{key} must be a list of strings")
    return value


def load_language_rows(registry_path: Path) -> list[LanguageRow]:
    payload = _read_json(registry_path)
    rows = payload.get("languages")
    if not isinstance(rows, list):
        raise TypeError("registry/languages.json must contain a languages list")
    languages: list[LanguageRow] = []
    for row in rows:
        if not isinstance(row, dict):
            raise TypeError("each language row must be an object")
        pipeline_id = row.get("id")
        name = row.get("name")
        pipeline_status = row.get("pipeline_status")
        dataset_status = row.get("dataset_status")
        seeking = row.get("seeking")
        if not all(
            isinstance(item, str) for item in (pipeline_id, name, pipeline_status, dataset_status)
        ):
            raise TypeError(
                "language id, name, pipeline_status, and dataset_status must be strings"
            )
        if not isinstance(seeking, bool):
            raise TypeError("language seeking must be boolean")
        languages.append(
            LanguageRow(
                pipeline_id=pipeline_id,
                name=name,
                pipeline_status=pipeline_status,
                dataset_status=dataset_status,
                seeking=seeking,
            )
        )
    return languages


def _validate_required_paths(
    root: Path, base: Path, required: list[str], errors: list[str]
) -> None:
    for rel in required:
        target = base / rel
        if not target.exists():
            errors.append(f"missing required path: {target.relative_to(root)}")


def _validate_pipeline_readme(root: Path, row: LanguageRow, errors: list[str]) -> None:
    readme_path = root / "pipelines" / row.pipeline_id / "README.md"
    dataset_readme = root / "dataset" / row.pipeline_id / "README.md"
    for path in (readme_path, dataset_readme):
        if not path.exists():
            errors.append(f"missing README: {path.relative_to(root)}")
            continue
        text = path.read_text(encoding="utf-8")
        if row.pipeline_id not in text:
            errors.append(f"{path.relative_to(root)} does not mention {row.pipeline_id}")
        if row.name not in text:
            errors.append(f"{path.relative_to(root)} does not mention {row.name}")
    if row.pipeline_id != "BENI" and readme_path.exists():
        text = readme_path.read_text(encoding="utf-8").lower()
        if "91.7%" in text or "active pipeline" in text:
            errors.append(
                f"{readme_path.relative_to(root)} contains unsupported operational claims"
            )


def _validate_schema_file(path: Path) -> list[str]:
    payload = _read_json(path)
    errors: list[str] = []
    fields = payload.get("fields")
    for key in ("domain", "version", "description", "fields"):
        if key not in payload:
            errors.append(f"{path}: missing schema key {key}")
    if not isinstance(fields, list) or not fields:
        errors.append(f"{path}: fields must be a non-empty list")
        return errors
    for index, field in enumerate(fields):
        if not isinstance(field, dict):
            errors.append(f"{path}: field {index} must be an object")
            continue
        for key in ("name", "type", "values", "description"):
            if key not in field:
                errors.append(f"{path}: field {index} missing {key}")
        values = field.get("values")
        if not isinstance(values, list) or not values:
            errors.append(f"{path}: field {index} values must be a non-empty list")
    return errors


def validate_repository(
    repo_root: Path, registry_path: Path, contract_path: Path
) -> ValidationReport:
    contract = _read_json(contract_path)
    rows = load_language_rows(registry_path)
    required_files = _string_list(contract, "required_pipeline_files")
    required_scaffold_files = _string_list(contract, "required_scaffold_files")
    required_dirs = _string_list(contract, "required_pipeline_dirs")
    pipeline_statuses = set(_string_list(contract, "pipeline_statuses"))
    dataset_statuses = set(_string_list(contract, "dataset_statuses"))
    messages: list[str] = []
    errors: list[str] = []

    template = repo_root / "pipelines" / "template"
    _validate_required_paths(repo_root, template, required_files + required_dirs, errors)
    messages.append("template contract paths checked")

    seen_ids: set[str] = set()
    for row in rows:
        if row.pipeline_id in seen_ids:
            errors.append(f"duplicate pipeline id: {row.pipeline_id}")
        seen_ids.add(row.pipeline_id)
        if row.pipeline_status not in pipeline_statuses:
            errors.append(f"{row.pipeline_id}: invalid pipeline_status {row.pipeline_status}")
        if row.dataset_status not in dataset_statuses:
            errors.append(f"{row.pipeline_id}: invalid dataset_status {row.dataset_status}")
        pipeline_base = repo_root / "pipelines" / row.pipeline_id
        dataset_base = repo_root / "dataset" / row.pipeline_id
        _validate_required_paths(repo_root, pipeline_base, required_files + required_dirs, errors)
        if row.pipeline_status != "active":
            _validate_required_paths(repo_root, pipeline_base, required_scaffold_files, errors)
        _validate_required_paths(repo_root, dataset_base, ["README.md"], errors)
        _validate_pipeline_readme(repo_root, row, errors)

    for schema_path in sorted((repo_root / "pipelines").glob("*/annotation/schemas/*.json")):
        if schema_path.name == "README.md":
            continue
        errors.extend(_validate_schema_file(schema_path))
    messages.append(f"{len(rows)} registry pipelines checked")
    return ValidationReport(messages=tuple(messages), errors=tuple(errors))
