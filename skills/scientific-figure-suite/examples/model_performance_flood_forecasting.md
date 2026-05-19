# Example: Model Performance Flood Forecasting

## User Request

```text
fig-model-performance Compare three AI flood forecasting models using NSE, KGE, RMSE, observed-vs-predicted plots, residuals, and uncertainty intervals. I have not uploaded raw data yet.
```

## Expected Routing

```text
model-performance -> multipanel-composer -> journal-style-translator -> caption-alttext -> figure-auditor
```

## Expected Status

```text
DATA_STATUS: MISSING
STYLE_STATUS: ESTIMATED or UNVERIFIED
REPRODUCIBILITY_STATUS: DESIGN_ONLY
EXPORT_STATUS: NEEDS_RENDER
INTEGRITY_STATUS: PASS_WITH_WARNINGS
```

## Expected Behavior

- Do not invent NSE, KGE, RMSE, observed values, predictions, or intervals.
- Ask for prediction table with observed, predicted, model, split, timestamp/site, and uncertainty bounds if available.
- Recommend parity, residual, metric interval, and uncertainty/calibration panels.
