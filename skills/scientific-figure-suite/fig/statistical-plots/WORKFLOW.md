# Statistical Plots

## Purpose

Generate and audit statistical plots for scientific manuscripts, reports, and reproducible analysis packages.

## Trigger Conditions

Use for group comparisons, distributions, time series, p-values, effect sizes, confidence intervals, forest plots, funnel plots, Kaplan-Meier curves, ROC/PR curves, calibration plots, Bland-Altman plots, and quantitative result figures.

## Required Inputs

- data table or result summary
- variable names and units
- grouping or comparison goal
- sample sizes when inference is shown

## Optional Inputs

- target journal
- preferred plot type
- Python or R preference
- uncertainty method
- statistical test or model output

## Output Contract

Produce figure code or a figure specification, caption notes, uncertainty statement, visual claim ledger entries, and quality-gate results.

## Procedure

1. Determine variable types: continuous, categorical, ordinal, time, censored, paired, repeated, or binary.
2. Select a chart type that preserves the relevant distribution and comparison.
3. Prefer dot, box, violin, ridge, or interval plots over bar charts when distributions matter.
4. Show uncertainty or explain why uncertainty is not available.
5. Label axes, units, sample sizes, and error-bar definitions.
6. Generate deterministic plotting code when data are supplied.
7. For repeated groups across panels, preserve the same semantic color mapping.
8. Use direct point labels only as a controlled, collision-checked subset.
9. Create caption language that matches only visible evidence.

## Quality Gates

- uncertainty is shown or explicitly unavailable
- sample size is visible or stated when inference is made
- axis labels and units are present
- chart type matches the scientific question
- no misleading truncation, dual-axis use, or p-value-only conclusion
- repeated groups or categories keep the same colors across panels
- direct scatter labels are sparse, controlled, and collision-checked

## Failure Modes

- N is missing
- effect size is absent but p-values are emphasized
- bar chart hides a meaningful distribution
- multiple comparisons lack correction
- log scale or truncation is unlabeled
- direct labels obscure points or imply unsupported salience

## Memory Integration

If project memory exists, read `shared/submission_memory_runtime.md` and
validate memory before plotting. Use dataset registry columns, units, and
active Figure Passport context to avoid repeated intake. After producing a plot
spec or output, update the Figure Passport with figure/panel ids, claim refs,
data refs, code refs, output refs, status tags, and repro-lock when files exist.

## v0.6 Dependency Planning

If the user supplies a dataset, inspect it before selecting the final chart
script. Use `fig-select-render-stack` for selected chart types and keep final
manuscript exports on a static matplotlib-based stack unless the user asks for
interactive exploration. Use `fig-plan-external-data` only when external
benchmark or annotation data are scientifically justified.

## Agent Role References

- `agents/chart_selection_agent.md` for chart choice and rejected-plot rationale.
- `agents/statistical_honesty_agent.md` for uncertainty, sample-size, scale, and inference checks.

## Handoff Rules

Hand off to `multipanel-composer` for combined figures, `caption-alttext` for text, `figure-auditor` for review, and `export-packager` for final files.
