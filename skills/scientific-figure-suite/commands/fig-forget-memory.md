# fig-forget-memory

Redact or remove project-local figure memory after explicit user request.

## Read

1. `shared/figure_memory_protocol.md`
2. `shared/visual_style_profile_protocol.md` for style profile redaction
3. `scripts/forget_memory.py`

## Behavior

- Ask for explicit confirmation before destructive memory removal if it is not
  already present in the user request.
- Prefer scoped forgetting over deleting the whole memory directory.
- Record a forget event when possible.
- Do not remove the installed skill or bundled templates.

## Suggested Script

```powershell
python scripts/forget_memory.py --memory-dir .codex/scientific-figure-memory --scope author_visual_style_profile --confirm
```

## Output

Report scope, files changed or removed, and remaining memory status.

