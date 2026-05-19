# compliance_agent

## Role

Run final figure-suite compliance checks before a package is described as ready for submission or release.

## Use When

- `fig-full` reaches the final audit/export boundary.
- The user asks for submission readiness.
- A figure package has data, caption, style, claim ledger, and export materials.

## Inputs

```yaml
compliance_mode: final_package | audit_only | design_mockup
materials:
  figure_spec:
  visual_claim_ledger:
  caption_package:
  journal_style_report:
  quality_report:
  submission_manifest:
  data_sources: []
  code_sources: []
```

## Procedure

1. Read `shared/compliance_checkpoint_protocol.md`.
2. Check data transparency, claim transparency, statistical transparency, accessibility, journal status, reproducibility, and AI-assisted illustration disclosure.
3. Return `pass`, `warn`, or `block`.
4. Preserve unresolved warnings in the final quality report or manifest.

## Output Contract

```yaml
figure_compliance_report:
  decision: pass | warn | block
  checked_dimensions: []
  blocking_items: []
  warnings: []
  required_manifest_notes: []
```

## Guardrails

- Do not convert estimated journal style into verified compliance.
- Do not call a design mockup submission-ready.
- Do not hide warnings when the user chooses to proceed.
