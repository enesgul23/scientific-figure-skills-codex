# Figure Set Submission Runtime

## Purpose

Defines the manuscript-level runtime. v0.4 aggregates individual figure and
panel memory into a figure set, indexes exported package files, checks
cross-figure consistency, and records a submission-readiness decision. v0.6
adds render-quality, dependency-plan, and external-data decision evidence as
readiness inputs. v0.7 adds multi-panel layout audit evidence for optical-grid,
colorbar, semantic color, and direct-label risks. v0.8 adds text layout audit
evidence for overlap, clipping, colorbar-title crowding, and terminology.

## Memory Files

Project-local files:

```text
.codex/scientific-figure-memory/
  figure_set_manifest.json
  submission_package_index.json
  cross_figure_consistency_history.jsonl
  submission_readiness_history.jsonl
  visual_regression_history.jsonl
  multipanel_layout_history.jsonl
  text_layout_history.jsonl
  dependency_plan_history.jsonl
  external_data_plan_history.jsonl
```

These files are project memory. Do not place real project content inside the
installed skill directory.

## Runtime Sequence

1. Validate memory.
2. Run repro-lock audit and resolve stale figures or panels.
3. Build `figure_set_manifest.json` from Figure Passport.
4. Audit cross-figure consistency.
5. Build `submission_package_index.json` from exported files.
6. Audit render quality and visual regression for exported files when outputs exist.
7. Audit multi-panel layout quality when figures include multiple panels,
   colorbars, map/scatter labels, or shared legends.
8. Audit text layout quality before final readiness when text layout artifacts
   or exported SVG-derived text boxes are available.
9. Audit submission readiness.
10. Append readiness decision to `submission_readiness_history.jsonl`.

## Figure Set Manifest

The figure set manifest summarizes every figure intended for the manuscript:

- figure id
- title and purpose
- current version
- target journal/style status
- data/reproducibility/integrity status
- stale status
- output files
- panel count
- unresolved requirements

This manifest is derived from Figure Passport. Do not manually use it to hide
stale or unresolved figure state.

## Cross-Figure Consistency

Check:

- figure ids are unique and ordered
- style status does not silently mix `VERIFIED` and `UNVERIFIED`
- target journal and article context are consistent or explicitly justified
- panel labels follow one convention
- output format availability is consistent for comparable figures
- stale figures are visible
- captions, alt text, visual claims, and audit artifacts exist where required
- latest render-quality audit has not failed
- latest multi-panel layout audit has not failed when applicable
- latest text layout audit has not failed when applicable

## Submission Package Index

The package index records exported package files with SHA-256 hashes, roles, and
figure links. It is not a ZIP builder. It is an integrity index for whatever
package directory or file list the user provides.

## Readiness Decision

Allowed readiness results:

- `READY`: no blockers and journal status is verified or explicitly waived.
- `READY_WITH_WARNINGS`: no blockers but warnings remain.
- `BLOCKED`: stale artifacts, missing required files, missing data/code for
  data-derived figures, failed layout/render audits, missing audit evidence, or
  unsupported journal claims.
- `NOT_RUN`: readiness was not evaluated.

Do not use "submission-ready" wording unless the result is `READY` and the
journal target is `VERIFIED`, or the user explicitly accepts an unverified
journal waiver for internal review.
