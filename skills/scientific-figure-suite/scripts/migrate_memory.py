from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from _common import exit_with_results, main_error
from _memory import REQUIRED_JSONL_FILES, SCHEMA_VERSION, default_pipeline_state, load_json, resolve_memory_dir, save_json, utc_now


def ensure_jsonl_files(memory_dir: Path, created: list[str]) -> None:
    for filename in REQUIRED_JSONL_FILES:
        path = memory_dir / filename
        if not path.exists():
            path.write_text("", encoding="utf-8")
            created.append(filename)


def migrate_manifest(memory_dir: Path) -> None:
    manifest_path = memory_dir / "memory_manifest.json"
    if not manifest_path.exists():
        return
    data = load_json(manifest_path)
    manifest = data.setdefault("memory_manifest", {})
    manifest["schema_version"] = SCHEMA_VERSION
    manifest["updated_at"] = utc_now()
    files = manifest.setdefault("files", {})
    files.setdefault("journal_guideline_verification", "journal_guideline_verification.jsonl")
    files.setdefault("visual_audit_artifact", "visual_audit_artifact.jsonl")
    files.setdefault("figure_set_manifest", "figure_set_manifest.json")
    files.setdefault("submission_package_index", "submission_package_index.json")
    files.setdefault("cross_figure_consistency_history", "cross_figure_consistency_history.jsonl")
    files.setdefault("submission_readiness_history", "submission_readiness_history.jsonl")
    files.setdefault("figure_decision_log", "figure_decision_log.jsonl")
    files.setdefault("visual_regression_history", "visual_regression_history.jsonl")
    files.setdefault("dependency_plan_history", "dependency_plan_history.jsonl")
    files.setdefault("external_data_plan_history", "external_data_plan_history.jsonl")
    pipeline_state = manifest.setdefault("pipeline_state", default_pipeline_state())
    for key, value in default_pipeline_state().items():
        pipeline_state.setdefault(key, value)
    save_json(manifest_path, data)


def ensure_json_files(memory_dir: Path, created: list[str]) -> None:
    now = utc_now()
    project_id = "unknown-project"
    manifest_path = memory_dir / "memory_manifest.json"
    if manifest_path.exists():
        project_id = load_json(manifest_path).get("memory_manifest", {}).get("project_id", project_id)
    defaults = {
        "figure_set_manifest.json": {
            "figure_set_manifest": {
                "schema_version": SCHEMA_VERSION,
                "project_id": project_id,
                "created_at": now,
                "updated_at": now,
                "figures": [],
                "style_consistency_status": "NOT_RUN",
                "readiness_status": "NOT_RUN",
                "unresolved_requirements": [],
            }
        },
        "submission_package_index.json": {
            "submission_package_index": {
                "schema_version": SCHEMA_VERSION,
                "project_id": project_id,
                "created_at": now,
                "updated_at": now,
                "package_root": None,
                "files": [],
                "index_status": "NOT_RUN",
            }
        },
    }
    for filename, data in defaults.items():
        path = memory_dir / filename
        if not path.exists():
            save_json(path, data)
            created.append(filename)


def migrate_runtime_indexes(memory_dir: Path) -> None:
    for filename, root_key in [
        ("figure_set_manifest.json", "figure_set_manifest"),
        ("submission_package_index.json", "submission_package_index"),
    ]:
        path = memory_dir / filename
        if not path.exists():
            continue
        data = load_json(path)
        root = data.setdefault(root_key, {})
        root["schema_version"] = SCHEMA_VERSION
        root["updated_at"] = utc_now()
        save_json(path, data)


def migrate_passport(memory_dir: Path) -> None:
    passport_path = memory_dir / "figure_passport.json"
    if not passport_path.exists():
        return
    data = load_json(passport_path)
    passport = data.setdefault("figure_passport", {})
    passport["schema_version"] = SCHEMA_VERSION
    passport["updated_at"] = utc_now()
    figures = passport.setdefault("figures", [])
    if isinstance(figures, list):
        for figure in figures:
            if not isinstance(figure, dict):
                continue
            figure.setdefault("panels", [])
            figure.setdefault("stale", False)
            figure.setdefault("stale_reasons", [])
    save_json(passport_path, data)


def migrate(memory_dir: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    created: list[str] = []
    if not memory_dir.is_dir():
        return [f"memory directory missing: {memory_dir}"], warnings
    ensure_json_files(memory_dir, created)
    ensure_jsonl_files(memory_dir, created)
    migrate_manifest(memory_dir)
    migrate_passport(memory_dir)
    migrate_runtime_indexes(memory_dir)
    if created:
        warnings.append("created missing memory files: " + ", ".join(created))
    print(f"[MIGRATE] memory schema_version={SCHEMA_VERSION}")
    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Migrate scientific figure memory to the current schema.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--memory-dir", default=None)
    args = parser.parse_args()
    try:
        memory_dir = resolve_memory_dir(args.project_root, args.memory_dir)
        errors, warnings = migrate(memory_dir)
        exit_with_results(errors, warnings)
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
