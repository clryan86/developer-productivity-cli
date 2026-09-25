from pathlib import Path

from devpulse.audit import audit, markdown

def test_good_repo_scores_high(tmp_path: Path):
    (tmp_path / "README.md").write_text("# Demo")
    (tmp_path / "LICENSE").write_text("MIT")
    (tmp_path / ".gitignore").write_text(".venv")
    (tmp_path / "pyproject.toml").write_text('[project]\nname="demo"\nversion="0.1"')
    (tmp_path / "tests").mkdir()
    (tmp_path / ".github/workflows").mkdir(parents=True)
    (tmp_path / ".github/workflows/ci.yml").write_text("name: CI")
    (tmp_path / "app.py").write_text("x = 1\n")
    result = audit(tmp_path)
    assert result["score"] == 100
    assert result["counts"]["fail"] == 0
    assert "DevPulse Audit" in markdown(result)

def test_syntax_and_secret_findings_fail(tmp_path: Path):
    (tmp_path / "bad.py").write_text("def broken(:\n")
    secret_text = "api_" + "key=" + '"' + "abcdefghijklmnopqrstuvwxyz123456" + '"'
    (tmp_path / "config.txt").write_text(secret_text)
    result = audit(tmp_path)
    assert result["counts"]["fail"] >= 2
    assert result["score"] < 100
