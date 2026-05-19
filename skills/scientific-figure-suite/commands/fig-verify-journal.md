# fig-verify-journal

Append target-journal guideline verification evidence.

## Read

1. `fig/journal-style-translator/WORKFLOW.md`
2. `shared/submission_memory_runtime.md`
3. `scripts/audit_journal_verification.py`

## Behavior

- Use `VERIFIED` only for current official or user-provided guideline evidence.
- Append `journal_guideline_verification.jsonl`.
- Update `journal_targets.json`.
- Preserve unresolved requirements for `ESTIMATED` or `UNVERIFIED` status.

## Suggested Script

```powershell
python scripts/audit_journal_verification.py --memory-dir .codex/scientific-figure-memory --journal "Nature" --source-type live_official --status VERIFIED --source-ref "<official-url-or-local-guideline-file>"
```

## Output

Report journal, status, source type, source ref, and unresolved requirements.

