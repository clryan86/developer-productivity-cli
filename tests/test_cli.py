from pathlib import Path
from devpulse.cli import main

def test_cli_json_report(tmp_path: Path, capsys):
    (tmp_path / "README.md").write_text("# x")
    code = main(["audit", str(tmp_path), "--format", "json", "--fail-on", "never"])
    assert code == 0
    assert '"score"' in capsys.readouterr().out

def test_cli_writes_markdown(tmp_path: Path):
    target = tmp_path / "report.md"
    code = main(["audit", str(tmp_path), "--format", "markdown", "--output", str(target), "--fail-on", "never"])
    assert code == 0
    assert target.exists()
    assert "Repository score" in target.read_text()
