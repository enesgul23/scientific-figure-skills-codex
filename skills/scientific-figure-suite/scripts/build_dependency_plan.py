from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from _common import load_structured_file, main_error, write_json
from _memory import utc_now
from select_library_stack import build_selection, load_environment_status
from validate_library_pool import pool_libraries


def library_index(pool_data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(item.get("library_id")): item for item in pool_libraries(pool_data) if isinstance(item, dict)}


def install_commands(libraries: list[str], index: dict[str, dict[str, Any]]) -> list[str]:
    if not libraries:
        return []
    pip_packages = [str(index.get(library_id, {}).get("pip_name") or library_id) for library_id in libraries]
    conda_packages = [str(index.get(library_id, {}).get("conda_name") or library_id) for library_id in libraries]
    return [
        "python -m pip install " + " ".join(pip_packages),
        "conda install -c conda-forge " + " ".join(conda_packages),
    ]


def import_checks(libraries: list[str], index: dict[str, dict[str, Any]]) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []
    for library_id in libraries:
        library = index.get(library_id, {})
        import_name = str(library.get("import_probe", {}).get("import_name") or library_id)
        checks.append({"library_id": library_id, "import_name": import_name, "check": f"python -c \"import {import_name}\""})
    return checks


def build_plan(
    skill_dir: Path,
    chart_type: str | None,
    dataset_profile_path: str,
    environment_probe_path: str,
    library_pool_path: Path,
    render_registry_path: Path,
) -> dict[str, Any]:
    pool = load_structured_file(library_pool_path)
    index = library_index(pool)
    registry = load_structured_file(render_registry_path)
    profile = load_structured_file(dataset_profile_path) if dataset_profile_path else None
    environment = load_environment_status(Path(environment_probe_path)) if environment_probe_path else {}
    selection_root = build_selection(chart_type, profile, registry, environment)
    selection = selection_root["library_stack_selection"]
    required = selection["required_libraries"]
    recommended = selection["recommended_libraries"]
    optional = selection["optional_libraries"]
    blocked_ids = [str(item.get("library_id")) for item in selection["blocked_libraries"]]
    to_install = blocked_ids if blocked_ids else [item for item in [*required, *recommended] if item in index]
    return {
        "dependency_plan": {
            "created_at": utc_now(),
            "chart_type": chart_type,
            "dataset_profile": dataset_profile_path or None,
            "environment_probe": environment_probe_path or None,
            "selected_stack": selection["selected_stack"],
            "required_libraries": required,
            "recommended_libraries": recommended,
            "optional_libraries": optional,
            "blocked_libraries": selection["blocked_libraries"],
            "install_commands": install_commands(to_install, index),
            "import_checks": import_checks([*required, *recommended, *optional], index),
            "selection_rationale": selection["selection_rationale"],
            "fallback_renderer": selection["fallback_renderer"],
            "reproducibility_notes": selection["reproducibility_notes"],
            "warnings": selection.get("warnings", []),
            "library_pool": str(library_pool_path.relative_to(skill_dir) if library_pool_path.is_relative_to(skill_dir) else library_pool_path),
        }
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a dependency plan for scientific figure rendering.")
    parser.add_argument("--skill-dir", default=Path(__file__).resolve().parents[1])
    parser.add_argument("--chart-type", default="")
    parser.add_argument("--dataset-profile", default="")
    parser.add_argument("--environment-probe", default="")
    parser.add_argument("--library-pool", default="assets/library_pool/library_pool.json")
    parser.add_argument("--render-registry", default="assets/render_registry/render_registry.json")
    parser.add_argument("--out", default="")
    args = parser.parse_args()
    try:
        skill_dir = Path(args.skill_dir).resolve()
        plan = build_plan(
            skill_dir,
            args.chart_type or None,
            args.dataset_profile,
            args.environment_probe,
            skill_dir / args.library_pool,
            skill_dir / args.render_registry,
        )
        if args.out:
            write_json(Path(args.out), plan)
            print(f"[DEPENDENCY-PLAN] wrote {args.out}")
        else:
            print(json.dumps(plan, indent=2, sort_keys=True))
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
