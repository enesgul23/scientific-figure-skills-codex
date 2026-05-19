---
description: Build project-local figure pipeline dashboard
---

Read `shared/figure_memory_protocol.md`, then run the pipeline-state dashboard
workflow.

Preferred script:

```powershell
python scripts/build_pipeline_dashboard.py --memory-dir <memory-dir>
```

Use `--out <dashboard.json>` when the user asks for a file artifact. The
dashboard reports active stage, completed stages, blocked stages, stale figures,
journal status, latest consistency/render/readiness results, and next actions.
