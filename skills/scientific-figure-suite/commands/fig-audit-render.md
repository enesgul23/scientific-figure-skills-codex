---
description: Audit rendered figure files for visual QA and regression sanity
---

Use for file-level render-quality checks after figure export.

Preferred script:

```powershell
python scripts/audit_render_quality.py --figure-id <fig_id> --file <output.png> --file <output.svg> --expected-formats pdf,svg,png
```

Add `--append-memory --memory-dir <memory-dir>` when project memory is enabled.
The audit checks file presence, hashes, byte size, raster dimensions, blank or
near-blank raster output, SVG text/title presence, expected formats, and optional
baseline differences.

For multi-panel optical-grid, colorbar, semantic color, or direct station-label
issues, run `fig-audit-multipanel-layout` as a separate layout audit.
