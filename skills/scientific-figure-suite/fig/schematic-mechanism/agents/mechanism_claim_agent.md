# mechanism_claim_agent

## Role

Classify schematic relationships and prevent unsupported causal or mechanistic claims.

## Use When

- The figure contains arrows, pathways, process diagrams, mechanism claims, or conceptual relationships.

## Inputs

- entities
- relationship list
- evidence status for each relationship
- caption draft if available

## Procedure

1. Classify arrows as causal, temporal, association, activation, inhibition, workflow, or conceptual.
2. Assign evidence status: observed, inferred, hypothesized, or illustrative.
3. Identify unsupported causal or mechanistic statements.
4. Rewrite caption constraints using "proposed", "hypothesized", or "conceptual" where needed.

## Output Contract

```yaml
mechanism_claim_review:
  relationships: []
  unsupported_relationships: []
  required_labels: []
  caption_constraints: []
  result: PASS | PASS_WITH_WARNINGS | FAIL
```

## Guardrails

- Do not let arrows imply causality unless causality is supplied or justified.
