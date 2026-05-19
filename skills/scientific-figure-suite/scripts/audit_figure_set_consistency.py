from __future__ import annotations

import argparse
from collections import Counter
from typing import Any

from _common import exit_with_results, main_error
from _memory import append_jsonl, load_json, read_jsonl, resolve_memory_dir, save_json, utc_now


def as_report(project_id: str, result: str, checks: list[dict[str, Any]], blockers: list[str], warnings: list[str]) -> dict[str, Any]:
    return {
        "cross_figure_consistency_report": {
            "created_at": utc_now(),
            "project_id": project_id,
            "result": result,
            "checks": checks,
            "blocking_issues": blockers,
            "warnings": warnings,
        }
    }


def audit(args: argparse.Namespace) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    memory_dir = resolve_memory_dir(args.project_root, args.memory_dir)
    manifest_path = memory_dir / "figure_set_manifest.json"
    if not manifest_path.exists():
        return [f"figure set manifest missing: {manifest_path}"], warnings
    data = load_json(manifest_path)
    manifest = data.get("figure_set_manifest", {})
    figures = manifest.get("figures", []) if isinstance(manifest, dict) else []
    if not isinstance(figures, list):
        return ["figure_set_manifest.figures must be a list"], warnings

    checks: list[dict[str, Any]] = []
    blockers: list[str] = []
    report_warnings: list[str] = []
    figure_ids = [figure.get("figure_id") for figure in figures if isinstance(figure, dict)]
    duplicates = [item for item, count in Counter(figure_ids).items() if item and count > 1]
    if duplicates:
        blockers.append("Duplicate figure ids: " + ", ".join(sorted(duplicates)))
    checks.append({"check": "unique_figure_ids", "result": "FAIL" if duplicates else "PASS"})

    if not figures:
        blockers.append("Figure set is empty.")
    stale = [figure.get("figure_id") for figure in figures if isinstance(figure, dict) and figure.get("stale") is True]
    if stale:
        blockers.append("Stale figures: " + ", ".join(str(item) for item in stale))
    checks.append({"check": "no_stale_figures", "result": "FAIL" if stale else "PASS"})

    style_statuses = {
        figure.get("status_tags", {}).get("STYLE_STATUS")
        for figure in figures
        if isinstance(figure, dict) and isinstance(figure.get("status_tags"), dict)
    }
    style_statuses.discard(None)
    if len(style_statuses) > 1:
        report_warnings.append("Mixed STYLE_STATUS values across figures: " + ", ".join(sorted(style_statuses)))
    checks.append({"check": "style_status_consistency", "result": "PASS_WITH_WARNINGS" if len(style_statuses) > 1 else "PASS"})

    no_outputs = [figure.get("figure_id") for figure in figures if isinstance(figure, dict) and not figure.get("outputs")]
    if no_outputs:
        report_warnings.append("Figures without outputs: " + ", ".join(str(item) for item in no_outputs))
    checks.append({"check": "outputs_present", "result": "PASS_WITH_WARNINGS" if no_outputs else "PASS"})

    audited_paths = {
        entry.get("path")
        for entry in read_jsonl(memory_dir / "visual_audit_artifact.jsonl")
        if entry.get("path")
    }
    missing_audits: list[str] = []
    for figure in figures:
        if not isinstance(figure, dict):
            continue
        for output in figure.get("outputs", []) or []:
            if output not in audited_paths:
                missing_audits.append(str(output))
    if missing_audits and args.require_visual_audits:
        blockers.append("Outputs without visual audit artifacts: " + ", ".join(sorted(missing_audits)))
    elif missing_audits:
        report_warnings.append("Outputs without visual audit artifacts: " + ", ".join(sorted(missing_audits)))
    checks.append({"check": "visual_audit_artifacts", "result": "FAIL" if missing_audits and args.require_visual_audits else ("PASS_WITH_WARNINGS" if missing_audits else "PASS")})

    result = "FAIL" if blockers else ("PASS_WITH_WARNINGS" if report_warnings else "PASS")
    report = as_report(str(manifest.get("project_id", "unknown-project")), result, checks, blockers, report_warnings)
    append_jsonl(memory_dir / "cross_figure_consistency_history.jsonl", report)
    if args.update:
        manifest["style_consistency_status"] = result
        manifest["updated_at"] = utc_now()
        save_json(manifest_path, data)
    print(f"[FIGURE-SET-AUDIT] {result}")
    errors.extend(blockers)
    warnings.extend(report_warnings)
    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit cross-figure consistency for a figure set manifest.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--memory-dir", default=None)
    parser.add_argument("--require-visual-audits", action="store_true")
    parser.add_argument("--update", action="store_true")
    args = parser.parse_args()
    try:
        errors, warnings = audit(args)
        exit_with_results(errors, warnings)
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
