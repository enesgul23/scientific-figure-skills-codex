# Cross-Model Verification

Cross-model review is optional and disabled by default.

## When Useful

- high-stakes clinical or biomedical figures
- journal submission package audits
- suspected unsupported visual claims
- complex multi-panel model-performance figures
- final graphical abstracts with mechanism claims

## Rule

Use another model or independent reviewer only when the user explicitly asks for cross-model or independent review. Do not claim cross-model verification unless it actually ran.

## Output Contract

```yaml
cross_model_review:
  enabled: true
  reviewer:
  materials_reviewed: []
  disagreements: []
  resolved_decisions: []
  unresolved_risks: []
```

## Default

If not run, write:

```yaml
cross_model_review:
  enabled: false
```
