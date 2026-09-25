from __future__ import annotations
import argparse
import json
from pathlib import Path
from .audit import audit, markdown
from .doctor import doctor

def main(argv=None):
    parser = argparse.ArgumentParser(prog="devpulse", description="Repository health and developer-environment diagnostics.")
    sub = parser.add_subparsers(dest="command", required=True)
    audit_parser = sub.add_parser("audit")
    audit_parser.add_argument("path", nargs="?", default=".")
    audit_parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    audit_parser.add_argument("--output")
    audit_parser.add_argument("--fail-on", choices=["never", "warn", "fail"], default="fail")
    doctor_parser = sub.add_parser("doctor")
    doctor_parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    if args.command == "doctor":
        result = doctor()
        print(json.dumps(result, indent=2) if args.json else _doctor_text(result))
        return 0

    result = audit(Path(args.path))
    text = json.dumps(result, indent=2) if args.format == "json" else markdown(result) if args.format == "markdown" else _text(result)
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text, end="" if text.endswith("\n") else "\n")
    if args.fail_on == "fail" and result["counts"]["fail"]:
        return 1
    if args.fail_on == "warn" and (result["counts"]["fail"] or result["counts"]["warn"]):
        return 1
    return 0

def _text(result):
    lines = [f"DevPulse: {Path(result['root']).name} — {result['score']}/100"]
    for finding in result["findings"]:
        location = f" ({finding['path']}:{finding['line']})" if finding.get("path") and finding.get("line") else f" ({finding['path']})" if finding.get("path") else ""
        lines.append(f"[{finding['status'].upper():4}] {finding['check']}: {finding['message']}{location}")
    return "\n".join(lines) + "\n"

def _doctor_text(result):
    lines = [f"Python {result['python']['version']} — {result['python']['executable']}", result["platform"]]
    for name, data in result["tools"].items():
        lines.append(f"{name:8} {'OK' if data['installed'] else 'MISSING'} {data['version'] or ''}".rstrip())
    return "\n".join(lines)

if __name__ == "__main__":
    raise SystemExit(main())
