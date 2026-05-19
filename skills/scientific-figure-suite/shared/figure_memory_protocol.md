# Figure Memory Protocol

## Purpose

Defines project-local memory for scientific figure work. This is not Codex
personal memory. It is an auditable file layer that lets a long figure project
carry project profile, journal targets, figure passports, dataset metadata,
visual claims, audit history, and reset/resume state across sessions.
v0.6 also carries pipeline-state, figure decisions, render-quality history,
dependency planning history, and external-data planning history.

## Storage Boundary

Default project-local location:

```text
.codex/scientific-figure-memory/
```

Do not write user-specific or project-specific memory inside the installed skill
directory. The installed skill contains protocols, schemas, templates, and
scripts only.

## Memory Levels

| Level | Intended use | Required files |
|---|---|---|
| Lightweight | Early planning or a single figure | `project_profile.json`, `journal_targets.json`, `figure_passport.json` |
| Research-grade | Manuscript figure set | lightweight files plus `visual_claim_ledger.jsonl`, `dataset_registry.json`, `quality_audit_history.jsonl`, `memory_manifest.json` |
| Submission-grade | Journal submission preparation | research-grade files plus `revision_boundary_ledger.jsonl`, `journal_guideline_verification.jsonl`, `visual_audit_artifact.jsonl`, `figure_decision_log.jsonl`, `visual_regression_history.jsonl`, `dependency_plan_history.jsonl`, `external_data_plan_history.jsonl`, `author_visual_style_profile.json`, current guideline verification records |

Default to research-grade memory when the user asks to initialize figure memory.

## Canonical Files

| File | Role |
|---|---|
| `memory_manifest.json` | Single source of truth for memory version, active figure, pipeline state, validation state, and last update. |
| `project_profile.json` | Project identity, scientific field, visual goals, export defaults, and accessibility policy. |
| `journal_targets.json` | Target journal profiles, status, source, unresolved requirements, and verification dates. |
| `figure_passport.json` | Inventory of figures, versions, output files, scripts, status tags, and current version pointers. |
| `visual_claim_ledger.jsonl` | Append-style mapping from visual claims to data, encodings, figures, and support status. |
| `dataset_registry.json` | Dataset paths, column meanings, units, preprocessing notes, and validation timestamps. |
| `quality_audit_history.jsonl` | Append-style quality gate, accessibility, journal, export, and integrity results. |
| `revision_boundary_ledger.jsonl` | Hash-linked reset/resume entries for long projects. |
| `journal_guideline_verification.jsonl` | Append-style evidence ledger for current target-journal figure guidance checks. |
| `visual_audit_artifact.jsonl` | Append-style file-level audit evidence with hashes, format, size, and dimensions when available. |
| `figure_decision_log.jsonl` | Append-style scoping, waiver, design-only, mockup, and user-approved style decisions. |
| `visual_regression_history.jsonl` | Append-style render-quality and visual regression audit reports. |
| `dependency_plan_history.jsonl` | Append-style library-stack and dependency planning decisions. |
| `external_data_plan_history.jsonl` | Append-style external data decisions, provenance gaps, and approval gates. |
| `author_visual_style_profile.json` | Optional author or lab visual style preferences from user-approved samples. |

## Write Rules

1. Initialize only missing files unless the user explicitly asks to force or
   reset memory.
2. Update JSON files deterministically with stable keys and timestamps.
3. Append to JSONL ledgers for claims, audit history, and reset/resume events.
4. Do not delete or rewrite ledger history except under an explicit
   `fig-forget-memory` request.
5. Preserve unresolved requirements. Do not convert `ESTIMATED` or
   `UNVERIFIED` journal targets into `VERIFIED` without current official or
   user-provided guidelines.
6. Do not treat memory as evidence. Values stored in memory still need source
   files, generated code, or user-provided records when a figure claim is made.
7. Never import another project's memory without explicit user direction.
8. Mark figure or panel entries stale when repro-lock hashes drift.
9. Do not mark journal targets `VERIFIED` without a matching journal guideline
   verification ledger entry from `live_official` or `user_provided` source.

## Command Lifecycle

| Alias | Behavior |
|---|---|
| `fig-init-memory` | Create project-local memory files from templates. Do not overwrite existing files unless explicitly forced. |
| `fig-load-memory` | Read memory summary, active figure, journal status, and unresolved requirements before figure work. |
| `fig-update-memory` | Update the Figure Passport and append claim, dataset, audit, or boundary entries after figure changes. |
| `fig-summarize-memory` | Produce a compact dashboard: project, active figure, figures, datasets, journals, audits, open risks. |
| `fig-validate-memory` | Run structural checks for required files, valid statuses, JSON/JSONL parseability, and journal verification status. |
| `fig-forget-memory` | Redact or remove selected memory only after explicit user confirmation. |
| `fig-resume-project` | Verify a reset boundary hash and continue from the Figure Passport. |
| `fig-status` | Build the pipeline dashboard from project-local memory and update `memory_manifest.pipeline_state`. |
| `fig-plan-libraries` | Inspect data and plan the minimal library stack without installing packages. |
| `fig-plan-external-data` | Decide whether external data are justified and provenance-complete without downloading data. |

## Memory Load Checklist

When loading memory, report:

- memory directory path
- project id and field
- active figure, if any
- target journals and style statuses
- figure inventory and current versions
- dataset registry count and missing paths, if checked
- unresolved journal or data requirements
- latest quality audit status
- whether any reset boundary awaits resume
- stale figure or panel entries
- latest journal guideline verification status
- latest visual regression/render-quality status
- latest dependency plan status
- latest external data plan and approval blockers
- next actions from `memory_manifest.pipeline_state`

## Status Discipline

Use suite status values exactly:

```text
DATA_STATUS: PROVIDED / INFERRED / MISSING / MOCKUP
STYLE_STATUS: VERIFIED / ESTIMATED / UNVERIFIED
REPRODUCIBILITY_STATUS: CODED / DESIGN_ONLY / PARTIAL
INTEGRITY_STATUS: PASS / PASS_WITH_WARNINGS / FAIL
```

If memory conflicts with current files, current files win and memory must be
updated or marked stale.

## Privacy Boundary

Author visual style, lab preferences, journal choices, and dataset paths may be
private. Store them only in project-local memory. Do not include them in
examples, templates, shared protocols, or the installed skill package.
