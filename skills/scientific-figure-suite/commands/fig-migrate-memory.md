# fig-migrate-memory

Migrate project-local scientific figure memory to the current schema.

## Read

1. `shared/submission_memory_runtime.md`
2. `shared/figure_memory_protocol.md`
3. `scripts/migrate_memory.py`

## Behavior

- Add missing runtime ledger and index files.
- Update `schema_version`.
- Add panel/stale fields to existing Figure Passport entries.
- Preserve all append-only ledger history.

## Suggested Script

```powershell
python scripts/migrate_memory.py --memory-dir .codex/scientific-figure-memory
```

## Output

Report created files, migrated schema version, and any warnings.
