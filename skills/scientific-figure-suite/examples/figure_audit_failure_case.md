# Example: Figure Audit Failure Case

## Input

Caption says: "Model A proves groundwater coupling causes superior flood forecasts across all basins."

Figure materials:

- parity scatter only
- no residuals
- no split description
- no basin-level error table
- no causal experiment

## Expected Audit Findings

- `UNSUPPORTED_CLAIM`: causal mechanism not supported.
- `MISSING_METADATA`: validation split missing.
- `STATISTICAL_HONESTY`: "across all basins" not supported without basin-level evidence.
- Required fix: rephrase as association or provide causal/domain evidence.
