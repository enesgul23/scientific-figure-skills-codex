# fig-build-submission-package

Build a hash index for exported submission package files.

## Read

1. `fig/export-packager/WORKFLOW.md`
2. `shared/figure_set_submission_runtime.md`
3. `scripts/build_submission_package_index.py`

## Behavior

- Index supplied files or a package directory.
- Compute SHA-256 for every indexed file.
- Link files to figure ids when possible from filename or explicit arguments.
- Write `submission_package_index.json`.

## Suggested Script

```powershell
python scripts/build_submission_package_index.py --memory-dir .codex/scientific-figure-memory --package-root figures/output
```

## Output

Report indexed file count, missing package root issues, and index path.

