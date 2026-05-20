# Multipanel Composer

## Purpose

Compose multiple panels into a coherent, journal-oriented figure layout with clear message hierarchy, consistent labels, aligned axes, and efficient whitespace.

## Trigger Conditions

Use when the user asks for a multi-panel figure, panel arrangement, Nature-style panel, combined figure, figure layout, shared legend, or journal column sizing.

## Required Inputs

- panel list
- intended scientific message
- target journal or target size
- panel priorities

## Optional Inputs

- shared legends
- colorbar count, label text, and colorbar placement needs
- column width
- aspect ratios
- panel dependency order
- desired final formats
- semantic color map for repeated groups, models, station classes, or risk levels
- direct station/point label policy for maps or scatter panels
- text layout artifact or expected text roles when titles, labels, legends,
  annotations, or colorbar titles are dense

## Output Contract

Produce layout specification, panel map, label plan, legend and colorbar plan,
semantic color map, dimensions, optical-grid audit requirements, and export
implications. When text is material to the layout, include `text_elements`
with roles, bounding boxes, priority, wrapping, abbreviation, and overlap-check
status.

## Procedure

1. Rank panels by scientific importance and reading order.
2. Choose a grid or flow that supports the message rather than equalizing all panels.
3. Assign lowercase bold upright panel labels.
4. Align comparable axes and share scales where comparison is intended.
5. Consolidate legends and colorbars where possible, but require explicit
   colorbar boxes and label spacing checks when colorbars are present.
6. Preserve semantic color identity across panels for repeated categories.
7. Use direct station or point labels only as a controlled, collision-checked
   subset in map or scatter panels.
8. Minimize whitespace without crowding text, labels, colorbars, or data.
9. If automatic layout gives an uneven optical grid, switch to manual axes boxes
   or an audited panel layout template.
10. Hand long colorbar titles to the Text Layout Intelligence Runtime so the
    colorbar can keep a short title and move detail to the caption.

## Quality Gates

- panel labels are sequential and consistent
- reading order is logical
- comparable panels use comparable scales
- text remains legible at final size
- shared legends and colorbars do not dominate
- `constrained_layout` or `tight_layout` alone is not treated as sufficient for
  colorbar-heavy multi-panel figures
- colorbar labels have collision and spacing checks before final export
- same-row panel boxes share top and bottom bounds within tolerance
- repeated semantic categories keep the same colors across panels
- map/scatter station labels are controlled, sparse, and collision-checked
- text layout audit passes for titles, tick labels, axis labels, colorbar
  titles, direct labels, and annotations
- visual review includes optical grid quality, not only successful code execution

## Failure Modes

- too many panels for target size
- inconsistent scales imply false comparison
- labels are unreadable
- message hierarchy is weak
- individual panels have incompatible aspect needs
- colorbars compress panel boxes or create label collisions
- the same category changes color across panels
- direct station labels clutter map/scatter panels
- automatic layout creates visibly uneven panel bounds
- title, axis-label, tick-label, legend, annotation, or colorbar text overlaps
  or clips outside the figure/axes bounds

## Memory Integration

If project memory exists, read `shared/submission_memory_runtime.md` and
validate memory before composition. Treat panel-level Figure Passport entries as
the source of panel identity, purpose, claim refs, stale status, and output refs.
Do not package a composed figure as current when any required panel is stale.

## Agent Role References

- `agents/layout_architect_agent.md` for panel hierarchy, reading order, grid, and dimensions.
- `agents/panel_consistency_agent.md` for colors, labels, scales, notation, and legends.

## Handoff Rules

Hand off to `fig-audit-multipanel-layout` before final audit when the figure has
multiple panels, colorbars, maps, scatter panels, or direct labels. Then run
`fig-audit-text-layout` when text layout artifacts are available. Hand off to
`journal-style-translator` for sizing, `caption-alttext` for panel legend text,
`figure-auditor` for layout review, and `export-packager` for final files.
