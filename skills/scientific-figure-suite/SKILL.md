---
name: scientific-figure-suite
description: >
  Create, design, audit, and export publication-quality scientific figures,
  statistical plots, multi-panel journal figures, graphical abstracts, clinical
  figures, model-performance visualizations, geospatial maps, omics figures,
  figure captions, alt text, visual claim ledgers, accessibility checks, image
  integrity checks, and journal-style submission packages for Nature, Science,
  The Lancet, Cell, NEJM, JAMA, BMJ, PNAS, IEEE, Elsevier, and Springer Nature
  contexts, including project-local Figure Passport memory, visual style
  profiles, dataset registries, journal target memory, reset/resume boundaries,
  append-only visual audit ledgers, panel-level passports, repro-lock stale
  detection, journal guideline verification ledgers, and renderer starter
  kits, figure set manifests, cross-figure consistency audits, submission
  package indexes, submission-readiness reports, figure scoping, pipeline
  dashboards, renderer registries, style-token validation, visual regression
  checks, render-quality audits, multi-panel optical-grid audits, colorbar
  layout checks, semantic color consistency checks, controlled station-label
  audits, library-pool planning, dependency selection,
  Python environment probing, and external-data acquisition decisions. Use when the user asks for scientific charts, research figures,
  journal-ready plots, Nature-style figures, Science-style figures,
  Lancet-style figures, graphical abstracts, figure audits, caption writing,
  visual claim checking, reproducible figure export, project figure memory,
  figure passport, visual passport, resume a figure project, stale artifact
  detection, journal verification memory, or command-style aliases such as
  fig-plan, fig-audit, fig-caption, fig-export, fig-model-performance,
  fig-graphical-abstract, fig-full, fig-init-memory, fig-load-memory,
  fig-update-memory, fig-summarize-memory, fig-forget-memory,
  fig-validate-memory, fig-resume-project, fig-migrate-memory,
  fig-audit-repro-lock, fig-verify-journal, fig-audit-visual-artifact,
  fig-build-figure-set, fig-audit-figure-set, fig-build-submission-package,
  fig-audit-readiness, fig-scope, fig-status, fig-render-template,
  fig-audit-render, fig-audit-multipanel-layout, fig-plan-libraries,
  fig-probe-environment, fig-select-render-stack, or fig-plan-external-data.
---

# Scientific Figure Suite

This is a Codex-native router skill for publication-quality scientific figure
work. Route through this file first, then read only the workflow, command
recipe, shared protocol, reference, template, or script needed for the active
task.

## Versioning

This package is version `0.7.0`. Keep repo-root `VERSION` and
`manifest.json` `adapter_version` synchronized. Keep `SKILL.md` frontmatter
minimal so Codex skill discovery remains stable.

## Positioning

Read `POSITIONING.md` when the task raises scope, authorship, scientific
integrity, or "submission-ready" concerns. This suite is a scientific figure
production assistant, not an autonomous evidence generator and not a journal
compliance oracle.

## Mode Registry

Read `MODE_REGISTRY.md` when the user invokes command aliases, asks for a mode,
or when a workflow must choose between planning, rendering, auditing, revision,
or full-package execution.

## First Rule

Do not load the whole suite by default. Select one workflow, read that
workflow's `WORKFLOW.md`, then load only the needed files. Internal workflow
entry files are named `WORKFLOW.md`, not `SKILL.md`, so Codex registers only
this root router skill.

## Scientific Priority

Always apply:

```text
truth > reproducibility > interpretability > journal compliance > visual elegance > novelty
```

Do not improve visual appeal by weakening data accuracy, statistical honesty,
reproducibility, accessibility, journal-status accuracy, or caption integrity.

## Workflow Router

| User intent | Read first |
|---|---|
| General figure request, unclear data or target | `fig/intake-design/WORKFLOW.md` |
| Statistical chart or quantitative result figure | `fig/statistical-plots/WORKFLOW.md` |
| AI, ML, or model-performance figure | `fig/model-performance/WORKFLOW.md` |
| Clinical, biomedical, epidemiology, or trial figure | `fig/clinical-biomedical/WORKFLOW.md` |
| Map, geospatial, raster, or spatial figure | `fig/geospatial-maps/WORKFLOW.md` |
| Omics or bioinformatics figure | `fig/omics-bioinformatics/WORKFLOW.md` |
| Multi-panel composition | `fig/multipanel-composer/WORKFLOW.md` |
| Mechanism, schematic, or conceptual diagram | `fig/schematic-mechanism/WORKFLOW.md` |
| Graphical abstract | `fig/graphical-abstract/WORKFLOW.md` |
| Nature, Science, Lancet, Cell, NEJM, JAMA, BMJ, PNAS, IEEE, Elsevier, or Springer Nature style | `fig/journal-style-translator/WORKFLOW.md` |
| Caption, legend, note, or alt text | `fig/caption-alttext/WORKFLOW.md` |
| Figure quality or integrity audit | `fig/figure-auditor/WORKFLOW.md` |
| PDF, SVG, EPS, TIFF, or PNG export package | `fig/export-packager/WORKFLOW.md` |

If the request spans multiple workflows, start with `fig/intake-design/WORKFLOW.md`
unless the user clearly asks for a single phase.

### Figure Intent Scoping Override

Apply this override before render, export, style, or full-package routing.

If the user asks for a scientific figure, paper figure, journal-ready figure,
Nature/Science/Lancet-style figure, graphical abstract, or "make a figure" but
does not provide a clear scientific message, data status, figure type, target
journal/article context, or output format, route to `fig/intake-design/WORKFLOW.md`
in scoping mode first.

First response in this path:

1. State that the request is routed to figure scoping because required rendering
   inputs are missing.
2. Ask no more than five concrete questions covering scientific message, data,
   figure type, journal/manuscript context, and output format.
3. Produce or request a `figure_intake` artifact. Do not render or export files
   until the missing inputs are resolved.
4. If data are absent and the user only wants a concept, mark the work
   `NON_DATA_MOCKUP` or `DATA_STATUS: MISSING`.

## Command Alias Router

Codex does not install native slash commands from this package. If the user's
request starts with a slash alias such as `/fig-plan` or a plain alias such as
`fig-plan`, treat it as a mode shortcut, strip the alias token from the task
text, read the matching `commands/fig-*.md` recipe, then route to the workflow
below.

| Alias | Read command recipe | Then route to |
|---|---|---|
| `/fig-plan`, `fig-plan` | `commands/fig-plan.md` | `fig/intake-design/WORKFLOW.md` in planning mode |
| `/fig-scope`, `fig-scope` | `commands/fig-scope.md` | `fig/intake-design/WORKFLOW.md` in scoping mode |
| `/fig-audit`, `fig-audit` | `commands/fig-audit.md` | `fig/figure-auditor/WORKFLOW.md` |
| `/fig-caption`, `fig-caption` | `commands/fig-caption.md` | `fig/caption-alttext/WORKFLOW.md` |
| `/fig-export`, `fig-export` | `commands/fig-export.md` | `fig/export-packager/WORKFLOW.md` |
| `/fig-model-performance`, `fig-model-performance` | `commands/fig-model-performance.md` | `fig/model-performance/WORKFLOW.md` |
| `/fig-graphical-abstract`, `fig-graphical-abstract` | `commands/fig-graphical-abstract.md` | `fig/graphical-abstract/WORKFLOW.md` |
| `/fig-style`, `fig-style` | `commands/fig-style.md` | `fig/journal-style-translator/WORKFLOW.md` |
| `/fig-full`, `fig-full` | `commands/fig-full.md` | `fig/intake-design/WORKFLOW.md` then full production chain |
| `/fig-init-memory`, `fig-init-memory` | `commands/fig-init-memory.md` | `shared/figure_memory_protocol.md` |
| `/fig-load-memory`, `fig-load-memory` | `commands/fig-load-memory.md` | `shared/figure_memory_protocol.md` |
| `/fig-update-memory`, `fig-update-memory` | `commands/fig-update-memory.md` | `shared/figure_memory_protocol.md` |
| `/fig-summarize-memory`, `fig-summarize-memory` | `commands/fig-summarize-memory.md` | `shared/figure_memory_protocol.md` |
| `/fig-forget-memory`, `fig-forget-memory` | `commands/fig-forget-memory.md` | `shared/figure_memory_protocol.md` |
| `/fig-validate-memory`, `fig-validate-memory` | `commands/fig-validate-memory.md` | `shared/figure_memory_protocol.md` |
| `/fig-resume-project`, `fig-resume-project` | `commands/fig-resume-project.md` | `shared/figure_passport_reset_boundary.md` |
| `/fig-migrate-memory`, `fig-migrate-memory` | `commands/fig-migrate-memory.md` | `shared/submission_memory_runtime.md` |
| `/fig-audit-repro-lock`, `fig-audit-repro-lock` | `commands/fig-audit-repro-lock.md` | `shared/submission_memory_runtime.md` |
| `/fig-verify-journal`, `fig-verify-journal` | `commands/fig-verify-journal.md` | `fig/journal-style-translator/WORKFLOW.md` |
| `/fig-audit-visual-artifact`, `fig-audit-visual-artifact` | `commands/fig-audit-visual-artifact.md` | `fig/figure-auditor/WORKFLOW.md` |
| `/fig-build-figure-set`, `fig-build-figure-set` | `commands/fig-build-figure-set.md` | `shared/figure_set_submission_runtime.md` |
| `/fig-audit-figure-set`, `fig-audit-figure-set` | `commands/fig-audit-figure-set.md` | `shared/figure_set_submission_runtime.md` |
| `/fig-build-submission-package`, `fig-build-submission-package` | `commands/fig-build-submission-package.md` | `fig/export-packager/WORKFLOW.md` |
| `/fig-audit-readiness`, `fig-audit-readiness` | `commands/fig-audit-readiness.md` | `shared/figure_set_submission_runtime.md` |
| `/fig-status`, `fig-status` | `commands/fig-status.md` | `shared/figure_memory_protocol.md` and pipeline dashboard |
| `/fig-render-template`, `fig-render-template` | `commands/fig-render-template.md` | render registry |
| `/fig-audit-render`, `fig-audit-render` | `commands/fig-audit-render.md` | render-quality audit |
| `/fig-audit-multipanel-layout`, `fig-audit-multipanel-layout` | `commands/fig-audit-multipanel-layout.md` | multi-panel layout quality audit |
| `/fig-plan-libraries`, `fig-plan-libraries` | `commands/fig-plan-libraries.md` | library-pool dependency planning |
| `/fig-probe-environment`, `fig-probe-environment` | `commands/fig-probe-environment.md` | Python environment probe |
| `/fig-select-render-stack`, `fig-select-render-stack` | `commands/fig-select-render-stack.md` | renderer dependency stack selection |
| `/fig-plan-external-data`, `fig-plan-external-data` | `commands/fig-plan-external-data.md` | external data decision protocol |

If the Codex client reserves slash-prefixed input before it reaches the model,
tell the user to use the plain alias form, for example `fig-plan my figure`.

## Memory Protocol

This suite supports ARS-style project memory through project-local files, not
through Codex personal memory and not by writing private project state inside
the installed skill folder.

Default memory location:

```text
.codex/scientific-figure-memory/
```

Use memory only when the user asks to initialize, load, update, summarize,
forget, resume, or continue a scientific figure project. For memory tasks, read
`shared/figure_memory_protocol.md` first. For reset/resume boundaries, read
`shared/figure_passport_reset_boundary.md`. For author or lab visual style
calibration, read `shared/visual_style_profile_protocol.md`.

Memory files:

- `memory_manifest.json`: single source of truth for project memory state,
  version, active figure, stages, and validation status.
- `project_profile.json`: project-level visual goals and constraints.
- `journal_targets.json`: target journal profiles and verification status.
- `figure_passport.json`: figure inventory, versions, outputs, and status tags.
- `figure_set_manifest.json`: manuscript-level figure inventory and cross-figure status.
- `submission_package_index.json`: indexed package files with hashes and figure links.
- `visual_claim_ledger.jsonl`: append-style claim-to-visual evidence mapping.
- `dataset_registry.json`: datasets, columns, units, preprocessing notes.
- `quality_audit_history.jsonl`: append-style quality gate results.
- `revision_boundary_ledger.jsonl`: hash-linked reset/resume boundaries.
- `journal_guideline_verification.jsonl`: append-style evidence for current
  journal guideline checks.
- `visual_audit_artifact.jsonl`: append-style file-level audit artifacts with
  hashes, dimensions when available, and gate status.
- `cross_figure_consistency_history.jsonl`: append-style figure set consistency results.
- `submission_readiness_history.jsonl`: append-style submission readiness decisions.
- `figure_decision_log.jsonl`: append-style scoping, waiver, mockup, and style decisions.
- `visual_regression_history.jsonl`: append-style render-quality and visual regression results.
- `multipanel_layout_history.jsonl`: append-style multi-panel optical-grid, colorbar, semantic color, and direct-label layout audits.
- `dependency_plan_history.jsonl`: append-style dependency plans and library stack decisions.
- `external_data_plan_history.jsonl`: append-style external data acquisition decisions.
- `author_visual_style_profile.json`: optional visual style memory from
  user-approved samples.

Memory rules:

1. Never store project-specific memory inside the installed skill directory.
2. Never silently overwrite memory; initialize missing files or require an
   explicit update/forget command.
3. Treat append-only ledgers as history; add entries instead of rewriting prior
   audit or boundary events.
4. Mark journal targets `VERIFIED` only from current official or user-provided
   guidelines; otherwise use `ESTIMATED` or `UNVERIFIED`.
5. Do not import memory from another project unless the user explicitly asks.
6. Do not infer submission readiness from memory alone; quality gates must pass.
7. Author visual style is a soft preference below truth, reproducibility,
   journal requirements, accessibility, and statistical honesty.
8. Treat stored panel outputs as stale when data, code, output, or environment
   hashes drift from the stored repro-lock.

## Multi-Workflow Chains

For a journal-ready multi-panel figure:

```text
intake-design -> domain workflow -> multipanel-composer -> fig-audit-multipanel-layout -> journal-style-translator -> caption-alttext -> figure-auditor -> export-packager
```

For a graphical abstract:

```text
intake-design -> schematic-mechanism -> graphical-abstract -> journal-style-translator -> caption-alttext -> figure-auditor
```

For audit-only requests:

```text
figure-auditor -> journal-style-translator if target journal is named -> caption-alttext if caption is present
```

For a full figure-package request:

```text
intake-design -> domain workflow -> multipanel-composer if needed -> journal-style-translator -> caption-alttext -> figure-auditor -> export-packager
```

## Codex Runtime Mapping

Apply these mappings when workflow or command files use suite terminology:

| Suite wording | Codex behavior |
|---|---|
| agent, reviewer, specialist, handoff | Read the referenced role prompt file when it exists and perform that phase inline. |
| dispatch, call workflow, trigger workflow | Read the target `WORKFLOW.md` and continue in the current conversation. |
| subagent or parallel reviewer | Do not spawn agents automatically; use Codex subagents only when the user explicitly asks for delegation or parallel agents. |
| live journal verification | Browse official or user-provided current guidelines when the user asks for verified compliance. Otherwise mark style as estimated or unverified. |
| generate final data figure | Generate only from supplied data or code. If data are missing, produce `NON_DATA_MOCKUP` or ask for inputs. |
| choose plotting libraries | Use the library pool, dataset inspection, render registry, and environment probe. Do not install packages automatically. |
| download external data | Plan only unless the user explicitly approves download and provenance is complete. |
| memory, passport, visual passport | Use project-local `.codex/scientific-figure-memory/` files and the memory scripts; never write project memory into the skill folder. |
| Bash, Python, script | Treat as available local tooling subject to Codex filesystem and safety rules. |

## Agent Prompt Use

When a workflow lists agents:

1. Read the workflow `WORKFLOW.md` to identify the phase and artifact needed.
2. Read the specific `agents/<name>.md` files for the current phase.
3. Treat each agent file as a scoped role prompt with an input/output contract.
4. Produce the phase output in the current conversation unless the user requested files.
5. Use `shared/handoff_schemas.md` when moving artifacts between phases.

Do not spawn Codex subagents automatically. Agent files are role prompts by
default; use actual parallel subagents only when the user explicitly asks for
delegation or parallel agent work.

## Canonical Agent Files

Use these exact filenames. Do not invent alternatives from memory.

`fig/intake-design/agents/`:
`figure_intake_agent.md`, `scientific_message_agent.md`.

`fig/statistical-plots/agents/`:
`chart_selection_agent.md`, `statistical_honesty_agent.md`.

`fig/model-performance/agents/`:
`performance_diagnostic_agent.md`, `validation_split_agent.md`,
`uncertainty_calibration_agent.md`.

`fig/clinical-biomedical/agents/`:
`clinical_reporting_agent.md`, `denominator_endpoint_agent.md`.

`fig/geospatial-maps/agents/`:
`spatial_integrity_agent.md`, `cartographic_design_agent.md`.

`fig/omics-bioinformatics/agents/`:
`omics_threshold_agent.md`, `bioinformatics_visual_agent.md`.

`fig/multipanel-composer/agents/`:
`layout_architect_agent.md`, `panel_consistency_agent.md`.

`fig/schematic-mechanism/agents/`:
`mechanism_claim_agent.md`.

`fig/graphical-abstract/agents/`:
`visual_narrative_agent.md`, `evidence_boundary_agent.md`.

`fig/journal-style-translator/agents/`:
`journal_policy_agent.md`, `style_token_agent.md`.

`fig/caption-alttext/agents/`:
`caption_integrity_agent.md`, `alt_text_agent.md`.

`fig/figure-auditor/agents/`:
`visual_integrity_reviewer_agent.md`, `statistical_reviewer_agent.md`,
`accessibility_reviewer_agent.md`.

`fig/export-packager/agents/`:
`export_manifest_agent.md`, `reproducibility_packager_agent.md`.

## Shared Resources

Use `shared/` for cross-workflow contracts and gates:

- `shared/status_taxonomy.md` defines output status labels.
- `shared/handoff_schemas.md` defines structured artifacts passed between phases.
- `shared/figure_quality_gates.md` defines mandatory and advisory figure gates.
- `shared/visual_claim_protocol.md` defines claim-ledger semantics.
- `shared/journal_verification_protocol.md` defines verified/estimated/unverified style handling.
- `shared/reproducibility_protocol.md` defines code, data, manifest, and export traceability.
- `shared/figure_pipeline_state_machine.md` defines staged full-package flow.
- `shared/failure_recovery_protocol.md` defines what to do when gates fail.
- `shared/mode_registry.md` defines planning, render, audit, revision, and package modes.
- `shared/mode_spectrum.md` defines fidelity, balanced, and originality tradeoffs.
- `shared/accessibility_protocol.md` defines color, contrast, text, and alt-text checks.
- `shared/image_integrity_protocol.md` defines raw image and manipulation audit limits.
- `shared/domain_router_matrix.md` maps data domains to workflows, agents, and gates.
- `shared/review_rubrics.md` defines severity and scoring rubrics for figure review.
- `shared/compliance_checkpoint_protocol.md` defines mandatory reporting checks.
- `shared/artifact_reproducibility_pattern.md` defines figure passport/repro-lock semantics.
- `shared/ground_truth_isolation_pattern.md` defines benchmark/evaluation separation.
- `shared/cross_model_verification.md` defines optional independent review semantics.
- `shared/figure_memory_protocol.md` defines project-local memory files, write rules, and lifecycle commands.
- `shared/figure_passport_reset_boundary.md` defines hash-linked reset/resume boundaries for long figure projects.
- `shared/visual_style_profile_protocol.md` defines optional author or lab visual style memory.
- `shared/submission_memory_runtime.md` defines workflow-memory integration, panel passports, repro-lock, and stale detection.
- `shared/figure_set_submission_runtime.md` defines v0.4 figure set manifests, package indexing, cross-figure consistency, and readiness gates.
- `shared/external_data_decision_protocol.md` defines when external data can be proposed and what provenance is required.
- `shared/multipanel_layout_quality_protocol.md` defines v0.7 optical-grid, colorbar, semantic color, and direct-label layout rules.
- `assets/render_registry/render_registry.json` defines chart-type to renderer and dependency mappings.
- `assets/library_pool/library_pool.json` defines the Python-first library metadata pool.
- `shared/contracts/style_token.schema.json` defines style-token validation shape.
- `shared/contracts/visual_regression_report.schema.json` defines render-quality report shape.
- `shared/contracts/multipanel_layout_audit.schema.json` defines multi-panel layout audit shape.
- `shared/contracts/library_pool.schema.json` defines library-pool metadata shape.
- `shared/contracts/dependency_plan.schema.json` defines dependency-plan output shape.
- `shared/contracts/data_acquisition_plan.schema.json` defines external-data plan output shape.
- `shared/agents/compliance_agent.md` defines the shared compliance role prompt.
- `shared/agents/memory_curator_agent.md` defines the shared memory curator role prompt.
- `shared/contracts/` contains JSON schemas for major handoff artifacts.

Use `templates/` for reusable output skeletons and `examples/` for realistic
non-binary fixtures. Do not load all templates or examples by default; open only
the one matching the active task.

When a workflow points to `shared/...`, resolve it under this skill directory.
When it points to `references/...`, `assets/...`, `scripts/...`, or
`commands/...`, resolve it under this skill directory.

## Verification Discipline

For data values, p-values, confidence intervals, sample sizes, model metrics,
image features, map attributes, journal policies, and current submission
requirements, verify against supplied files, generated code, user-provided
guidelines, or current official sources. If verification is not possible, mark
the item unverified instead of inventing support.

Never fabricate references, sample sizes, clinical outcomes, model metrics,
biological mechanisms, map projections, or journal compliance claims.

## Journal Compliance Guardrail

Never claim verified compliance with a journal's current figure requirements
unless the active task includes current official guidelines or user-provided
current guidelines. If guidance is unavailable, mark the output as
`STYLE_PROFILE_ESTIMATED` or `STYLE_PROFILE_UNVERIFIED`.

Allowed language includes `Nature-inspired estimated profile` and
`target-journal style estimate pending guideline verification`. Do not write
`Nature-compliant`, `Science-compliant`, `Lancet-compliant`, or
`submission-ready for [journal]` unless status is `VERIFIED`.

## Data Integrity Guardrail

Never invent data values, sample sizes, p-values, confidence intervals, model
metrics, biological mechanisms, clinical outcomes, map attributes, or image
features. If data are missing, ask for data or produce a clearly marked
`NON_DATA_MOCKUP` design plan.

## Output Status Tags

Every figure package or plan must report:

```text
DATA_STATUS: PROVIDED / INFERRED / MISSING / MOCKUP
STYLE_STATUS: VERIFIED / ESTIMATED / UNVERIFIED
REPRODUCIBILITY_STATUS: CODED / DESIGN_ONLY / PARTIAL
EXPORT_STATUS: READY / NEEDS_RENDER / NEEDS_JOURNAL_CHECK
INTEGRITY_STATUS: PASS / PASS_WITH_WARNINGS / FAIL
```

Read `shared/status_taxonomy.md` when a status is ambiguous.

## Required Final Package

When producing a complete figure package, provide:

- figure specification
- runnable Python or R code when data are available
- caption and alt text
- visual claim ledger
- quality report
- export instructions or generated files
- submission manifest
- journal style status
- dependency plan when libraries beyond the default static stack are required
- external data acquisition plan when external basemap, benchmark, evidence, or annotation data are proposed

If project memory is enabled, also update or emit the relevant Figure Passport
entry, visual claim ledger entries, dataset registry references, and quality
audit history entries.
