# Statistical Graph Grammar

Use this reference for quantitative result figures.

## Chart Selection

- Use dot, strip, box, violin, or interval plots when distributions matter.
- Use bars mainly for totals, proportions, or simple categorical summaries.
- Use line charts for ordered time, dose, depth, or sequence.
- Use scatter plots for relationships between continuous variables.
- Use forest plots for effect estimates with confidence intervals.
- Use calibration plots for probabilistic prediction or model calibration.
- Use Bland-Altman plots for method agreement.
- Use ROC/PR curves for classification, with AUC only as a summary.

## Required Labels

- x and y variables
- units for dimensional values
- sample size or denominator when inference is made
- uncertainty definition: SD, SE, CI, IQR, percentile interval, bootstrap interval
- group or split labels

## Avoid

- p-value-only storytelling
- hiding raw data behind bars when N is small or distribution matters
- dual y-axis without strong justification
- truncated axes without disclosure
- comparing groups with inconsistent scales
- using 3D chart effects for 2D data

## Statistical Honesty Flags

- Multiple comparisons require correction or explicit exploratory status.
- Log scales require visible labels.
- Outlier removal requires a transparent rule.
- Error bars must be defined in caption or legend.
- If sample size differs by group, show or state it.
