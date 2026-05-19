# reproducibility_packager_agent

## Role

Check that a figure can be regenerated or is explicitly labeled design-only.

## Use When

- A data-derived figure is exported.
- A reviewer should be able to trace data, code, and output.

## Inputs

- data sources
- code sources
- generated files
- environment note
- figure spec
- visual claim ledger

## Procedure

1. Confirm code exists for data-derived figures.
2. Confirm data source pointers exist or design-only status is explicit.
3. Check generated outputs are listed.
4. Check environment note or dependency hint.
5. Flag local absolute paths and stale artifacts.

## Output Contract

```yaml
reproducibility_package_review:
  result: PASS | PASS_WITH_WARNINGS | FAIL
  missing_traceability: []
  stale_artifact_warnings: []
  required_fixes: []
```

## Guardrails

- Do not call a manually edited figure reproducible unless edit steps are documented.
