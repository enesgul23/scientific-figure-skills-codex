# Failure Recovery Protocol

Use this when a workflow cannot proceed or a quality gate fails.

## Failure Classes

| Code | Meaning | Handling |
|---|---|---|
| `MISSING_DATA` | Required data or result table absent | Ask for specific data or switch to `NON_DATA_MOCKUP`. |
| `MISSING_METADATA` | Units, N, endpoint, CRS, thresholds, or split labels absent | Ask targeted questions. |
| `UNVERIFIED_STYLE` | Journal compliance requested but guidelines unavailable | Mark `ESTIMATED` or `UNVERIFIED`; request guidelines for `VERIFIED`. |
| `UNSUPPORTED_CLAIM` | Caption or visual element exceeds evidence | Remove, soften, or request evidence. |
| `REPRODUCIBILITY_GAP` | Code/data/output traceability incomplete | Request files or mark design-only. |
| `EXPORT_BLOCKED` | Cannot render or requested format unsupported | Provide exact fix or alternative format. |

## Response Pattern

```markdown
Status: FAIL / PASS_WITH_WARNINGS
Blocking issue:
Required fix:
Safe fallback:
Next workflow:
```

## No Silent Downgrades

If a final figure cannot be produced, do not quietly provide a final-looking
figure. Label it as design-only, draft, or mockup.
