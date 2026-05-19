# fig-build-figure-set

Build manuscript-level figure set memory from the Figure Passport.

## Read

1. `shared/figure_set_submission_runtime.md`
2. `shared/submission_memory_runtime.md`
3. `scripts/build_figure_set_manifest.py`

## Behavior

- Read project-local Figure Passport.
- Summarize each figure, current version, outputs, status tags, stale state,
  panel count, and unresolved requirements.
- Write `figure_set_manifest.json`.

## Suggested Script

```powershell
python scripts/build_figure_set_manifest.py --memory-dir .codex/scientific-figure-memory
```

## Output

Report figure count, stale count, unresolved requirements, and manifest path.

