# Reproducibility Protocol

Use this protocol for coded figures, export packages, and audit reports.

## Required Traceability

For data-derived figures, record:

- figure ID
- data sources
- code sources
- generated output files
- style profile/status
- visual claim ledger
- caption and alt text files
- quality report
- environment note or dependency hint

## Path Rules

- Prefer repository-relative paths.
- Do not embed local user directories in released artifacts.
- Fail loudly when required data are missing.
- Do not silently fall back to old files.

## Design-Only Exception

If data are absent, the package may be `DESIGN_ONLY` or `NON_DATA_MOCKUP`.
Do not present it as evidence-derived or submission-ready.

## Freshness

If data, code, caption, or claim ledger changes after audit, downstream quality
reports and manifests should be treated as stale until regenerated or reviewed.
