# Mode Registry

Use these modes in command recipes and workflow handoffs.

| Mode | Purpose | Typical alias |
|---|---|---|
| `planning` | Convert request into figure plan and missing inputs | `fig-plan` |
| `scoping` | Narrow underspecified figure intent before rendering | `fig-scope` |
| `render` | Generate data-derived figure code/output | domain-specific |
| `registry-render` | Render from the template registry | `fig-render-template` |
| `audit` | Review figure/spec/caption/package for gates | `fig-audit` |
| `render-audit` | Check rendered files for visual QA/regression sanity | `fig-audit-render` |
| `multipanel-layout-audit` | Check optical grid, colorbars, semantic colors, and direct labels | `fig-audit-multipanel-layout` |
| `text-layout-audit` | Check text overlap, clipping, axis bounds, colorbar titles, and terminology | `fig-audit-text-layout` |
| `text-layout-repair` | Repair crowded text layout without changing scientific meaning | `fig-repair-text-layout` |
| `caption` | Write caption, note, legend, and alt text | `fig-caption` |
| `style` | Translate target journal style and status | `fig-style` |
| `export` | Build export package and manifest | `fig-export` |
| `full` | Run staged pipeline from intake to package | `fig-full` |
| `revision` | Repair an existing figure after audit findings | none |
| `memory-init` | Create project-local Figure Passport memory | `fig-init-memory` |
| `memory-load` | Validate and summarize existing figure memory | `fig-load-memory` |
| `memory-update` | Update Figure Passport and append ledger entries | `fig-update-memory` |
| `memory-forget` | Redact or remove explicitly requested memory scope | `fig-forget-memory` |
| `memory-resume` | Resume from a Figure Passport reset boundary hash | `fig-resume-project` |
| `memory-migrate` | Upgrade memory schema without deleting history | `fig-migrate-memory` |
| `repro-lock-audit` | Detect stale data/code/output hashes | `fig-audit-repro-lock` |
| `journal-verify` | Append target-journal guideline evidence | `fig-verify-journal` |
| `visual-artifact-audit` | Hash and record checked output files | `fig-audit-visual-artifact` |
| `figure-set-build` | Build manuscript-level figure set manifest | `fig-build-figure-set` |
| `figure-set-audit` | Check cross-figure consistency | `fig-audit-figure-set` |
| `submission-package-build` | Build a hash index of package files | `fig-build-submission-package` |
| `submission-readiness` | Decide full figure package readiness | `fig-audit-readiness` |
| `pipeline-status` | Summarize project-local pipeline state | `fig-status` |
| `library-planning` | Plan required, recommended, optional, and blocked Python libraries | `fig-plan-libraries` |
| `environment-probe` | Probe import/version availability without installing packages | `fig-probe-environment` |
| `render-stack-selection` | Select the minimal Python render stack from registry, dataset, and environment context | `fig-select-render-stack` |
| `external-data-planning` | Decide whether external data are scientifically needed and provenance-complete | `fig-plan-external-data` |

## Mode Rules

- `planning` may run without data, but must mark missing inputs.
- `scoping` must not render files.
- `render` requires supplied data or code.
- `registry-render` requires a valid registry entry and required data columns.
- Dependency modes must not install packages automatically.
- `external-data-planning` must not download data without explicit user approval and complete provenance.
- `audit` may run with partial materials, but must mark unverifiable gates.
- `render-audit` checks rendered files, not scientific truth.
- `multipanel-layout-audit` checks whether the optical grid and colorbar/direct-label layout are fit for manuscript use.
- `text-layout-audit` blocks readiness when text overlap, clipping, unreadable fonts, or invalid terminology fails.
- `text-layout-repair` must be followed by a fresh `text-layout-audit`.
- `style` can be verified only with current official or user-provided guidance.
- `full` must include audit before export.
- Memory modes use project-local `.codex/scientific-figure-memory/` storage and must not write project memory inside the installed skill folder.
