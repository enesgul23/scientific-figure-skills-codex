---
description: Full scientific figure production package mode
---

Trigger `fig/intake-design/WORKFLOW.md`, then route through the necessary domain
workflow and downstream package stages.

Default chain:

```text
intake-design -> domain workflow -> multipanel-composer if needed -> fig-audit-multipanel-layout if needed -> journal-style-translator -> caption-alttext -> figure-auditor -> export-packager
```

Produce a complete package only when data, code, style status, caption, claim
ledger, quality gates, and export requirements are sufficiently resolved.
