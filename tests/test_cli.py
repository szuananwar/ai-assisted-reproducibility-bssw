from checker.cli import _github_clone_url, build_parser, main


def test_github_url_normalization():
    clone_url, name = _github_clone_url("https://github.com/example/scientific-project")
    assert clone_url == "https://github.com/example/scientific-project.git"
    assert name == "scientific-project"


def test_invalid_github_host():
    try:
        _github_clone_url("https://example.com/owner/repository")
    except ValueError as exc:
        assert "public HTTPS GitHub URLs" in str(exc)
    else:
        raise AssertionError("Expected ValueError for a non-GitHub URL.")


def test_parser_defaults():
    parser = build_parser()
    args = parser.parse_args(["assess", "."])
    assert args.command == "assess"
    assert args.domain == "general"
    assert args.hpc_applicable is True
    assert args.json is False


def test_cli_assesses_local_repository(tmp_path, capsys):
    (tmp_path / "README.md").write_text("# Example\n\nRun with python example.py\n", encoding="utf-8")
    (tmp_path / "requirements.txt").write_text("numpy==2.0.0\n", encoding="utf-8")
    (tmp_path / "LICENSE").write_text("MIT\n", encoding="utf-8")
    exit_code = main(["assess", str(tmp_path), "--no-hpc"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "ReproPilot Assessment" in captured.out
    assert "Presence:" in captured.out
    assert "Quality:" in captured.out


def test_cli_writes_json_report(tmp_path):
    repository = tmp_path / "repository"
    repository.mkdir()
    (repository / "README.md").write_text("# Example\n\nInstallation and run instructions.\n", encoding="utf-8")
    output = tmp_path / "assessment.json"
    exit_code = main(["assess", str(repository), "--no-hpc", "--output", str(output)])
    assert exit_code == 0
    assert output.exists()
    content = output.read_text(encoding="utf-8")
    assert '"presence"' in content
    assert '"quality"' in content
