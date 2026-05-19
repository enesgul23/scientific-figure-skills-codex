# Model Performance

## Purpose

Visualize AI, ML, statistical, hydrologic, biomedical, engineering, or forecasting model performance with error, calibration, uncertainty, domain shift, and interpretability.

## Trigger Conditions

Use for observed-vs-predicted plots, residual diagnostics, model comparison, confusion matrices, ROC/PR curves, reliability diagrams, SHAP plots, uncertainty intervals, ablation studies, and metric table-to-figure work.

## Required Inputs

- observations or ground-truth labels
- predictions or predicted probabilities
- model names
- metric definitions

## Optional Inputs

- train, validation, internal test, external test, or field-validation split
- cross-validation folds
- bootstrap or uncertainty samples
- target journal
- domain-specific metrics such as NSE, KGE, CCC, AUROC, AUPRC, or Brier score

## Output Contract

Produce a model-performance figure package that considers agreement, error structure, calibration or uncertainty, and generalization. Do not reduce the story to one success metric.

## Procedure

1. Check whether ground truth and held-out data are available.
2. Separate train, internal validation, external validation, and field validation when labels exist.
3. Select diagnostic panels: parity, residuals, metric intervals, calibration, uncertainty, confusion matrix, or domain coverage.
4. Use shared limits for comparable parity panels and include the 1:1 line.
5. Add tolerance bands only when the threshold is justified by the study.
6. Report metrics compactly and define them in caption or notes.
7. Flag unsupported claims such as "state of the art" or "external validation" when evidence is missing.

## Quality Gates

- train/test separation is clear
- residuals or error distribution are considered
- calibration or uncertainty is considered when probabilities or intervals exist
- shared limits are used for comparable panels
- overclaiming is avoided

## Failure Modes

- only training metrics are provided
- no ground truth is available
- model split definitions are missing
- metric formulas are ambiguous
- selected model was chosen using the same external data now claimed as independent

## Memory Integration

If project memory exists, read `shared/submission_memory_runtime.md` and
validate memory before generating model-performance visuals. Use dataset
registry split metadata and existing Figure Passport versions to detect stale
metrics or panels. After producing diagnostics, update panel-level passport
entries with split, metric, claim, data, code, output, and repro-lock refs.

## v0.6 Dependency Planning

Inspect prediction datasets before rendering. ROC/PR, calibration, and metric
figures should select `scikit-learn` only when metric computation is needed;
otherwise use the minimal pandas/numpy/matplotlib stack. External validation
or benchmark data must go through `fig-plan-external-data` and be flagged for
train/validation/test contamination risk.

## Agent Role References

- `agents/performance_diagnostic_agent.md` for model diagnostic panel selection.
- `agents/validation_split_agent.md` for train/test/external validation integrity.
- `agents/uncertainty_calibration_agent.md` for interval, coverage, and calibration checks.

## Handoff Rules

Hand off to `multipanel-composer` for multi-diagnostic layouts, `journal-style-translator` for target sizing, `caption-alttext` for text, and `figure-auditor` for validation.
