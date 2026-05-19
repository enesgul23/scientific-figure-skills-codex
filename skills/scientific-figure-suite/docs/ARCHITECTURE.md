# Architecture

## Package Shape

```text
scientific-figure-suite/
  SKILL.md
  MODE_REGISTRY.md
  POSITIONING.md
  fig/*/WORKFLOW.md
  fig/*/agents/*.md
  shared/
  shared/agents/
  shared/contracts/
  commands/
  references/
  templates/
  examples/
  scripts/
  tests/
```

Project-local runtime memory, when initialized, lives outside this package:

```text
project-root/
  .codex/scientific-figure-memory/
    memory_manifest.json
    project_profile.json
    journal_targets.json
    figure_passport.json
    figure_set_manifest.json
    submission_package_index.json
    visual_claim_ledger.jsonl
    dataset_registry.json
    quality_audit_history.jsonl
    revision_boundary_ledger.jsonl
    journal_guideline_verification.jsonl
    visual_audit_artifact.jsonl
    cross_figure_consistency_history.jsonl
    submission_readiness_history.jsonl
    figure_decision_log.jsonl
    visual_regression_history.jsonl
    dependency_plan_history.jsonl
    external_data_plan_history.jsonl
    author_visual_style_profile.json
```

## Runtime Flow

1. `SKILL.md` routes by intent or command alias.
2. The selected `WORKFLOW.md` defines phase procedure.
3. Workflow-specific `agents/*.md` files act as scoped role prompts.
4. `shared/handoff_schemas.md` and `shared/contracts/*.schema.json` define artifact shape.
5. `shared/figure_memory_protocol.md` governs project-local Figure Passport memory.
6. `shared/submission_memory_runtime.md` binds memory to workflow entry, panel passports, repro-lock, visual audit artifacts, and journal verification ledgers.
7. `shared/figure_set_submission_runtime.md` aggregates figures into a figure set, package index, consistency report, and readiness decision.
8. `assets/library_pool/library_pool.json` defines Python plotting and data library metadata without installing anything.
9. `scripts/inspect_dataset.py`, `scripts/probe_python_environment.py`, and `scripts/build_dependency_plan.py` choose a minimal render stack.
10. `shared/external_data_decision_protocol.md` and `scripts/plan_external_data.py` decide whether external data are scientifically justified.
11. `assets/render_registry/render_registry.json` maps chart types to reusable renderer templates, expected columns, and dependencies.
12. `scripts/audit_render_quality.py` records visual regression and render-quality evidence.
13. `scripts/build_pipeline_dashboard.py` summarizes active stage, blockers, latest artifacts, and next actions.
14. `figure-auditor` and shared compliance checks gate final packaging.
15. `export-packager` creates or describes files and manifest.

## Library Intelligence Runtime

v0.6.0 is Python-first. The suite plans a minimal stack from four inputs:

- dataset inspection
- requested chart type or figure intent
- render registry dependency metadata
- optional environment probe results

The runtime emits `dependency_plan.json`; it does not install packages. Heavy
geospatial, omics, survival, graph, 3D, or image packages should include a
lower-risk fallback when possible.

## External Data Boundary

External data are planned only when scientifically justified. Contextual map
layers, benchmark datasets, evidence-bearing external records, and annotation
resources require source, license, citation, access date, hash when downloaded,
and usage role. v0.6.0 does not download external data without explicit user
approval.

## Non-Runtime Materials

Examples and templates are support material. Load only the matching file for the active task. Do not bulk-load the whole suite.
