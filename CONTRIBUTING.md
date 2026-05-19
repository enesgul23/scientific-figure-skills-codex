# Contributing

Thank you for improving Scientific Figure Skills for Codex.

## Development Rules

- Keep the project skill-only. Do not add a web app, service backend, or hosted dependency.
- Root discovery must remain `skills/scientific-figure-suite/SKILL.md`.
- Internal workflows must use `WORKFLOW.md`, not nested `SKILL.md`.
- Project memory must stay project-local under `.codex/scientific-figure-memory/`; do not store private memory inside the installed skill.
- Journal requirements may be marked `VERIFIED` only from current official or user-provided guidance.
- Library selection is plan-only. Do not add scripts that silently install packages.
- External data acquisition is plan-only unless the user explicitly approves download with complete provenance.

## Validation

Run this before opening a pull request:

```powershell
python quick_validate.py
```

The validation suite checks structure, schemas, memory migration, renderer
registry smoke tests, dependency planning, and external data planning.

## Pull Request Checklist

- The change preserves the scientific priority: truth > reproducibility > interpretability > journal compliance > visual elegance > novelty.
- New command aliases are listed in `SKILL.md`, `manifest.json`, and `MODE_REGISTRY.md`.
- New artifact shapes include a schema or documented contract.
- New runtime behavior is covered by `quick_validate.py`.
- No `__pycache__`, local memory, generated outputs, or private data are committed.
