# Multipanel Layout Quality Protocol

## Purpose

v0.7 adds explicit layout quality control for multi-panel scientific figures.
The protocol treats layout as an auditable scientific artifact, not a side
effect of `constrained_layout`, `tight_layout`, or another automatic renderer.

## Rules

1. Multi-panel figures with colorbars require explicit colorbar layout control.
2. `constrained_layout` or `tight_layout` alone is not sufficient when colorbars,
   shared legends, inset axes, or unequal panel priorities are present.
3. Repeated semantic categories, models, groups, station classes, or risk levels
   must keep the same color across panels unless the exception is captioned.
4. Direct station or point labels in maps and scatter panels are allowed only as
   a controlled, collision-checked subset. Prefer numbered/indexed callouts,
   inset tables, or external legends for dense station networks.
5. Colorbar labels must be checked for collision and spacing before final export.
   Long technical labels should move to the caption or use a short colorbar
   title with units.
6. The layout audit must ask whether panel boxes in the same visual row share
   the same top and bottom bounds.
7. If automatic layout produces poor spacing, label collisions, or an uneven
   optical grid, switch to manual axes boxes or an explicitly audited layout
   template.
8. Visual review must answer whether the optical grid is coherent, not merely
   whether the code ran and files exist.

## Required Layout Spec Fields

For final multi-panel layout audits, prefer:

```yaml
layout_name: figure_01_layout
layout_engine: manual_axes
manual_axes_fallback: true
semantic_color_map:
  observed: "#0072B2"
  model_a: "#D55E00"
panels:
  - id: a
    plot_type: scatter
    bbox: {x0: 0.08, y0: 0.56, width: 0.38, height: 0.34}
    color_bindings:
      observed: "#0072B2"
      model_a: "#D55E00"
    direct_labels:
      count: 0
      policy: controlled
      collision_checked: true
      max_count: 8
  - id: b
    plot_type: geospatial_map
    bbox: {x0: 0.55, y0: 0.56, width: 0.30, height: 0.34}
    colorbar:
      label: "Error"
      short_label: "Error"
      label_overlap_checked: true
      label_spacing_checked: true
      bbox: {x0: 0.88, y0: 0.58, width: 0.025, height: 0.30}
```

## Runtime

Use:

```powershell
python scripts/audit_multipanel_layout.py --layout layout.yaml --out multipanel_layout_audit.json
```

Add `--append-memory --memory-dir .codex/scientific-figure-memory` when project
memory is enabled. The audit appends to `multipanel_layout_history.jsonl`.
