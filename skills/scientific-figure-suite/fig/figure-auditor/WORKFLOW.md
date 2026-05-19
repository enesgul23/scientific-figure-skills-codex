# Figure Auditor

## Purpose

Audit scientific figures for data accuracy, chart appropriateness, statistical honesty, accessibility, journal style status, caption integrity, reproducibility, export readiness, render quality, and image integrity.

## Trigger Conditions

Use when the user asks to audit, check, review, validate, quality-control, prepare for submission, inspect journal compliance, or evaluate visual integrity.

## Required Inputs

- figure image, figure specification, or figure code
- caption or intended claim
- target journal if any

## Optional Inputs

- data source
- visual claim ledger
- style profile
- article type
- export files
- baseline render files for visual regression checks

## Output Contract

Produce `figure_quality_report.md`:

```markdown
# Figure Quality Report

Figure ID:
Target journal:
Style status:
Data status:

## Gate Results
| Gate | Result | Notes |
|---|---|---|

## Required fixes before submission
## Optional improvements
```

## Procedure

1. Check data provenance and reproducibility.
2. Check visual claim ledger alignment.
3. Check chart appropriateness and statistical honesty.
4. Check axes, units, scales, legends, colorbars, and panel labels.
5. Check accessibility: color, contrast, minimum text size, redundancy, alt text.
6. Check journal style status without claiming unverified compliance.
7. Check export readiness.
8. Check render-quality evidence for blank outputs, dimensions, expected formats, and SVG text/title presence when exported files are supplied.
9. Check image integrity for microscopy, gel/blot, radiology, or other scientific images when applicable.

## Quality Gates

- mandatory gates are run
- result labels are `PASS`, `PASS_WITH_WARNINGS`, or `FAIL`
- failure reasons are actionable
- praise is not used as a substitute for evidence
- unresolved verification gaps are visible

## Failure Modes

- image is provided without data, code, or provenance
- journal rules are unverifiable
- caption overclaims
- figure relies on manual edits that cannot be reproduced
- raw image manipulation cannot be assessed from supplied files

## Memory Integration

If project memory exists, read `shared/submission_memory_runtime.md` and
validate memory before audit. Run repro-lock stale checks when Figure Passport
entries include stored hashes. Append quality gate results to
`quality_audit_history.jsonl`, file-level audit artifacts to
`visual_audit_artifact.jsonl`, and render-quality reports to
`visual_regression_history.jsonl` for checked outputs.

## Agent Role References

- `agents/visual_integrity_reviewer_agent.md` for visual claims and image integrity.
- `agents/statistical_reviewer_agent.md` for quantitative, model, and inference checks.
- `agents/accessibility_reviewer_agent.md` for color, contrast, text, redundancy, and alt text.

## Handoff Rules

Hand off to `caption-alttext` when text needs repair and to `export-packager` after `PASS` or `PASS_WITH_WARNINGS`.
