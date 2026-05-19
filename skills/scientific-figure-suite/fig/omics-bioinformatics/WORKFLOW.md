# Omics Bioinformatics

## Purpose

Create omics and bioinformatics figures such as volcano plots, clustered heatmaps, PCA/UMAP/t-SNE plots, enrichment bubble plots, pathway summaries, expression plots, and biomarker survival figures.

## Trigger Conditions

Use when the user mentions differential expression, gene sets, proteins, metabolites, pathways, enrichment, normalization, clustering, sample groups, volcano, heatmap, PCA, UMAP, or survival by biomarker group.

## Required Inputs

- expression table, count matrix, or summarized results
- group labels
- normalization method
- statistical thresholds
- multiple-testing correction method when inferential claims are made

## Optional Inputs

- gene or feature labels
- pathway database/version
- target journal
- batch-correction method
- color annotation tracks

## Output Contract

Produce omics figure code or specification, threshold notes, correction notes, caption, and visual claim ledger entries.

## Procedure

1. Identify data type: RNA-seq, proteomics, metabolomics, single-cell, pathway, or survival-linked biomarker.
2. Check normalization, filtering, and batch handling.
3. Check multiple-testing correction and threshold definitions.
4. Select visualization and limit labels to interpretable signals.
5. Include group, threshold, and database/version notes in caption.
6. Separate descriptive pathway enrichment from mechanistic proof.

## Quality Gates

- FDR or correction status is stated
- thresholds are stated
- sample groups are clear
- labels do not overcrowd the figure
- biological mechanisms are not invented

## Failure Modes

- missing correction for many tests
- too many labels
- pathway database/version omitted
- unsupported biological mechanism
- normalization method unavailable

## Memory Integration

If project memory exists, read `shared/submission_memory_runtime.md` and
validate memory before omics visualization. Use dataset registry metadata for
assay, contrast, threshold, and identifier fields. Update Figure Passport panels
and visual claim ledger entries for volcano, heatmap, pathway, enrichment, and
cluster claims.

## v0.6 Dependency Planning

Inspect AnnData, count matrices, or tabular omics data before render planning.
UMAP, dotplot, and single-cell figures should select `scanpy`/`anndata` only
when the data format and task require them. Pathway, ontology, gene-set, or
reference annotation data require `fig-plan-external-data` and complete
provenance before use.

## Agent Role References

- `agents/omics_threshold_agent.md` for normalization, FDR, threshold, and database checks.
- `agents/bioinformatics_visual_agent.md` for plot selection, labels, and annotation strategy.

## Handoff Rules

Hand off to `caption-alttext`, `figure-auditor`, and `export-packager`; use `schematic-mechanism` only for explicitly supported biological process diagrams.
