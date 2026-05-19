# fig-summarize-memory

Summarize project-local figure memory for a dashboard or handoff.

## Read

1. `shared/figure_memory_protocol.md`
2. `scripts/summarize_memory.py`

## Behavior

- Keep the summary short enough to paste into a new session.
- Include active figure, current versions, journal status, dataset count, latest
  audit status, and unresolved requirements.
- Do not expose private details unrelated to the current figure task.

## Suggested Script

```powershell
python scripts/summarize_memory.py --memory-dir .codex/scientific-figure-memory
```

## Output

Return a compact memory dashboard.

