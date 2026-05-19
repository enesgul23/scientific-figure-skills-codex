# Figure Pipeline State Machine

Use for `fig-full` and other staged figure-package requests.

## Stages

| Stage | Name | Primary workflow | Deliverable |
|---|---|---|---|
| 0 | INTAKE | `intake-design` | Figure intake |
| 1 | DOMAIN DESIGN | domain workflow | Figure spec and claim draft |
| 2 | COMPOSITION | `multipanel-composer` | Layout spec |
| 3 | STYLE | `journal-style-translator` | Journal style report |
| 4 | TEXT | `caption-alttext` | Caption and alt text |
| 5 | AUDIT | `figure-auditor` | Quality report |
| 6 | EXPORT | `export-packager` | Submission manifest and files/commands |

## Transitions

```text
INTAKE -> DOMAIN DESIGN -> COMPOSITION -> STYLE -> TEXT -> AUDIT -> EXPORT
```

Skip `COMPOSITION` only for single-panel figures. Skip `STYLE` only when no
target style or export constraint matters. Do not skip `AUDIT` for final
packages.

## Checkpoints

- After `INTAKE`: confirm missing inputs or mockup status.
- Before `AUDIT`: confirm the figure spec, caption, style report, and claim ledger exist.
- Before `EXPORT`: require `PASS` or `PASS_WITH_WARNINGS`; list unresolved warnings.

## Recovery

- If `AUDIT` fails on data or claims, return to the domain workflow.
- If `AUDIT` fails on style language, return to `journal-style-translator`.
- If `AUDIT` fails on caption, return to `caption-alttext`.
- If `EXPORT` fails, return to `export-packager` after fixing file paths or formats.
