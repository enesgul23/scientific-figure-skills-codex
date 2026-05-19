# fig-audit-readiness

Audit submission readiness for the full figure set and package.

## Read

1. `shared/figure_set_submission_runtime.md`
2. `scripts/audit_submission_readiness.py`
3. `fig/figure-auditor/WORKFLOW.md`
4. `fig/export-packager/WORKFLOW.md`

## Behavior

- Validate memory.
- Require no stale figures or panels.
- Require package index files to exist and match hashes.
- Require visual audit artifacts for final outputs.
- Require latest multi-panel layout audit not to fail when multi-panel figures,
  colorbars, shared legends, maps, scatter labels, or station labels are present.
- Require journal verification unless the user explicitly allows an unverified
  journal waiver for internal review.
- Append `submission_readiness_history.jsonl`.

## Suggested Script

```powershell
python scripts/audit_submission_readiness.py --memory-dir .codex/scientific-figure-memory
```

## Output

Return READY, READY_WITH_WARNINGS, or BLOCKED with gates, blockers, and warnings.
