from cli.app import main


def test_status_prints_registry_rows(capsys) -> None:
    exit_code = main(["status"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "BENI" in output
    assert "Total pipelines: 10" in output


def test_validate_accepts_current_repository(capsys) -> None:
    exit_code = main(["validate"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Validation passed" in output
