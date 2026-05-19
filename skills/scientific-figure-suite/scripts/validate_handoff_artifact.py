from __future__ import annotations

import argparse
from typing import Any

from _common import VALID_DATA_STATUSES, VALID_STYLE_STATUSES, exit_with_results, load_structured_file, main_error


VALID_GATE_RESULTS = {"PASS", "PASS_WITH_WARNINGS", "FAIL", "NOT_APPLICABLE", "NOT_VERIFIABLE"}
VALID_INTEGRITY_STATUSES = {"PASS", "PASS_WITH_WARNINGS", "FAIL"}


def get_path(data: dict[str, Any], path: str) -> Any:
    current: Any = data
    for part in path.split("."):
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


def require(data: dict[str, Any], fields: list[str], errors: list[str]) -> None:
    for field in fields:
        value = get_path(data, field)
        if value in (None, "", []):
            errors.append(f"{field} is required")


def validate_intake(data: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    intake = data.get("figure_intake", data)
    if not isinstance(intake, dict):
        return ["figure_intake must be a mapping"], warnings
    require(
        intake,
        [
            "goal",
            "target_journal.name",
            "target_journal.style_status",
            "data_status",
            "style_status",
            "figure_type_candidates",
            "selected_workflow_chain",
            "missing_inputs",
            "risk_flags",
        ],
        errors,
    )
    if intake.get("data_status") not in VALID_DATA_STATUSES:
        errors.append("data_status has invalid value")
    if intake.get("style_status") not in VALID_STYLE_STATUSES:
        errors.append("style_status has invalid value")
    if get_path(intake, "target_journal.style_status") not in VALID_STYLE_STATUSES:
        errors.append("target_journal.style_status has invalid value")
    return errors, warnings


def validate_journal_style(data: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    report = data.get("journal_style", data)
    if not isinstance(report, dict):
        return ["journal_style must be a mapping"], warnings
    require(
        report,
        [
            "target",
            "guideline_source",
            "status",
            "applied_decisions",
            "unresolved_requirements",
            "allowed_language",
            "forbidden_language",
            "compliance_statement",
        ],
        errors,
    )
    if report.get("status") not in VALID_STYLE_STATUSES:
        errors.append("status has invalid value")
    text = str(report.get("compliance_statement", "")).lower()
    if report.get("status") != "VERIFIED" and ("compliant" in text or "submission-ready" in text):
        errors.append("non-VERIFIED style report uses forbidden compliance language")
    if report.get("status") in {"ESTIMATED", "UNVERIFIED"} and not report.get("unresolved_requirements"):
        warnings.append("unresolved_requirements should not be empty for ESTIMATED/UNVERIFIED")
    return errors, warnings


def validate_caption_package(data: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    package = data.get("caption_package", data)
    if not isinstance(package, dict):
        return ["caption_package must be a mapping"], warnings
    require(
        package,
        [
            "figure_id",
            "caption_title",
            "caption_body",
            "panel_legend",
            "notes",
            "in_text_reference",
            "short_alt_text",
            "extended_alt_text",
            "claim_alignment_summary",
            "missing_details",
        ],
        errors,
    )
    if len(str(package.get("short_alt_text", ""))) > 280:
        warnings.append("short_alt_text is long; consider moving detail to extended_alt_text")
    return errors, warnings


def validate_quality_report(data: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    report = data.get("figure_quality_report", data)
    if not isinstance(report, dict):
        return ["figure_quality_report must be a mapping"], warnings
    require(
        report,
        [
            "figure_id",
            "target_journal",
            "style_status",
            "data_status",
            "gate_results",
            "overall_integrity_status",
        ],
        errors,
    )
    for list_field in ["blocking_issues", "required_fixes_before_submission", "optional_improvements"]:
        if list_field not in report:
            errors.append(f"{list_field} is required")
        elif not isinstance(report.get(list_field), list):
            errors.append(f"{list_field} must be a list")
    if report.get("style_status") not in VALID_STYLE_STATUSES:
        errors.append("style_status has invalid value")
    if report.get("data_status") not in VALID_DATA_STATUSES:
        errors.append("data_status has invalid value")
    if report.get("overall_integrity_status") not in VALID_INTEGRITY_STATUSES:
        errors.append("overall_integrity_status has invalid value")
    gates = report.get("gate_results", [])
    if not isinstance(gates, list) or not gates:
        errors.append("gate_results must be a non-empty list")
    else:
        for index, gate in enumerate(gates, start=1):
            if not isinstance(gate, dict):
                errors.append(f"gate_results[{index}] must be a mapping")
                continue
            if gate.get("result") not in VALID_GATE_RESULTS:
                errors.append(f"gate_results[{index}].result has invalid value")
    return errors, warnings


def validate_submission_manifest(data: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    manifest = data.get("submission_manifest", data)
    if not isinstance(manifest, dict):
        return ["submission_manifest must be a mapping"], warnings
    require(
        manifest,
        [
            "figure_id",
            "created_at",
            "files",
            "data_sources",
            "code_sources",
            "style_status",
            "data_status",
            "reproducibility_status",
            "quality_report",
            "caption",
            "alt_text",
            "visual_claim_ledger",
            "environment_note",
            "unresolved_requirements",
        ],
        errors,
    )
    if manifest.get("style_status") not in VALID_STYLE_STATUSES:
        errors.append("style_status has invalid value")
    if manifest.get("data_status") not in VALID_DATA_STATUSES:
        errors.append("data_status has invalid value")
    if manifest.get("data_status") != "MOCKUP" and not manifest.get("data_sources"):
        errors.append("data_sources are required unless data_status is MOCKUP")
    return errors, warnings


VALIDATORS = {
    "figure_intake": validate_intake,
    "journal_style_report": validate_journal_style,
    "caption_package": validate_caption_package,
    "figure_quality_report": validate_quality_report,
    "submission_manifest": validate_submission_manifest,
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a scientific figure suite handoff artifact.")
    parser.add_argument("artifact")
    parser.add_argument("--type", required=True, choices=sorted(VALIDATORS))
    args = parser.parse_args()
    try:
        data = load_structured_file(args.artifact)
        if not isinstance(data, dict):
            raise ValueError("artifact must be a mapping")
        errors, warnings = VALIDATORS[args.type](data)
        exit_with_results(errors, warnings)
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
