# DevPulse — Developer Productivity CLI

[![CI](https://github.com/clryan86/developer-productivity-cli/actions/workflows/ci.yml/badge.svg)](https://github.com/clryan86/developer-productivity-cli/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![CLI](https://img.shields.io/badge/Product-Developer%20CLI-6C63FF)
![Zero Runtime Dependencies](https://img.shields.io/badge/runtime%20dependencies-zero-success)

A zero-runtime-dependency Python CLI that audits repository health, scans for common engineering risks, inventories technical debt, checks Python syntax, inspects developer tooling, and emits terminal, JSON, or Markdown reports.

Unlike the other portfolio services, DevPulse is designed as an installable command-line product.

## Commands

```bash
python -m devpulse audit .
python -m devpulse audit . --format json
python -m devpulse audit . --format markdown --output audit.md
python -m devpulse doctor
python -m devpulse doctor --json
```

When installed as a package:

```bash
devpulse audit .
```

## Audit checks

- README, LICENSE and `.gitignore` presence
- GitHub Actions workflow detection
- test-directory detection
- dependency-manifest detection
- Python AST/syntax validation
- high-signal secret-pattern scanning
- TODO/FIXME/HACK technical-debt inventory
- file/language inventory

## CI-friendly behavior

`--fail-on fail` returns non-zero when failure findings exist. `--fail-on warn` treats warnings as blocking too. `--fail-on never` always produces a report without blocking a pipeline.

## Environment doctor

The doctor command reports the active Python interpreter/platform and checks availability/version information for Git, Docker, Node, npm, Ruff and pytest.

## Design goals

- no runtime third-party packages
- safe static inspection—does not execute repository Python files
- useful locally and in CI
- machine-readable output for automation
- Markdown output for pull-request artifacts
- focused, explainable checks instead of opaque scoring

## Tests

```bash
pip install -r requirements-dev.txt
pytest
ruff check .
```

## Roadmap

- configurable check plugins
- cyclomatic-complexity analyzer
- dependency freshness adapter
- test coverage ingestion
- Git status/branch-health checks
- SARIF output
- GitHub annotations
- monorepo workspace mode

## Author

**Christopher Ryan**  
Python • Developer Tooling • Automation • QA

## License

MIT
