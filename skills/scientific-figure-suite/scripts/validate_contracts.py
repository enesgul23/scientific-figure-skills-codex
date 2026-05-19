from __future__ import annotations

import argparse
import json
from pathlib import Path

from _common import exit_with_results, main_error


REQUIRED_SCHEMA_KEYS = {"$schema", "title", "type"}


def validate_contracts(skill_dir: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    contracts_dir = skill_dir / "shared" / "contracts"
    if not contracts_dir.is_dir():
        return ["shared/contracts directory is missing"], warnings

    schemas = sorted(contracts_dir.glob("*.schema.json"))
    if not schemas:
        return ["no JSON schema contracts found"], warnings

    for schema_path in schemas:
        try:
            data = json.loads(schema_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{schema_path.name}: invalid JSON: {exc}")
            continue
        missing = REQUIRED_SCHEMA_KEYS - set(data)
        if missing:
            errors.append(f"{schema_path.name}: missing schema keys {sorted(missing)}")
        if data.get("type") != "object":
            warnings.append(f"{schema_path.name}: root type is not object")
        if not data.get("required"):
            warnings.append(f"{schema_path.name}: no root required fields")

    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate scientific figure suite JSON contract schemas.")
    parser.add_argument("skill_dir", help="Path to scientific-figure-suite")
    args = parser.parse_args()
    try:
        errors, warnings = validate_contracts(Path(args.skill_dir))
        exit_with_results(errors, warnings)
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
