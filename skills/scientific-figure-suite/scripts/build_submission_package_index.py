from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from _common import exit_with_results, main_error
from _memory import SCHEMA_VERSION, load_json, resolve_memory_dir, save_json, sha256_file, utc_now


FIGURE_FORMATS = {"pdf", "svg", "eps", "png", "tif", "tiff", "jpg", "jpeg"}


def infer_role(path: Path) -> str:
    suffix = path.suffix.lower().lstrip(".")
    name = path.name.lower()
    if suffix in FIGURE_FORMATS:
        return "figure_output"
    if suffix in {"py", "r", "ipynb"}:
        return "code"
    if suffix in {"csv", "tsv", "xlsx", "json", "yaml", "yml"}:
        return "data_or_manifest"
    if "caption" in name:
        return "caption"
    if "alt" in name:
        return "alt_text"
    return "supporting_file"


def infer_figure_id(path: Path, known_ids: set[str], explicit: str | None) -> str | None:
    if explicit:
        return explicit
    name = path.name.lower()
    for figure_id in known_ids:
        if figure_id.lower() in name:
            return figure_id
    return None


def collect_files(project_root: Path, package_root: str | None, explicit_files: list[str]) -> tuple[list[Path], list[str]]:
    errors: list[str] = []
    files: list[Path] = []
    if package_root:
        root = (project_root / package_root).resolve()
        if not root.is_dir():
            errors.append(f"package root missing: {package_root}")
        else:
            files.extend(path for path in sorted(root.rglob("*")) if path.is_file())
    for item in explicit_files:
        path = (project_root / item).resolve()
        if not path.exists() or not path.is_file():
            errors.append(f"package file missing: {item}")
        else:
            files.append(path)
    unique = []
    seen: set[Path] = set()
    for path in files:
        if path not in seen:
            seen.add(path)
            unique.append(path)
    return unique, errors


def build(args: argparse.Namespace) -> tuple[list[str], list[str]]:
    warnings: list[str] = []
    project_root = Path(args.project_root).expanduser().resolve()
    memory_dir = resolve_memory_dir(project_root, args.memory_dir)
    manifest = load_json(memory_dir / "memory_manifest.json").get("memory_manifest", {})
    passport = load_json(memory_dir / "figure_passport.json").get("figure_passport", {})
    known_ids = {
        str(figure.get("figure_id"))
        for figure in passport.get("figures", []) or []
        if isinstance(figure, dict) and figure.get("figure_id")
    }
    files, errors = collect_files(project_root, args.package_root, args.file)
    entries: list[dict[str, Any]] = []
    for path in files:
        rel_path = path.relative_to(project_root).as_posix()
        entries.append(
            {
                "path": rel_path,
                "sha256": sha256_file(path),
                "byte_size": path.stat().st_size,
                "role": infer_role(path),
                "figure_id": infer_figure_id(path, known_ids, args.figure_id),
            }
        )
    now = utc_now()
    index_status = "FAIL" if errors else ("PASS_WITH_WARNINGS" if not entries else "PASS")
    if not entries:
        warnings.append("submission package index has no files")
    data = {
        "submission_package_index": {
            "schema_version": SCHEMA_VERSION,
            "project_id": manifest.get("project_id", "unknown-project"),
            "created_at": now,
            "updated_at": now,
            "package_root": args.package_root,
            "files": entries,
            "index_status": index_status,
        }
    }
    save_json(memory_dir / "submission_package_index.json", data)
    print(f"[PACKAGE-INDEX] files={len(entries)} status={index_status}")
    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a submission package hash index.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--memory-dir", default=None)
    parser.add_argument("--package-root")
    parser.add_argument("--file", action="append", default=[])
    parser.add_argument("--figure-id")
    args = parser.parse_args()
    try:
        errors, warnings = build(args)
        exit_with_results(errors, warnings)
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
