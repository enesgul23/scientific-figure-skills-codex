from __future__ import annotations

import argparse
from pathlib import Path

from _common import exit_with_results, main_error
from _memory import (
    VALID_MEMORY_LEVELS,
    initial_memory_files,
    is_inside_installed_skill_dir,
    looks_like_installed_skill_dir,
    resolve_memory_dir,
    slug,
)


def init_memory(
    project_root: Path,
    memory_dir_arg: str | None,
    project_id: str | None,
    field: str,
    target_journals: list[str],
    memory_level: str,
    force: bool,
) -> tuple[list[str], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    created: list[str] = []

    if memory_level not in VALID_MEMORY_LEVELS:
        return [], [], [f"memory_level must be one of {sorted(VALID_MEMORY_LEVELS)}"]

    if memory_dir_arg is None and looks_like_installed_skill_dir(project_root.resolve()):
        return [], [], ["refusing to create project memory inside the installed skill directory"]

    memory_dir = resolve_memory_dir(project_root, memory_dir_arg)
    if is_inside_installed_skill_dir(memory_dir):
        return [], [], ["refusing to create project memory inside the installed skill directory"]
    memory_dir.mkdir(parents=True, exist_ok=True)

    effective_project_id = slug(project_id or project_root.resolve().name)
    files = initial_memory_files(effective_project_id, field, target_journals, memory_level)
    for filename, content in files.items():
        path = memory_dir / filename
        if path.exists() and not force:
            warnings.append(f"already exists: {path}")
            continue
        path.write_text(content, encoding="utf-8")
        created.append(str(path))

    return created, warnings, errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize project-local scientific figure memory.")
    parser.add_argument("--project-root", default=".", help="Project root for default .codex memory location")
    parser.add_argument("--memory-dir", default=None, help="Explicit memory directory")
    parser.add_argument("--project-id", default=None)
    parser.add_argument("--field", default="unspecified")
    parser.add_argument("--target-journal", action="append", default=[])
    parser.add_argument("--memory-level", default="RESEARCH_GRADE", choices=sorted(VALID_MEMORY_LEVELS))
    parser.add_argument("--force", action="store_true", help="Overwrite existing memory files")
    args = parser.parse_args()
    try:
        created, warnings, errors = init_memory(
            Path(args.project_root),
            args.memory_dir,
            args.project_id,
            args.field,
            args.target_journal,
            args.memory_level,
            args.force,
        )
        for item in created:
            print(f"[CREATE] {item}")
        exit_with_results(errors, warnings)
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
