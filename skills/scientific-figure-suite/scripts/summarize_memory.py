from __future__ import annotations

import argparse
from pathlib import Path

from _common import main_error
from _memory import load_json, read_jsonl, resolve_memory_dir


def summarize(memory_dir: Path) -> list[str]:
    manifest = load_json(memory_dir / "memory_manifest.json").get("memory_manifest", {})
    profile = load_json(memory_dir / "project_profile.json").get("project_profile", {})
    journals = load_json(memory_dir / "journal_targets.json").get("journal_targets", {}).get("targets", [])
    passport = load_json(memory_dir / "figure_passport.json").get("figure_passport", {})
    datasets = load_json(memory_dir / "dataset_registry.json").get("dataset_registry", {}).get("datasets", [])
    audits = read_jsonl(memory_dir / "quality_audit_history.jsonl")
    boundaries = read_jsonl(memory_dir / "revision_boundary_ledger.jsonl")
    visual_regressions = read_jsonl(memory_dir / "visual_regression_history.jsonl")

    figures = passport.get("figures", []) if isinstance(passport, dict) else []
    consumed = {entry.get("consumes_hash") for entry in boundaries if entry.get("kind") == "resume"}
    awaiting = [entry for entry in boundaries if entry.get("kind") == "boundary" and entry.get("hash") not in consumed]
    latest_audit = audits[-1] if audits else None
    latest_visual_regression = visual_regressions[-1] if visual_regressions else None

    lines = [
        "Figure Memory Dashboard",
        f"- memory_dir: {memory_dir}",
        f"- project_id: {manifest.get('project_id') or profile.get('project_id')}",
        f"- field: {profile.get('field', 'unspecified')}",
        f"- memory_level: {manifest.get('memory_level', 'unknown')}",
        f"- active_figure_id: {manifest.get('active_figure_id')}",
        f"- figures: {len(figures)}",
        f"- datasets: {len(datasets)}",
        f"- journal_targets: {len(journals)}",
    ]
    if journals:
        journal_bits = [f"{item.get('journal')}={item.get('status')}" for item in journals if isinstance(item, dict)]
        lines.append(f"- journal_statuses: {', '.join(journal_bits)}")
    if latest_audit:
        lines.append(
            f"- latest_audit: {latest_audit.get('figure_id')} {latest_audit.get('gate')} {latest_audit.get('result')}"
        )
    if latest_visual_regression:
        report = latest_visual_regression.get("visual_regression_report", latest_visual_regression)
        lines.append(f"- latest_visual_regression: {report.get('figure_id')} {report.get('result')}")
    pipeline_state = manifest.get("pipeline_state", {})
    if isinstance(pipeline_state, dict):
        lines.append(f"- pipeline_active_stage: {pipeline_state.get('active_stage')}")
        next_actions = pipeline_state.get("next_actions") or []
        if next_actions:
            lines.append("- next_actions:")
            lines.extend(f"  - {item}" for item in next_actions)
    lines.append(f"- awaiting_resume_boundaries: {len(awaiting)}")
    if awaiting:
        latest = awaiting[-1]
        lines.append(f"- latest_resume_hash: {latest.get('hash')} next={latest.get('next_stage')}")
    unresolved = manifest.get("unresolved_requirements") or []
    if unresolved:
        lines.append("- unresolved_requirements:")
        lines.extend(f"  - {item}" for item in unresolved)
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize project-local scientific figure memory.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--memory-dir", default=None)
    args = parser.parse_args()
    try:
        memory_dir = resolve_memory_dir(args.project_root, args.memory_dir)
        for line in summarize(memory_dir):
            print(line)
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
