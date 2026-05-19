---
description: Plan which Python plotting and data libraries are relevant for a supplied dataset or chart type
---

Read `assets/library_pool/library_pool.json`, inspect the dataset if present,
and build a dependency plan. Do not install packages.

Preferred scripts:

```powershell
python scripts/inspect_dataset.py --input <dataset> --out dataset_profile.json
python scripts/probe_python_environment.py --out environment_probe.json
python scripts/build_dependency_plan.py --chart-type <chart_type> --dataset-profile dataset_profile.json --environment-probe environment_probe.json --out dependency_plan.json
```

Report required, recommended, optional, and blocked libraries with rationale.
If heavy geospatial, omics, survival, 3D, or graph packages are selected, also
offer the lower-risk fallback stack.
