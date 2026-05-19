# Handoff Schemas

Cross-workflow artifact contracts. Producers must include required fields before
handoff. Consumers must request repair when required fields are missing.

## Validation Rule

If a required field is missing, return:

```text
HANDOFF_INCOMPLETE: [missing fields]
```

Do not proceed with a partial artifact unless the user explicitly asks for a
design-only or draft-only output and the status labels show the limitation.

## Schema 1: Figure Intake

Producer: `fig/intake-design/WORKFLOW.md`.

Consumers: all domain workflows.

Required fields:

| Field | Type | Meaning |
|---|---|---|
| `goal` | string | One-sentence scientific objective. |
| `target_journal` | object | `{name, article_type, style_status, guideline_source}`. |
| `data_status` | enum | `PROVIDED`, `INFERRED`, `MISSING`, or `MOCKUP`. |
| `style_status` | enum | `VERIFIED`, `ESTIMATED`, or `UNVERIFIED`. |
| `figure_type_candidates` | list | Candidate figure types and rationale. |
| `selected_workflow_chain` | list | Ordered workflow chain. |
| `missing_inputs` | list | Concrete blocker inputs. |
| `risk_flags` | list | Integrity, style, data, or domain risks. |

Example:

```yaml
figure_intake:
  goal: "Compare three flood-forecasting models across agreement, residuals, and uncertainty."
  target_journal:
    name: Nature
    article_type: research_article
    style_status: ESTIMATED
    guideline_source: stored_estimate
  data_status: MISSING
  style_status: ESTIMATED
  figure_type_candidates:
    - model_performance_multipanel
  selected_workflow_chain:
    - intake-design
    - model-performance
    - multipanel-composer
    - journal-style-translator
    - caption-alttext
    - figure-auditor
    - export-packager
  missing_inputs:
    - observed and predicted values by model and split
  risk_flags:
    - metrics must not be invented
```

## Schema 2: Figure Spec

Producer: domain workflows and `multipanel-composer`.

Consumers: `caption-alttext`, `figure-auditor`, `export-packager`.

Required fields:

| Field | Type | Meaning |
|---|---|---|
| `figure_id` | string | Stable identifier such as `figure_01`. |
| `figure_type` | string | Plot/layout family. |
| `data_status` | enum | Status from taxonomy. |
| `target_journal` | object | Includes `name`, `style_status`, `guideline_source`. |
| `panels` | list | Panel specs with ID, purpose, data source, and plot type. |
| `axes` | object | Axis labels and units when applicable. |
| `data_sources` | list | Data paths, table names, or user-provided summaries. |
| `code_sources` | list | Script paths or planned script names. |
| `style_profile` | object | Token/profile decisions or reference. |
| `export` | object | Formats and DPI. |

Panel object:

```yaml
id: a
title: "Observed vs predicted"
purpose: "Agreement diagnostic"
plot_type: parity_scatter
data_source: "predictions.csv"
claim_ids: [C1]
status: PLANNED | CODED | RENDERED | NEEDS_DATA
```

## Schema 3: Visual Claim Ledger

Producer: any evidence-bearing workflow.

Consumers: `caption-alttext`, `figure-auditor`.

Required fields:

| Field | Type | Meaning |
|---|---|---|
| `figure_id` | string | Figure identifier. |
| `data_status` | enum | Data status. |
| `claims` | list | Claim objects. |

Claim object required fields:

- `id`
- `claim_text`
- `claim_type`
- `visual_element`
- `data_source`
- `computation_source`
- `support_status`
- `uncertainty_shown`
- `caption_alignment`
- `risk_level`
- `required_fix` for unsupported, unverifiable, or high-risk claims

## Schema 4: Journal Style Report

Producer: `journal-style-translator`.

Consumers: `multipanel-composer`, `figure-auditor`, `export-packager`.

Required fields:

- `target`
- `guideline_source`
- `status`
- `checked_at`
- `applied_decisions`
- `unresolved_requirements`
- `allowed_language`
- `forbidden_language`
- `compliance_statement`

## Schema 5: Caption Package

Producer: `caption-alttext`.

Consumers: `figure-auditor`, `export-packager`.

Required fields:

- `figure_id`
- `caption_title`
- `caption_body`
- `panel_legend`
- `notes`
- `in_text_reference`
- `short_alt_text`
- `extended_alt_text`
- `claim_alignment_summary`
- `missing_details`

## Schema 6: Figure Quality Report

Producer: `figure-auditor`.

Consumers: `export-packager`, user.

Required fields:

- `figure_id`
- `target_journal`
- `style_status`
- `data_status`
- `gate_results`
- `blocking_issues`
- `required_fixes_before_submission`
- `optional_improvements`
- `overall_integrity_status`

## Schema 7: Submission Manifest

Producer: `export-packager`.

Consumer: final package.

Required fields:

- `figure_id`
- `created_at`
- `files`
- `data_sources`
- `code_sources`
- `style_status`
- `quality_report`
- `caption`
- `alt_text`
- `visual_claim_ledger`
- `environment_note`
- `unresolved_requirements`

## Schema 8: Figure Passport

Producer: any workflow that hands off a major artifact.

Consumer: every downstream workflow.

Purpose: preserve lineage and staleness.

Required fields:

- `artifact_id`
- `artifact_type`
- `version_label`
- `source_workflow`
- `source_agent`
- `created_at`
- `inputs_used`
- `status_tags`
- `stale_if_modified`

If source data, code, caption, style report, or claim ledger changes, downstream
audit and manifest artifacts become stale until reviewed again.

## Schema 9: Figure Memory Manifest

Producer: `fig-init-memory`, `fig-update-memory`, memory curator.

Consumer: every workflow that continues a project from memory.

Purpose: single source of truth for project-local memory state.

Required fields:

- `schema_version`
- `project_id`
- `memory_level`
- `created_at`
- `updated_at`
- `active_figure_id`
- `current_stage`
- `validation_status`
- `files`

## Schema 10: Figure Passport Inventory

Producer: memory curator and figure-producing workflows.

Consumer: memory load, resume, audit, export.

Required fields:

- `schema_version`
- `figures`

Each figure entry should include:

- `figure_id`
- `title`
- `purpose`
- `dataset_refs`
- `claim_refs`
- `current_version`
- `versions`
- `status_tags`

## Schema 11: Reset Boundary Entry

Producer: memory curator when a checkpoint or resume boundary is requested.

Consumer: `fig-resume-project`.

Required boundary fields:

- `kind: boundary`
- `hash`
- `hash_mode`
- `created_at`
- `figure_id`
- `completed_stage`
- `next_stage`
- `artifact_refs`
- `verification_status`

Required resume fields:

- `kind: resume`
- `created_at`
- `consumes_hash`
- `next_stage`

Boundary and resume entries live in `revision_boundary_ledger.jsonl` and are
append-only.

## Schema 12: Figure Set Manifest

Producer: `fig-build-figure-set`.

Consumer: `fig-audit-figure-set`, `fig-audit-readiness`, `export-packager`.

Required fields:

- `schema_version`
- `project_id`
- `created_at`
- `updated_at`
- `figures`
- `style_consistency_status`
- `readiness_status`

## Schema 13: Submission Package Index

Producer: `fig-build-submission-package`.

Consumer: `fig-audit-readiness`.

Required fields:

- `schema_version`
- `project_id`
- `created_at`
- `updated_at`
- `files`
- `index_status`

Each file entry should include `path`, `sha256`, `byte_size`, `role`, and
`figure_id` when applicable.

## Schema 14: Submission Readiness Report

Producer: `fig-audit-readiness`.

Consumer: user and final package.

Required fields:

- `created_at`
- `project_id`
- `result`
- `gate_results`
- `blockers`
- `warnings`

`READY` means all required gates passed. `READY_WITH_WARNINGS` means no blockers
remain but warnings are visible. `BLOCKED` means the package must not be called
submission-ready.

## Schema 15: Pipeline Dashboard

Producer: `fig-status`.

Consumer: user, memory curator, full-package workflow.

Required fields:

- `created_at`
- `project_id`
- `active_stage`
- `completed_stages`
- `blocked_stages`
- `last_artifacts`
- `blockers`
- `warnings`
- `next_actions`
- `readiness_summary`

The dashboard is a state summary, not a substitute for the underlying ledgers.

## Schema 16: Style Token

Producer: bundled style token profiles or `fig-style`.

Consumer: renderer registry, journal-style translator, auditor.

Required fields:

- `profile_name`
- `status`
- `requires_live_verification`
- `font`
- `accessibility`
- `export`

Stored estimated journal profiles must not be marked `VERIFIED` unless current
official or user-provided guidance is checked in the active task.

## Schema 17: Visual Regression Report

Producer: `fig-audit-render`.

Consumer: `fig-audit-readiness`, user, export-packager.

Required fields:

- `created_at`
- `figure_id`
- `result`
- `files`
- `blockers`
- `warnings`

This report checks render quality and file sanity. It does not verify scientific
truth, statistical correctness, or journal compliance by itself.

## Schema 18: Library Pool Entry

Producer: bundled library metadata.

Consumer: dependency planner and render stack selector.

Required fields:

- `library_id`
- `package_name`
- `import_names`
- `pip_name`
- `conda_name`
- `category`
- `domains`
- `chart_families`
- `data_formats`
- `output_formats`
- `capabilities`
- `limitations`
- `publication_grade`
- `install_risk`
- `system_dependencies`
- `selection_priority`
- `fallbacks`
- `import_probe`

The library pool is metadata only. It must never imply that all listed
libraries should be installed.

## Schema 19: Dependency Plan

Producer: `fig-plan-libraries` or `fig-select-render-stack`.

Consumer: `fig-render-template`, memory curator, user.

Required fields:

- `created_at`
- `selected_stack`
- `required_libraries`
- `recommended_libraries`
- `optional_libraries`
- `blocked_libraries`
- `install_commands`
- `import_checks`
- `selection_rationale`
- `fallback_renderer`
- `reproducibility_notes`

Install commands are advisory only. They must not be executed unless the user
explicitly asks for installation.

## Schema 20: Data Acquisition Plan

Producer: `fig-plan-external-data`.

Consumer: user, dataset registry, memory curator.

Required fields:

- `created_at`
- `decision`
- `approval_required`
- `download_allowed`
- `items`
- `risks`
- `blockers`

Each item must classify the external data role as `contextual`, `evidentiary`,
`benchmark`, or `annotation`. Missing source, license, or citation blocks use.

## Schema 21: Multipanel Layout Audit

Producer: `fig-audit-multipanel-layout`.

Consumer: `figure-auditor`, `fig-audit-readiness`, user.

Required fields:

- `created_at`
- `layout_name`
- `result`
- `layout_engine`
- `panel_count`
- `colorbar_count`
- `checks`
- `blockers`
- `warnings`

The audit must explicitly cover panel-box geometry, same-row top/bottom
alignment, colorbar layout control, semantic color consistency, controlled
map/scatter direct labels, and manual fallback for poor automatic layout.
