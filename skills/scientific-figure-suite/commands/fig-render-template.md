---
description: Render a data-driven figure from the render template registry
---

Read `assets/render_registry/render_registry.json`, then use the selected
registry template.

Preferred script:

```powershell
python scripts/render_from_registry.py --chart-type <chart_type> --data <data.csv> --outdir <outdir>
```

When a dependency plan exists, pass it before rendering:

```powershell
python scripts/render_from_registry.py --chart-type <chart_type> --data <data.csv> --outdir <outdir> --dependency-plan dependency_plan.json
```

Use `--column role=column_name` when the user's data column names differ from
the registry defaults. Do not invent data. If required columns are missing,
return the missing roles and ask for a corrected table.
