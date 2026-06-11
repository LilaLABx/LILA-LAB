from pathlib import Path

from cli.validation import validate_repository


def test_xeni_pipeline_contract_accepts_current_repository(repo_root: Path) -> None:
    report = validate_repository(
        repo_root=repo_root,
        registry_path=repo_root / "registry" / "languages.json",
        contract_path=repo_root / "registry" / "xeni_pipeline_contract.json",
    )

    assert report.errors == ()


def test_xeni_pipeline_contract_rejects_missing_pipeline_readme(
    tmp_path: Path, repo_root: Path
) -> None:
    bad_pipeline = tmp_path / "pipelines" / "BENI"
    bad_dataset = tmp_path / "dataset" / "BENI"
    bad_pipeline.mkdir(parents=True)
    bad_dataset.mkdir(parents=True)
    (tmp_path / "registry").mkdir()
    (tmp_path / "registry" / "languages.json").write_text(
        '{"languages":[{"id":"BENI","name":"Bangla","pipeline_status":"active",'
        '"dataset_status":"complete","seeking":false}]}',
        encoding="utf-8",
    )

    report = validate_repository(
        repo_root=tmp_path,
        registry_path=tmp_path / "registry" / "languages.json",
        contract_path=repo_root / "registry" / "xeni_pipeline_contract.json",
    )

    assert any("missing required path" in error for error in report.errors)
