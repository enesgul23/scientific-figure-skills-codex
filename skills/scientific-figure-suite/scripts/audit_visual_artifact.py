from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from _common import exit_with_results, main_error
from _memory import append_jsonl, resolve_memory_dir, sha256_file, utc_now


def image_dimensions(path: Path) -> tuple[int | None, int | None, list[str]]:
    notes: list[str] = []
    try:
        from PIL import Image  # type: ignore
    except ImportError:
        return None, None, ["Pillow not available; dimensions not read."]
    try:
        with Image.open(path) as image:
            return int(image.width), int(image.height), notes
    except Exception as exc:
        return None, None, [f"dimensions not read: {exc}"]


def audit(args: argparse.Namespace) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    project_root = Path(args.project_root).expanduser().resolve()
    path = (project_root / args.path).resolve()
    if not path.exists() or not path.is_file():
        return [f"visual artifact file missing: {args.path}"], warnings

    width, height, dimension_notes = image_dimensions(path)
    notes = [*args.note, *dimension_notes]
    if dimension_notes:
        warnings.extend(dimension_notes)
    entry: dict[str, Any] = {
        "created_at": utc_now(),
        "figure_id": args.figure_id,
        "panel_id": args.panel_id,
        "path": args.path,
        "sha256": sha256_file(path),
        "format": path.suffix.lower().lstrip("."),
        "byte_size": path.stat().st_size,
        "width_px": width,
        "height_px": height,
        "result": args.result,
        "gate_summary": args.gate,
        "notes": notes,
    }
    memory_dir = resolve_memory_dir(project_root, args.memory_dir)
    append_jsonl(memory_dir / "visual_audit_artifact.jsonl", entry)
    print(f"[VISUAL-AUDIT-ARTIFACT] {args.figure_id} {args.path} {entry['sha256']}")
    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Append a file-level visual audit artifact entry.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--memory-dir", default=None)
    parser.add_argument("--figure-id", required=True)
    parser.add_argument("--panel-id")
    parser.add_argument("--path", required=True)
    parser.add_argument("--result", default="PASS_WITH_WARNINGS", choices=["PASS", "PASS_WITH_WARNINGS", "FAIL", "NOT_VERIFIABLE"])
    parser.add_argument("--gate", action="append", default=[])
    parser.add_argument("--note", action="append", default=[])
    args = parser.parse_args()
    try:
        errors, warnings = audit(args)
        exit_with_results(errors, warnings)
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
