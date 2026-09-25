from __future__ import annotations
from pathlib import Path
from .checks import debt, inventory, python_syntax, secrets, structure

def audit(root: Path):
    root = Path(root).resolve()
    findings = []
    for fn in (structure, python_syntax, secrets, debt):
        findings.extend(fn(root))
    counts = {status: sum(f.status == status for f in findings) for status in ("pass", "warn", "fail", "info")}
    score = max(0, 100 - counts["fail"] * 25 - counts["warn"] * 7)
    return {"root": str(root), "score": score, "counts": counts, "inventory": inventory(root), "findings": [f.dict() for f in findings]}

def markdown(result):
    lines = [
        f"# DevPulse Audit — {Path(result['root']).name}", "",
        f"**Repository score: {result['score']}/100**", "",
        f"Files: {result['inventory']['files']} • Python: {result['inventory']['python_files']} • Bytes: {result['inventory']['bytes']:,}",
        "", "## Findings", "",
    ]
    icon = {"pass": "✅", "warn": "⚠️", "fail": "❌", "info": "ℹ️"}
    for finding in result["findings"]:
        location = f" — `{finding['path']}:{finding['line']}`" if finding.get("path") and finding.get("line") else f" — `{finding['path']}`" if finding.get("path") else ""
        lines.append(f"- {icon[finding['status']]} **{finding['check']}**: {finding['message']}{location}")
    return "\n".join(lines) + "\n"
