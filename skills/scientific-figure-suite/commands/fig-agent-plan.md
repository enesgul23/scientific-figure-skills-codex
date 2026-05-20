# fig-agent-plan

Build an agentic runbook from project memory and optional intake or dataset
artifacts. Do not render, install packages, download data, or change memory.

```bash
python scripts/build_agentic_runbook.py --memory-dir .codex/scientific-figure-memory --out agentic_runbook.json
python scripts/validate_agentic_runbook.py agentic_runbook.json
```
