from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


VALID_STYLE_STATUSES = {"VERIFIED", "ESTIMATED", "UNVERIFIED"}
VALID_DATA_STATUSES = {"PROVIDED", "INFERRED", "MISSING", "MOCKUP"}


def load_structured_file(path: str | Path) -> Any:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Missing file: {file_path}")

    text = file_path.read_text(encoding="utf-8")
    if file_path.suffix.lower() == ".json":
        return json.loads(text)

    try:
        import yaml  # type: ignore
    except ImportError as exc:
        raise RuntimeError("PyYAML is required for YAML files.") from exc

    return yaml.safe_load(text)


def write_json(path: str | Path, data: Any) -> None:
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def flatten_strings(value: Any) -> str:
    parts: list[str] = []

    def walk(item: Any) -> None:
        if isinstance(item, str):
            parts.append(item)
        elif isinstance(item, dict):
            for sub in item.values():
                walk(sub)
        elif isinstance(item, list):
            for sub in item:
                walk(sub)

    walk(value)
    return "\n".join(parts)


def result_line(status: str, message: str) -> str:
    return f"[{status}] {message}"


def exit_with_results(errors: list[str], warnings: list[str] | None = None) -> None:
    warnings = warnings or []
    for warning in warnings:
        print(result_line("WARN", warning))
    if errors:
        for error in errors:
            print(result_line("FAIL", error))
        raise SystemExit(1)
    print(result_line("PASS", "validation passed"))
    raise SystemExit(0)


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def parse_csv_arg(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def main_error(exc: Exception) -> None:
    print(result_line("FAIL", str(exc)), file=sys.stderr)
    raise SystemExit(1)
