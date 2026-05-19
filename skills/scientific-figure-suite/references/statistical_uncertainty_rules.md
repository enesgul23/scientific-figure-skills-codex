# Statistical Uncertainty Rules

Use this reference when figures include intervals, statistical tests, model performance, or estimates.

## Interval Definitions

- `SD`: spread of observed values.
- `SE`: uncertainty in the estimated mean.
- `CI`: uncertainty interval for a parameter or effect estimate.
- `PI`: prediction interval for future or individual observations.
- `IQR`: middle 50 percent of observed values.
- `bootstrap_interval`: resampling-based uncertainty, requiring seed and method.

## Required Disclosures

- interval type
- confidence or coverage level
- sample size or denominator
- bootstrap seed and replicates when applicable
- whether uncertainty was estimated on train, validation, or test data
- whether intervals were calibrated independently

## Model Figures

- Pair aggregate metrics with residual or error distribution views.
- Do not claim calibration unless a calibration plot or calibration metric supports it.
- Do not claim uncertainty quality unless coverage is evaluated.
- Use identical axis limits for comparable observed-vs-predicted panels.

## Clinical Figures

- Use confidence intervals for effect estimates.
- Show censoring in survival curves when data are available.
- State denominators for risk, rate, adverse-event, and subgroup plots.

## Red Flags

- CI shown but N missing.
- Prediction intervals displayed without coverage assessment.
- External validation claimed without independent data.
- P-value stars dominate effect sizes.
