# Omics Figure Rules

Use this reference for omics and bioinformatics plots.

## Required Metadata

- assay or data type
- normalization method
- filtering criteria
- group labels
- statistical model or test
- multiple-testing correction
- thresholds for fold change, FDR, expression, enrichment, or loading
- database and version for pathway/enrichment analysis

## Figure Rules

- Volcano plots need fold-change axis, significance axis, thresholds, and FDR status.
- Heatmaps need row/column scaling status and annotation tracks.
- PCA/UMAP/t-SNE plots need input features and preprocessing.
- Enrichment bubble plots need gene ratio, adjusted p-value, term source, and database version.
- Cluster labels should not imply biology unless supported.

## Red Flags

- no multiple-testing correction
- too many labels
- pathway claims treated as mechanisms
- batch correction omitted when relevant
- dimensionality reduction shown without preprocessing details
