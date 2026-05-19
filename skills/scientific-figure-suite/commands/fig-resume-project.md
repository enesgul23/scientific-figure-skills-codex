# fig-resume-project

Resume a scientific figure project from a Figure Passport reset boundary.

## Read

1. `shared/figure_passport_reset_boundary.md`
2. `shared/figure_memory_protocol.md`
3. `shared/agents/memory_curator_agent.md`
4. `scripts/resume_figure_project.py`
5. `scripts/validate_memory.py`

## Invocation

```text
fig-resume-project resume_from_figure_passport=<hash>
```

## Behavior

- Verify that the hash exists in `revision_boundary_ledger.jsonl`.
- Refuse double-resume when the hash is already consumed.
- Warn on stale or unverified boundary state.
- Load the Figure Passport and route to the stored next stage unless the user
  explicitly overrides it.
- Append a resume entry after successful consumption.

## Suggested Script

```powershell
python scripts/resume_figure_project.py --memory-dir .codex/scientific-figure-memory --hash <hash>
```

## Output

Emit a resume acknowledgment with hash, figure id, recovered version, next stage,
and unresolved requirements.
