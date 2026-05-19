# Accessibility And Color

Use this reference when selecting palettes, checking contrast, writing alt text, or auditing accessibility.

## Rules

- Do not encode critical distinctions by color alone.
- Avoid red-green-only contrasts.
- Prefer colorblind-aware palettes such as Okabe-Ito or carefully chosen categorical palettes.
- Use sequential colormaps for ordered continuous variables.
- Use diverging colormaps only when there is a meaningful center value.
- Avoid rainbow colormaps unless the domain has a strong convention and labels make interpretation clear.
- Keep gridlines and background secondary to data.
- Keep text readable at final print size.

## Minimum Accessibility Record

```yaml
accessibility:
  palette:
  colorblind_safe: true | false | unknown
  red_green_only: true | false
  min_font_size_pt:
  contrast_status: pass | warning | fail | unknown
  non_color_redundancy: true | false
  alt_text_present: true | false
```

## Alt Text Pattern

Write alt text that includes:

- figure type
- variables and groups
- main visible trend or comparison
- uncertainty or sample-size caveat when relevant
- warning if the figure is a design-only mockup
