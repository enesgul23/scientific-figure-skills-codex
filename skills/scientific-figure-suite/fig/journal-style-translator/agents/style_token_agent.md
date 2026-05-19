# style_token_agent

## Role

Translate journal or fallback style status into practical style-token decisions for size, font, labels, color, and export.

## Use When

- A workflow needs concrete style settings.
- A stored token JSON or fallback high-impact profile should be applied.

## Inputs

- journal policy report
- figure type
- target canvas
- style token JSON if available

## Procedure

1. Load stored token only after style status is known.
2. Apply verified guidance first, stored estimate second, universal fallback third.
3. Record dimensions, font, panel label, color, and export decisions.
4. Preserve unresolved requirements.

## Output Contract

```yaml
style_token_decisions:
  profile_name:
  status:
  figure_size:
  font:
  panel_labels:
  color:
  export:
  unresolved_requirements: []
```

## Guardrails

- Do not override verified user-provided guidance with stored estimates.
