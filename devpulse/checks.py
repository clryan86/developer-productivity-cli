from __future__ import annotations
import ast
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

SKIP = {".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache", ".ruff_cache", "dist", "build"}
SECRET_PATTERNS = [
    ("AWS access key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("Private key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("Generic API key", re.compile(r"(?i)(?:api[_-]?key|token|secret)\s*[=:]\s*["'][A-Za-z0-9_\-]{20,}["']")),
]

@dataclass
class Finding:
    check: str
    status: str
    message: str
    path: str | None = None
    line: int | None = None
    def dict(self):
        return asdict(self)

def files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if path.is_file() and not any(part in SKIP for part in path.relative_to(root).parts):
            yield path

def structure(root: Path):
    checks = [("README", "README.md"), ("License", "LICENSE"), ("Git ignore", ".gitignore")]
    out = []
    for label, name in checks:
        exists = (root / name).exists()
        out.append(Finding(label, "pass" if exists else "warn", f"{name} " + ("present" if exists else "missing"), name))
    workflow_dir = root / ".github" / "workflows"
    ci = list(workflow_dir.glob("*.yml")) + list(workflow_dir.glob("*.yaml")) if workflow_dir.exists() else []
    out.append(Finding("CI", "pass" if ci else "warn", f"{len(ci)} workflow(s) found" if ci else "No GitHub Actions workflow found", ".github/workflows"))
    tests = (root / "tests").exists()
    out.append(Finding("Tests", "pass" if tests else "warn", "tests directory present" if tests else "tests directory missing", "tests"))
    deps = any((root / x).exists() for x in ("pyproject.toml", "requirements.txt", "package.json", "go.mod", "Cargo.toml"))
    out.append(Finding("Dependencies", "pass" if deps else "info", "Dependency manifest found" if deps else "No common dependency manifest found"))
    return out

def python_syntax(root: Path):
    out = []
    for path in files(root):
        if path.suffix != ".py":
            continue
        try:
            ast.parse(path.read_text(encoding="utf-8", errors="replace"), filename=str(path))
        except SyntaxError as exc:
            out.append(Finding("Python syntax", "fail", exc.msg, str(path.relative_to(root)), exc.lineno))
    if not out:
        out.append(Finding("Python syntax", "pass", "All discovered Python files parse successfully"))
    return out

def secrets(root: Path):
    out = []
    for path in files(root):
        if path.stat().st_size > 1_000_000 or path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".db"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for line_no, line in enumerate(text.splitlines(), 1):
            for name, pattern in SECRET_PATTERNS:
                if pattern.search(line):
                    out.append(Finding("Secret scan", "fail", f"Potential {name}", str(path.relative_to(root)), line_no))
    if not out:
        out.append(Finding("Secret scan", "pass", "No high-signal secret patterns detected"))
    return out

def debt(root: Path):
    pattern = re.compile(r"\b(TODO|FIXME|HACK|XXX)\b", re.I)
    out = []
    for path in files(root):
        if path.stat().st_size > 500_000:
            continue
        for line_no, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            if pattern.search(line):
                out.append(Finding("Technical debt", "info", line.strip()[:180], str(path.relative_to(root)), line_no))
    if not out:
        out.append(Finding("Technical debt", "pass", "No TODO/FIXME/HACK markers found"))
    return out

def inventory(root: Path):
    file_list = list(files(root))
    extensions = {}
    for path in file_list:
        key = path.suffix or "[none]"
        extensions[key] = extensions.get(key, 0) + 1
    return {
        "files": len(file_list),
        "bytes": sum(path.stat().st_size for path in file_list),
        "extensions": dict(sorted(extensions.items(), key=lambda x: (-x[1], x[0]))),
        "python_files": sum(path.suffix == ".py" for path in file_list),
    }
