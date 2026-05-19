# Visual Style Profile Protocol

## Purpose

Defines optional author, lab, or project visual style memory for scientific
figures. This is a soft guide for visual consistency, not a license to override
scientific accuracy, accessibility, or journal requirements.

Store the profile in project-local memory:

```text
.codex/scientific-figure-memory/author_visual_style_profile.json
```

## When to Use

Use only when the user asks to learn, reuse, load, update, or forget visual
style preferences, or when a project memory profile already exists and the user
asks to continue a figure project.

## Sample Sources

Acceptable style calibration sources:

- prior user-authored figures
- a manuscript figure set
- lab visual guidelines
- slide decks or graphical abstracts
- user-written notes about preferred figure style

Do not infer personal style from unrelated files without explicit permission.

## Extracted Dimensions

| Dimension | Examples |
|---|---|
| Palette behavior | colorblind-safe sets, grayscale preference, accent color restraint |
| Typography | font family, label density, panel-label style, minimum text size |
| Layout grammar | panel spacing, aspect ratios, inset usage, legend placement |
| Data density | sparse explanatory style vs dense journal-ready style |
| Annotation style | arrows, callouts, direct labels, statistical brackets |
| Uncertainty display | intervals, distributions, density, calibration panels |
| Domain idioms | hydrographs, forest plots, volcano plots, maps, confusion matrices |
| Export preferences | PDF/SVG/TIFF/PNG choices and review raster DPI |

## Priority Hierarchy

Apply visual style only under this order:

```text
truth > reproducibility > statistical honesty > accessibility > journal rules > project style > author visual style
```

If a style preference conflicts with accessibility or journal requirements, use
the stricter requirement and log the conflict in the Figure Passport or quality
audit history.

## Profile Status

Use:

- `NONE`: no profile exists.
- `PARTIAL`: profile built from fewer than three samples or mixed authorship.
- `USER_APPROVED`: user confirmed the profile.
- `STALE`: profile exists but conflicts with current journal or project rules.
- `FORGOTTEN`: profile was explicitly redacted.

## Forbidden Uses

Do not:

- use visual style memory as scientific evidence
- use style memory to justify invented data values
- call a figure submission-ready because it matches a profile
- store author style memory inside the installed skill directory
- preserve style memory after a confirmed forget request

