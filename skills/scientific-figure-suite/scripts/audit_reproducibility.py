from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from _common import as_list, exit_with_results, load_structured_file, main_error


def path_exists(base_dir: Path, value: Any) -> bool:
    if isinstance(value, dict):
        value = value.get("path")
    if not value:
        return False
    return (base_dir / str(value)).exists()


def validate(data: dict[str, Any], base_dir: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    design_only = data.get("design_only") is True or data.get("data_status") == "MOCKUP"
    code_sources = as_list(data.get("code_sources") or data.get("code"))
    data_sources = as_list(data.get("data_sources") or data.get("data"))
    outputs = as_list(data.get("files") or data.get("outputs"))

    if not code_sources and not design_only:
        errors.append("code_sources are required for data-derived figures")
    for code_source in code_sources:
        if not path_exists(base_dir, code_source):
            errors.append(f"code source missing: {code_source}")

    if not data_sources and not design_only:
        errors.append("data_sources are required unless design_only or MOCKUP")
    for data_source in data_sources:
        if not path_exists(base_dir, data_source):
            warnings.append(f"data source path not found locally: {data_source}")

    if not outputs:
        errors.append("generated outputs/files must be listed")

    if not data.get("environment_note"):
        warnings.append("environment_note is not listed")

    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit reproducibility metadata.")
    parser.add_argument("manifest")
    parser.add_argument("--base-dir", default=".")
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
