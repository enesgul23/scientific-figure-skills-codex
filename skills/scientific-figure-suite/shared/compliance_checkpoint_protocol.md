# Compliance Checkpoint Protocol

Use this before final packaging or when the user asks for journal/submission readiness.

## Checkpoint Inputs

- figure spec
- visual claim ledger
- caption package
- journal style report
- quality report
- export manifest or file list
- data/code provenance

## Compliance Dimensions

| Dimension | Required evidence |
|---|---|
| Data transparency | data source or design-only label |
| Claim transparency | visual claim ledger |
| Statistical transparency | N, uncertainty, metric definitions, corrections |
| Accessibility | alt text, color and text checks |
| Journal status | verified/estimated/unverified source |
| Reproducibility | code/data/output manifest |
| AI disclosure | design-only or AI-assisted illustrative elements labeled when relevant |

## Decisions

- `pass`: all required evidence present.
- `warn`: unresolved items exist but are visible.
- `block`: final/submission-ready claim would be misleading.

## Override

The user may choose to proceed with warnings, but the suite must preserve the warning in the manifest or quality report.
