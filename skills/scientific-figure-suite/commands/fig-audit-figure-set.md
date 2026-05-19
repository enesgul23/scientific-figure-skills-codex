# fig-audit-figure-set

Audit cross-figure consistency across a manuscript figure set.

## Read

1. `shared/figure_set_submission_runtime.md`
2. `scripts/audit_figure_set_consistency.py`

## Behavior

- Check duplicate figure ids, stale figure state, mixed journal/style status,
  missing outputs, missing visual audit artifacts, and missing claim evidence.
- Append `cross_figure_consistency_history.jsonl`.
- Update `figure_set_manifest.json` consistency status.

## Suggested Script

```powershell
python scripts/audit_figure_set_consistency.py --memory-dir .codex/scientific-figure-memory --update
```

## Output

Return PASS, PASS_WITH_WARNINGS, or FAIL with blocking issues and warnings.

