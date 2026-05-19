# Journal Style Profiles

Journal and publisher rules are living constraints. Treat these profiles as stored estimates unless the active task includes current official guidance or user-provided current guidance.

## Status Model

```yaml
style_status:
  VERIFIED: official current guideline checked in this task or provided by user
  ESTIMATED: stored profile used, not checked live in this task
  UNVERIFIED: no reliable profile available
```

## Nature Estimated Profile

```yaml
nature_estimated:
  status: ESTIMATED
  requires_live_verification: true
  single_column_width_mm: 89
  double_column_width_mm: 183
  one_and_half_column_width_mm: [120, 136]
  page_depth_mm: 247
  font: [Helvetica, Arial]
  panel_label: "8 pt bold upright lowercase"
  other_text_range_pt: [5, 7]
  line_weight_pt: [0.25, 1.0]
  raster_photo_dpi: [300, 600]
  vector_preferred: true
  color_space: "RGB recommended, CMYK acceptable"
```

## Placeholder Profiles

Use this pattern for Science, The Lancet, Cell, NEJM, JAMA, BMJ, PNAS, IEEE, Elsevier, and Springer Nature until verified:

```yaml
profile:
  status: UNVERIFIED
  requires_live_guideline_check: true
  dimensions: unknown_until_verified
  accepted_formats: unknown_until_verified
  resolution: unknown_until_verified
  font_rules: unknown_until_verified
  caption_rules: unknown_until_verified
```

## Universal High-Impact Fallback

```yaml
universal_high_impact:
  status: ESTIMATED
  vector_default: true
  raster_min_dpi: 300
  formats: [PDF, SVG, EPS, TIFF, PNG]
  font: [Arial, Helvetica, DejaVu Sans]
  min_text_size_pt: 6
  preferred_text_size_pt: [7, 9]
  panel_labels: lowercase_bold_upright
  accessibility: colorblind_safe
  avoid:
    - 3D effects
    - pie charts unless composition is the scientific message
    - rainbow maps
    - red-green-only contrast
    - unsupported dual y-axis
    - truncated axes without disclosure
    - unlabelled units
    - missing uncertainty
```

## Compliance Language

Allowed:

- `Nature-inspired estimated profile`
- `Target-journal style estimate pending guideline verification`
- `Verified against user-provided journal instructions dated [date]`

Forbidden unless status is `VERIFIED`:

- `Nature-compliant`
- `Science-compliant`
- `Lancet-compliant`
- `submission-ready for [journal]`
