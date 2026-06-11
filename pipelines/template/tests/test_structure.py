"""Verify that the pipeline directory structure follows the XENI standard."""

from pathlib import Path

import pytest

REQUIRED_DIRS = ["annotation", "data", "database", "experiment", "indices"]
REQUIRED_FILES = ["README.md", "requirements.txt"]


def find_pipeline_root() -> Path:
    """Find the pipeline root by looking for the README with pipeline name."""
    return Path(__file__).resolve().parent.parent


def test_required_directories_exist():
    root = find_pipeline_root()
    for dir_name in REQUIRED_DIRS:
        assert (root / dir_name).is_dir(), f"Missing required directory: {dir_name}/"


def test_required_files_exist():
    root = find_pipeline_root()
    for file_name in REQUIRED_FILES:
        assert (root / file_name).is_file(), f"Missing required file: {file_name}"


def test_readme_has_pipeline_name():
    root = find_pipeline_root()
    readme = (root / "README.md").read_text()
    assert "ENI" in readme, "README.md should contain the pipeline name (e.g., BENI, AENI)"


def test_annotation_schemas_are_json():
    schemas_dir = find_pipeline_root() / "annotation" / "schemas"
    if schemas_dir.is_dir():
        json_files = list(schemas_dir.glob("*.json"))
        if json_files:
            import json
            for f in json_files:
                data = json.loads(f.read_text())
                assert isinstance(data, dict), f"{f.name} is not a valid JSON object"
