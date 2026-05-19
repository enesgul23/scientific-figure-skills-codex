# Mode Registry

Single source of truth for scientific figure suite modes. Update this file when
adding command aliases, workflow modes, or validator expectations.

## Modes

| Mode | Spectrum | Output | Oversight | Triggers |
|---|---|---|---|---|
| `planning` | Originality | Figure intake, candidate visuals, missing-input list | Very High | `fig-plan`, vague figure request |
| `scoping` | Originality | Figure-intent narrowing without render/export | Very High | `fig-scope`, underspecified journal-style figure request |
| `render` | Balanced | Data-derived code and figure outputs | High | "draw", "plot", "generate figure from data" |
| `registry-render` | Balanced | Registry-selected template render and manifest | High | `fig-render-template` |
| `audit` | Fidelity | Quality report with gates and fixes | Medium | `fig-audit`, "review/check this figure" |
| `render-audit` | Fidelity | Visual QA and regression sanity report | Medium | `fig-audit-render` |
| `caption` | Fidelity | Caption, note, in-text reference, alt text | Medium | `fig-caption`, "write caption" |
| `style` | Fidelity | Journal style report and token decisions | Medium | `fig-style`, "Nature-style", "journal-ready" |
| `export` | Fidelity | Export package and manifest | Low | `fig-export`, "PDF/SVG/TIFF package" |
| `revision` | Balanced | Revised spec/caption/code plan after audit findings | High | "fix these audit issues" |
| `full` | Balanced | Staged intake -> domain -> style -> caption -> audit -> export package | Very High | `fig-full`, "complete figure package" |
| `memory-init` | Fidelity | Project-local memory scaffold | High | `fig-init-memory` |
| `memory-load` | Fidelity | Validated memory dashboard | Medium | `fig-load-memory`, "continue this figure project" |
| `memory-update` | Fidelity | Updated Figure Passport and ledgers | High | `fig-update-memory` |
| `memory-forget` | Fidelity | Redacted or removed memory scope | Very High | `fig-forget-memory` |
| `memory-resume` | Fidelity | Resume acknowledgment from boundary hash | High | `fig-resume-project` |
| `memory-migrate` | Fidelity | Memory schema migration | High | `fig-migrate-memory` |
| `repro-lock-audit` | Fidelity | Stale artifact detection | High | `fig-audit-repro-lock` |
| `journal-verify` | Fidelity | Journal guideline verification ledger update | High | `fig-verify-journal` |
| `visual-artifact-audit` | Fidelity | File-level visual audit artifact entry | Medium | `fig-audit-visual-artifact` |
| `figure-set-build` | Fidelity | Manuscript-level figure set manifest | Medium | `fig-build-figure-set` |
| `figure-set-audit` | Fidelity | Cross-figure consistency report | High | `fig-audit-figure-set` |
| `submission-package-build` | Fidelity | Hash-indexed submission package | Medium | `fig-build-submission-package` |
| `submission-readiness` | Fidelity | Full figure set readiness decision | Very High | `fig-audit-readiness` |
| `pipeline-status` | Fidelity | Project-local pipeline dashboard | Medium | `fig-status` |
| `library-planning` | Fidelity | Dependency plan and library rationale | High | `fig-plan-libraries` |
| `environment-probe` | Fidelity | Import/version availability report | Low | `fig-probe-environment` |
| `render-stack-selection` | Fidelity | Minimal Python render stack selection | High | `fig-select-render-stack` |
| `external-data-planning` | Fidelity | Data acquisition decision and provenance blockers | Very High | `fig-plan-external-data` |

## Mode Rules

- `planning` can proceed without data, but must mark `DATA_STATUS: MISSING` or `MOCKUP`.
- `scoping` must not render or export files.
- `render` requires supplied data, code, or image assets.
- `registry-render` requires a matching render registry entry and required data columns.
- `library-planning`, `environment-probe`, and `render-stack-selection` must not install packages automatically.
- `external-data-planning` must not download data automatically and must record source, license, citation, role, and contamination risk when external data are proposed.
- `audit` can run on partial materials, but unverifiable gates must stay visible.
- `render-audit` checks output-file quality only; it does not prove scientific correctness.
- `style` can be `VERIFIED` only with current official or user-provided guidance.
- `full` must include `figure-auditor` before `export-packager`.
- Memory modes must use project-local `.codex/scientific-figure-memory/` files and must not store project memory in the installed skill folder.
- `memory-resume` requires a matching unconsumed Figure Passport boundary hash.

## Summary

| Spectrum | Modes |
|---|---|
| Fidelity | audit, render-audit, caption, style, export, memory-init, memory-load, memory-update, memory-forget, memory-resume, memory-migrate, repro-lock-audit, journal-verify, visual-artifact-audit, figure-set-build, figure-set-audit, submission-package-build, submission-readiness, pipeline-status, library-planning, environment-probe, render-stack-selection, external-data-planning |
| Balanced | render, registry-render, revision, full |
| Originality | planning, scoping |
