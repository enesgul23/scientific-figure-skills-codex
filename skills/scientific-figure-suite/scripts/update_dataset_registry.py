from __future__ import annotations

import argparse
from pathlib import Path

from _common import exit_with_results, main_error
from _memory import load_json, resolve_memory_dir, save_json, update_manifest_timestamp, utc_now


def parse_pairs(values: list[str]) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"expected key=value pair: {value}")
        key, item = value.split("=", 1)
        parsed[key.strip()] = item.strip()
    return parsed


def update_dataset(args: argparse.Namespace) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    memory_dir = resolve_memory_dir(args.project_root, args.memory_dir)
    registry_path = memory_dir / "dataset_registry.json"
    if not registry_path.exists():
        return [f"dataset registry missing: {registry_path}"], warnings
    data = load_json(registry_path)
    datasets = data.setdefault("dataset_registry", {}).setdefault("datasets", [])
    if not isinstance(datasets, list):
        return ["dataset_registry.datasets must be a list"], warnings

    project_root = Path(args.project_root).expanduser().resolve()
    if args.check_path and not (project_root / args.path).exists():
        warnings.append(f"dataset path not found: {args.path}")

    columns = parse_pairs(args.column)
    units = parse_pairs(args.unit)
    now_date = args.last_validated or utc_now().split("T", 1)[0]
    entry = None
    for item in datasets:
        if isinstance(item, dict) and item.get("dataset_id") == args.dataset_id:
            entry = item
            break
    if entry is None:
        entry = {"dataset_id": args.dataset_id}
        datasets.append(entry)

    entry.update(
        {
            "path": args.path,
            "columns": columns,
            "units": units,
            "preprocessing": args.preprocessing,
            "missing_values": args.missing_values,
            "last_validated": now_date,
            "source_type": args.source_type,
            "source_url": args.source_url,
            "license": args.license,
            "citation": args.citation,
            "downloaded_at": args.downloaded_at,
            "sha256": args.sha256,
            "usage_role": args.usage_role,
            "contamination_risk": args.contamination_risk,
        }
    )
    save_json(registry_path, data)
    update_manifest_timestamp(memory_dir)
    print(f"[DATASET-REGISTRY] {args.dataset_id} path={args.path}")
    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Update project-local dataset registry memory.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--memory-dir", default=None)
    parser.add_argument("--dataset-id", required=True)
    parser.add_argument("--path", required=True)
    parser.add_argument("--column", action="append", default=[])
    parser.add_argument("--unit", action="append", default=[])
    parser.add_argument("--preprocessing")
    parser.add_argument("--missing-values")
    parser.add_argument("--last-validated")
    parser.add_argument(
        "--source-type",
        choices=["user_provided", "generated", "external_planned", "external_downloaded"],
        default="user_provided",
    )
    parser.add_argument("--source-url")
    parser.add_argument("--license")
    parser.add_argument("--citation")
    parser.add_argument("--downloaded-at")
    parser.add_argument("--sha256")
    parser.add_argument(
        "--usage-role",
        choices=["contextual", "evidentiary", "benchmark", "annotation", "none"],
        default="none",
    )
    parser.add_argument(
        "--contamination-risk",
        choices=["none", "low", "medium", "high", "unknown"],
        default="none",
    )
    parser.add_argument("--check-path", action="store_true")
    args = parser.parse_args()
    try:
        errors, warnings = update_dataset(args)
        exit_with_results(errors, warnings)
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
