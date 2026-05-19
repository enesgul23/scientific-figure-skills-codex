from __future__ import annotations

import argparse
import ast
from pathlib import Path
from typing import Any

from _common import exit_with_results, load_structured_file, main_error


REQUIRED_FIELDS = {
    "chart_type",
    "template_path",
    "required_columns",
    "optional_columns",
    "supported_domains",
    "default_outputs",
    "compatible_style_tokens",
    "audit_hooks",
    "library_stack_ids",
    "required_libraries",
    "optional_libraries",
    "unsupported_without",
    "dependency_profile",
    "external_data_roles",
}


def registry_entries(registry: dict[str, Any]) -> list[dict[str, Any]]:
    root = registry.get("render_registry", registry)
    entries = root.get("templates") if isinstance(root, dict) else None
    if not isinstance(entries, list):
        raise ValueError("render_registry.templates must be a list")
    return entries


def validate(skill_dir: Path, registry_path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    registry = load_structured_file(registry_path)
    if not isinstance(registry, dict):
        return ["render registry must be a JSON object"], warnings
    seen: set[str] = set()
    for index, entry in enumerate(registry_entries(registry), start=1):
        if not isinstance(entry, dict):
            errors.append(f"registry entry {index} must be an object")
            continue
        missing = REQUIRED_FIELDS - set(entry)
        if missing:
            errors.append(f"registry entry {index} missing fields: {sorted(missing)}")
            continue
        chart_type = str(entry.get("chart_type"))
        if chart_type in seen:
            errors.append(f"duplicate chart_type: {chart_type}")
        seen.add(chart_type)
        if not isinstance(entry.get("required_columns"), list) or not entry.get("required_columns"):
            errors.append(f"{chart_type}: required_columns must be a non-empty list")
        for list_field in [
            "optional_columns",
            "supported_domains",
            "default_outputs",
            "compatible_style_tokens",
            "audit_hooks",
            "library_stack_ids",
            "required_libraries",
            "optional_libraries",
            "unsupported_without",
            "external_data_roles",
        ]:
            if not isinstance(entry.get(list_field), list):
                errors.append(f"{chart_type}: {list_field} must be a list")
        if not entry.get("required_libraries"):
            errors.append(f"{chart_type}: required_libraries must be non-empty")
        if not entry.get("library_stack_ids"):
            errors.append(f"{chart_type}: library_stack_ids must be non-empty")
        if not isinstance(entry.get("dependency_profile"), str) or not entry.get("dependency_profile"):
            errors.append(f"{chart_type}: dependency_profile must be a non-empty string")
        unsupported = set(str(item) for item in entry.get("unsupported_without", []))
        required = set(str(item) for item in entry.get("required_libraries", []))
        if not unsupported.issubset(required):
            warnings.append(f"{chart_type}: unsupported_without should be a subset of required_libraries")
        template_path = skill_dir / str(entry.get("template_path", ""))
        if not template_path.is_file():
            errors.append(f"{chart_type}: template file missing: {entry.get('template_path')}")
            continue
        try:
            ast.parse(template_path.read_text(encoding="utf-8"), filename=str(template_path))
        except SyntaxError as exc:
            errors.append(f"{chart_type}: template is not valid Python: {exc}")
        if "png" not in [str(item).lower() for item in entry.get("default_outputs", [])]:
            warnings.append(f"{chart_type}: default_outputs should include png for visual QA")
    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the scientific figure render template registry.")
    parser.add_argument("--skill-dir", default=".")
    parser.add_argument("--registry", default="assets/render_registry/render_registry.json")
    args = parser.parse_args()
    try:
        skill_dir = Path(args.skill_dir).resolve()
        errors, warnings = validate(skill_dir, skill_dir / args.registry)
        exit_with_results(errors, warnings)
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
