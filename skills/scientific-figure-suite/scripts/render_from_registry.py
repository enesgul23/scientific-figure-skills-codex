from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from _common import load_structured_file, main_error, parse_csv_arg, write_json
from _memory import sha256_file, utc_now
from validate_render_template_registry import registry_entries


def load_table_as_csv(data_path: Path, outdir: Path, basename: str) -> Path:
    if data_path.suffix.lower() == ".csv":
        return data_path
    try:
        import pandas as pd  # type: ignore
    except ImportError as exc:
        raise RuntimeError("pandas is required to convert non-CSV data for render templates") from exc
    if data_path.suffix.lower() == ".json":
        frame = pd.read_json(data_path)
    else:
        raise ValueError("render_from_registry supports CSV and JSON data")
    csv_path = outdir / f"{basename}_input.csv"
    frame.to_csv(csv_path, index=False)
    return csv_path


def select_entry(registry: dict[str, Any], chart_type: str) -> dict[str, Any]:
    for entry in registry_entries(registry):
        if entry.get("chart_type") == chart_type:
            return entry
    raise ValueError(f"unknown chart_type: {chart_type}")


def parse_column_overrides(values: list[str]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"--column must use role=column form: {value}")
        role, column = value.split("=", 1)
        mapping[role.strip()] = column.strip()
    return mapping


def validate_dependency_plan(path_value: str, chart_type: str) -> dict[str, Any] | None:
    if not path_value:
        return None
    plan_path = Path(path_value).resolve()
    data = load_structured_file(plan_path)
    if not isinstance(data, dict):
        raise ValueError("dependency plan must be a JSON object")
    plan = data.get("dependency_plan", data)
    if not isinstance(plan, dict):
        raise ValueError("dependency_plan must be an object")
    plan_chart_type = plan.get("chart_type")
    if plan_chart_type and plan_chart_type != chart_type:
        raise ValueError(f"dependency plan chart_type {plan_chart_type} does not match requested {chart_type}")
    blocked = plan.get("blocked_libraries", [])
    if blocked:
        blocked_ids = []
        for item in blocked:
            if isinstance(item, dict):
                blocked_ids.append(str(item.get("library_id", item)))
            else:
                blocked_ids.append(str(item))
        raise RuntimeError("required libraries missing for render: " + ", ".join(blocked_ids))
    return {"path": str(plan_path), "plan": plan}


def available_columns(csv_path: Path) -> list[str]:
    try:
        import pandas as pd  # type: ignore
    except ImportError as exc:
        raise RuntimeError("pandas is required to inspect render input columns") from exc
    return [str(item) for item in pd.read_csv(csv_path, nrows=1).columns]


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a scientific figure from the template registry.")
    parser.add_argument("--skill-dir", default=Path(__file__).resolve().parents[1])
    parser.add_argument("--registry", default="assets/render_registry/render_registry.json")
    parser.add_argument("--chart-type", required=True)
    parser.add_argument("--data", required=True)
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--basename", default="")
    parser.add_argument("--formats", default="")
    parser.add_argument("--style-token", default="")
    parser.add_argument("--dependency-plan", default="", help="Optional dependency_plan.json produced by build_dependency_plan.py")
    parser.add_argument("--column", action="append", default=[], help="Column override in role=column form")
    parser.add_argument("--manifest", default="")
    args = parser.parse_args()
    try:
        skill_dir = Path(args.skill_dir).resolve()
        outdir = Path(args.outdir).resolve()
        outdir.mkdir(parents=True, exist_ok=True)
        basename = args.basename or args.chart_type
        registry = load_structured_file(skill_dir / args.registry)
        if not isinstance(registry, dict):
            raise ValueError("render registry must be a JSON object")
        entry = select_entry(registry, args.chart_type)
        dependency_context = validate_dependency_plan(args.dependency_plan, args.chart_type)
        csv_path = load_table_as_csv(Path(args.data).resolve(), outdir, basename)
        columns = available_columns(csv_path)
        overrides = parse_column_overrides(args.column)
        required_roles = [str(item) for item in entry.get("required_columns", [])]
        optional_roles = [str(item) for item in entry.get("optional_columns", [])]

        role_to_column: dict[str, str] = {}
        missing: list[str] = []
        for role in required_roles:
            column = overrides.get(role, role)
            if column not in columns:
                missing.append(f"{role} -> {column}")
            role_to_column[role] = column
        for role in optional_roles:
            column = overrides.get(role, role)
            if column in columns:
                role_to_column[role] = column
        if missing:
            raise ValueError("missing required input columns: " + ", ".join(missing))

        formats = parse_csv_arg(args.formats) or [str(item) for item in entry.get("default_outputs", [])]
        template_path = skill_dir / str(entry["template_path"])
        env = os.environ.copy()
        env["MPLBACKEND"] = "Agg"
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        written: list[dict[str, Any]] = []
        for fmt in formats:
            output = outdir / f"{basename}.{fmt.lower()}"
            command = [sys.executable, str(template_path), "--csv", str(csv_path)]
            for role, column in role_to_column.items():
                command.extend([f"--{role.replace('_', '-')}", column])
            command.extend(["--out", str(output)])
            result = subprocess.run(command, env=env, text=True, capture_output=True, check=False)
            if result.returncode != 0:
                raise RuntimeError(result.stderr.strip() or result.stdout.strip() or f"render failed for {fmt}")
            written.append(
                {
                    "path": str(output),
                    "format": fmt.lower(),
                    "sha256": sha256_file(output),
                    "byte_size": output.stat().st_size,
                }
            )

        manifest = {
            "render_manifest": {
                "created_at": utc_now(),
                "chart_type": args.chart_type,
                "template_path": str(entry["template_path"]),
                "data": str(Path(args.data)),
                "style_token": args.style_token or None,
                "dependency_plan": dependency_context["path"] if dependency_context else None,
                "columns": role_to_column,
                "files": written,
            }
        }
        manifest_path = Path(args.manifest).resolve() if args.manifest else outdir / f"{basename}_render_manifest.json"
        write_json(manifest_path, manifest)
        print(f"[RENDER-REGISTRY] {args.chart_type} wrote {len(written)} file(s)")
        print(f"[RENDER-REGISTRY] manifest {manifest_path}")
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
