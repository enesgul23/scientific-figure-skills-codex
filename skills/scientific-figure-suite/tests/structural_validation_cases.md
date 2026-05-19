# Structural Validation Cases

These fixtures are used by the suite validators.

## Commands

```powershell
python scripts/validate_skill.py .
python scripts/validate_figure_spec.py tests/sample_figure_spec.yaml
python scripts/validate_visual_claim_ledger.py tests/sample_visual_claim_ledger.yaml
python scripts/validate_handoff_artifact.py tests/sample_figure_intake.yaml --type figure_intake
python scripts/validate_handoff_artifact.py tests/sample_journal_style_report.yaml --type journal_style_report
python scripts/validate_handoff_artifact.py tests/sample_caption_package.yaml --type caption_package
python scripts/validate_handoff_artifact.py tests/sample_quality_report.yaml --type figure_quality_report
python scripts/validate_handoff_artifact.py tests/sample_submission_manifest.json --type submission_manifest
```

## Expected

All commands should return `PASS` for the committed fixtures.
