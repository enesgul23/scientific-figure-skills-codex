# fig-validate-memory

Validate project-local scientific figure memory.

## Read

1. `shared/figure_memory_protocol.md`
2. `scripts/validate_memory.py`

## Behavior

- Check required memory files.
- Parse JSON and JSONL files.
- Validate status values.
- Warn on unverified journal targets, missing active figures, stale dataset
  paths, duplicate figure ids, and consumed reset boundaries.

## Suggested Script

```powershell
python scripts/validate_memory.py --memory-dir .codex/scientific-figure-memory
```

## Output

Return PASS/FAIL with actionable warnings.

