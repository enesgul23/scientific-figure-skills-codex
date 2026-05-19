from __future__ import annotations

import argparse
import importlib.metadata
import importlib.util
from pathlib import Path
from typing import Any

from _common import load_structured_file, main_error, write_json
from _memory import utc_now
from validate_library_pool import pool_libraries


def probe_library(library: dict[str, Any]) -> dict[str, Any]:
    import_names = [str(item) for item in library.get("import_names", [])]
    chosen_import = str(library.get("import_probe", {}).get("import_name") or (import_names[0] if import_names else ""))
    available = False
    import_name_used = None
    for import_name in [chosen_import, *[name for name in import_names if name != chosen_import]]:
        if not import_name:
            continue
        if importlib.util.find_spec(import_name) is not None:
            available = True
            import_name_used = import_name
            break
    version = None
    if available:
        for distribution_name in [str(library.get("pip_name") or ""), str(library.get("package_name") or "")]:
            if not distribution_name:
                continue
            try:
                version = importlib.metadata.version(distribution_name)
                break
            except importlib.metadata.PackageNotFoundError:
                continue
    return {
        "library_id": library.get("library_id"),
        "package_name": library.get("package_name"),
        "pip_name": library.get("pip_name"),
        "conda_name": library.get("conda_name"),
        "status": "AVAILABLE" if available else "MISSING",
        "version": version,
        "import_name_used": import_name_used,
        "install_risk": library.get("install_risk"),
        "publication_grade": library.get("publication_grade"),
    }


def build_probe(skill_dir: Path, library_pool: Path, selected: list[str]) -> dict[str, Any]:
    data = load_structured_file(library_pool)
    libraries = pool_libraries(data)
    selected_set = set(selected)
    if selected_set:
        libraries = [item for item in libraries if str(item.get("library_id")) in selected_set]
    return {
        "environment_probe": {
            "created_at": utc_now(),
            "python_executable": str(Path(__import__("sys").executable)),
            "library_pool": str(library_pool.relative_to(skill_dir) if library_pool.is_relative_to(skill_dir) else library_pool),
            "libraries": [probe_library(library) for library in libraries],
        }
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Probe Python import availability for Scientific Figure Suite libraries.")
    parser.add_argument("--skill-dir", default=Path(__file__).resolve().parents[1])
    parser.add_argument("--library-pool", default="assets/library_pool/library_pool.json")
    parser.add_argument("--library", action="append", default=[], help="Library id to probe. May be repeated.")
    parser.add_argument("--out", default="")
    args = parser.parse_args()
    try:
        skill_dir = Path(args.skill_dir).resolve()
        pool_path = (skill_dir / args.library_pool).resolve() if not Path(args.library_pool).is_absolute() else Path(args.library_pool)
        probe = build_probe(skill_dir, pool_path, [str(item) for item in args.library])
        if args.out:
            write_json(Path(args.out), probe)
            print(f"[ENV-PROBE] wrote {args.out}")
        else:
            print(__import__("json").dumps(probe, indent=2, sort_keys=True))
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
