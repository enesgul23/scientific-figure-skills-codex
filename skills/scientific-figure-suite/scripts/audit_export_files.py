from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from _common import as_list, exit_with_results, load_structured_file, main_error


VECTOR_FORMATS = {"pdf", "svg", "eps"}
RASTER_FORMATS = {"png", "tif", "tiff", "jpg", "jpeg"}


def validate(manifest: dict[str, Any], base_dir: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not manifest.get("figure_id"):
        errors.append("figure_id is required")

    files = as_list(manifest.get("files"))
    if not files:
        errors.append("files list is required")
    else:
        seen_formats: set[str] = set()
        for item in files:
            path_text = item.get("path") if isinstance(item, dict) else str(item)
            file_path = base_dir / path_text
            suffix = file_path.suffix.lower().lstrip(".")
            if suffix:
                seen_formats.add(suffix)
            if not file_path.exists():
                errors.append(f"listed export file is missing: {path_text}")
        if not (seen_formats & VECTOR_FORMATS):
            warnings.append("no vector export listed")
        if not (seen_formats & RASTER_FORMATS):
            warnings.append("no raster review export listed")

    if not manifest.get("style_status"):
        errors.append("style_status is required")
    if not manifest.get("quality_report"):
        warnings.append("quality_report is not listed")

    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit exported figure files against a manifest.")
    parser.add_argument("manifest")
    parser.add_argument("--base-dir", default=".", help="Base directory for manifest file paths")
    args = parser.parse_args()
    try:
        data = load_structured_file(args.manifest)
        if not isinstance(data, dict):
            raise ValueError("manifest must be a mapping")
        errors, warnings = validate(data, Path(args.base_dir))
        exit_with_results(errors, warnings)
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
