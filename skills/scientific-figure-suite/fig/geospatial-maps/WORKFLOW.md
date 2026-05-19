# Geospatial Maps

## Purpose

Create maps and spatial scientific figures with coordinate reference system integrity, scale, legends, source disclosure, and reproducible geospatial processing.

## Trigger Conditions

Use for study-area maps, flood extent, basin/catchment maps, station networks, rasters, DEM/slope maps, choropleths, inset maps, time-slice map panels, and spatial model-error overlays.

## Required Inputs

- spatial data paths or layer descriptions
- CRS/projection
- variable to map
- area of interest
- units and data source

## Optional Inputs

- basemap source
- scale-bar and north-arrow preference
- inset map
- color ramp preference
- target journal
- vector/raster export requirement

## Output Contract

Produce map figure specification, cartographic requirements, code outline or runnable code, source/projection notes, and quality checks.

## Procedure

1. Verify CRS for every spatial layer.
2. Identify layer types: vector, raster, point station, boundary, basemap, or model output.
3. Choose map encoding and color ramp appropriate to the mapped variable.
4. Add scale bar, legend, units, source, projection, and north arrow when appropriate.
5. Use inset maps when geographic context is otherwise unclear.
6. Export linework as vector and continuous rasters at suitable resolution.

## Quality Gates

- CRS/projection is stated
- scale, legend, units, and data source are present
- color ramp is not misleading
- choropleth bins are justified
- basemap licensing/source is not hidden

## Failure Modes

- CRS is missing
- map has no scale or legend
- basemap source is unverified
- choropleth bins distort interpretation
- raster resolution is insufficient for the target output

## Memory Integration

If project memory exists, read `shared/submission_memory_runtime.md` and
validate memory before map work. Use dataset registry projection, resolution,
extent, layer, and preprocessing notes when present. Update panel-level Figure
Passport entries with spatial data refs, code refs, output refs, cartographic
status, and repro-lock hashes for rendered map panels.

## v0.6 Dependency Planning

Inspect spatial data before render planning. Vector data should prefer
`geopandas` plus static matplotlib output; raster or NetCDF data should route
through `rasterio`/`xarray` planning. Basemaps, boundaries, and contextual map
layers are external data and must pass `fig-plan-external-data` with source,
license, citation, and contextual/evidentiary role classification.

## Agent Role References

- `agents/spatial_integrity_agent.md` for CRS, projection, layer, and source checks.
- `agents/cartographic_design_agent.md` for map encoding, bins, legend, scale, and inset design.

## Handoff Rules

Hand off to `multipanel-composer` for map panels, `caption-alttext` for source and projection notes, `figure-auditor` for spatial integrity, and `export-packager` for format selection.
