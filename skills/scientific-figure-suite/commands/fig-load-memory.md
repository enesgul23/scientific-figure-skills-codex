# fig-load-memory

Load project-local scientific figure memory before continuing figure work.

## Read

1. `shared/figure_memory_protocol.md`
2. `shared/agents/memory_curator_agent.md`
3. `scripts/summarize_memory.py`
4. `scripts/validate_memory.py`

## Behavior

- Validate memory before trusting it.
- Summarize only the relevant project, figure, journal, dataset, claim, and audit
  state.
- Treat memory as project context, not as independent scientific evidence.
- Flag stale paths, unverified journal profiles, and open quality gates.

## Suggested Script

```powershell
python scripts/validate_memory.py --memory-dir .codex/scientific-figure-memory
python scripts/summarize_memory.py --memory-dir .codex/scientific-figure-memory
```

## Output

Provide a compact dashboard and route to the next figure workflow.

