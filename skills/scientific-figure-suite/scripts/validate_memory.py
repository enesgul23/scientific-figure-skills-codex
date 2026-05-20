from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from _common import VALID_DATA_STATUSES, exit_with_results, main_error
from _memory import (
    REQUIRED_JSON_FILES,
    REQUIRED_JSONL_FILES,
    VALID_MEMORY_LEVELS,
    VALID_STYLE_PROFILE_STATUSES,
    VALID_STYLE_STATUSES,
    VALID_VALIDATION_STATUSES,
    load_json,
    read_jsonl,
    resolve_memory_dir,
    update_manifest_timestamp,
)


VALID_INTEGRITY_STATUSES = {"PASS", "PASS_WITH_WARNINGS", "FAIL"}
VALID_REPRO_STATUS = {"CODED", "DESIGN_ONLY", "PARTIAL"}
VALID_READINESS_STATUSES = {"READY", "READY_WITH_WARNINGS", "BLOCKED", "NOT_RUN"}
VALID_REPORT_RESULTS = {"PASS", "PASS_WITH_WARNINGS", "FAIL", "NOT_RUN"}
VALID_DATASET_SOURCE_TYPES = {"user_provided", "generated", "external_planned", "external_downloaded"}
VALID_EXTERNAL_USAGE_ROLES = {"contextual", "evidentiary", "benchmark", "annotation", "none"}
VALID_CONTAMINATION_RISK = {"none", "low", "medium", "high", "unknown"}
HASH_RE = re.compile(r"^[0-9a-f]{12}$")


def validate_json_file(path: Path, errors: list[str]) -> dict[str, Any]:
    try:
        data = load_json(path)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path.name}: invalid JSON: {exc}")
        return {}
    if not isinstance(data, dict):
        errors.append(f"{path.name}: root must be an object")
        return {}
    return data


def validate_jsonl_file(path: Path, errors: list[str]) -> list[dict[str, Any]]:
    try:
        return read_jsonl(path)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        errors.append(f"{path.name}: invalid JSONL: {exc}")
        return []


def normalize_ref(value: Any, prefix: str) -> str:
    text = str(value or "")
    if text.startswith(prefix + ":"):
        return text.split(":", 1)[1]
    return text


def project_root_from_memory_dir(memory_dir: Path) -> Path:
    if memory_dir.parent.name == ".codex":
        return memory_dir.parent.parent
    return memory_dir.parent


def validate_repro_lock(lock: Any, context: str, errors: list[str], warnings: list[str]) -> None:
    if lock is None:
        return
    if not isinstance(lock, dict):
        errors.append(f"{context}: repro_lock must be an object")
        return
    if lock.get("hash_algorithm") and lock.get("hash_algorithm") != "sha256":
        errors.append(f"{context}: repro_lock.hash_algorithm must be sha256")
    if lock.get("audit_status") in {"STALE", "MISSING"}:
        warnings.append(f"{context}: repro_lock audit_status is {lock.get('audit_status')}")
    for field in ["data_hashes", "code_hashes", "output_hashes"]:
        if field in lock and not isinstance(lock.get(field), dict):
            errors.append(f"{context}: repro_lock.{field} must be an object")


def validate_memory(memory_dir: Path, check_paths: bool = False) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not memory_dir.is_dir():
        return [f"memory directory missing: {memory_dir}"], warnings

    for filename in REQUIRED_JSON_FILES:
        if not (memory_dir / filename).is_file():
            errors.append(f"required memory JSON missing: {filename}")
    for filename in REQUIRED_JSONL_FILES:
        if not (memory_dir / filename).is_file():
            errors.append(f"required memory JSONL missing: {filename}")
    if errors:
        return errors, warnings

    manifest_data = validate_json_file(memory_dir / "memory_manifest.json", errors)
    profile_data = validate_json_file(memory_dir / "project_profile.json", errors)
    journal_data = validate_json_file(memory_dir / "journal_targets.json", errors)
    passport_data = validate_json_file(memory_dir / "figure_passport.json", errors)
    figure_set_data = validate_json_file(memory_dir / "figure_set_manifest.json", errors)
    package_index_data = validate_json_file(memory_dir / "submission_package_index.json", errors)
    dataset_data = validate_json_file(memory_dir / "dataset_registry.json", errors)
    style_data = validate_json_file(memory_dir / "author_visual_style_profile.json", errors)

    manifest = manifest_data.get("memory_manifest", {})
    if not isinstance(manifest, dict):
        errors.append("memory_manifest.json: memory_manifest must be an object")
    else:
        if not manifest.get("project_id"):
            errors.append("memory_manifest.project_id is required")
        if manifest.get("memory_level") not in VALID_MEMORY_LEVELS:
            errors.append("memory_manifest.memory_level has invalid value")
        if manifest.get("validation_status") not in VALID_VALIDATION_STATUSES:
            errors.append("memory_manifest.validation_status has invalid value")
        pipeline_state = manifest.get("pipeline_state")
        if not isinstance(pipeline_state, dict):
            errors.append("memory_manifest.pipeline_state must be an object")
        else:
            for field in ["completed_stages", "blocked_stages", "last_artifacts", "next_actions"]:
                if not isinstance(pipeline_state.get(field), list):
                    errors.append(f"memory_manifest.pipeline_state.{field} must be a list")
            if pipeline_state.get("readiness_summary") not in VALID_READINESS_STATUSES:
                errors.append("memory_manifest.pipeline_state.readiness_summary has invalid value")

    profile = profile_data.get("project_profile", {})
    if not isinstance(profile, dict) or not profile.get("project_id"):
        errors.append("project_profile.project_id is required")

    journal_targets = journal_data.get("journal_targets", {}).get("targets", [])
    if not isinstance(journal_targets, list):
        errors.append("journal_targets.targets must be a list")
    else:
        for index, target in enumerate(journal_targets, start=1):
            if not isinstance(target, dict):
                errors.append(f"journal_targets[{index}] must be an object")
                continue
            status = target.get("status")
            source = target.get("guideline_source")
            if status not in VALID_STYLE_STATUSES:
                errors.append(f"journal target {index} has invalid status")
            if status == "VERIFIED" and source not in {"live_official", "user_provided"}:
                errors.append(f"journal target {target.get('journal', index)} VERIFIED requires live_official or user_provided source")
            if status in {"ESTIMATED", "UNVERIFIED"} and not target.get("unresolved_requirements"):
                warnings.append(f"journal target {target.get('journal', index)} should list unresolved requirements")

    project_root = project_root_from_memory_dir(memory_dir)
    dataset_ids: set[str] = set()
    figure_ids: set[str] = set()
    passport = passport_data.get("figure_passport", {})
    figures = passport.get("figures", []) if isinstance(passport, dict) else []
    seen_figures: set[str] = set()
    if not isinstance(figures, list):
        errors.append("figure_passport.figures must be a list")
    else:
        for figure in figures:
            if not isinstance(figure, dict):
                errors.append("figure_passport figure entries must be objects")
                continue
            figure_id = figure.get("figure_id")
            if not figure_id:
                errors.append("figure_passport figure_id is required")
                continue
            if figure_id in seen_figures:
                errors.append(f"duplicate figure_id in figure_passport: {figure_id}")
            seen_figures.add(figure_id)
            figure_ids.add(figure_id)
            status_tags = figure.get("status_tags", {})
            if isinstance(status_tags, dict):
                if status_tags.get("DATA_STATUS") and status_tags.get("DATA_STATUS") not in VALID_DATA_STATUSES:
                    errors.append(f"{figure_id}: invalid DATA_STATUS")
                if status_tags.get("STYLE_STATUS") and status_tags.get("STYLE_STATUS") not in VALID_STYLE_STATUSES:
                    errors.append(f"{figure_id}: invalid STYLE_STATUS")
                if status_tags.get("REPRODUCIBILITY_STATUS") and status_tags.get("REPRODUCIBILITY_STATUS") not in VALID_REPRO_STATUS:
                    errors.append(f"{figure_id}: invalid REPRODUCIBILITY_STATUS")
                if status_tags.get("INTEGRITY_STATUS") and status_tags.get("INTEGRITY_STATUS") not in VALID_INTEGRITY_STATUSES:
                    errors.append(f"{figure_id}: invalid INTEGRITY_STATUS")
            validate_repro_lock(figure.get("repro_lock"), figure_id, errors, warnings)
            if figure.get("stale") is True:
                warnings.append(f"{figure_id}: figure marked stale")
            panels = figure.get("panels", [])
            if panels and not isinstance(panels, list):
                errors.append(f"{figure_id}: panels must be a list")
            elif isinstance(panels, list):
                seen_panels: set[str] = set()
                for panel in panels:
                    if not isinstance(panel, dict):
                        errors.append(f"{figure_id}: panel entries must be objects")
                        continue
                    panel_id = panel.get("panel_id")
                    if not panel_id:
                        errors.append(f"{figure_id}: panel_id is required")
                        continue
                    if panel_id in seen_panels:
                        errors.append(f"{figure_id}: duplicate panel_id {panel_id}")
                    seen_panels.add(panel_id)
                    validate_repro_lock(panel.get("repro_lock"), f"{figure_id}.{panel_id}", errors, warnings)
                    if panel.get("stale") is True:
                        warnings.append(f"{figure_id}.{panel_id}: panel marked stale")

    datasets = dataset_data.get("dataset_registry", {}).get("datasets", [])
    if not isinstance(datasets, list):
        errors.append("dataset_registry.datasets must be a list")
    else:
        for dataset in datasets:
            if not isinstance(dataset, dict):
                errors.append("dataset entries must be objects")
                continue
            if not dataset.get("dataset_id"):
                errors.append("dataset_id is required")
            else:
                dataset_ids.add(str(dataset.get("dataset_id")))
            source_type = dataset.get("source_type")
            if source_type and source_type not in VALID_DATASET_SOURCE_TYPES:
                errors.append(f"dataset {dataset.get('dataset_id')}: invalid source_type")
            usage_role = dataset.get("usage_role")
            if usage_role and usage_role not in VALID_EXTERNAL_USAGE_ROLES:
                errors.append(f"dataset {dataset.get('dataset_id')}: invalid usage_role")
            contamination_risk = dataset.get("contamination_risk")
            if contamination_risk and contamination_risk not in VALID_CONTAMINATION_RISK:
                errors.append(f"dataset {dataset.get('dataset_id')}: invalid contamination_risk")
            if source_type == "external_downloaded":
                for field in ["source_url", "license", "citation", "downloaded_at", "sha256"]:
                    if not dataset.get(field):
                        errors.append(f"dataset {dataset.get('dataset_id')}: external_downloaded requires {field}")
            if source_type == "external_planned" and not (dataset.get("source_url") or dataset.get("citation")):
                warnings.append(f"dataset {dataset.get('dataset_id')}: external_planned should include source_url or citation")
            dataset_path = dataset.get("path")
            if check_paths and dataset_path and not (project_root / dataset_path).exists():
                warnings.append(f"dataset path not found from project root: {dataset_path}")

    style_profile = style_data.get("author_visual_style_profile", {})
    if not isinstance(style_profile, dict):
        errors.append("author_visual_style_profile must be an object")
    elif style_profile.get("status") not in VALID_STYLE_PROFILE_STATUSES:
        errors.append("author_visual_style_profile.status has invalid value")

    claim_entries = validate_jsonl_file(memory_dir / "visual_claim_ledger.jsonl", errors)
    seen_claims: set[str] = set()
    for index, claim in enumerate(claim_entries, start=1):
        claim_id = claim.get("claim_id") or claim.get("id")
        if not claim_id:
            errors.append(f"visual_claim_ledger line {index}: claim_id is required")
        elif claim_id in seen_claims:
            errors.append(f"duplicate visual claim id: {claim_id}")
        else:
            seen_claims.add(str(claim_id))
        claim_figure = claim.get("figure_id")
        if claim_figure and figure_ids and claim_figure not in figure_ids:
            errors.append(f"visual claim {claim_id}: unknown figure_id {claim_figure}")
        data_source = claim.get("data_source")
        if data_source:
            if dataset_ids and normalize_ref(data_source, "dataset") not in dataset_ids:
                warnings.append(f"visual claim {claim_id}: data_source not in dataset registry: {data_source}")
            elif not dataset_ids:
                warnings.append(f"visual claim {claim_id}: dataset registry is empty for data_source {data_source}")

    normalized_claim_ids = {normalize_ref(item, "claim") for item in seen_claims}
    for figure in (figures if isinstance(figures, list) else []):
        if not isinstance(figure, dict):
            continue
        figure_id = figure.get("figure_id")
        for claim_ref in figure.get("claim_refs", []) or []:
            if seen_claims and normalize_ref(claim_ref, "claim") not in normalized_claim_ids:
                warnings.append(f"{figure_id}: claim_ref not in visual_claim_ledger: {claim_ref}")
            elif not seen_claims:
                warnings.append(f"{figure_id}: visual_claim_ledger is empty for claim_ref {claim_ref}")
        for dataset_ref in figure.get("dataset_refs", []) or []:
            if dataset_ids and normalize_ref(dataset_ref, "dataset") not in dataset_ids:
                warnings.append(f"{figure_id}: dataset_ref not in dataset_registry: {dataset_ref}")
            elif not dataset_ids:
                warnings.append(f"{figure_id}: dataset_registry is empty for dataset_ref {dataset_ref}")
        for panel in figure.get("panels", []) or []:
            if not isinstance(panel, dict):
                continue
            data_source = panel.get("data_source")
            if data_source and dataset_ids and normalize_ref(data_source, "dataset") not in dataset_ids:
                warnings.append(f"{figure_id}.{panel.get('panel_id')}: panel data_source not in dataset_registry: {data_source}")
            elif data_source and not dataset_ids:
                warnings.append(f"{figure_id}.{panel.get('panel_id')}: dataset_registry is empty for panel data_source {data_source}")

    validate_jsonl_file(memory_dir / "quality_audit_history.jsonl", errors)
    journal_verifications = validate_jsonl_file(memory_dir / "journal_guideline_verification.jsonl", errors)
    verified_sources = {
        entry.get("journal")
        for entry in journal_verifications
        if entry.get("status") == "VERIFIED" and entry.get("source_type") in {"live_official", "user_provided"}
    }
    for target in (journal_targets if isinstance(journal_targets, list) else []):
        if isinstance(target, dict) and target.get("status") == "VERIFIED" and target.get("journal") not in verified_sources:
            warnings.append(f"journal target {target.get('journal')} is VERIFIED but has no matching verification ledger entry")
    visual_artifacts = validate_jsonl_file(memory_dir / "visual_audit_artifact.jsonl", errors)
    for index, artifact in enumerate(visual_artifacts, start=1):
        if artifact.get("figure_id") and figure_ids and artifact.get("figure_id") not in figure_ids:
            errors.append(f"visual_audit_artifact line {index}: unknown figure_id {artifact.get('figure_id')}")
        if check_paths and artifact.get("path") and not (project_root / str(artifact.get("path"))).exists():
            warnings.append(f"visual audit artifact path not found: {artifact.get('path')}")

    figure_set = figure_set_data.get("figure_set_manifest", {})
    if not isinstance(figure_set, dict):
        errors.append("figure_set_manifest must be an object")
    else:
        if figure_set.get("style_consistency_status") not in VALID_REPORT_RESULTS:
            errors.append("figure_set_manifest.style_consistency_status has invalid value")
        if figure_set.get("readiness_status") not in VALID_READINESS_STATUSES:
            errors.append("figure_set_manifest.readiness_status has invalid value")
        fs_figures = figure_set.get("figures", [])
        if not isinstance(fs_figures, list):
            errors.append("figure_set_manifest.figures must be a list")
        for item in (fs_figures if isinstance(fs_figures, list) else []):
            if isinstance(item, dict) and item.get("figure_id") and figure_ids and item.get("figure_id") not in figure_ids:
                warnings.append(f"figure_set_manifest references unknown figure_id: {item.get('figure_id')}")

    package_index = package_index_data.get("submission_package_index", {})
    if not isinstance(package_index, dict):
        errors.append("submission_package_index must be an object")
    else:
        if package_index.get("index_status") not in VALID_REPORT_RESULTS:
            errors.append("submission_package_index.index_status has invalid value")
        package_files = package_index.get("files", [])
        if not isinstance(package_files, list):
            errors.append("submission_package_index.files must be a list")
        for item in (package_files if isinstance(package_files, list) else []):
            if not isinstance(item, dict):
                errors.append("submission_package_index file entries must be objects")
                continue
            if not item.get("path") or not item.get("sha256"):
                errors.append("submission_package_index file entries require path and sha256")
            if check_paths and item.get("path") and not (project_root / str(item.get("path"))).exists():
                warnings.append(f"submission package file path not found: {item.get('path')}")

    consistency_entries = validate_jsonl_file(memory_dir / "cross_figure_consistency_history.jsonl", errors)
    for index, entry in enumerate(consistency_entries, start=1):
        report = entry.get("cross_figure_consistency_report", entry)
        if isinstance(report, dict) and report.get("result") not in {"PASS", "PASS_WITH_WARNINGS", "FAIL"}:
            errors.append(f"cross_figure_consistency_history line {index}: invalid result")
    readiness_entries = validate_jsonl_file(memory_dir / "submission_readiness_history.jsonl", errors)
    for index, entry in enumerate(readiness_entries, start=1):
        report = entry.get("submission_readiness_report", entry)
        if isinstance(report, dict) and report.get("result") not in VALID_READINESS_STATUSES - {"NOT_RUN"}:
            errors.append(f"submission_readiness_history line {index}: invalid result")
    decision_entries = validate_jsonl_file(memory_dir / "figure_decision_log.jsonl", errors)
    for index, entry in enumerate(decision_entries, start=1):
        decision = entry.get("figure_decision", entry)
        if not isinstance(decision, dict):
            errors.append(f"figure_decision_log line {index}: entry must be an object")
            continue
        if not decision.get("decision_type") or not decision.get("decision"):
            errors.append(f"figure_decision_log line {index}: decision_type and decision are required")
    regression_entries = validate_jsonl_file(memory_dir / "visual_regression_history.jsonl", errors)
    for index, entry in enumerate(regression_entries, start=1):
        report = entry.get("visual_regression_report", entry)
        if not isinstance(report, dict):
            errors.append(f"visual_regression_history line {index}: entry must be an object")
            continue
        if report.get("result") not in {"PASS", "PASS_WITH_WARNINGS", "FAIL"}:
            errors.append(f"visual_regression_history line {index}: invalid result")
    multipanel_entries = validate_jsonl_file(memory_dir / "multipanel_layout_history.jsonl", errors)
    for index, entry in enumerate(multipanel_entries, start=1):
        report = entry.get("multipanel_layout_audit", entry)
        if not isinstance(report, dict):
            errors.append(f"multipanel_layout_history line {index}: entry must be an object")
            continue
        if report.get("result") not in {"PASS", "PASS_WITH_WARNINGS", "FAIL"}:
            errors.append(f"multipanel_layout_history line {index}: invalid result")
    text_layout_entries = validate_jsonl_file(memory_dir / "text_layout_history.jsonl", errors)
    for index, entry in enumerate(text_layout_entries, start=1):
        report = entry.get("text_layout_report", entry)
        if not isinstance(report, dict):
            errors.append(f"text_layout_history line {index}: entry must be an object")
            continue
        if report.get("result") not in {"PASS", "PASS_WITH_WARNINGS", "FAIL"}:
            errors.append(f"text_layout_history line {index}: invalid result")
    dependency_entries = validate_jsonl_file(memory_dir / "dependency_plan_history.jsonl", errors)
    for index, entry in enumerate(dependency_entries, start=1):
        plan = entry.get("dependency_plan", entry)
        if not isinstance(plan, dict):
            errors.append(f"dependency_plan_history line {index}: entry must be an object")
            continue
        if not isinstance(plan.get("required_libraries", []), list):
            errors.append(f"dependency_plan_history line {index}: required_libraries must be a list")
        if not (plan.get("selected_stack") or plan.get("required_libraries")):
            errors.append(f"dependency_plan_history line {index}: selected_stack or required_libraries is required")
    external_entries = validate_jsonl_file(memory_dir / "external_data_plan_history.jsonl", errors)
    for index, entry in enumerate(external_entries, start=1):
        plan = entry.get("data_acquisition_plan", entry)
        if not isinstance(plan, dict):
            errors.append(f"external_data_plan_history line {index}: entry must be an object")
            continue
        if plan.get("decision") not in {"NOT_REQUIRED", "RECOMMENDED_WITH_APPROVAL", "BLOCKED_PENDING_SOURCE", "REJECTED"}:
            errors.append(f"external_data_plan_history line {index}: invalid decision")
    boundary_entries = validate_jsonl_file(memory_dir / "revision_boundary_ledger.jsonl", errors)
    boundary_hashes: set[str] = set()
    consumed_hashes: set[str] = set()
    for index, entry in enumerate(boundary_entries, start=1):
        kind = entry.get("kind")
        if kind not in {"boundary", "resume", "forget"}:
            errors.append(f"revision_boundary_ledger line {index}: invalid kind")
            continue
        if kind == "boundary":
            hash_value = entry.get("hash")
            if not isinstance(hash_value, str) or not HASH_RE.match(hash_value):
                errors.append(f"revision_boundary_ledger line {index}: boundary hash must be 12 lowercase hex characters")
            elif hash_value in boundary_hashes:
                errors.append(f"duplicate boundary hash: {hash_value}")
            else:
                boundary_hashes.add(hash_value)
        if kind == "resume":
            consumes_hash = entry.get("consumes_hash")
            if not isinstance(consumes_hash, str) or not HASH_RE.match(consumes_hash):
                errors.append(f"revision_boundary_ledger line {index}: resume consumes_hash must be 12 lowercase hex characters")
            elif consumes_hash in consumed_hashes:
                errors.append(f"boundary hash consumed more than once: {consumes_hash}")
            else:
                consumed_hashes.add(consumes_hash)

    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate project-local scientific figure memory.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--memory-dir", default=None)
    parser.add_argument("--check-paths", action="store_true")
    parser.add_argument("--update-manifest", action="store_true")
    args = parser.parse_args()
    try:
        memory_dir = resolve_memory_dir(args.project_root, args.memory_dir)
        errors, warnings = validate_memory(memory_dir, check_paths=args.check_paths)
        if args.update_manifest and memory_dir.is_dir():
            status = "FAIL" if errors else ("PASS_WITH_WARNINGS" if warnings else "PASS")
            update_manifest_timestamp(memory_dir, status)
        exit_with_results(errors, warnings)
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
