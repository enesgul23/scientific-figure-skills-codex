from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

from _common import exit_with_results, main_error


TURKISH_RE = re.compile("[\\u00e7\\u011f\\u0131\\u00f6\\u015f\\u00fc\\u00c7\\u011e\\u0130\\u00d6\\u015e\\u00dc]")
VERSION_RE = re.compile(r"version[`\s:=\{\}\"-]+([0-9]+\.[0-9]+\.[0-9]+)", re.IGNORECASE)
MAX_FRONTMATTER_DESCRIPTION = 900
MAX_COMMAND_LINES = 90
MAX_MARKDOWN_LINE = 220
TEXT_SUFFIXES = {".md", ".py", ".json", ".yaml", ".yml", ".cff", ".sh", ".txt"}


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[3]


def tracked_files(repo_root: Path) -> list[Path]:
    try:
        result = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
            cwd=repo_root,
            text=True,
            capture_output=True,
            check=True,
        )
        return [repo_root / line.strip() for line in result.stdout.splitlines() if line.strip()]
    except Exception:
        return [path for path in repo_root.rglob("*") if path.is_file() and ".git" not in path.parts]


def text_for(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def frontmatter_description_length(skill_md: Path) -> int:
    text = text_for(skill_md)
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, flags=re.DOTALL)
    if not match:
        return 0
    body = match.group(1)
    collecting = False
    parts: list[str] = []
    for line in body.splitlines():
        if line.startswith("description:"):
            collecting = True
            parts.append(line.split(":", 1)[1].strip())
            continue
        if collecting and (line.startswith(" ") or not line.strip()):
            parts.append(line.strip())
            continue
        if collecting:
            break
    return len(" ".join(parts))


def version_hits(text: str) -> set[str]:
    return set(VERSION_RE.findall(text))


def validate_versions(repo_root: Path, errors: list[str]) -> None:
    version = (repo_root / "VERSION").read_text(encoding="utf-8").strip()
    manifest = json.loads((repo_root / "skills" / "scientific-figure-suite" / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("adapter_version") != version:
        errors.append("manifest adapter_version does not match VERSION")
    for rel in ["skills/scientific-figure-suite/SKILL.md", "CITATION.cff", "README.md"]:
        hits = version_hits(text_for(repo_root / rel))
        if version not in hits:
            errors.append(f"{rel}: version {version} not found")


def line_exempt(path: Path, line: str) -> bool:
    stripped = line.strip()
    return (
        not stripped
        or stripped.startswith("|")
        or stripped.startswith("http")
        or "http://" in stripped
        or "https://" in stripped
        or path.suffix.lower() == ".jsonl"
        or "```" in stripped
    )


def validate(repo_root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    files = tracked_files(repo_root)
    for path in files:
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = text_for(path)
        if TURKISH_RE.search(text):
            errors.append(f"Turkish character found in tracked file: {path.relative_to(repo_root)}")
        if path.suffix.lower() == ".md":
            in_fence = False
            for number, line in enumerate(text.splitlines(), start=1):
                if line.strip().startswith("```"):
                    in_fence = not in_fence
                    continue
                if in_fence or line_exempt(path, line):
                    continue
                if len(line) > MAX_MARKDOWN_LINE:
                    warnings.append(f"{path.relative_to(repo_root)}:{number}: long markdown line")
    if list(repo_root.rglob("__pycache__")):
        errors.append("__pycache__ directories are present")
    if list(repo_root.rglob("*.pyc")):
        errors.append("compiled Python files are present")
    skill_md = repo_root / "skills" / "scientific-figure-suite" / "SKILL.md"
    description_len = frontmatter_description_length(skill_md)
    if description_len > MAX_FRONTMATTER_DESCRIPTION:
        errors.append(f"SKILL.md frontmatter description is too long: {description_len}")
    commands_dir = repo_root / "skills" / "scientific-figure-suite" / "commands"
    for command in commands_dir.glob("*.md"):
        line_count = len(text_for(command).splitlines())
        if line_count > MAX_COMMAND_LINES:
            errors.append(f"command recipe too long: {command.relative_to(repo_root)} ({line_count} lines)")
    validate_versions(repo_root, errors)
    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate repository hygiene for Scientific Figure Suite releases.")
    parser.add_argument("--repo-root", default=repo_root_from_script())
    args = parser.parse_args()
    try:
        errors, warnings = validate(Path(args.repo_root).resolve())
        exit_with_results(errors, warnings)
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
