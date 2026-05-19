# fig-update-memory

Update Figure Passport memory after figure planning, rendering, auditing,
captioning, or export.

## Read

1. `shared/figure_memory_protocol.md`
2. `shared/figure_passport_reset_boundary.md` when a reset boundary is needed
3. `shared/agents/memory_curator_agent.md`
4. `scripts/update_figure_passport.py`
5. `scripts/update_dataset_registry.py` when dataset memory changes
6. `scripts/append_visual_claim.py` when claim memory changes

## Behavior

- Update the current figure entry and version pointer.
- Append new version data instead of overwriting old version records.
- Preserve status tags and unresolved requirements.
- Append a reset boundary only when the user asks to pause, checkpoint, or
  resume later.

## Suggested Script

```powershell
python scripts/update_figure_passport.py --memory-dir .codex/scientific-figure-memory --figure-id fig_01 --version v1
python scripts/update_dataset_registry.py --memory-dir .codex/scientific-figure-memory --dataset-id dataset_id --path data/table.csv
python scripts/append_visual_claim.py --memory-dir .codex/scientific-figure-memory --claim-id claim:c01 --figure-id fig_01 --claim-text "Claim text" --visual-element "panel a" --support-status supported
```

## Output

Report changed fields, current version, status tags, and any reset boundary tag.
