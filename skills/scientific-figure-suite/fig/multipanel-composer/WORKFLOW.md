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
- column width
- aspect ratios
- panel dependency order
- desired final formats

## Output Contract

Produce layout specification, panel map, label plan, legend plan, dimensions, and export implications.

## Procedure

1. Rank panels by scientific importance and reading order.
2. Choose a grid or flow that supports the message rather than equalizing all panels.
3. Assign lowercase bold upright panel labels.
4. Align comparable axes and share scales where comparison is intended.
5. Consolidate legends and colorbars where possible.
6. Minimize whitespace without crowding text, labels, or data.

## Quality Gates

- panel labels are sequential and consistent
- reading order is logical
- comparable panels use comparable scales
- text remains legible at final size
- shared legends and colorbars do not dominate

## Failure Modes

- too many panels for target size
- inconsistent scales imply false comparison
- labels are unreadable
- message hierarchy is weak
- individual panels have incompatible aspect needs

## Memory Integration

If project memory exists, read `shared/submission_memory_runtime.md` and
validate memory before composition. Treat panel-level Figure Passport entries as
the source of panel identity, purpose, claim refs, stale status, and output refs.
Do not package a composed figure as current when any required panel is stale.

## Agent Role References

- `agents/layout_architect_agent.md` for panel hierarchy, reading order, grid, and dimensions.
- `agents/panel_consistency_agent.md` for colors, labels, scales, notation, and legends.

## Handoff Rules

Hand off to `journal-style-translator` for sizing, `caption-alttext` for panel legend text, `figure-auditor` for layout review, and `export-packager` for final files.
