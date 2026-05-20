# Scientific Figure Skills for Codex

**A Codex-native skill suite for planning, rendering, auditing, and packaging publication-grade scientific figures.**

Scientific Figure Skills for Codex turns figure work into a managed, auditable
production system: scoped intent, dataset inspection, renderer selection,
library planning, visual claim tracking, reproducible exports,
journal-style status, render-quality checks, dry-run runbooks, and
project-local figure memory.

[![Validation](https://github.com/enesgul23/scientific-figure-skills-codex/actions/workflows/validation.yml/badge.svg)](https://github.com/enesgul23/scientific-figure-skills-codex/actions/workflows/validation.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.9.0-blue.svg)](VERSION)

## Why This Exists

Scientific figures are not just graphics. They are evidence-bearing artifacts.

This suite is designed for researchers, technical authors, and Codex users who
need figures that are not only polished, but also traceable, reproducible,
statistically honest, accessible, and explicit about uncertainty, journal
status, and data provenance.

Core priority:

```text
truth > reproducibility > interpretability > journal compliance > visual elegance > novelty
```

The suite does not fabricate data, does not silently install packages, does not
download external data without approval, and does not claim verified journal
compliance unless current official or user-provided guidance is available.

## What It Can Do

- Scope vague figure requests before rendering.
- Design manuscript figures, graphical abstracts, multi-panel layouts, and domain-specific visualizations.
- Render figures from registry-backed Python templates.
- Inspect user datasets and choose an appropriate Python plotting/data stack.
- Probe the local Python environment without installing anything.
- Build dependency plans with required, recommended, optional, blocked, and fallback libraries.
- Decide whether external data are scientifically justified before acquisition.
- Build dry-run agentic runbooks and next-action reports from memory, registries, dependency plans, and audit ledgers.
- Run shell helpers for validation, diagnostics, agentic planning, release checks, and generated-cache cleanup.
- Track figure lineage through project-local Figure Passport memory.
- Maintain dataset registries, visual claim ledgers, audit ledgers, and reset/resume boundaries.
- Audit render quality, blank images, output formats, SVG labels, file hashes, and visual regression sanity.
- Audit multi-panel optical grids, colorbar spacing, semantic color consistency, and controlled station labels.
- Audit and repair text layout: titles, axis labels, tick labels, legends, colorbar titles, direct labels, annotations, clipping, overlap, and domain terminology.
- Package figures with captions, alt text, manifests, reproducibility notes, and readiness checks.

## Skill Layout

```text
skills/scientific-figure-suite/
  SKILL.md                         # Root Codex router skill
  manifest.json                    # Public interface and package metadata
  MODE_REGISTRY.md                 # Command and mode registry
  POSITIONING.md                   # Scope and integrity boundary
  commands/                        # Codex command recipes
  fig/*/WORKFLOW.md                # Internal workflow instructions
  shared/                          # Protocols, contracts, gates, handoff schemas
  shared/contracts/                # JSON schemas for suite artifacts
  references/                      # Scientific figure design references
  templates/                       # Reusable artifact templates
  assets/render_registry/          # Chart type to renderer metadata
  assets/render_templates/         # Python starter render templates
  assets/library_pool/             # Python library metadata pool
  assets/text_profiles/            # Bundled domain terminology profiles
  scripts/                         # Validators, renderers, memory, QA, planning runtime
  scripts/bin/                     # POSIX shell helpers for validation and runbooks
  tests/                           # Sample fixtures and smoke prompts
```

Codex should discover only:

```text
skills/scientific-figure-suite/SKILL.md
```

Internal workflows use `WORKFLOW.md` files and are intentionally not separate registered skills.

## Installation

Clone the repository:

```bash
git clone https://github.com/enesgul23/scientific-figure-skills-codex.git
cd scientific-figure-skills-codex
```

Install validation dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Install the skill into Codex by copying or symlinking the skill folder into your Codex skills directory.

Windows PowerShell copy example:

```powershell
$source = (Resolve-Path ".\skills\scientific-figure-suite").Path
$target = "$env:USERPROFILE\.codex\skills\scientific-figure-suite"
New-Item -ItemType Directory -Force -Path (Split-Path $target) | Out-Null
Copy-Item -Recurse -Force $source $target
```

Windows PowerShell symlink example:

```powershell
$source = (Resolve-Path ".\skills\scientific-figure-suite").Path
$target = "$env:USERPROFILE\.codex\skills\scientific-figure-suite"
New-Item -ItemType Directory -Force -Path (Split-Path $target) | Out-Null
New-Item -ItemType SymbolicLink -Path $target -Target $source
```

macOS/Linux copy example:

```bash
mkdir -p ~/.codex/skills
cp -R skills/scientific-figure-suite ~/.codex/skills/scientific-figure-suite
```

After installation, restart Codex or reload skills if your Codex environment supports skill reloads.

## Quick Start

Use the skill by naming it or by using one of its command aliases in Codex:

```text
Use $scientific-figure-suite to plan a journal-ready multi-panel model performance figure.
```

```text
fig-scope Nature-style scientific figure for a flood forecasting paper
```

```text
fig-plan-libraries for data/predictions.csv and a parity scatter figure
```

```text
fig-render-template parity_scatter from predictions.csv
```

```text
fig-audit-render exported files in figures/output
```

```text
fig-agent-plan for the current project memory
```

For underspecified requests, the suite routes to figure scoping first. It asks for the scientific message, data status, figure type, target journal context, and output format before rendering.

## Main Command Aliases

| Alias | Purpose |
|---|---|
| `fig-scope` | Clarify an underspecified figure request without rendering. |
| `fig-plan` | Produce a structured figure plan and workflow chain. |
| `fig-agent-plan` | Build a dry-run runbook from project memory and audit state. |
| `fig-agent-next` | Select the next safe action from an agentic runbook. |
| `fig-agent-resume` | Rebuild the runbook from project-local memory and resume planning. |
| `fig-doctor` | Diagnose environment, registry, library pool, and memory fixture health. |
| `fig-full` | Run the full staged figure production chain. |
| `fig-render-template` | Render from the registry-backed Python templates. |
| `fig-audit-render` | Run visual QA and render-quality checks. |
| `fig-audit-multipanel-layout` | Audit multi-panel layout geometry, colorbars, semantic colors, and optical grid quality. |
| `fig-audit-text-layout` | Audit text overlap, clipping, axis bounds, colorbar titles, direct labels, and terminology. |
| `fig-repair-text-layout` | Repair crowded text layout deterministically, then re-audit. |
| `fig-plan-libraries` | Inspect data and plan required plotting/data libraries. |
| `fig-probe-environment` | Probe available Python imports and versions. |
| `fig-select-render-stack` | Select a minimal Python render stack. |
| `fig-plan-external-data` | Decide whether external data are scientifically justified. |
| `fig-init-memory` | Initialize project-local Figure Passport memory. |
| `fig-status` | Build a pipeline dashboard from project memory. |
| `fig-audit-readiness` | Decide figure package readiness from memory and audit ledgers. |

## Supported Figure Domains

- Statistical plots and uncertainty displays.
- AI/ML/model-performance figures.
- Clinical, biomedical, survival, diagnostic, and trial figures.
- Geospatial vector, raster, study-area, and model-error maps.
- Omics and bioinformatics figures.
- Multi-panel journal figures.
- Graphical abstracts and mechanism diagrams.
- Captions, legends, notes, alt text, and export packages.

## Library Intelligence Runtime

Version `0.6.0` added a Python-first dependency planning layer.

The suite can inspect datasets, read the renderer registry, check the current Python environment, and produce a dependency plan. It does not install packages automatically.

Typical flow:

```bash
python skills/scientific-figure-suite/scripts/inspect_dataset.py \
  --input data/predictions.csv \
  --out dataset_profile.json

python skills/scientific-figure-suite/scripts/probe_python_environment.py \
  --out environment_probe.json

python skills/scientific-figure-suite/scripts/build_dependency_plan.py \
  --chart-type parity_scatter \
  --dataset-profile dataset_profile.json \
  --environment-probe environment_probe.json \
  --out dependency_plan.json
```

The generated plan includes:

- selected stack
- required libraries
- recommended libraries
- optional libraries
- blocked libraries
- install commands for user review
- import checks
- fallback renderer
- reproducibility notes

## External Data Decision Runtime

External data are allowed only when there is a scientific reason.

Valid roles:

- `contextual`: basemap, boundary, coastline, background context
- `evidentiary`: data supporting a figure claim
- `benchmark`: external validation or comparison data
- `annotation`: ontology, pathway, gene set, reference metadata

External data require source, license, citation, access date, hash when materialized, usage role, and contamination-risk review for model-performance work.

## Multipanel Layout Quality Runtime

Version `0.7.0` adds a dedicated multi-panel layout audit.

For complex manuscript figures, the suite does not treat `constrained_layout`
or `tight_layout` as sufficient by itself. Colorbar panels, shared legends,
maps, scatter panels, and station labels require explicit layout checks before
final export.

The audit checks:

- panel boxes do not overlap
- panel boxes in the same visual row share top and bottom bounds
- colorbars have explicit boxes, label spacing checks, and collision checks
- long colorbar labels use a short title or move detail to the caption
- repeated semantic categories keep the same colors across panels
- direct station or point labels are controlled and collision-checked
- automatic layout has a manual-axes fallback when optical grid quality fails

Multipanel layout audit example:

```bash
python skills/scientific-figure-suite/scripts/audit_multipanel_layout.py \
  --layout layout.yaml \
  --out multipanel_layout_audit.json
```

This audit is also wired into project memory through
`multipanel_layout_history.jsonl`, pipeline dashboards, and submission-readiness
checks. A failed layout audit blocks readiness wording until the panel boxes,
colorbars, semantic colors, or direct labels are repaired.

## Text Layout Intelligence Runtime

Version `0.8.0` adds a dedicated text layout audit and repair layer.

The suite no longer treats successful code execution as enough for text-heavy
figures. It checks whether figure titles, panel titles, axis labels, tick
labels, legends, colorbar titles, direct labels, and annotations are readable,
aligned, inside their bounds, non-overlapping, and worded with
domain-appropriate academic terminology.

The audit checks:

- text-text overlap and minimum spacing
- figure and axes clipping
- minimum font size and excessive rotation
- long title wrapping
- default right-side colorbar title placement
- grouped colorbar title safety
- direct-label density and collision control
- vague labels against bundled domain text profiles

Text layout audit example:

```bash
python skills/scientific-figure-suite/scripts/select_text_profile.py \
  --domain model-performance \
  --chart-type roc_pr_curve \
  --out text_profile_selection.json

python skills/scientific-figure-suite/scripts/audit_text_layout.py \
  --layout text_layout.yaml \
  --text-profile text_profile_selection.json \
  --out text_layout_report.json
```

Repair example:

```bash
python skills/scientific-figure-suite/scripts/repair_text_layout.py \
  --layout text_layout.yaml \
  --out repaired_text_layout.yaml

python skills/scientific-figure-suite/scripts/audit_text_layout.py \
  --layout repaired_text_layout.yaml
```

Text audits append to `text_layout_history.jsonl` when project memory is enabled. A failed text layout audit blocks submission-readiness wording until the labels are repaired and re-audited.

## Agentic Orchestration Runtime

Version `0.9.0` adds a dry-run-first orchestration layer. The suite can read
project memory, dependency plans, render history, text and multi-panel audits,
and readiness ledgers, then produce the next safe action without rendering or
mutating memory.

```bash
python skills/scientific-figure-suite/scripts/build_agentic_runbook.py \
  --memory-dir .codex/scientific-figure-memory \
  --out agentic_runbook.json

python skills/scientific-figure-suite/scripts/advance_agentic_runbook.py \
  --runbook agentic_runbook.json \
  --out agentic_run_report.json
```

Shell helper examples:

```bash
bash skills/scientific-figure-suite/scripts/bin/sfs-doctor.sh
bash skills/scientific-figure-suite/scripts/bin/sfs-agent-plan.sh --memory-dir .codex/scientific-figure-memory --out agentic_runbook.json
bash skills/scientific-figure-suite/scripts/bin/sfs-agent-next.sh --runbook agentic_runbook.json
```

On Windows, use Git Bash or WSL for the POSIX shell helpers. Python scripts remain the canonical runtime.

External data planning example:

```bash
python skills/scientific-figure-suite/scripts/plan_external_data.py \
  --chart-type geospatial_choropleth \
  --goal "need basemap context" \
  --source-name "Natural Earth" \
  --source-url "https://www.naturalearthdata.com/" \
  --license "public domain" \
  --citation "Natural Earth contributors" \
  --out data_acquisition_plan.json

python skills/scientific-figure-suite/scripts/validate_data_acquisition_plan.py \
  data_acquisition_plan.json
```

## Project Memory

Project memory is file-based, auditable, and local to the user project. It is not Codex personal memory.

Default location:

```text
.codex/scientific-figure-memory/
```

Memory can track:

- project profile
- journal targets and verification status
- figure passports
- figure set manifests
- dataset registry
- visual claim ledger
- quality audit history
- render-quality history
- multipanel layout audit history
- text layout audit history
- dependency plan history
- external data plan history
- agentic task queues and run history
- reset/resume boundaries
- optional author or lab visual style profile

Private project memory must not be committed to this repository.

## Validation

Run the full validation suite from the repository root:

```bash
python quick_validate.py
```

The validation suite checks:

- skill structure
- JSON contracts
- handoff fixtures
- style tokens
- renderer registry
- library pool metadata
- memory validation and migration
- pipeline dashboard
- render-template smoke tests
- visual QA pass/fail behavior
- multipanel layout optical-grid QA
- text layout audit and repair behavior
- dataset inspection
- dependency planning
- external data plan validation
- agentic runbook validation and next-action dry runs
- shell helper syntax and diagnostics
- repository hygiene, version sync, and no generated caches

GitHub Actions runs the same validation workflow on pull requests and pushes to `main`.

## Scientific Guardrails

This suite is intentionally conservative.

- It does not invent data, p-values, sample sizes, model metrics, clinical outcomes, map attributes, or biological mechanisms.
- It marks missing data as `MISSING` or `MOCKUP`.
- It treats journal profiles as `ESTIMATED` or `UNVERIFIED` unless current official or user-provided guidance is available.
- It treats external data as provenance-gated.
- It treats dependency installation as a user-approved step, not an automatic behavior.
- It treats agentic execution as dry-run-first and approval-gated for risky actions.
- It treats render-quality QA as a file sanity layer, not proof of scientific correctness.
- It treats text layout repair as conservative layout editing, not scientific wording invention.

## Citation

If this suite supports academic work, please cite it. GitHub can generate citation metadata directly from `CITATION.cff`.

Recommended citation:

```text
Gul, E. (2026). Scientific Figure Skills for Codex (Version 0.9.0) [Computer software]. GitHub. https://github.com/enesgul23/scientific-figure-skills-codex
```

BibTeX:

```bibtex
@software{gul_scientific_figure_skills_codex_2026,
  author = {Gul, Enes},
  title = {Scientific Figure Skills for Codex},
  year = {2026},
  version = {0.9.0},
  url = {https://github.com/enesgul23/scientific-figure-skills-codex},
  license = {MIT}
}
```

## License

MIT License. See [LICENSE](LICENSE).
