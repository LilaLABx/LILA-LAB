from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Final

REPO_ROOT: Final = Path(__file__).resolve().parents[2]


def _read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise TypeError(f"{path} must contain a JSON object")
    return payload


def _validate_schema(path: Path) -> list[str]:
    payload = _read_json(path)
    errors: list[str] = []
    for key in ("domain", "version", "description", "fields"):
        if key not in payload:
            errors.append(f"{path}: missing {key}")
    fields = payload.get("fields")
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
            errors.append(f"{path}: field {index} values must be non-empty")
    return errors


def validate_all(repo_root: Path = REPO_ROOT) -> list[str]:
    errors: list[str] = []
    schema_paths = sorted(repo_root.glob("pipelines/*/annotation/schemas/*.json"))
    for path in schema_paths:
        errors.extend(_validate_schema(path))
    if not schema_paths:
        errors.append("no annotation schema JSON files found")
    return errors


def main() -> int:
    errors = validate_all()
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    count = len(list(REPO_ROOT.glob("pipelines/*/annotation/schemas/*.json")))
    print(f"Validated {count} annotation schema file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
