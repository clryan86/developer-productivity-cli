# Architecture

```mermaid
flowchart TD
    CLI[Argparse CLI] --> A[Audit Coordinator]
    A --> S[Structure Checks]
    A --> P[Python AST Check]
    A --> K[Secret Scanner]
    A --> D[Debt Scanner]
    A --> I[File Inventory]
    CLI --> DOC[Environment Doctor]
    A --> O1[Terminal]
    A --> O2[JSON]
    A --> O3[Markdown]
```

The CLI intentionally uses only the Python standard library at runtime. Repository source is read as text and Python is parsed with `ast.parse`; project code is never imported or executed by the auditor.
