# Changelog

## 0.7.0 - 2026-05-20

- Added Multi-panel Layout Quality Runtime for optical-grid and colorbar layout audits.
- Added `fig-audit-multipanel-layout` command recipe.
- Added `audit_multipanel_layout.py` to check panel box alignment, overlap, colorbar spacing, semantic colors, and controlled map/scatter labels.
- Added `multipanel_layout_history.jsonl` project-memory ledger and readiness/dashboard integration.
- Added multipanel layout audit schema, template, protocol, and validation smoke tests.
- Updated multi-panel workflow guidance to require manual axes fallback when automatic layout is insufficient.

## 0.6.0 - 2026-05-19

- Added Library Intelligence Runtime for Python-first dependency planning.
- Added broad library pool metadata and structural validation.
- Added dataset inspection for CSV, JSON, Excel, GeoJSON, Shapefile, GeoTIFF, NetCDF, and AnnData-like inputs.
- Added Python environment probing without package installation.
- Added render stack selection and dependency plan generation.
- Added external data decision protocol and data acquisition plan validation.
- Extended renderer registry with dependency metadata.
- Extended project memory with dependency and external data ledgers.
- Extended validation smoke tests for v0.6 runtime behavior.
