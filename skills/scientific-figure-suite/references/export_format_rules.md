# Export Format Rules

Use this reference for final figure packaging.

## Format Selection

- Use PDF or SVG for graphs, line art, schematics, and mixed text/vector figures.
- Use TIFF or high-resolution PNG for photographs, microscopy, medical imaging, heatmaps, and raster maps.
- Use EPS only when the journal or production workflow requires it.
- Keep text as editable/embedded text for line art whenever possible.

## Minimum Package

```text
figure_01.pdf
figure_01.svg
figure_01_300dpi.png or figure_01_300dpi.tiff
figure_01_code.py or figure_01_code.R
figure_01_spec.yaml
figure_01_caption.md
figure_01_alt_text.md
figure_01_quality_report.md
submission_manifest.json
```

## Checks

- file names are stable and descriptive
- outputs are listed in manifest
- data and code paths are repository-relative
- style status is preserved
- unresolved journal requirements are not hidden
- no machine-specific local paths appear in released artifacts
