from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from _common import exit_with_results, main_error, write_json
from _memory import default_pipeline_state, load_json, read_jsonl, resolve_memory_dir, save_json, utc_now
from validate_memory import validate_memory


STAGE_ORDER = ["INTAKE", "DOMAIN_DESIGN", "COMPOSITION", "STYLE", "TEXT", "AUDIT", "EXPORT", "READINESS"]


def latest_report_result(memory_dir: Path, filename: str, wrapper_key: str) -> str | None:
    entries = read_jsonl(memory_dir / filename)
    for entry in reversed(entries):
        report = entry.get(wrapper_key, entry)
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
    blockers = []
    for item in plan.get("blocked_libraries", []) or []:
        if isinstance(item, dict):
            blockers.append(str(item.get("library_id", item)))
        else:
            blockers.append(str(item))
    return blockers


def latest_external_data_decision(memory_dir: Path) -> str | None:
    entries = read_jsonl(memory_dir / "external_data_plan_history.jsonl")
    if not entries:
        return None
    plan = entries[-1].get("data_acquisition_plan", entries[-1])
    if isinstance(plan, dict):
        return str(plan.get("decision") or "UNKNOWN")
    return "UNKNOWN"


def build_dashboard(memory_dir: Path, check_paths: bool = False) -> dict[str, Any]:
    errors, warnings = validate_memory(memory_dir, check_paths=check_paths)
    manifest_data = load_json(memory_dir / "memory_manifest.json")
    manifest = manifest_data.get("memory_manifest", {})
    passport = load_json(memory_dir / "figure_passport.json").get("figure_passport", {})
    figure_set = load_json(memory_dir / "figure_set_manifest.json").get("figure_set_manifest", {})
    package_index = load_json(memory_dir / "submission_package_index.json").get("submission_package_index", {})
    journals = load_json(memory_dir / "journal_targets.json").get("journal_targets", {}).get("targets", [])

    figures = passport.get("figures", []) if isinstance(passport, dict) else []
    stale_figures = [
        figure.get("figure_id")
        for figure in figures
        if isinstance(figure, dict) and figure.get("stale") is True
    ]
    unverified_journals = [
        target.get("journal")
        for target in journals
        if isinstance(target, dict) and target.get("status") != "VERIFIED"
    ]
    latest_consistency = latest_report_result(memory_dir, "cross_figure_consistency_history.jsonl", "cross_figure_consistency_report")
    latest_readiness = latest_report_result(memory_dir, "submission_readiness_history.jsonl", "submission_readiness_report")
    latest_regression = latest_report_result(memory_dir, "visual_regression_history.jsonl", "visual_regression_report")
    latest_multipanel_layout = latest_report_result(memory_dir, "multipanel_layout_history.jsonl", "multipanel_layout_audit")
    dependency_blockers = latest_dependency_blockers(memory_dir)
    external_data_decision = latest_external_data_decision(memory_dir)

    blockers: list[str] = []
    if errors:
        blockers.append(f"memory validation has {len(errors)} error(s)")
    if stale_figures:
        blockers.append("stale figures: " + ", ".join(str(item) for item in stale_figures))
    if latest_consistency == "FAIL":
        blockers.append("latest cross-figure consistency audit failed")
    if latest_regression == "FAIL":
        blockers.append("latest visual regression audit failed")
    if latest_multipanel_layout == "FAIL":
        blockers.append("latest multipanel layout audit failed")
    if dependency_blockers:
        blockers.append("latest dependency plan has missing required libraries: " + ", ".join(dependency_blockers))
    if external_data_decision == "BLOCKED_PENDING_SOURCE":
        blockers.append("latest external data plan is blocked pending source/license/citation")
    if latest_readiness == "BLOCKED":
        blockers.append("latest submission readiness audit is BLOCKED")

    next_actions: list[str] = []
    if errors:
        next_actions.append("Run fig-migrate-memory, then fig-validate-memory.")
    if stale_figures:
        next_actions.append("Refresh stale figure outputs and rerun repro-lock audit.")
    if not figure_set.get("figures"):
        next_actions.append("Run fig-build-figure-set.")
    if package_index.get("index_status") == "NOT_RUN" or not package_index.get("files"):
        next_actions.append("Run fig-build-submission-package after exports exist.")
    if latest_consistency is None:
        next_actions.append("Run fig-audit-figure-set.")
    if latest_regression is None:
        next_actions.append("Run fig-audit-render on exported figure files.")
    if latest_multipanel_layout is None and figure_set.get("figures"):
        next_actions.append("Run fig-audit-multipanel-layout for multi-panel figures before readiness.")
    if dependency_blockers:
        next_actions.append("Install required libraries only if approved, or select a fallback render stack.")
    if external_data_decision == "BLOCKED_PENDING_SOURCE":
        next_actions.append("Resolve external data source, license, citation, and approval before use.")
    if unverified_journals:
        next_actions.append("Verify current journal guidance or record an explicit internal-review waiver.")
    if not next_actions:
        next_actions.append("Run fig-audit-readiness for the final readiness decision.")

    completed_stages = []
    if figures:
        completed_stages.extend(["INTAKE", "DOMAIN_DESIGN"])
    if figure_set.get("figures"):
        completed_stages.append("COMPOSITION")
    if latest_consistency in {"PASS", "PASS_WITH_WARNINGS"}:
        completed_stages.append("AUDIT")
    if package_index.get("files"):
        completed_stages.append("EXPORT")
    if latest_readiness in {"READY", "READY_WITH_WARNINGS"}:
        completed_stages.append("READINESS")

    blocked_stages = []
    if errors:
        blocked_stages.append("INTAKE")
    if stale_figures or latest_consistency == "FAIL" or latest_regression == "FAIL" or latest_multipanel_layout == "FAIL":
        blocked_stages.append("AUDIT")
    if not package_index.get("files"):
        blocked_stages.append("EXPORT")
    if latest_readiness == "BLOCKED":
        blocked_stages.append("READINESS")

    readiness_summary = latest_readiness or figure_set.get("readiness_status") or "NOT_RUN"
    if readiness_summary not in {"READY", "READY_WITH_WARNINGS", "BLOCKED", "NOT_RUN"}:
        readiness_summary = "NOT_RUN"
    active_stage = manifest.get("current_stage") or (blocked_stages[0] if blocked_stages else None)
    if active_stage is None:
        active_stage = next((stage for stage in STAGE_ORDER if stage not in completed_stages), "READINESS")

    return {
        "pipeline_dashboard": {
            "created_at": utc_now(),
            "project_id": manifest.get("project_id", "unknown-project"),
            "active_figure_id": manifest.get("active_figure_id"),
            "active_stage": active_stage,
            "completed_stages": completed_stages,
            "blocked_stages": blocked_stages,
            "last_artifacts": {
                "figure_count": len(figures) if isinstance(figures, list) else 0,
                "figure_set_status": figure_set.get("style_consistency_status"),
                "package_index_status": package_index.get("index_status"),
                "latest_consistency": latest_consistency or "NOT_RUN",
                "latest_visual_regression": latest_regression or "NOT_RUN",
                "latest_multipanel_layout": latest_multipanel_layout or "NOT_RUN",
                "latest_dependency_blockers": dependency_blockers,
                "latest_external_data_decision": external_data_decision or "NOT_RUN",
                "latest_readiness": latest_readiness or "NOT_RUN",
            },
            "blockers": blockers,
            "warnings": warnings + ([f"unverified journal targets: {', '.join(str(item) for item in unverified_journals)}"] if unverified_journals else []),
            "next_actions": next_actions,
            "readiness_summary": readiness_summary,
        }
    }


def update_manifest_pipeline_state(memory_dir: Path, dashboard: dict[str, Any]) -> None:
    manifest_path = memory_dir / "memory_manifest.json"
    data = load_json(manifest_path)
    manifest = data.setdefault("memory_manifest", {})
    payload = dashboard["pipeline_dashboard"]
    state = default_pipeline_state()
    state.update(
        {
            "active_stage": payload.get("active_stage"),
            "completed_stages": payload.get("completed_stages", []),
            "blocked_stages": payload.get("blocked_stages", []),
            "last_artifacts": [payload.get("last_artifacts", {})],
            "next_actions": payload.get("next_actions", []),
            "readiness_summary": payload.get("readiness_summary", "NOT_RUN"),
        }
    )
    manifest["pipeline_state"] = state
    manifest["current_stage"] = payload.get("active_stage")
    manifest["updated_at"] = utc_now()
    save_json(manifest_path, data)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a project-local scientific figure pipeline dashboard.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--memory-dir", default=None)
    parser.add_argument("--check-paths", action="store_true")
    parser.add_argument("--out", default="")
    parser.add_argument("--no-update-manifest", action="store_true")
    args = parser.parse_args()
    try:
        memory_dir = resolve_memory_dir(args.project_root, args.memory_dir)
        dashboard = build_dashboard(memory_dir, check_paths=args.check_paths)
        if not args.no_update_manifest:
            update_manifest_pipeline_state(memory_dir, dashboard)
        if args.out:
            write_json(args.out, dashboard)
            print(f"[PIPELINE-DASHBOARD] wrote {args.out}")
        else:
            print(json.dumps(dashboard, indent=2, sort_keys=True))
        warnings = dashboard["pipeline_dashboard"].get("warnings", [])
        fatal_errors = [
            blocker
            for blocker in dashboard["pipeline_dashboard"].get("blockers", [])
            if str(blocker).startswith("memory validation")
        ]
        exit_with_results(fatal_errors, warnings)
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
