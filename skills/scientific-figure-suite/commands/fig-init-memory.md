# fig-init-memory

Initialize project-local scientific figure memory.

## Read

1. `shared/figure_memory_protocol.md`
2. `shared/agents/memory_curator_agent.md`
3. `scripts/init_memory.py` if files should be created

## Behavior

- Use `.codex/scientific-figure-memory/` unless the user supplies a path.
- Create research-grade memory by default.
- Do not overwrite existing memory unless the user explicitly requests force.
- Record target journals as `ESTIMATED` or `UNVERIFIED` unless current official
  or user-provided guidelines are active in the task.

## Suggested Script

```powershell
python scripts/init_memory.py --project-root . --project-id <project_id>
```

## Output

Report memory path, files created, files already present, project id, target
journals, and next recommended command.

