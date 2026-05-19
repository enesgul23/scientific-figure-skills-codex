from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from _common import VALID_DATA_STATUSES, exit_with_results, main_error
from _memory import (
    BOUNDARY_HASH_MODE,
    VALID_STYLE_STATUSES,
    append_jsonl,
    compute_boundary_hash,
    load_json,
    read_jsonl,
    resolve_memory_dir,
    save_json,
    sha256_file,
    utc_now,
)


VALID_REPRODUCIBILITY_STATUSES = {"CODED", "DESIGN_ONLY", "PARTIAL"}
VALID_INTEGRITY_STATUSES = {"PASS", "PASS_WITH_WARNINGS", "FAIL"}


def find_figure(figures: list[dict[str, Any]], figure_id: str) -> dict[str, Any] | None:
    for figure in figures:
        if figure.get("figure_id") == figure_id:
            return figure
    return None


def make_status_tags(args: argparse.Namespace) -> dict[str, str]:
    tags: dict[str, str] = {}
    if args.data_status:
        tags["DATA_STATUS"] = args.data_status
    if args.style_status:
        tags["STYLE_STATUS"] = args.style_status
    if args.reproducibility_status:
        tags["REPRODUCIBILITY_STATUS"] = args.reproducibility_status
    if args.integrity_status:
        tags["INTEGRITY_STATUS"] = args.integrity_status
    return tags


def path_hashes(project_root: Path, paths: list[str], label: str, errors: list[str]) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for item in paths:
        path = (project_root / item).resolve()
        if not path.exists():
            errors.append(f"{label} file missing for repro-lock: {item}")
            continue
        if not path.is_file():
            errors.append(f"{label} path is not a file for repro-lock: {item}")
            continue
        hashes[item] = sha256_file(path)
    return hashes


def build_repro_lock(args: argparse.Namespace, project_root: Path, errors: list[str]) -> dict[str, Any] | None:
    if not args.repro_lock:
        return None
    return {
        "created_at": utc_now(),
        "hash_algorithm": "sha256",
        "data_hashes": path_hashes(project_root, args.data_file, "data", errors),
        "code_hashes": path_hashes(project_root, args.code_file, "code", errors),
        "output_hashes": path_hashes(project_root, args.output, "output", errors),
        "render_command": args.render_command,
        "environment_note": args.environment_note,
        "audit_status": "NOT_RUN",
    }


def find_panel(panels: list[dict[str, Any]], panel_id: str) -> dict[str, Any] | None:
    for panel in panels:
        if panel.get("panel_id") == panel_id:
            return panel
    return None


def update_panel(figure: dict[str, Any], args: argparse.Namespace, repro_lock: dict[str, Any] | None) -> None:
    if not args.panel_id:
        return
    panels = figure.setdefault("panels", [])
    panel = find_panel(panels, args.panel_id)
    if panel is None:
        panel = {
            "panel_id": args.panel_id,
            "purpose": args.panel_purpose or args.purpose or "",
            "data_source": args.panel_data_source,
            "claim_refs": args.panel_claim_ref or args.claim_ref,
            "script_ref": args.panel_script_ref or args.script,
            "outputs": args.panel_output or args.output,
            "status_tags": {},
            "repro_lock": None,
            "stale": False,
            "stale_reasons": [],
        }
        panels.append(panel)
    else:
        if args.panel_purpose:
            panel["purpose"] = args.panel_purpose
        if args.panel_data_source:
            panel["data_source"] = args.panel_data_source
        if args.panel_claim_ref:
            panel["claim_refs"] = sorted(set(panel.get("claim_refs", []) + args.panel_claim_ref))
        if args.panel_script_ref:
            panel["script_ref"] = args.panel_script_ref
        if args.panel_output:
            panel["outputs"] = sorted(set(panel.get("outputs", []) + args.panel_output))
    status_tags = make_status_tags(args)
    if status_tags:
        panel.setdefault("status_tags", {}).update(status_tags)
    if repro_lock is not None:
        panel["repro_lock"] = repro_lock
        panel["stale"] = False
        panel["stale_reasons"] = []


def validate_status_args(args: argparse.Namespace) -> list[str]:
    errors: list[str] = []
    if args.data_status and args.data_status not in VALID_DATA_STATUSES:
        errors.append(f"--data-status must be one of {sorted(VALID_DATA_STATUSES)}")
    if args.style_status and args.style_status not in VALID_STYLE_STATUSES:
        errors.append(f"--style-status must be one of {sorted(VALID_STYLE_STATUSES)}")
    if args.reproducibility_status and args.reproducibility_status not in VALID_REPRODUCIBILITY_STATUSES:
        errors.append(f"--reproducibility-status must be one of {sorted(VALID_REPRODUCIBILITY_STATUSES)}")
    if args.integrity_status and args.integrity_status not in VALID_INTEGRITY_STATUSES:
        errors.append(f"--integrity-status must be one of {sorted(VALID_INTEGRITY_STATUSES)}")
    return errors


def update_passport(args: argparse.Namespace) -> tuple[list[str], list[str]]:
    errors = validate_status_args(args)
    warnings: list[str] = []
    if errors:
        return errors, warnings

    memory_dir = resolve_memory_dir(args.project_root, args.memory_dir)
    project_root = Path(args.project_root).expanduser().resolve()
    passport_path = memory_dir / "figure_passport.json"
    if not passport_path.exists():
        return [f"figure passport missing: {passport_path}"], warnings

    data = load_json(passport_path)
    passport = data.setdefault("figure_passport", {})
    figures = passport.setdefault("figures", [])
    if not isinstance(figures, list):
        return ["figure_passport.figures must be a list"], warnings

    now = utc_now()
    repro_lock = build_repro_lock(args, project_root, errors)
    if errors:
        return errors, warnings
    figure = find_figure(figures, args.figure_id)
    if figure is None:
        figure = {
            "figure_id": args.figure_id,
            "title": args.title or args.figure_id,
            "purpose": args.purpose or "",
            "chart_type": args.chart_type or "",
            "journal_profile": args.journal_profile or "",
            "dataset_refs": args.dataset_ref,
            "claim_refs": args.claim_ref,
            "versions": [],
            "current_version": None,
            "status_tags": {},
            "created_at": now,
            "updated_at": now,
        }
        figures.append(figure)
    else:
        for field in ["title", "purpose", "chart_type", "journal_profile"]:
            value = getattr(args, field)
            if value:
                figure[field] = value
        if args.dataset_ref:
            figure["dataset_refs"] = sorted(set(figure.get("dataset_refs", []) + args.dataset_ref))
        if args.claim_ref:
            figure["claim_refs"] = sorted(set(figure.get("claim_refs", []) + args.claim_ref))
        figure["updated_at"] = now

    status_tags = make_status_tags(args)
    if status_tags:
        figure.setdefault("status_tags", {}).update(status_tags)
    if repro_lock is not None and not args.panel_id:
        figure["repro_lock"] = repro_lock
        figure["stale"] = False
        figure["stale_reasons"] = []

    if args.version:
        versions = figure.setdefault("versions", [])
        version_entry = {
            "version": args.version,
            "created_at": now,
            "script": args.script,
            "outputs": args.output,
            "notes": args.note,
            "status_tags": status_tags or figure.get("status_tags", {}),
        }
        versions.append(version_entry)
        figure["current_version"] = args.version
    update_panel(figure, args, repro_lock)

    passport["updated_at"] = now
    save_json(passport_path, data)

    if args.append_boundary:
        if not args.completed_stage or not args.next_stage:
            return ["--append-boundary requires --completed-stage and --next-stage"], warnings
        ledger_path = memory_dir / "revision_boundary_ledger.jsonl"
        prior_entries = read_jsonl(ledger_path)
        boundary = {
            "kind": "boundary",
            "hash": "000000000000",
            "hash_mode": BOUNDARY_HASH_MODE,
            "created_at": now,
            "figure_id": args.figure_id,
            "from_version": args.from_version,
            "to_version": args.version or figure.get("current_version"),
            "completed_stage": args.completed_stage,
            "next_stage": args.next_stage,
            "reason": args.boundary_reason or "Figure memory checkpoint.",
            "artifact_refs": ["figure_passport.json"],
            "verification_status": args.boundary_verification_status,
        }
        boundary["hash"] = compute_boundary_hash(prior_entries, boundary)
        append_jsonl(ledger_path, boundary)
        print(f"[FIGURE-PASSPORT-RESET: hash={boundary['hash']}, figure_id={args.figure_id}, next={args.next_stage}]")

    print(f"[UPDATE] figure_passport.json figure_id={args.figure_id}")
    manifest_path = memory_dir / "memory_manifest.json"
    if manifest_path.exists():
        manifest_data = load_json(manifest_path)
        manifest = manifest_data.setdefault("memory_manifest", {})
        manifest["active_figure_id"] = args.figure_id
        if args.completed_stage:
            manifest["current_stage"] = args.completed_stage
        manifest["updated_at"] = now
        save_json(manifest_path, manifest_data)
    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Update project-local Figure Passport memory.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--memory-dir", default=None)
    parser.add_argument("--figure-id", required=True)
    parser.add_argument("--title")
    parser.add_argument("--purpose")
    parser.add_argument("--chart-type")
    parser.add_argument("--journal-profile")
    parser.add_argument("--dataset-ref", action="append", default=[])
    parser.add_argument("--claim-ref", action="append", default=[])
    parser.add_argument("--panel-id")
    parser.add_argument("--panel-purpose")
    parser.add_argument("--panel-data-source")
    parser.add_argument("--panel-claim-ref", action="append", default=[])
    parser.add_argument("--panel-script-ref")
    parser.add_argument("--panel-output", action="append", default=[])
    parser.add_argument("--version")
    parser.add_argument("--from-version")
    parser.add_argument("--script")
    parser.add_argument("--output", action="append", default=[])
    parser.add_argument("--note")
    parser.add_argument("--data-status")
    parser.add_argument("--style-status")
    parser.add_argument("--reproducibility-status")
    parser.add_argument("--integrity-status")
    parser.add_argument("--repro-lock", action="store_true")
    parser.add_argument("--data-file", action="append", default=[])
    parser.add_argument("--code-file", action="append", default=[])
    parser.add_argument("--render-command")
    parser.add_argument("--environment-note")
    parser.add_argument("--append-boundary", action="store_true")
    parser.add_argument("--completed-stage")
    parser.add_argument("--next-stage")
    parser.add_argument("--boundary-reason")
    parser.add_argument("--boundary-verification-status", default="UNVERIFIED", choices=["VERIFIED", "STALE", "UNVERIFIED"])
    args = parser.parse_args()
    try:
        errors, warnings = update_passport(args)
        exit_with_results(errors, warnings)
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
