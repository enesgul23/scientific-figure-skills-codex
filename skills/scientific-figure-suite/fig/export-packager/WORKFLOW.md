# Export Packager

## Purpose

Prepare final scientific figure submission packages with formats, manifests, captions, alt text, source data pointers, code pointers, and reproducibility metadata.

## Trigger Conditions

Use when the user asks to export, package, submit, produce PDF/SVG/EPS/TIFF/PNG files, build a manifest, or assemble a reproducible figure bundle.

## Required Inputs

- figure code or source image
- target formats
- style profile or export constraints
- figure ID

## Optional Inputs

- target journal
- file naming convention
- DPI requirement
- data sources
- quality report
- visual regression/render-quality report

## Output Contract

Produce export files or exact export commands plus `submission_manifest.json`.

Typical package:

```text
figure_01.pdf
figure_01.svg
figure_01_300dpi.png
figure_01_300dpi.tiff
figure_01_code.py
figure_01_spec.yaml
figure_01_caption.md
figure_01_alt_text.md
figure_01_quality_report.md
submission_manifest.json
```

## Procedure

1. Choose vector formats for line art and graph text.
2. Choose raster formats and DPI for photographs, microscopy, heatmaps, or raster maps.
3. Check font embedding and avoid rasterized text for line art.
4. Build manifest with code, data, captions, alt text, quality report, and style status.
5. Run or require render-quality audit for exported files when preparing a final package.
6. Use repository-relative paths in manifests.
7. Mark unresolved journal requirements instead of claiming final submission readiness.

## Quality Gates

- formats match figure type
- raster DPI is sufficient
- manifest is complete
- code and data are linked
- style status is preserved
- file names are stable and descriptive

## Failure Modes

- figure cannot render
- code or source image is missing
- requested file format is unsupported
- fonts are unembedded or text is outlined unexpectedly
- data pointer is absent for a data-derived figure

## Memory Integration

If project memory exists, read `shared/submission_memory_runtime.md` and
validate memory before export. Refuse submission-grade packaging when required
figures or panels are stale, when journal status is incorrectly marked
`VERIFIED`, when exported files lack visual audit artifacts, or when the latest
visual regression report is `FAIL`. Update the Figure Passport and submission
manifest with output hashes and unresolved requirements.

## v0.6 Dependency Planning

Before packaging registry-rendered outputs, check whether a dependency plan
exists and whether any required library remained blocked at render time. If
external data were used, the package must include source, license, citation,
access date, hash, usage role, and approval status.

## Agent Role References

- `agents/export_manifest_agent.md` for final manifest and package completeness.
- `agents/reproducibility_packager_agent.md` for code/data/output traceability.

## Handoff Rules

Final stage. If export gates fail, return to the domain workflow, `journal-style-translator`, or `figure-auditor` as appropriate.
