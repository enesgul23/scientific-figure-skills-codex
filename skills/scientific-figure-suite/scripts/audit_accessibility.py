from __future__ import annotations

import argparse
from typing import Any

from _common import exit_with_results, load_structured_file, main_error


def validate(data: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    accessibility = data.get("accessibility", data)
    if not isinstance(accessibility, dict):
        return ["accessibility must be a mapping"], warnings

    if not accessibility.get("palette"):
        errors.append("palette is required")
    if accessibility.get("red_green_only") is True:
        errors.append("red_green_only must be false")
    if accessibility.get("colorblind_safe") is not True:
        warnings.append("colorblind_safe is not confirmed true")

    min_font_size = accessibility.get("min_font_size_pt")
    if not isinstance(min_font_size, (int, float)):
        errors.append("min_font_size_pt is required")
    elif min_font_size < 6:
        errors.append("min_font_size_pt must be at least 6")

    if accessibility.get("alt_text_present") is not True:
        errors.append("alt_text_present must be true")
    if accessibility.get("contrast_status") in (None, "unknown"):
        errors.append("contrast_status must not be unknown")
    if accessibility.get("non_color_redundancy") is not True:
        warnings.append("non_color_redundancy is not confirmed true")

    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit figure accessibility metadata.")
    parser.add_argument("accessibility_spec")
    args = parser.parse_args()
    try:
        data = load_structured_file(args.accessibility_spec)
        if not isinstance(data, dict):
            raise ValueError("accessibility spec must be a mapping")
        errors, warnings = validate(data)
        exit_with_results(errors, warnings)
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
