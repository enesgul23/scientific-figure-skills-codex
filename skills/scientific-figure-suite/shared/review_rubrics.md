# Review Rubrics

Use for figure quality reports and revision prioritization.

## Severity

| Severity | Meaning | Action |
|---|---|---|
| P0 Blocking | Figure is misleading, unsupported, or not reproducible for final use. | Must fix before final output. |
| P1 Major | Scientific interpretation or submission readiness is materially weakened. | Fix before submission. |
| P2 Moderate | Clarity, consistency, accessibility, or style issue. | Fix when practical. |
| P3 Minor | Cosmetic or small polish issue. | Optional. |

## Scores

Use 1-5 only when a score helps summarize an audit.

| Dimension | 1 | 3 | 5 |
|---|---|---|---|
| Evidence faithfulness | unsupported | partially supported | fully traceable |
| Statistical honesty | misleading | adequate caveats | transparent uncertainty |
| Visual clarity | confusing | readable | immediately interpretable |
| Multipanel layout | uneven boxes, crowding, collisions | mostly aligned with visible caveats | coherent optical grid with audited colorbars and labels |
| Accessibility | inaccessible | mostly usable | color/text/alt robust |
| Journal readiness | unverified and incomplete | estimated with gaps | verified or clearly packaged |
| Reproducibility | manual/untraceable | partial traceability | rerunnable package |

Do not average scores to hide a P0 issue.

Treat inconsistent semantic colors, uncontrolled station labels, and failed
colorbar spacing in a final multi-panel figure as at least P1 unless the figure
is explicitly draft-only.
