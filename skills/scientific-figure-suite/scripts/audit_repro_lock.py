from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from _common import exit_with_results, main_error
from _memory import load_json, resolve_memory_dir, save_json, sha256_file, utc_now


def compare_hash_group(project_root: Path, stored: dict[str, str], label: str, reasons: list[str]) -> None:
    for rel_path, expected_hash in stored.items():
        path = (project_root / rel_path).resolve()
        if not path.exists():
            reasons.append(f"{label} missing: {rel_path}")
            continue
        actual_hash = sha256_file(path)
        if actual_hash != expected_hash:
            reasons.append(f"{label} hash drift: {rel_path}")


def audit_lock(project_root: Path, item: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    lock = item.get("repro_lock")
    if not isinstance(lock, dict):
        return ["repro_lock missing"]
    compare_hash_group(project_root, lock.get("data_hashes", {}), "data", reasons)
    compare_hash_group(project_root, lock.get("code_hashes", {}), "code", reasons)
    compare_hash_group(project_root, lock.get("output_hashes", {}), "output", reasons)
    if reasons:
        lock["audit_status"] = "STALE"
        lock["audited_at"] = utc_now()
    else:
        lock["audit_status"] = "PASS"
        lock["audited_at"] = utc_now()
    return reasons


def audit(memory_dir: Path, project_root: Path, update_stale: bool) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    passport_path = memory_dir / "figure_passport.json"
    if not passport_path.exists():
        return [f"figure passport missing: {passport_path}"], warnings
    data = load_json(passport_path)
    passport = data.get("figure_passport", {})
    figures = passport.get("figures", []) if isinstance(passport, dict) else []
    if not isinstance(figures, list):
        return ["figure_passport.figures must be a list"], warnings

    for figure in figures:
        if not isinstance(figure, dict):
            continue
        figure_reasons: list[str] = []
        if figure.get("repro_lock"):
            figure_reasons.extend(audit_lock(project_root, figure))
        for panel in figure.get("panels", []) or []:
            if not isinstance(panel, dict):
                continue
            panel_reasons = audit_lock(project_root, panel) if panel.get("repro_lock") else []
            if panel_reasons:
                warnings.append(f"{figure.get('figure_id')} panel {panel.get('panel_id')} stale: {'; '.join(panel_reasons)}")
                if update_stale:
                    panel["stale"] = True
                    panel["stale_reasons"] = panel_reasons
                    figure_reasons.extend([f"panel {panel.get('panel_id')}: {reason}" for reason in panel_reasons])
        if figure_reasons:
            warnings.append(f"{figure.get('figure_id')} stale: {'; '.join(figure_reasons)}")
            if update_stale:
                figure["stale"] = True
                figure["stale_reasons"] = figure_reasons
        elif figure.get("repro_lock") or figure.get("panels"):
            if update_stale:
                figure["stale"] = False
                figure["stale_reasons"] = []

    if update_stale:
        passport["updated_at"] = utc_now()
        save_json(passport_path, data)

    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Figure Passport repro-lock hashes and mark stale drift.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--memory-dir", default=None)
    parser.add_argument("--update-stale", action="store_true")
    args = parser.parse_args()
    try:
        project_root = Path(args.project_root).expanduser().resolve()
        memory_dir = resolve_memory_dir(project_root, args.memory_dir)
        errors, warnings = audit(memory_dir, project_root, args.update_stale)
        exit_with_results(errors, warnings)
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
