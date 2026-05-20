# Agentic Orchestration Protocol

Version: 0.9.0

Use this protocol when a figure project needs the next safe action rather than a
single command recipe.

## Runtime Rules

- Build a runbook before executing multi-stage work.
- Default to dry-run and report the selected next action.
- Execute only whitelisted suite scripts when `--execute` is explicit.
- Never install packages, download external data, delete project files, push to
  GitHub, or claim verified journal compliance automatically.
- Use project-local memory only; do not write project memory into the installed
  skill directory.

## Artifacts

- `agentic_runbook.json`: ordered stages, evidence, guardrails, next action.
- `agentic_run_report.json`: selected action, dry-run/execution status, output.
- `agentic_task_queue.jsonl`: optional append-style task queue.
- `agentic_run_history.jsonl`: optional append-style run history.

## Stage Order

```text
INTAKE
DATASET_INSPECTION
DEPENDENCY_PLANNING
RENDER_STACK_SELECTION
RENDER
MULTIPANEL_LAYOUT_AUDIT
TEXT_LAYOUT_AUDIT
RENDER_QUALITY_AUDIT
STYLE_STATUS
CAPTION_ALT_TEXT
FIGURE_SET
SUBMISSION_PACKAGE
READINESS
```

Failed text, multipanel, render-quality, dependency, external-data, stale
repro-lock, and journal-status gates must surface as the next actionable repair
or approval-gated step.
