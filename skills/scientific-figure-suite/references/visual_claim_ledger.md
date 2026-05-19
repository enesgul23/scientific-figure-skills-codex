# Visual Claim Ledger

A visual claim ledger prevents figures from making unsupported visual claims.

## Schema

```yaml
visual_claim_ledger:
  figure_id: figure_01
  generated_at:
  data_status: PROVIDED | MISSING | MOCKUP
  claims:
    - id: C1
      claim_text:
      claim_type: descriptive | comparative | causal | predictive | mechanistic | methodological
      visual_element:
      data_source:
      computation_source:
      support_status: supported | partially_supported | unsupported | unverifiable
      uncertainty_shown: true | false | not_applicable
      caption_alignment: aligned | overclaims | underexplains
      risk_level: low | medium | high
      required_fix:
```

## Mandatory Rule

Every visual element that implies a result must map to a data source, computation source, or explicit design-only label.

## Claim Types

- `descriptive`: states what is visible.
- `comparative`: compares groups, models, places, or time periods.
- `causal`: states that one factor causes another.
- `predictive`: states predictive performance or forecast behavior.
- `mechanistic`: states biological, physical, or engineering mechanism.
- `methodological`: states workflow, protocol, or data-processing design.

## Examples

```yaml
- id: C1
  claim_text: "Observed discharge peaks on day 4."
  claim_type: descriptive
  visual_element: "panel a hydrograph"
  data_source: "discharge.csv column Q_obs"
  computation_source: "draw_fig01.py"
  support_status: supported
  uncertainty_shown: not_applicable
  caption_alignment: aligned
  risk_level: low
  required_fix: ""
```

```yaml
- id: C2
  claim_text: "Groundwater coupling causes improved flood prediction."
  claim_type: causal
  visual_element: "panel d mechanism arrow"
  data_source: ""
  computation_source: ""
  support_status: unsupported
  uncertainty_shown: false
  caption_alignment: overclaims
  risk_level: high
  required_fix: "Rephrase as hypothesis or provide causal evidence."
```
