from pathlib import Path

from cli.validation import load_language_rows


def test_registry_language_rows_have_matching_pipeline_and_dataset_docs(repo_root: Path) -> None:
    rows = load_language_rows(repo_root / "registry" / "languages.json")

    for row in rows:
        pipeline_readme = repo_root / "pipelines" / row.pipeline_id / "README.md"
        dataset_readme = repo_root / "dataset" / row.pipeline_id / "README.md"

        assert pipeline_readme.exists(), f"missing pipeline README for {row.pipeline_id}"
        assert dataset_readme.exists(), f"missing dataset README for {row.pipeline_id}"
        assert row.pipeline_id in pipeline_readme.read_text(encoding="utf-8")
        assert row.pipeline_id in dataset_readme.read_text(encoding="utf-8")


def test_extension_index_mentions_every_registry_pipeline(repo_root: Path) -> None:
    rows = load_language_rows(repo_root / "registry" / "languages.json")
    index_text = (repo_root / "technical-reports" / "extensions" / "INDEX.md").read_text(
        encoding="utf-8"
    )

    missing = [row.pipeline_id for row in rows if row.pipeline_id not in index_text]

    assert missing == []


def test_stable_schema_registry_locations_exist(repo_root: Path) -> None:
    import json

    payload = json.loads((repo_root / "registry" / "schemas.json").read_text(encoding="utf-8"))
    schemas = payload["schemas"]
    missing: list[str] = []
    for schema in schemas:
        if schema["status"] == "stable":
            location = schema["location"]
            if location is None or not (repo_root / location).exists():
                missing.append(schema["id"])

    assert missing == []
