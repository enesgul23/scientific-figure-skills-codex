# Geospatial Figure Rules

Use this reference for maps and spatial scientific figures.

## Required Map Metadata

- CRS or projection
- area of interest
- spatial data sources
- units
- scale bar or scale statement
- legend and colorbar labels
- basemap source and license when used

## Encoding Rules

- Use sequential color ramps for magnitude.
- Use diverging ramps only with a meaningful center.
- Use categorical palettes for classes.
- Do not use misleading choropleth bins.
- Show station markers with edge strokes on colored backgrounds.
- Use inset maps when regional context is needed.

## Export Rules

- Keep vector boundaries and labels as vector when possible.
- Export raster layers at sufficient DPI.
- Preserve aspect ratio and projection.
- Do not mix layers with incompatible CRS without transformation.

## Red Flags

- missing CRS
- no scale or legend
- unverified basemap
- map color ramp implies precision not present in data
- coordinate axes or units missing for analytical maps
