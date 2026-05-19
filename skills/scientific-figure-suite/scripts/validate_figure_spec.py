from __future__ import annotations

import argparse
from typing import Any

from _common import VALID_DATA_STATUSES, VALID_STYLE_STATUSES, exit_with_results, load_structured_file, main_error


def get_style_status(spec: dict[str, Any]) -> str | None:
    target = spec.get("target_journal") or spec.get("journal_style") or {}
    if isinstance(target, dict):
        return target.get("style_status") or target.get("status")
    return spec.get("style_status")


def validate(spec: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not spec.get("figure_id"):
        errors.append("figure_id is required")
    if not spec.get("figure_type"):
        errors.append("figure_type is required")

    data_status = spec.get("data_status")
    if data_status not in VALID_DATA_STATUSES:
        errors.append(f"data_status must be one of {sorted(VALID_DATA_STATUSES)}")

    style_status = get_style_status(spec)
    if style_status not in VALID_STYLE_STATUSES:
        errors.append(f"target journal style status must be one of {sorted(VALID_STYLE_STATUSES)}")

    axes = spec.get("axes")
    if axes:
        if not isinstance(axes, dict):
            errors.append("axes must be a mapping")
        else:
            for axis_name, axis in axes.items():
                if not isinstance(axis, dict):
                    errors.append(f"axis {axis_name} must be a mapping")
                    continue
                if not axis.get("label"):
                    errors.append(f"axis {axis_name} missing label")
                if axis.get("units") in (None, ""):
                    warnings.append(f"axis {axis_name} has no units; confirm variable is dimensionless")

    export = spec.get("export")
    if not isinstance(export, dict):
        errors.append("export mapping is required")
    else:
        formats = export.get("formats")
        if not formats:
            errors.append("export.formats is required")
        if "png" in formats or "tiff" in formats:
            dpi = export.get("dpi")
            if not isinstance(dpi, int) or dpi < 300:
                errors.append("raster exports require export.dpi >= 300")

    if data_status == "MOCKUP" and spec.get("reproducibility_status") == "CODED":
        warnings.append("mockup data with CODED reproducibility should be checked")

    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a scientific figure spec YAML/JSON file.")
    parser.add_argument("figure_spec")
    args = parser.parse_args()
    try:
        data = load_structured_file(args.figure_spec)
        if not isinstance(data, dict):
            raise ValueError("figure spec must be a mapping")
        errors, warnings = validate(data)
        exit_with_results(errors, warnings)
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
