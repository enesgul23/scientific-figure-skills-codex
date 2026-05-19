# Expected Routing

| Prompt signal | First workflow | Common chain |
|---|---|---|
| vague figure request | `intake-design` scoping mode | `intake-design -> domain workflow after missing inputs are resolved` |
| underspecified Nature-style paper figure | `intake-design` scoping mode | no render/export until data, message, figure type, target context, and output format are resolved |
| Nature-style multi-panel model figure | `intake-design` | `intake-design -> model-performance -> multipanel-composer -> journal-style-translator -> caption-alttext -> figure-auditor -> export-packager` |
| observed vs predicted, residuals | `model-performance` | `model-performance -> multipanel-composer -> caption-alttext -> figure-auditor` |
| boxplot, violin, forest, ROC | `statistical-plots` | `statistical-plots -> caption-alttext -> figure-auditor` |
| clinical forest plot, Kaplan-Meier | `clinical-biomedical` | `clinical-biomedical -> journal-style-translator -> caption-alttext -> figure-auditor` |
| map, raster, CRS, flood extent | `geospatial-maps` | `geospatial-maps -> multipanel-composer -> export-packager` |
| volcano, heatmap, UMAP, enrichment | `omics-bioinformatics` | `omics-bioinformatics -> caption-alttext -> figure-auditor` |
| mechanism or workflow diagram | `schematic-mechanism` | `schematic-mechanism -> caption-alttext -> figure-auditor` |
| graphical abstract | `graphical-abstract` | `intake-design -> schematic-mechanism -> graphical-abstract -> journal-style-translator -> figure-auditor` |
| caption or alt text | `caption-alttext` | `caption-alttext -> figure-auditor` |
| audit or review | `figure-auditor` | `figure-auditor -> journal-style-translator if target journal is named` |
| export or package | `export-packager` | `export-packager` |
