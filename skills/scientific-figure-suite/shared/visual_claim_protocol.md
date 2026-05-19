# Visual Claim Protocol

Use this protocol whenever a figure, caption, or graphical abstract implies a
scientific result.

## Claim Classes

- `descriptive`: what is visible.
- `comparative`: difference or similarity between groups, models, places, or times.
- `predictive`: model or forecast performance.
- `causal`: one factor causes another.
- `mechanistic`: biological, physical, clinical, or engineering mechanism.
- `methodological`: workflow, protocol, data lineage, or model-lock claim.

## Support Status

- `supported`: supplied data/code directly supports the claim.
- `partially_supported`: evidence exists but a caveat is required.
- `unsupported`: no supplied evidence supports the claim.
- `unverifiable`: current materials are insufficient to verify.

## Blocking Rules

- Unsupported causal and mechanistic claims must be removed, rephrased as hypotheses, or supported with evidence.
- Captions must not upgrade `partially_supported` or `unverifiable` claims.
- Design-only graphics must mark evidence-bearing-looking elements as illustrative.
- If the ledger is missing for a complete package, `figure-auditor` should return `FAIL`.
