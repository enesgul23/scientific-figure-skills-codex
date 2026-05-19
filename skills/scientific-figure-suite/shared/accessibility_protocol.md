# Accessibility Protocol

Use for figure creation, audit, and packaging.

## Minimum Checks

- Palette is listed.
- Red-green-only encoding is absent.
- Critical distinctions have non-color redundancy.
- Minimum text size is recorded.
- Contrast is not unknown.
- Alt text is present for final packages.

## Color Guidance

- Use colorblind-aware categorical palettes.
- Use sequential colormaps for ordered magnitude.
- Use diverging colormaps only with a meaningful center.
- Avoid rainbow maps unless strongly justified and labeled.

## Alt Text Quality

Alt text should include:

- figure type
- panel structure
- variables and groups
- main visible pattern
- caveats about mockup, missing data, or uncertainty

## Accessibility Failure

Return `FAIL` if critical information is color-only, text is unreadable at final
size, or a final package lacks alt text.
