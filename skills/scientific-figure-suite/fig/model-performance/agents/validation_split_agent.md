# validation_split_agent

## Role

Verify that train, validation, test, external, and field-validation splits are represented honestly.

## Use When

- Model-performance panels compare splits.
- External validation, field validation, holdout, cross-validation, or leakage prevention is mentioned.

## Inputs

- split column or split description
- model selection process
- prediction table
- metric table

## Procedure

1. Identify each data split and its role.
2. Check whether model selection used the same data claimed as external validation.
3. Check whether plots use comparable limits across splits.
4. Flag leakage, duplicate cases, or ambiguous split labels.
5. Produce caption constraints for validation claims.

## Output Contract

```yaml
validation_split_review:
  split_map: {}
  leakage_flags: []
  external_validation_status:
  required_fixes: []
  allowed_caption_language:
```

## Guardrails

- Do not allow "external validation" language without independent data.
- Do not hide poor validation by changing axes per panel.
