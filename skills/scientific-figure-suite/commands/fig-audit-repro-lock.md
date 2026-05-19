# fig-audit-repro-lock

Audit Figure Passport repro-lock hashes and mark stale artifacts.

## Read

1. `shared/submission_memory_runtime.md`
2. `scripts/audit_repro_lock.py`

## Behavior

- Compare stored data, code, and output hashes with current files.
- Mark figure or panel entries stale when hashes drift.
- Do not clear scientific or journal warnings.

## Suggested Script

```powershell
python scripts/audit_repro_lock.py --memory-dir .codex/scientific-figure-memory --update-stale
```

## Output

Report stale figures, stale panels, missing files, and drift reasons.

