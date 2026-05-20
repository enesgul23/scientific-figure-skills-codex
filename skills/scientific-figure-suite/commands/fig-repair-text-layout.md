# fig-repair-text-layout

Use this command recipe when a figure has overlapping, clipped, crowded, vague,
or poorly aligned text and the user wants deterministic repair suggestions or a
repaired layout artifact.

## Behavior

1. Read the current layout artifact.
2. Preserve scientific meaning.
3. Wrap long titles before reducing font size.
4. Reserve margins for axis labels that exceed the axes area.
5. Rotate or wrap crowded tick labels.
6. Convert long colorbar titles to short titles plus caption notes.
7. Hide only low-priority direct labels when crowding cannot be repaired.
8. Re-run `fig-audit-text-layout` after repair.

## Default Invocation

```bash
python scripts/repair_text_layout.py --layout layout.yaml --out repaired_layout.yaml
python scripts/audit_text_layout.py --layout repaired_layout.yaml --out text_layout_report.json
```
