from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Any

from _common import load_structured_file, main_error, write_json
from _memory import utc_now
from validate_agentic_runbook import root, validate


WHITELISTED_SCRIPT_ALIASES = {
    "fig-status": ["scripts/build_pipeline_dashboard.py"],
    "fig-build-figure-set": ["scripts/build_figure_set_manifest.py"],
    "fig-audit-figure-set": ["scripts/audit_figure_set_consistency.py"],
    "fig-audit-readiness": ["scripts/audit_submission_readiness.py"],
    "fig-audit-render": ["scripts/audit_render_quality.py"],
    "fig-audit-multipanel-layout": ["scripts/audit_multipanel_layout.py"],
    "fig-audit-text-layout": ["scripts/audit_text_layout.py"],
    "fig-plan-libraries": ["scripts/build_dependency_plan.py"],
}


def selected_action(runbook: dict[str, Any]) -> dict[str, Any]:
    action = runbook.get("next_action")
    if isinstance(action, dict) and action.get("alias"):
        return action
    for stage in runbook.get("stages", []) or []:
        if not isinstance(stage, dict):
            continue
        action = stage.get("recommended_action")
        if isinstance(action, dict) and action.get("alias"):
            return action
    return {"alias": "fig-audit-readiness", "reason": "No action found.", "approval_required": False, "gated": False, "command": []}


def build_report(runbook: dict[str, Any], action: dict[str, Any], executed: bool, blocked: bool, output: str = "") -> dict[str, Any]:
    return {
        "agentic_run_report": {
            "created_at": utc_now(),
            "run_id": runbook.get("run_id"),
            "project_id": runbook.get("project_id"),
            "dry_run": not executed,
            "blocked": blocked,
            "selected_action": action,
            "output": output,
        }
    }


def execute_action(skill_dir: Path, action: dict[str, Any]) -> tuple[bool, str]:
    alias = str(action.get("alias") or "")
    if action.get("approval_required") is True or action.get("gated") is True:
        return True, "Action is approval-gated and was not executed."
    if alias not in WHITELISTED_SCRIPT_ALIASES:
        return True, f"Alias is not whitelisted for execution: {alias}"
    command = [sys.executable, *WHITELISTED_SCRIPT_ALIASES[alias]]
    result = subprocess.run(command, cwd=skill_dir, text=True, capture_output=True, check=False)
    output = "\n".join(part for part in [result.stdout.strip(), result.stderr.strip()] if part)
    return result.returncode != 0, output


def main() -> None:
    parser = argparse.ArgumentParser(description="Advance an agentic runbook by selecting the next safe action.")
    parser.add_argument("--runbook", required=True)
    parser.add_argument("--skill-dir", default=Path(__file__).resolve().parents[1])
    parser.add_argument("--out", default="")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    try:
        errors, _warnings = validate(Path(args.runbook))
        if errors:
            raise ValueError("invalid runbook: " + "; ".join(errors))
        runbook = root(load_structured_file(args.runbook))
        action = selected_action(runbook)
        blocked = False
        output = ""
        executed = False
        if args.execute:
            blocked, output = execute_action(Path(args.skill_dir).resolve(), action)
            executed = not blocked
        report = build_report(runbook, action, executed=executed, blocked=blocked, output=output)
        if args.out:
            write_json(args.out, report)
            print(f"[AGENTIC-NEXT] wrote {args.out}")
        print(__import__("json").dumps(report, indent=2, sort_keys=True))
        if blocked and args.execute:
            raise SystemExit(1)
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
