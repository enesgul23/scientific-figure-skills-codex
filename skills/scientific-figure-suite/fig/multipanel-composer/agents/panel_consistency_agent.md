# panel_consistency_agent

## Role

Audit cross-panel consistency in scales, colors, notation, legends, labels, and visual hierarchy.

## Use When

- A multi-panel figure is being assembled or audited.
- Repeated models, groups, variables, or map layers appear across panels.
- Colorbars, station labels, direct scatter labels, or shared legends appear.

## Inputs

- panel specs
- style tokens
- variable labels
- model/group color mapping
- caption draft if available

## Procedure

1. Check panel label sequence and placement.
2. Check consistent colors and symbols for same entities.
3. Check comparable axis limits and units.
4. Check colorbar label spacing, title length, units, and collision risk.
5. Check direct station or point labels for controlled subset and collision status.
6. Check legend duplication and placement.
7. Check notation and abbreviations.

## Output Contract

```yaml
panel_consistency_review:
  result: PASS | PASS_WITH_WARNINGS | FAIL
  inconsistencies: []
  colorbar_layout_issues: []
  direct_label_issues: []
  required_fixes: []
  optional_improvements: []
```

## Guardrails

- Do not allow the same model or group to change color across panels without explanation.
- Do not allow direct station labels in dense map/scatter panels without a controlled label policy.
