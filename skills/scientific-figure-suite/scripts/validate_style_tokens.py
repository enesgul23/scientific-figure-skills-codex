from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from _common import exit_with_results, load_structured_file, main_error
from _memory import VALID_STYLE_STATUSES


def list_value(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def minimum_font_size(token: dict[str, Any]) -> float | None:
    accessibility = token.get("accessibility", {})
    if isinstance(accessibility, dict) and isinstance(accessibility.get("minimum_font_size_pt"), (int, float)):
        return float(accessibility["minimum_font_size_pt"])
    text_size = token.get("text_size_pt", {})
    if isinstance(text_size, dict):
        values = [
            value
            for key, value in text_size.items()
            if key in {"minimum", "preferred_min", "other_min", "panel_label"}
            and isinstance(value, (int, float))
        ]
        if values:
            return float(min(values))
    return None


def has_palette(token: dict[str, Any]) -> bool:
    palette = token.get("palette")
    accessibility = token.get("accessibility", {})
    if isinstance(accessibility, dict) and accessibility.get("palette"):
        palette = accessibility.get("palette")
    if isinstance(palette, list):
        return bool(palette)
    if isinstance(palette, dict):
        return any(bool(value) for value in palette.values())
    return False


def colorblind_safe(token: dict[str, Any]) -> bool:
    accessibility = token.get("accessibility", {})
    if isinstance(accessibility, dict) and accessibility.get("colorblind_safe") is True:
        return True
    return token.get("colorblind_safe") is True


def validate_token(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    data = load_structured_file(path)
    if not isinstance(data, dict):
        return [f"{path.name}: token must be a JSON object"], warnings
    profile_name = data.get("profile_name")
    if not profile_name:
        errors.append(f"{path.name}: profile_name is required")
    elif path.stem != "universal" and profile_name != path.stem:
        warnings.append(f"{path.name}: profile_name does not match file stem")
    if data.get("status") not in VALID_STYLE_STATUSES:
        errors.append(f"{path.name}: status must be VERIFIED, ESTIMATED, or UNVERIFIED")
    if not isinstance(data.get("requires_live_verification"), bool):
        errors.append(f"{path.name}: requires_live_verification must be boolean")
    if data.get("status") == "VERIFIED" and data.get("requires_live_verification") is True:
        errors.append(f"{path.name}: stored estimated profile cannot be VERIFIED while requires_live_verification is true")
    font = data.get("font")
    if not isinstance(font, dict) or not (list_value(font.get("preferred")) + list_value(font.get("fallback"))):
        errors.append(f"{path.name}: font preferred or fallback family is required")
    min_size = minimum_font_size(data)
    if min_size is None:
        errors.append(f"{path.name}: minimum font size is required")
    elif min_size < 5:
        errors.append(f"{path.name}: minimum font size must be at least 5 pt")
    if not has_palette(data):
        errors.append(f"{path.name}: color palette is required")
    if not colorblind_safe(data):
        errors.append(f"{path.name}: colorblind_safe must be true")
    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate scientific figure style token JSON files.")
    parser.add_argument("--tokens-dir", default="assets/style_tokens")
    args = parser.parse_args()
    try:
        tokens_dir = Path(args.tokens_dir)
        paths = sorted(tokens_dir.glob("*.json"))
        if not paths:
            raise FileNotFoundError(f"no style token JSON files found in {tokens_dir}")
        errors: list[str] = []
        warnings: list[str] = []
        for path in paths:
            token_errors, token_warnings = validate_token(path)
            errors.extend(token_errors)
            warnings.extend(token_warnings)
        exit_with_results(errors, warnings)
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
