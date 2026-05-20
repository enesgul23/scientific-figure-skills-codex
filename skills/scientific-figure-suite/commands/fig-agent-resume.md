# fig-agent-resume

Resume planning from project-local memory by rebuilding the dashboard and
agentic runbook. This is a planning action; it does not render or mutate project
memory unless a later explicit command does so.

```bash
python scripts/build_agentic_runbook.py --memory-dir .codex/scientific-figure-memory --out agentic_runbook.json
python scripts/advance_agentic_runbook.py --runbook agentic_runbook.json
```
