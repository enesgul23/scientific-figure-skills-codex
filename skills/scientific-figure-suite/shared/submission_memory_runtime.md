# Submission Memory Runtime

## Purpose

Defines the v0.3 submission-grade runtime layer. Figure memory is no longer only
an optional project notebook; it participates in workflow entry, figure updates,
quality audits, export packaging, stale detection, resume boundaries, pipeline
status dashboards, render-quality evidence, multi-panel layout evidence, and
text layout evidence. v0.9 adds agentic runbooks and next-action reports.

## Workflow Integration

Every workflow must apply this memory sequence when project memory exists or the
user asks to continue a project:

1. Load `.codex/scientific-figure-memory/memory_manifest.json`.
2. Validate memory with `scripts/validate_memory.py`.
3. Read active figure, journal targets, dataset registry, and unresolved
   requirements.
4. Before producing new work, check whether the relevant figure or panel is
   stale by repro-lock.
5. After producing or auditing work, update the Figure Passport and append
   audit, claim, journal verification, visual artifact, decision, visual
   regression, multipanel-layout, text-layout, dependency-plan, or
   external-data-plan ledger, plus agentic run history when a runbook is used
   entries.
6. If pausing or moving to another session, create a Figure Passport reset
   boundary.

If memory is absent, continue normally and offer `fig-init-memory` only when a
long-running or submission-grade project would benefit from it.

## Panel-Level Passport

Each multi-panel figure may contain `panels[]` under the Figure Passport figure
entry.

Panel fields:

- `panel_id`
- `purpose`
- `data_source`
- `claim_refs`
- `script_ref`
- `outputs`
- `status_tags`
- `repro_lock`
- `stale`
- `stale_reasons`

Panel state is more specific than figure state. If a panel is stale, the figure
is stale until the panel is rerendered or the stale reason is explicitly
resolved.

## Repro-Lock

Repro-lock records hashes for:

- data files
- code files
- output files
- environment note
- render command

Use `scripts/audit_repro_lock.py` to compare current files against stored
hashes. Hash drift must not be ignored. Mark the relevant panel or figure as
stale and require rerender or re-audit before submission packaging.

## Journal Verification Ledger

Use `journal_guideline_verification.jsonl` for current guideline evidence.
`journal_targets.json` can be `VERIFIED` only when the ledger includes a current
entry with `source_type: live_official` or `source_type: user_provided` for that
journal.

Stored estimates remain useful for planning, but they do not satisfy verified
submission readiness.

## Visual Audit Artifact Ledger

Use `visual_audit_artifact.jsonl` for file-level evidence:

- file path
- SHA-256 hash
- format
- byte size
- dimensions when available
- audit result
- gate summary

Quality reports summarize findings; visual audit artifacts preserve the file
identity that was actually checked.

## Visual Regression Ledger

Use `visual_regression_history.jsonl` for render-quality evidence:

- expected output formats
- hashes and byte sizes
- raster dimensions and pixel variance
- blank or near-blank detection
- SVG text/title presence
- optional baseline comparison

This ledger is a render sanity check. It does not replace statistical,
scientific, journal, or caption integrity review.

## Multipanel Layout Ledger

Use `multipanel_layout_history.jsonl` for layout evidence:

- panel box geometry and overlap
- same-row top/bottom alignment
- colorbar bbox, label collision, and spacing checks
- semantic color consistency across panels
- controlled direct station or point labels in maps/scatter panels
- manual axes fallback when automatic layout is insufficient

This ledger answers whether the optical grid is credible. It does not replace
render-quality, statistical, scientific, journal, or caption review.

## Text Layout Ledger

Use `text_layout_history.jsonl` for text layout evidence:

- text-text overlap and minimum spacing
- text overflow beyond figure or axes bounds
- minimum font size and excessive rotation
- colorbar title length, placement, and crowding
- direct-label density and collision control
- bundled domain terminology and vague-label checks

`FAIL` blocks readiness until text layout is repaired and re-audited.

## Dependency Plan Ledger

Use `dependency_plan_history.jsonl` when a figure uses or plans a render stack.
The latest plan should list required, recommended, optional, and blocked
libraries. Missing required libraries block registry rendering until the user
installs them or approves a fallback.

## External Data Plan Ledger

Use `external_data_plan_history.jsonl` when a figure may require basemaps,
boundaries, benchmarks, evidence-bearing external records, or annotation
resources. Plans are append-only and must record whether the decision is
`NOT_REQUIRED`, `RECOMMENDED_WITH_APPROVAL`, `BLOCKED_PENDING_SOURCE`, or
`REJECTED`.

## Agentic Run Ledger

Use `agentic_run_history.jsonl` for dry-run or whitelisted execution reports.
Use `agentic_task_queue.jsonl` only for explicit queued runbook tasks. These
ledgers must not record hidden package installation, external data download,
deletion, Git push, or journal verification automation.

## Submission-Grade Acceptance

A submission-grade package should have:

- validated memory
- no stale figure or panel repro-locks
- journal target `VERIFIED` or explicit unresolved `UNVERIFIED/ESTIMATED` status
- visual audit artifact for every exported final file
- latest visual regression/render-quality audit not failed
- latest multi-panel layout audit not failed when multi-panel figures,
  colorbars, maps, scatter labels, or shared legends are present
- latest text layout audit not failed when text layout evidence is available
- latest dependency plan has no unresolved required-library blockers for rendered outputs
- external data plans are either `NOT_REQUIRED` or have complete provenance and user approval
- latest agentic next action has no unresolved blocker when agentic mode is used
- quality audit history with latest gate results
- Figure Passport reset/resume ledger cleanly consumed or no pending boundary
- export manifest that references the same file hashes as audit artifacts
