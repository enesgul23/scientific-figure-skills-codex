---
description: Select the minimal Python render stack for a chart type and dataset profile
---

Use dataset inspection, the renderer registry, the library pool, and optional
environment probe results to select a minimal Python-first stack.

Preferred script:

```powershell
python scripts/select_library_stack.py --chart-type <chart_type> --dataset-profile dataset_profile.json --environment-probe environment_probe.json --out library_stack_selection.json
```

For final manuscript artwork, prefer the static matplotlib-based stack unless
the user explicitly asks for an interactive supplement or dashboard.
