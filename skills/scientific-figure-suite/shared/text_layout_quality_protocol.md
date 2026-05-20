# Text Layout Quality Protocol

Version: 0.8.0

This protocol defines the Text Layout Intelligence Runtime. It treats figure text
as a quality-controlled scientific artifact, not as a cosmetic afterthought.

## Scope

The runtime audits and repairs:

- figure titles
- panel titles
- x and y axis labels
- tick labels
- legend titles and labels
- colorbar titles and tick labels
- panel labels
- direct labels
- annotations

The default behavior is auto-fix plus audit. Repair may shorten, wrap, rotate,
reserve margins, or hide low-priority direct labels, but it must not rewrite the
scientific meaning.

## Text Element Contract

Every text element should expose these fields when possible:

- `text`
- `role`
- `panel_id`
- `bbox`
- `font_size_pt`
- `rotation`
- `anchor`
- `priority`
- `can_wrap`
- `can_abbreviate`
- `in_axes_bounds`
- `overlap_checked`

Allowed roles:

- `figure_title`
- `panel_title`
- `x_label`
- `y_label`
- `tick_label`
- `legend_title`
- `legend_label`
- `colorbar_title`
- `colorbar_tick_label`
- `panel_label`
- `direct_label`
- `annotation`

Bounding boxes are normalized figure coordinates unless a renderer-specific
layout artifact states otherwise.

## Quality Rules

1. Text must not overlap higher-priority text.
2. Text must not exceed figure bounds unless the element is explicitly marked as
   external caption text.
3. Axis labels and tick labels must remain inside the allocated axes or reserved
   margin area.
4. Font size must remain readable for manuscript export.
5. Excessive tick rotation is a warning unless labels are clipped or unreadable.
6. Direct labels on scatter and map panels require a controlled label policy.
7. Long titles should wrap before they force axis or colorbar clipping.
8. Long colorbar titles should move detailed wording to the caption and keep a
   short title on the colorbar.
9. `constrained_layout` or `tight_layout` alone is not sufficient evidence of
   final text layout quality.
10. Final readiness requires a recorded text layout audit.

## Colorbar Text Policy

The default colorbar location is the right side of the owning plot or panel.

A grouped colorbar may move to the outer edge of a multi-panel group only when:

- the panels share the same scale and semantic variable,
- text audit passes,
- the colorbar title is short or safely wrapped,
- panel boxes are not compressed or misaligned,
- the colorbar label spacing was explicitly checked.

Long colorbar descriptions belong in the caption. The colorbar itself should use
compact academic wording such as `Error`, `RMSE`, `Discharge`, `Expression`, or
`Adjusted P`.

## Domain Terminology

Bundled domain text profiles live in:

`assets/text_profiles/domain_text_profiles.json`

They provide canonical axis labels, title patterns, unit formatting rules,
accepted abbreviations, forbidden vague labels, and caption-expansion
suggestions. User-supplied glossary terms may override bundled profiles for the
active project, but the override should be recorded in project-local memory.

## Memory

Text audits append to:

`.codex/scientific-figure-memory/text_layout_history.jsonl`

Failed text layout audits block submission readiness.

## Runtime Commands

```bash
python scripts/select_text_profile.py --domain model-performance --chart-type roc_pr_curve
python scripts/audit_text_layout.py --layout layout.yaml --out text_layout_report.json
python scripts/repair_text_layout.py --layout layout.yaml --out repaired_layout.yaml
```
