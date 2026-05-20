from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from _common import load_structured_file, main_error, write_json
from _memory import load_json, read_jsonl, resolve_memory_dir, utc_now
from build_pipeline_dashboard import build_dashboard


SCHEMA_VERSION = "0.9.0"
RUNBOOK_STAGES = [
    "INTAKE",
    "DATASET_INSPECTION",
    "DEPENDENCY_PLANNING",
    "RENDER_STACK_SELECTION",
    "RENDER",
    "MULTIPANEL_LAYOUT_AUDIT",
    "TEXT_LAYOUT_AUDIT",
    "RENDER_QUALITY_AUDIT",
    "STYLE_STATUS",
    "CAPTION_ALT_TEXT",
    "FIGURE_SET",
    "SUBMISSION_PACKAGE",
    "READINESS",
]


def latest_report(memory_dir: Path, filename: str, wrapper_key: str) -> dict[str, Any] | None:
    entries = read_jsonl(memory_dir / filename)
    for entry in reversed(entries):
        report = entry.get(wrapper_key, entry)
        if isinstance(report, dict):
            return report
    return None


def action(
    alias: str,
    reason: str,
    command: list[str] | None = None,
    approval_required: bool = False,
    gated: bool = False,
) -> dict[str, Any]:
    return {
        "alias": alias,
        "reason": reason,
        "command": command or [],
        "approval_required": approval_required,
        "gated": gated,
    }


def stage(name: str, status: str, recommended_action: dict[str, Any] | None = None, evidence: str = "") -> dict[str, Any]:
    return {
        "stage": name,
        "status": status,
        "evidence": evidence,
        "recommended_action": recommended_action,
    }


def first_action(stages: list[dict[str, Any]]) -> dict[str, Any]:
    priority_groups = [
        ({"BLOCKED"}, False),
        ({"WAITING", "READY"}, True),
        ({"NOT_STARTED"}, False),
    ]
    for status_group, require_gate in priority_groups:
        for item in stages:
            candidate = item.get("recommended_action")
            if isinstance(candidate, dict) and item.get("status") in status_group:
                if require_gate and not (candidate.get("gated") or candidate.get("approval_required")):
                    continue
                result = dict(candidate)
                result["stage"] = item.get("stage")
                return result
    for item in stages:
        candidate = item.get("recommended_action")
        if isinstance(candidate, dict) and item.get("status") in {"BLOCKED", "READY", "WAITING"}:
            result = dict(candidate)
            result["stage"] = item.get("stage")
            return result
    return action("fig-audit-readiness", "No earlier actionable stage found.", ["scripts/audit_submission_readiness.py"])


def load_intake(path: str) -> dict[str, Any] | None:
    if not path:
        return None
    data = load_structured_file(path)
    return data.get("figure_intake", data) if isinstance(data, dict) else None


def has_registered_datasets(memory_dir: Path) -> bool:
    data = load_json(memory_dir / "dataset_registry.json")
    registry = data.get("dataset_registry", data) if isinstance(data, dict) else {}
    return bool(isinstance(registry, dict) and registry.get("datasets"))


def build_runbook(args: argparse.Namespace) -> dict[str, Any]:
    project_root = Path(args.project_root).expanduser().resolve()
    memory_dir = resolve_memory_dir(project_root, args.memory_dir)
    dashboard = build_dashboard(memory_dir, check_paths=args.check_paths)["pipeline_dashboard"]
    artifacts = dashboard.get("last_artifacts", {})
    blockers = [str(item) for item in dashboard.get("blockers", [])]
    next_actions = [str(item) for item in dashboard.get("next_actions", [])]
    intake = load_intake(args.figure_intake)

    text_report = latest_report(memory_dir, "text_layout_history.jsonl", "text_layout_report")
    multipanel_report = latest_report(memory_dir, "multipanel_layout_history.jsonl", "multipanel_layout_audit")
    regression_report = latest_report(memory_dir, "visual_regression_history.jsonl", "visual_regression_report")
    dependency_report = latest_report(memory_dir, "dependency_plan_history.jsonl", "dependency_plan")
    external_report = latest_report(memory_dir, "external_data_plan_history.jsonl", "data_acquisition_plan")

    run_stages: list[dict[str, Any]] = []
    if intake:
        run_stages.append(stage("INTAKE", "DONE", evidence="figure_intake supplied"))
    elif artifacts.get("figure_count", 0):
        run_stages.append(stage("INTAKE", "DONE", evidence="figure passport contains figures"))
    else:
        run_stages.append(stage("INTAKE", "READY", action("fig-scope", "Create figure_intake before rendering.")))

    dataset_status = (
        "DONE"
        if args.dataset_profile or has_registered_datasets(memory_dir)
        else ("WAITING" if artifacts.get("figure_count", 0) else "NOT_STARTED")
    )
    run_stages.append(stage("DATASET_INSPECTION", dataset_status, action("fig-plan-libraries", "Inspect dataset before dependency planning.") if dataset_status == "WAITING" else None))

    dependency_blockers = artifacts.get("latest_dependency_blockers", [])
    if dependency_blockers:
        run_stages.append(stage("DEPENDENCY_PLANNING", "BLOCKED", action("fig-plan-libraries", "Required libraries are missing; install is approval-gated.", approval_required=True, gated=True), ", ".join(dependency_blockers)))
    else:
        run_stages.append(stage("DEPENDENCY_PLANNING", "DONE" if dependency_report else "READY", action("fig-plan-libraries", "Create dependency plan before registry rendering.") if not dependency_report else None))

    run_stages.append(stage("RENDER_STACK_SELECTION", "DONE" if dependency_report else "READY", action("fig-select-render-stack", "Select minimal render stack from registry and environment.") if not dependency_report else None))
    run_stages.append(stage("RENDER", "DONE" if artifacts.get("latest_visual_regression") not in {None, "NOT_RUN"} else "READY", action("fig-render-template", "Render only from supplied data and an approved dependency plan.")))

    if multipanel_report and multipanel_report.get("result") == "FAIL":
        run_stages.append(stage("MULTIPANEL_LAYOUT_AUDIT", "BLOCKED", action("fig-audit-multipanel-layout", "Repair layout spec, then rerun multipanel layout audit."), "latest multipanel layout audit failed"))
    else:
        status = "DONE" if artifacts.get("latest_multipanel_layout") in {"PASS", "PASS_WITH_WARNINGS"} else "READY"
        run_stages.append(stage("MULTIPANEL_LAYOUT_AUDIT", status, action("fig-audit-multipanel-layout", "Audit optical grid and colorbar layout before readiness.") if status == "READY" else None))

    if text_report and text_report.get("result") == "FAIL":
        run_stages.append(stage("TEXT_LAYOUT_AUDIT", "BLOCKED", action("fig-repair-text-layout", "Repair text layout, then rerun fig-audit-text-layout."), "latest text layout audit failed"))
    else:
        status = "DONE" if artifacts.get("latest_text_layout") in {"PASS", "PASS_WITH_WARNINGS"} else "READY"
        run_stages.append(stage("TEXT_LAYOUT_AUDIT", status, action("fig-audit-text-layout", "Audit text overlap, clipping, and terminology before export.") if status == "READY" else None))

    if regression_report and regression_report.get("result") == "FAIL":
        run_stages.append(stage("RENDER_QUALITY_AUDIT", "BLOCKED", action("fig-audit-render", "Rerender or repair blank/missing outputs, then rerun visual QA."), "latest visual regression audit failed"))
    else:
        status = "DONE" if artifacts.get("latest_visual_regression") in {"PASS", "PASS_WITH_WARNINGS"} else "READY"
        run_stages.append(stage("RENDER_QUALITY_AUDIT", status, action("fig-audit-render", "Audit exported files for render quality.") if status == "READY" else None))

    external_decision = artifacts.get("latest_external_data_decision")
    if external_decision in {"RECOMMENDED_WITH_APPROVAL", "BLOCKED_PENDING_SOURCE"} or (external_report and external_report.get("approval_required")):
        run_stages.append(stage("STYLE_STATUS", "WAITING", action("fig-plan-external-data", "Resolve external data plan before using external records.", approval_required=True, gated=True), str(external_decision)))
    elif any("Verify current journal guidance" in item for item in next_actions):
        run_stages.append(stage("STYLE_STATUS", "WAITING", action("fig-verify-journal", "Journal verification needs current official or user-provided guidance.", approval_required=True, gated=True), "unverified journal target"))
    else:
        run_stages.append(stage("STYLE_STATUS", "DONE"))

    run_stages.append(stage("CAPTION_ALT_TEXT", "READY", action("fig-caption", "Create or update caption and alt text after figure evidence is stable.")))
    run_stages.append(stage("FIGURE_SET", "DONE" if artifacts.get("figure_set_status") not in {None, "NOT_RUN"} else "READY", action("fig-build-figure-set", "Build figure set manifest.") if artifacts.get("figure_set_status") in {None, "NOT_RUN"} else None))
    run_stages.append(stage("SUBMISSION_PACKAGE", "DONE" if artifacts.get("package_index_status") not in {None, "NOT_RUN"} else "READY", action("fig-build-submission-package", "Build package index after exports exist.") if artifacts.get("package_index_status") in {None, "NOT_RUN"} else None))
    run_stages.append(stage("READINESS", "READY", action("fig-audit-readiness", "Run final readiness audit once earlier blockers are resolved.")))

    created_at = utc_now()
    runbook = {
        "agentic_runbook": {
            "schema_version": SCHEMA_VERSION,
            "created_at": created_at,
            "run_id": f"agentic-{created_at.replace(':', '').replace('-', '')}",
            "project_id": dashboard.get("project_id", "unknown-project"),
            "mode": "DRY_RUN_FIRST",
            "memory_dir": str(memory_dir),
            "dashboard_summary": {
                "active_stage": dashboard.get("active_stage"),
                "readiness_summary": dashboard.get("readiness_summary"),
                "blockers": blockers,
                "next_actions": next_actions,
            },
            "stages": run_stages,
            "next_action": first_action(run_stages),
            "guardrails": [
                "Do not install packages automatically.",
                "Do not download external data without explicit approval.",
                "Do not claim verified journal compliance without current official or user-provided guidance.",
                "Do not write project memory inside the installed skill directory.",
            ],
        }
    }
    return runbook


def main() -> None:
    parser = argparse.ArgumentParser(description="Build an agentic scientific figure runbook from project memory and optional artifacts.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--memory-dir", default=None)
    parser.add_argument("--figure-intake", default="")
    parser.add_argument("--dataset-profile", default="")
    parser.add_argument("--check-paths", action="store_true")
    parser.add_argument("--out", default="")
    args = parser.parse_args()
    try:
        runbook = build_runbook(args)
        if args.out:
            write_json(args.out, runbook)
            print(f"[AGENTIC-RUNBOOK] wrote {args.out}")
        else:
            print(__import__("json").dumps(runbook, indent=2, sort_keys=True))
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
