from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from _common import exit_with_results, load_structured_file, main_error
from build_agentic_runbook import RUNBOOK_STAGES


VALID_STATUS = {"DONE", "READY", "BLOCKED", "WAITING", "NOT_STARTED"}
BLOCKED_ALIASES = {"pip", "conda", "git", "curl", "wget", "fig-verify-journal-download"}


def root(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError("agentic runbook must be a JSON object")
    runbook = data.get("agentic_runbook", data)
    if not isinstance(runbook, dict):
        raise ValueError("agentic_runbook must be an object")
    return runbook


def validate(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    runbook = root(load_structured_file(path))
    for field in ["schema_version", "created_at", "run_id", "project_id", "mode", "stages", "next_action", "guardrails"]:
        if field not in runbook:
            errors.append(f"missing required field: {field}")
    stages = runbook.get("stages", [])
    if not isinstance(stages, list) or not stages:
        errors.append("stages must be a non-empty list")
        return errors, warnings
    seen: set[str] = set()
    for index, item in enumerate(stages, start=1):
        if not isinstance(item, dict):
            errors.append(f"stage {index}: must be an object")
            continue
        name = str(item.get("stage") or "")
        status = str(item.get("status") or "")
        if name not in RUNBOOK_STAGES:
            errors.append(f"stage {index}: invalid stage {name}")
        if name in seen:
            errors.append(f"duplicate stage: {name}")
        seen.add(name)
        if status not in VALID_STATUS:
            errors.append(f"{name}: invalid status {status}")
        action = item.get("recommended_action")
        if action is not None and not isinstance(action, dict):
            errors.append(f"{name}: recommended_action must be an object or null")
        if isinstance(action, dict):
            alias = str(action.get("alias") or "")
            if not alias:
                errors.append(f"{name}: recommended_action.alias is required")
            if alias in BLOCKED_ALIASES:
                errors.append(f"{name}: unsafe alias is forbidden")
            if action.get("approval_required") is True and action.get("gated") is not True:
                warnings.append(f"{name}: approval-required action should be marked gated")
    missing = [stage for stage in RUNBOOK_STAGES if stage not in seen]
    if missing:
        errors.append("missing stages: " + ", ".join(missing))
    next_action = runbook.get("next_action")
    if not isinstance(next_action, dict) or not next_action.get("alias"):
        errors.append("next_action.alias is required")
    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate an agentic Scientific Figure Suite runbook.")
    parser.add_argument("runbook")
    args = parser.parse_args()
    try:
        errors, warnings = validate(Path(args.runbook))
        exit_with_results(errors, warnings)
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
