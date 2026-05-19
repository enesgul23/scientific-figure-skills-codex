from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from _common import exit_with_results, main_error
from _memory import SCHEMA_VERSION, load_json, resolve_memory_dir, save_json, utc_now


def current_outputs(figure: dict[str, Any]) -> list[str]:
    current_version = figure.get("current_version")
    outputs: list[str] = []
    for version in figure.get("versions", []) or []:
        if isinstance(version, dict) and version.get("version") == current_version:
            outputs.extend(str(item) for item in version.get("outputs", []) or [])
    if not outputs:
        for panel in figure.get("panels", []) or []:
            if isinstance(panel, dict):
                outputs.extend(str(item) for item in panel.get("outputs", []) or [])
    return sorted(set(outputs))


def summarize_figure(figure: dict[str, Any]) -> dict[str, Any]:
    panels = [panel for panel in figure.get("panels", []) or [] if isinstance(panel, dict)]
    panel_stale = any(panel.get("stale") is True for panel in panels)
    status_tags = figure.get("status_tags", {}) if isinstance(figure.get("status_tags"), dict) else {}
    unresolved = list(figure.get("unresolved_requirements", []) or [])
    if figure.get("stale") is True or panel_stale:
        unresolved.append("Figure or panel is stale by repro-lock.")
    return {
        "figure_id": figure.get("figure_id"),
        "title": figure.get("title"),
        "purpose": figure.get("purpose"),
        "current_version": figure.get("current_version"),
        "journal_profile": figure.get("journal_profile"),
        "status_tags": status_tags,
        "stale": bool(figure.get("stale") is True or panel_stale),
        "panel_count": len(panels),
        "outputs": current_outputs(figure),
        "claim_refs": figure.get("claim_refs", []) or [],
        "dataset_refs": figure.get("dataset_refs", []) or [],
        "unresolved_requirements": sorted(set(unresolved)),
    }


def build(memory_dir: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    manifest_path = memory_dir / "memory_manifest.json"
    passport_path = memory_dir / "figure_passport.json"
    if not manifest_path.exists():
        return [f"memory manifest missing: {manifest_path}"], warnings
    if not passport_path.exists():
        return [f"figure passport missing: {passport_path}"], warnings

    memory_manifest = load_json(manifest_path).get("memory_manifest", {})
    passport = load_json(passport_path).get("figure_passport", {})
    figures = passport.get("figures", []) if isinstance(passport, dict) else []
    if not isinstance(figures, list):
        return ["figure_passport.figures must be a list"], warnings

    now = utc_now()
    summarized = [summarize_figure(figure) for figure in figures if isinstance(figure, dict)]
    unresolved = sorted(
        {
            item
            for figure in summarized
            for item in (figure.get("unresolved_requirements", []) or [])
            if item
        }
    )
    data = {
        "figure_set_manifest": {
            "schema_version": SCHEMA_VERSION,
            "project_id": memory_manifest.get("project_id", "unknown-project"),
            "created_at": now,
            "updated_at": now,
            "figures": summarized,
            "style_consistency_status": "NOT_RUN",
            "readiness_status": "NOT_RUN",
            "unresolved_requirements": unresolved,
        }
    }
    save_json(memory_dir / "figure_set_manifest.json", data)
    print(f"[FIGURE-SET] wrote {memory_dir / 'figure_set_manifest.json'} figures={len(summarized)}")
    if not summarized:
        warnings.append("figure set is empty")
    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Build figure_set_manifest.json from Figure Passport memory.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--memory-dir", default=None)
    args = parser.parse_args()
    try:
        memory_dir = resolve_memory_dir(args.project_root, args.memory_dir)
        errors, warnings = build(memory_dir)
        exit_with_results(errors, warnings)
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
