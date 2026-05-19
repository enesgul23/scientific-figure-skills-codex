# Intake Design

## Purpose

Turn vague scientific figure requests into a structured, auditable figure production plan.

## Trigger Conditions

Use when data availability, scientific message, figure type, target journal, article type, or output format is unclear.
Use scoping mode when the user asks for a journal-style or paper figure but
does not provide enough information to render.

## Required Inputs

- user goal
- available data or explicit data absence
- target audience or manuscript context

## Optional Inputs

- target journal or publisher
- article type
- figure count
- preferred language
- preferred plotting environment
- target export formats

## Output Contract

Produce `figure_intake.yaml`:

```yaml
figure_intake:
  goal:
  target_journal:
  target_article_type:
  data_status: PROVIDED | INFERRED | MISSING | MOCKUP
  style_status: VERIFIED | ESTIMATED | UNVERIFIED
  figure_type_candidates: []
  selected_workflow_chain: []
  missing_inputs: []
  risk_flags: []
```

## Procedure

1. Classify the task as plot creation, layout, graphical abstract, caption, audit, or export.
2. Identify whether the user supplied raw data, summarized results, only a concept, or no data.
3. Identify target journal status: user-provided current guidance, official guidance available in task, stored estimate, or unavailable.
4. Select one primary workflow and any downstream workflows.
5. Ask no more than five missing-input questions when rendering cannot proceed.
6. If the user asks only for planning, produce the structured plan without writing figure code.
7. In scoping mode, do not render or export files; produce `figure_intake` and
   concrete next inputs only.

## Quality Gates

- data status is explicit
- style status is explicit
- no unsupported numeric, biological, clinical, or cartographic assumptions
- workflow chain is justified
- missing inputs are concrete and minimal
- supplied datasets are marked for inspection before render planning
- possible external data needs are routed to the external data decision gate

## Failure Modes

- user asks for final data figure but no data are available
- target journal is named but current guidance is not supplied or verified
- figure goal combines incompatible messages
- user asks for compliance language that cannot be supported

## Memory Integration

If project memory exists or the user asks to continue a figure project, read
`shared/submission_memory_runtime.md` and `shared/figure_memory_protocol.md`.
Load and validate `.codex/scientific-figure-memory/` before planning. Reuse
project profile, target journals, active figure, dataset registry, unresolved
requirements, and author visual style only as soft context. After intake,
update `memory_manifest.json` with the active stage and record whether a Figure
Passport entry should be created.

## v0.6 Dependency Planning

When a dataset is supplied during intake, record whether it should be inspected
with `scripts/inspect_dataset.py`. If a chart type is selected, plan the
minimal Python stack with `fig-plan-libraries` or `fig-select-render-stack`
before registry rendering. Do not install packages during intake.

## Agent Role References

- `agents/figure_intake_agent.md` for structured intake and workflow-chain selection.
- `agents/scientific_message_agent.md` for claim/message clarification.

## Handoff Rules

Route to the selected domain workflow. For journal-ready outputs, include `journal-style-translator`, `caption-alttext`, `figure-auditor`, and `export-packager` after the domain workflow.
