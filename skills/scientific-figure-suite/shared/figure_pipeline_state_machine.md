# Figure Pipeline State Machine

Use for `fig-full` and other staged figure-package requests.

## Stages

| Stage | Name | Primary workflow | Deliverable |
|---|---|---|---|
| 0 | INTAKE | `intake-design` | Figure intake |
| 1 | DOMAIN DESIGN | domain workflow | Figure spec and claim draft |
| 2 | COMPOSITION | `multipanel-composer` | Layout spec |
| 3 | STYLE | `journal-style-translator` | Journal style report |
| 4 | TEXT | `caption-alttext` plus Text Layout Intelligence Runtime | Caption, alt text, text layout report |
| 5 | AUDIT | `figure-auditor` | Quality report |
| 6 | EXPORT | `export-packager` | Submission manifest and files/commands |
| 7 | READINESS | `figure-auditor` plus submission runtime | Readiness decision |

## Transitions

```text
INTAKE -> DOMAIN DESIGN -> COMPOSITION -> STYLE -> TEXT -> AUDIT -> EXPORT -> READINESS
```

Skip `COMPOSITION` only for single-panel figures. Skip `STYLE` only when no
target style or export constraint matters. Do not skip `AUDIT` for final
packages.

## Checkpoints

- After `INTAKE`: confirm missing inputs or mockup status.
- Before `AUDIT`: confirm the figure spec, caption, style report, claim ledger,
  and text layout report exist when text layout artifacts are available.
- Before `EXPORT`: require `PASS` or `PASS_WITH_WARNINGS`; list unresolved warnings.
- Before `READINESS`: run agentic planning if the user asks for next-step
  orchestration instead of immediate packaging.

## Recovery

- If `AUDIT` fails on data or claims, return to the domain workflow.
- If `AUDIT` fails on style language, return to `journal-style-translator`.
- If `AUDIT` fails on caption, return to `caption-alttext`.
- If `AUDIT` fails on text overlap, clipping, or terminology, return to
  `fig-repair-text-layout` and rerun `fig-audit-text-layout`.
- If `EXPORT` fails, return to `export-packager` after fixing file paths or formats.
- If agentic planning finds a failed text, layout, render, dependency, or
  external-data gate, follow the selected dry-run next action before readiness.

## Agentic Mapping

`fig-agent-plan` uses a finer runbook order:

```text
INTAKE -> DATASET_INSPECTION -> DEPENDENCY_PLANNING -> RENDER_STACK_SELECTION -> RENDER -> MULTIPANEL_LAYOUT_AUDIT -> TEXT_LAYOUT_AUDIT -> RENDER_QUALITY_AUDIT -> STYLE_STATUS -> CAPTION_ALT_TEXT -> FIGURE_SET -> SUBMISSION_PACKAGE -> READINESS
```

This mapping is a planning surface. It must not install packages, download
data, push changes, or claim verified journal compliance automatically.
