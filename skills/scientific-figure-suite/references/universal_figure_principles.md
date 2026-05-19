# Universal Figure Principles

Use this reference for any scientific figure task.

## Priority

Apply:

```text
truth > reproducibility > interpretability > journal compliance > visual elegance > novelty
```

## Core Rules

- Every figure must answer a scientific question.
- Every plotted value must be traceable to a supplied data source or rerunnable code.
- Use one visual grammar across a manuscript: fonts, colors, marker sizes, line widths, panel labels, notation, and export settings.
- Prefer compact, information-rich figures over decorative layouts.
- Never hide uncertainty, validation splits, censoring, missingness, outliers, domain shift, or model limitations.
- Use vector output for line art and high-resolution raster output for image data.

## Default Canvas

- Single-column width: about 89 mm.
- Double-column width: about 180 to 183 mm.
- Default manuscript DPI for raster review output: 300 to 450.
- Keep text readable at final print size.

## Default Typography

- Prefer Arial, Helvetica, or DejaVu Sans.
- Use 7 to 9 pt text for compact manuscript panels.
- Use bold mainly for panel labels.
- Avoid decorative fonts, outline text, shadows, and large panel titles.

## Default Panel Labels

- Use lowercase bold upright labels: `a`, `b`, `c`.
- Keep label placement consistent across the figure.
- Use panel subtitles for conditions, not generic chart names.

## Default Color Rules

- Use colorblind-aware palettes.
- Assign colors by semantic identity, not plotting order.
- Do not rely on color alone; add shape, pattern, direct labels, or panel separation when needed.
- Avoid rainbow colormaps, red-green-only contrasts, decorative gradients, glows, and busy backgrounds.

## Final Audit Questions

1. What data produced this figure?
2. What code produced this figure?
3. What claim does each panel support?
4. Is uncertainty represented or explicitly unavailable?
5. Can the caption be written without inventing information?
