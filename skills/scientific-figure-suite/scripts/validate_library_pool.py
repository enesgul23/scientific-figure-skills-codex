from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from _common import exit_with_results, load_structured_file, main_error


REQUIRED_FIELDS = {
    "library_id",
    "package_name",
    "import_names",
    "pip_name",
    "conda_name",
    "category",
    "domains",
    "chart_families",
    "data_formats",
    "output_formats",
    "capabilities",
    "limitations",
    "publication_grade",
    "install_risk",
    "system_dependencies",
    "selection_priority",
    "fallbacks",
    "import_probe",
}
LIST_FIELDS = {
    "import_names",
    "domains",
    "chart_families",
    "data_formats",
    "output_formats",
    "capabilities",
    "limitations",
    "system_dependencies",
    "fallbacks",
}
PUBLICATION_GRADES = {"PRIMARY", "SUPPORT", "EXPLORATORY", "SPECIALIST"}
INSTALL_RISKS = {"LOW", "MEDIUM", "HIGH"}


def pool_libraries(data: dict[str, Any]) -> list[dict[str, Any]]:
    root = data.get("library_pool", data)
    libraries = root.get("libraries") if isinstance(root, dict) else None
    if not isinstance(libraries, list):
        raise ValueError("library_pool.libraries must be a list")
    return libraries


def validate(pool_path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    data = load_structured_file(pool_path)
    if not isinstance(data, dict):
        return ["library pool must be a JSON object"], warnings
    libraries = pool_libraries(data)
    seen: set[str] = set()
    library_ids: set[str] = set()
    for item in libraries:
        if isinstance(item, dict) and item.get("library_id"):
            library_ids.add(str(item["library_id"]))

    for index, library in enumerate(libraries, start=1):
        if not isinstance(library, dict):
            errors.append(f"library entry {index} must be an object")
            continue
        missing = REQUIRED_FIELDS - set(library)
        if missing:
            errors.append(f"library entry {index} missing fields: {sorted(missing)}")
            continue
        library_id = str(library.get("library_id"))
        if library_id in seen:
            errors.append(f"duplicate library_id: {library_id}")
        seen.add(library_id)
        for field in LIST_FIELDS:
            if not isinstance(library.get(field), list):
                errors.append(f"{library_id}: {field} must be a list")
        if not library.get("import_names"):
            errors.append(f"{library_id}: import_names must not be empty")
        if library.get("publication_grade") not in PUBLICATION_GRADES:
            errors.append(f"{library_id}: invalid publication_grade")
        if library.get("install_risk") not in INSTALL_RISKS:
            errors.append(f"{library_id}: invalid install_risk")
        priority = library.get("selection_priority")
        if not isinstance(priority, (int, float)):
            errors.append(f"{library_id}: selection_priority must be numeric")
        import_probe = library.get("import_probe")
        if not isinstance(import_probe, dict) or not import_probe.get("import_name"):
            errors.append(f"{library_id}: import_probe.import_name is required")
        for fallback in library.get("fallbacks", []):
            if fallback not in library_ids and fallback != "hexbin":
                warnings.append(f"{library_id}: fallback library not in pool: {fallback}")
    if len(libraries) < 30:
        warnings.append("library pool is small for a broad scientific figure suite")
    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate Scientific Figure Suite library pool metadata.")
    parser.add_argument("--skill-dir", default=Path(__file__).resolve().parents[1])
    parser.add_argument("--library-pool", default="assets/library_pool/library_pool.json")
    args = parser.parse_args()
    try:
        skill_dir = Path(args.skill_dir).resolve()
        errors, warnings = validate(skill_dir / args.library_pool)
        exit_with_results(errors, warnings)
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
