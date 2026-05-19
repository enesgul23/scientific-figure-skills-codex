# Model Performance Figure Package

## Required Data

- observed values or labels
- predictions or probabilities
- model names
- split labels
- metric definitions

## Recommended Panels

| Panel | Purpose | Required data |
|---|---|---|
| a | Observed vs predicted parity | observed, predicted, model, split |
| b | Residual diagnostics | observed, predicted |
| c | Metric comparison | model, split, metric value, uncertainty |
| d | Calibration or uncertainty | probabilities/intervals and outcomes |

## Required Checks

- train/test/external split integrity
- shared parity limits
- metric definitions
- uncertainty/calibration status
- unsupported SOTA or external-validation claims
