---
description: Decide whether a figure needs external data and create an auditable acquisition plan
---

Read `shared/external_data_decision_protocol.md`, then run or emulate
`scripts/plan_external_data.py`. Do not download internet data unless the user
explicitly asks and source, license, citation, and provenance are complete.

Preferred script:

```powershell
python scripts/plan_external_data.py --chart-type <chart_type> --dataset-profile dataset_profile.json --goal "<scientific goal>" --out data_acquisition_plan.json
python scripts/validate_data_acquisition_plan.py data_acquisition_plan.json
```

External data must be justified as contextual, evidentiary, benchmark, or
annotation data. "Make it look better" is not enough justification.
