# Interview Guide

## 30-second explanation

> DevPulse is a zero-runtime-dependency Python developer tool. It audits repositories for project hygiene, syntax errors, likely leaked secrets and technical-debt markers, inventories files, runs an environment doctor, and exports terminal, JSON or Markdown reports with CI-friendly exit codes.

## Why standard library only?

A developer tool should be easy to bootstrap even when the target environment is partially broken. Avoiding runtime dependencies reduces installation friction and supply-chain surface.

## Why AST parsing instead of importing modules?

Importing unknown code during an audit could execute side effects. `ast.parse` detects syntax errors without running the target repository.

## Resume bullets

- Built an installable zero-runtime-dependency Python CLI for repository health, syntax validation, secret scanning, technical-debt inventory and environment diagnostics.
- Added JSON/Markdown outputs and configurable CI exit-code thresholds for automation workflows.
- Implemented safe static inspection with AST parsing plus automated CLI/audit tests and GitHub Actions CI.
