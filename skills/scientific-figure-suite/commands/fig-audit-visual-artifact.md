# fig-audit-visual-artifact

Append a file-level visual audit artifact entry.

## Read

1. `fig/figure-auditor/WORKFLOW.md`
2. `shared/submission_memory_runtime.md`
3. `scripts/audit_visual_artifact.py`

## Behavior

- Hash the checked figure file.
- Record format, byte size, dimensions when available, result, and gate notes.
- Append `visual_audit_artifact.jsonl`.
- Use this as evidence of which file was audited, not as proof of scientific
  correctness by itself.

## Suggested Script

```powershell
python scripts/audit_visual_artifact.py --memory-dir .codex/scientific-figure-memory --figure-id fig_01 --path figures/output/fig_01.pdf --result PASS_WITH_WARNINGS --gate "journal style unverified"
```

## Output

Report figure id, file path, SHA-256, result, and warnings.

