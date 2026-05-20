# Validation

Run the complete validation set from the repository root:

```powershell
python quick_validate.py
```

Run from the skill directory:

```powershell
python scripts/validate_skill.py .
python scripts/validate_contracts.py .
python scripts/validate_figure_spec.py tests/sample_figure_spec.yaml
python scripts/validate_visual_claim_ledger.py tests/sample_visual_claim_ledger.yaml
python scripts/validate_style_tokens.py
python scripts/validate_render_template_registry.py
python scripts/validate_library_pool.py
python scripts/validate_agentic_runbook.py tests/sample_agentic_runbook.json
python scripts/validate_repo_hygiene.py
python scripts/audit_multipanel_layout.py --layout tests/sample_multipanel_layout.yaml
python scripts/audit_text_layout.py --layout tests/sample_text_layout.yaml
python scripts/select_text_profile.py --domain model-performance --chart-type roc_pr_curve
python scripts/validate_memory.py --memory-dir tests/sample_memory/scientific-figure-memory
python scripts/audit_repro_lock.py --memory-dir tests/sample_memory/scientific-figure-memory
python scripts/build_pipeline_dashboard.py --memory-dir tests/sample_memory/scientific-figure-memory --no-update-manifest
python scripts/build_agentic_runbook.py --memory-dir tests/sample_memory/scientific-figure-memory --out agentic_runbook.json
python scripts/advance_agentic_runbook.py --runbook agentic_runbook.json --out agentic_run_report.json
python scripts/validate_handoff_artifact.py tests/sample_figure_intake.yaml --type figure_intake
python scripts/validate_handoff_artifact.py tests/sample_journal_style_report.yaml --type journal_style_report
python scripts/validate_handoff_artifact.py tests/sample_caption_package.yaml --type caption_package
python scripts/validate_handoff_artifact.py tests/sample_quality_report.yaml --type figure_quality_report
python scripts/validate_handoff_artifact.py tests/sample_submission_manifest.json --type submission_manifest
```

Expected result: all commands return `PASS`.

`quick_validate.py` also performs temporary render-registry smoke tests and
render-quality checks outside the skill package. It also smoke-tests dataset
inspection, environment probing, dependency planning, render with a dependency
plan, external data plan validation, v0.7 multi-panel layout audit behavior,
and v0.8 text layout audit and repair behavior.
v0.9 validation also covers agentic runbook construction, next-action dry runs,
shell helper syntax, shell doctor smoke tests, and repository hygiene checks.

Shell helper checks:

```bash
bash -n scripts/bin/*.sh
bash scripts/bin/sfs-validate.sh --no-quick
bash scripts/bin/sfs-doctor.sh
```
