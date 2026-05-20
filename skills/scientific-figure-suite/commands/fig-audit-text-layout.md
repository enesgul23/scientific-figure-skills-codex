# fig-audit-text-layout

Use this command recipe when the user asks to check whether figure text is
readable, aligned, unclipped, non-overlapping, and academically worded.

## Behavior

1. Load the layout artifact, exported SVG-derived text boxes, or renderer context.
2. Select the bundled text profile if domain or chart type is known.
3. Run `scripts/audit_text_layout.py`.
4. Report blockers before warnings.
5. If project-local memory is enabled, append the report to
   `text_layout_history.jsonl`.

## Default Invocation

```bash
python scripts/audit_text_layout.py --layout layout.yaml --out text_layout_report.json
```

Use `--append-memory` only when the user is working in a project with initialized
Scientific Figure memory.
