# fig-agent-next

Select the next safe action from an agentic runbook. Default behavior is dry-run.
Use `--execute` only for whitelisted suite scripts and never for installs,
downloads, deletion, pushes, or verified journal checks.

```bash
python scripts/advance_agentic_runbook.py --runbook agentic_runbook.json --out agentic_run_report.json
```
