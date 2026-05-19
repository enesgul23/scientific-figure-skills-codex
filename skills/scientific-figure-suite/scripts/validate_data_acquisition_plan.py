from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from _common import exit_with_results, load_structured_file, main_error


VALID_DECISIONS = {"NOT_REQUIRED", "RECOMMENDED_WITH_APPROVAL", "BLOCKED_PENDING_SOURCE", "REJECTED"}
VALID_ROLES = {"contextual", "evidentiary", "benchmark", "annotation"}
VALID_STATUSES = {"planned", "needs_user_source", "ready_for_user_approval", "rejected"}
VALID_CONTAMINATION = {"none", "low", "medium", "high", "unknown"}


def validate_plan(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    data = load_structured_file(path)
    if not isinstance(data, dict):
        return ["data acquisition plan must be a JSON object"], warnings
    plan = data.get("data_acquisition_plan", data)
    if not isinstance(plan, dict):
        return ["data_acquisition_plan must be an object"], warnings
    decision = plan.get("decision")
    if decision not in VALID_DECISIONS:
        errors.append("data_acquisition_plan.decision has invalid value")
    if plan.get("download_allowed") is True:
        errors.append("v0.6.0 plans must not set download_allowed true")
    if not isinstance(plan.get("approval_required"), bool):
        errors.append("approval_required must be boolean")
    items = plan.get("items", [])
    if not isinstance(items, list):
        errors.append("items must be a list")
        items = []
    if decision in {"RECOMMENDED_WITH_APPROVAL", "BLOCKED_PENDING_SOURCE"} and not items:
        errors.append(f"{decision} requires at least one external data item")
    if decision == "NOT_REQUIRED" and items:
        warnings.append("NOT_REQUIRED plan contains items; check whether decision should be RECOMMENDED_WITH_APPROVAL")

    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            errors.append(f"item {index} must be an object")
            continue
        if item.get("usage_role") not in VALID_ROLES:
            errors.append(f"item {index}: invalid usage_role")
        if not item.get("scientific_justification"):
            errors.append(f"item {index}: scientific_justification is required")
        if item.get("status") not in VALID_STATUSES:
            errors.append(f"item {index}: invalid status")
        if item.get("contamination_risk") not in VALID_CONTAMINATION:
            errors.append(f"item {index}: invalid contamination_risk")
        if decision == "RECOMMENDED_WITH_APPROVAL":
            for field in ["source_url", "license", "citation"]:
                if not item.get(field):
                    errors.append(f"item {index}: RECOMMENDED_WITH_APPROVAL requires {field}")
        if item.get("usage_role") == "benchmark" and item.get("contamination_risk") in {"none", "low"}:
            warnings.append(f"item {index}: benchmark data should explicitly assess contamination risk")
    blockers = plan.get("blockers", [])
    if decision == "BLOCKED_PENDING_SOURCE" and not blockers:
        errors.append("BLOCKED_PENDING_SOURCE requires blockers")
    if not isinstance(blockers, list):
        errors.append("blockers must be a list")
    if not isinstance(plan.get("risks", []), list):
        errors.append("risks must be a list")
    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a Scientific Figure Suite data acquisition plan.")
    parser.add_argument("plan")
    args = parser.parse_args()
    try:
        errors, warnings = validate_plan(Path(args.plan))
        exit_with_results(errors, warnings)
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
