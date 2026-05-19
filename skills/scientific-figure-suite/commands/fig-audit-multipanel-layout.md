---
description: Audit multi-panel layout geometry, colorbars, semantic colors, and optical grid quality
---

Use for final or near-final multi-panel figure layout checks, especially when
colorbars, maps, scatter panels, shared legends, or station labels are present.

## Read

1. `shared/multipanel_layout_quality_protocol.md`
2. `fig/multipanel-composer/WORKFLOW.md`
3. `scripts/audit_multipanel_layout.py`

## Behavior

- Do not accept `constrained_layout` as the only quality control for complex
  multi-panel figures.
- Check explicit panel boxes, same-row top/bottom alignment, overlap, colorbar
  label spacing, semantic color consistency, and controlled map/scatter labels.
- Require a manual-axes fallback when automatic layout is used around colorbars.
- Append the report to `multipanel_layout_history.jsonl` when memory is enabled.

## Suggested Script

```powershell
python scripts/audit_multipanel_layout.py --layout layout.yaml --out multipanel_layout_audit.json
```

With memory:

```powershell
python scripts/audit_multipanel_layout.py --layout layout.yaml --append-memory --memory-dir .codex/scientific-figure-memory
```

## Output

Return `PASS`, `PASS_WITH_WARNINGS`, or `FAIL` with blockers and layout repair
actions. A `FAIL` result blocks submission-readiness wording.
