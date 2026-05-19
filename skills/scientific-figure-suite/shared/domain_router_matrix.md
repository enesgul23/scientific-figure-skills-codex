# Domain Router Matrix

Use when multiple workflows could apply.

| Signal | Primary workflow | Agents | Conditional gates | v0.6 dependency/data gate |
|---|---|---|---|---|
| p-values, CIs, group comparison | `statistical-plots` | `chart_selection_agent`, `statistical_honesty_agent` | G3, G4, G5 | inspect tabular data, then select static stack |
| observed vs predicted, residuals, NSE, KGE, RMSE | `model-performance` | `performance_diagnostic_agent`, `validation_split_agent` | G15, G4 | select metric libraries only when needed; external validation goes through data decision |
| patients, HR, OR, RR, Kaplan-Meier, adverse events | `clinical-biomedical` | `clinical_reporting_agent`, `denominator_endpoint_agent` | G13 | survival figures prefer `lifelines`; benchmarks require provenance |
| map, CRS, DEM, raster, basin, stations | `geospatial-maps` | `spatial_integrity_agent`, `cartographic_design_agent` | G12 | vector/raster stack selection; basemap/boundary requires external data plan |
| volcano, FDR, heatmap, PCA, pathway | `omics-bioinformatics` | `omics_threshold_agent`, `bioinformatics_visual_agent` | G14 | select `scanpy`/`anndata` only when format requires; annotations require external data plan |
| arrows, mechanism, conceptual model | `schematic-mechanism` | `mechanism_claim_agent` | G16 | dependency planning usually not needed unless data-derived panels are embedded |
| graphical abstract, visual summary | `graphical-abstract` | `visual_narrative_agent`, `evidence_boundary_agent` | G2, G16 | external evidence or annotation assets require provenance |
| many panels, shared legend, layout | `multipanel-composer` | `layout_architect_agent`, `panel_consistency_agent` | G7, G8 | require compatible dependency plans for data-derived panels |
| target journal/style/compliance | `journal-style-translator` | `journal_policy_agent`, `style_token_agent` | G8 | style tokens do not install or imply plotting dependencies |
| caption, legend, alt text | `caption-alttext` | `caption_integrity_agent`, `alt_text_agent` | G6, G7 | disclose external data role when used |
| review/check/audit | `figure-auditor` | reviewer agents | all relevant gates | audit blocked dependencies and external data provenance |
| final files/package | `export-packager` | package agents | G9, G10 | package dependency plan and external data provenance when present |
