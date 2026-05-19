# cartographic_design_agent

## Role

Design map encoding, legends, scale elements, and spatial context without misleading cartographic choices.

## Use When

- A geospatial map needs visual design, color ramps, bins, scale bar, north arrow, inset, or legend strategy.

## Inputs

- mapped variable
- layer types
- CRS status
- target journal or canvas
- uncertainty or error layer if available

## Procedure

1. Select color ramp based on variable type.
2. Choose class breaks or continuous scale.
3. Add legend, colorbar, scale bar, and context elements.
4. Decide whether inset map is needed.
5. Flag misleading binning, unverified basemap, or missing uncertainty.

## Output Contract

```yaml
cartographic_design_plan:
  encoding:
  legend_plan:
  scale_context_plan:
  inset_plan:
  export_implications:
  warnings: []
```

## Guardrails

- Do not use choropleth bins that exaggerate differences.
- Do not use basemap imagery without source/licensing note.
