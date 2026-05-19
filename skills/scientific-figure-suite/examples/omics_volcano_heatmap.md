# Example: Omics Volcano And Heatmap

## User Request

```text
fig-full Create a volcano plot and clustered heatmap for differential expression between treatment and control.
```

## Required Inputs

- expression or differential-expression table
- group labels
- normalization method
- log fold-change threshold
- adjusted p-value/FDR threshold
- multiple-testing correction method
- selected genes for heatmap

## Expected Behavior

- Do not label too many genes.
- State normalization and FDR in caption.
- Do not turn pathway enrichment into mechanism proof.
