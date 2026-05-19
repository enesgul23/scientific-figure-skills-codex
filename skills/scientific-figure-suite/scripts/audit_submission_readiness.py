from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from _common import exit_with_results, main_error
from _memory import append_jsonl, load_json, read_jsonl, resolve_memory_dir, save_json, sha256_file, utc_now
from validate_memory import validate_memory


def add_gate(gates: list[dict[str, Any]], name: str, result: str, note: str) -> None:
    gates.append({"gate": name, "result": result, "note": note})


def latest_consistency_result(memory_dir: Path) -> str | None:
    entries = read_jsonl(memory_dir / "cross_figure_consistency_history.jsonl")
    for entry in reversed(entries):
        report = entry.get("cross_figure_consistency_report", entry)
        if isinstance(report, dict) and report.get("result"):
            return str(report.get("result"))
    return None


def latest_visual_regression_result(memory_dir: Path) -> str | None:
    entries = read_jsonl(memory_dir / "visual_regression_history.jsonl")
    for entry in reversed(entries):
        report = entry.get("visual_regression_report", entry)
        if isinstance(report, dict) and report.get("result"):
            return str(report.get("result"))
    return None


def latest_dependency_blockers(memory_dir: Path) -> list[str]:
    entries = read_jsonl(memory_dir / "dependency_plan_history.jsonl")
    if not entries:
        return []
    plan = entries[-1].get("dependency_plan", entries[-1])
    if not isinstance(plan, dict):
        return ["latest dependency plan is malformed"]
    blocked: list[str] = []
    for item in plan.get("blocked_libraries", []) or []:
        if isinstance(item, dict):
            blocked.append(str(item.get("library_id", item)))
        else:
            blocked.append(str(item))
    return blocked


def latest_external_data_decision(memory_dir: Path) -> str | None:
    entries = read_jsonl(memory_dir / "external_data_plan_history.jsonl")
    if not entries:
        return None
    plan = entries[-1].get("data_acquisition_plan", entries[-1])
    if isinstance(plan, dict):
        return str(plan.get("decision") or "UNKNOWN")
    return "UNKNOWN"


def indexed_hashes(index: dict[str, Any], project_root: Path) -> tuple[list[str], list[str]]:
    blockers: list[str] = []
    warnings: list[str] = []
    for item in index.get("files", []) or []:
        if not isinstance(item, dict):
            blockers.append("submission package index contains a non-object file entry")
            continue
        rel_path = item.get("path")
        expected = item.get("sha256")
        if not rel_path or not expected:
            blockers.append("submission package index file entry missing path or sha256")
            continue
        path = project_root / str(rel_path)
        if not path.exists():
            blockers.append(f"indexed package file missing: {rel_path}")
            continue
        actual = sha256_file(path)
        if actual != expected:
            blockers.append(f"indexed package file hash drift: {rel_path}")
    if not index.get("files"):
        blockers.append("submission package index is empty")
    return blockers, warnings


def audit(args: argparse.Namespace) -> tuple[list[str], list[str]]:
    project_root = Path(args.project_root).expanduser().resolve()
    memory_dir = resolve_memory_dir(project_root, args.memory_dir)
    blockers: list[str] = []
    warnings: list[str] = []
    gates: list[dict[str, Any]] = []

    memory_errors, memory_warnings = validate_memory(memory_dir, check_paths=args.check_paths)
    if memory_errors:
        blockers.extend("memory: " + item for item in memory_errors)
        add_gate(gates, "memory_validation", "FAIL", f"{len(memory_errors)} error(s)")
    else:
        add_gate(gates, "memory_validation", "PASS_WITH_WARNINGS" if memory_warnings else "PASS", f"{len(memory_warnings)} warning(s)")
    warnings.extend("memory: " + item for item in memory_warnings)

    figure_set = load_json(memory_dir / "figure_set_manifest.json").get("figure_set_manifest", {})
    figures = figure_set.get("figures", []) if isinstance(figure_set, dict) else []
    if not figures:
        blockers.append("figure_set_manifest has no figures")
        add_gate(gates, "figure_set_manifest", "FAIL", "No figures listed")
    else:
        stale = [figure.get("figure_id") for figure in figures if isinstance(figure, dict) and figure.get("stale") is True]
        if stale:
            blockers.append("stale figures in figure set: " + ", ".join(str(item) for item in stale))
        unverified_styles = [
            figure.get("figure_id")
            for figure in figures
            if isinstance(figure, dict)
            and isinstance(figure.get("status_tags"), dict)
            and figure.get("status_tags", {}).get("STYLE_STATUS") != "VERIFIED"
        ]
        if unverified_styles and not args.allow_unverified_journal:
            blockers.append("figures with non-VERIFIED STYLE_STATUS: " + ", ".join(str(item) for item in unverified_styles))
        elif unverified_styles:
            warnings.append("figure style waiver used for: " + ", ".join(str(item) for item in unverified_styles))
        add_gate(gates, "figure_set_manifest", "FAIL" if stale or (unverified_styles and not args.allow_unverified_journal) else ("PASS_WITH_WARNINGS" if unverified_styles else "PASS"), f"figures={len(figures)} stale={len(stale)} unverified_style={len(unverified_styles)}")

    consistency = latest_consistency_result(memory_dir)
    if consistency == "FAIL":
        blockers.append("latest cross-figure consistency audit failed")
    elif consistency is None:
        warnings.append("no cross-figure consistency audit has been recorded")
    add_gate(gates, "cross_figure_consistency", consistency or "NOT_RUN", "Latest consistency result")

    package_index = load_json(memory_dir / "submission_package_index.json").get("submission_package_index", {})
    package_blockers, package_warnings = indexed_hashes(package_index, project_root)
    blockers.extend(package_blockers)
    warnings.extend(package_warnings)
    add_gate(gates, "submission_package_index", "FAIL" if package_blockers else "PASS", f"files={len(package_index.get('files', []) or [])}")

    audited_paths = {
        entry.get("path")
        for entry in read_jsonl(memory_dir / "visual_audit_artifact.jsonl")
        if entry.get("path")
    }
    output_paths = {
        output
        for figure in figures
        if isinstance(figure, dict)
        for output in (figure.get("outputs", []) or [])
    }
    missing_audits = sorted(output_paths - audited_paths)
    if missing_audits:
        blockers.append("figure outputs without visual audit artifacts: " + ", ".join(missing_audits))
    add_gate(gates, "visual_audit_artifacts", "FAIL" if missing_audits else "PASS", f"missing={len(missing_audits)}")

    visual_regression = latest_visual_regression_result(memory_dir)
    if visual_regression == "FAIL":
        blockers.append("latest visual regression/render-quality audit failed")
    elif visual_regression is None:
        warnings.append("no visual regression/render-quality audit has been recorded")
    add_gate(gates, "visual_regression", visual_regression or "NOT_RUN", "Latest render-quality result")

    dependency_blockers = latest_dependency_blockers(memory_dir)
    if dependency_blockers:
        blockers.append("latest dependency plan has missing required libraries: " + ", ".join(dependency_blockers))
    add_gate(gates, "dependency_plan", "FAIL" if dependency_blockers else "PASS", f"blocked={len(dependency_blockers)}")

    external_decision = latest_external_data_decision(memory_dir)
    if external_decision == "BLOCKED_PENDING_SOURCE":
        blockers.append("latest external data plan is blocked pending source/license/citation")
    elif external_decision in {"RECOMMENDED_WITH_APPROVAL", "REJECTED"}:
        warnings.append(f"latest external data decision: {external_decision}")
    add_gate(gates, "external_data_plan", "FAIL" if external_decision == "BLOCKED_PENDING_SOURCE" else (external_decision or "NOT_RUN"), "Latest external data decision")

    journal_targets = load_json(memory_dir / "journal_targets.json").get("journal_targets", {}).get("targets", [])
    unverified = [
        target.get("journal")
        for target in journal_targets
        if isinstance(target, dict) and target.get("status") != "VERIFIED"
    ]
    if unverified and not args.allow_unverified_journal:
        blockers.append("unverified journal targets: " + ", ".join(str(item) for item in unverified))
    elif unverified:
        warnings.append("journal waiver used for unverified targets: " + ", ".join(str(item) for item in unverified))
    add_gate(gates, "journal_verification", "FAIL" if unverified and not args.allow_unverified_journal else ("PASS_WITH_WARNINGS" if unverified else "PASS"), f"unverified={len(unverified)}")

    result = "BLOCKED" if blockers else ("READY_WITH_WARNINGS" if warnings else "READY")
    report = {
        "submission_readiness_report": {
            "created_at": utc_now(),
            "project_id": figure_set.get("project_id", package_index.get("project_id", "unknown-project")),
            "result": result,
            "gate_results": gates,
            "blockers": blockers,
            "warnings": warnings,
            "journal_waiver_used": bool(unverified and args.allow_unverified_journal),
        }
    }
    append_jsonl(memory_dir / "submission_readiness_history.jsonl", report)
    if isinstance(figure_set, dict):
        figure_set["readiness_status"] = result
        figure_set["updated_at"] = utc_now()
        save_json(memory_dir / "figure_set_manifest.json", {"figure_set_manifest": figure_set})
    print(f"[SUBMISSION-READINESS] {result}")
    return blockers, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit full figure set submission readiness.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--memory-dir", default=None)
    parser.add_argument("--check-paths", action="store_true")
    parser.add_argument("--allow-unverified-journal", action="store_true")
    args = parser.parse_args()
    try:
        errors, warnings = audit(args)
        exit_with_results(errors, warnings)
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
