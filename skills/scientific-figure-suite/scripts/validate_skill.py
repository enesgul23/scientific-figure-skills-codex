from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True

from _common import exit_with_results, main_error


REQUIRED_DIRS = [
    "fig",
    "references",
    "scripts",
    "assets",
    "tests",
    "agents",
    "commands",
    "shared",
    "templates",
    "examples",
    "docs",
]

REQUIRED_WORKFLOWS = [
    "intake-design",
    "statistical-plots",
    "model-performance",
    "clinical-biomedical",
    "geospatial-maps",
    "omics-bioinformatics",
    "multipanel-composer",
    "schematic-mechanism",
    "graphical-abstract",
    "journal-style-translator",
    "caption-alttext",
    "figure-auditor",
    "export-packager",
]


def load_manifest(skill_dir: Path, errors: list[str]) -> dict:
    manifest_path = skill_dir / "manifest.json"
    if not manifest_path.exists():
        errors.append("manifest.json is missing")
        return {}
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"manifest.json is invalid JSON: {exc}")
        return {}
    if not isinstance(data, dict):
        errors.append("manifest.json must contain an object")
        return {}
    return data


def parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, flags=re.DOTALL)
    if not match:
        return {}
    fields: dict[str, str] = {}
    current_key: str | None = None
    for raw_line in match.group(1).splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            continue
        if not line.startswith(" ") and ":" in line:
            key, value = line.split(":", 1)
            current_key = key.strip()
            fields[current_key] = value.strip()
        elif current_key:
            fields[current_key] += " " + line.strip()
    return fields


def check_listed_files(
    skill_dir: Path,
    listed: list[str],
    folder: str,
    suffixes: tuple[str, ...],
    errors: list[str],
) -> None:
    for item in listed:
        if not isinstance(item, str):
            errors.append(f"manifest {folder} entries must be strings")
            continue
        candidates = [skill_dir / folder / f"{item}{suffix}" for suffix in suffixes]
        if not any(path.exists() for path in candidates):
            expected = " or ".join(str(path.relative_to(skill_dir)) for path in candidates)
            errors.append(f"manifest-listed file missing: {expected}")


def check_manifest_paths(
    skill_dir: Path,
    listed: list[str],
    prefix: Path,
    suffixes: tuple[str, ...],
    field_name: str,
    errors: list[str],
) -> None:
    for item in listed:
        if not isinstance(item, str):
            errors.append(f"manifest {field_name} entries must be strings")
            continue
        candidates = [skill_dir / prefix / f"{item}{suffix}" for suffix in suffixes]
        if not any(path.exists() for path in candidates):
            expected = " or ".join(str(path.relative_to(skill_dir)) for path in candidates)
            errors.append(f"manifest-listed {field_name} file missing: {expected}")


def validate(skill_dir: Path) -> tuple[list[str], list[str]]:
    skill_dir = skill_dir.resolve()
    errors: list[str] = []
    warnings: list[str] = []

    manifest = load_manifest(skill_dir, errors)

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        errors.append("SKILL.md is missing")
    else:
        fields = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        if fields.get("name") != "scientific-figure-suite":
            errors.append("SKILL.md frontmatter name must be scientific-figure-suite")
        description = fields.get("description", "")
        if not description or "TODO" in description:
            errors.append("SKILL.md frontmatter description is missing or incomplete")
        if len(description) < 120:
            warnings.append("SKILL.md description is short for a router skill")
        body = skill_md.read_text(encoding="utf-8")
        for required_section in [
            "## Workflow Router",
            "## Command Alias Router",
            "## Agent Prompt Use",
            "## Canonical Agent Files",
            "## Shared Resources",
            "## Memory Protocol",
            "## Verification Discipline",
        ]:
            if required_section not in body:
                errors.append(f"SKILL.md missing section: {required_section}")

    for dirname in REQUIRED_DIRS:
        if not (skill_dir / dirname).is_dir():
            errors.append(f"required directory missing: {dirname}")

    fig_dir = skill_dir / "fig"
    if fig_dir.exists():
        nested_skills = [path for path in fig_dir.rglob("SKILL.md")]
        if nested_skills:
            errors.append("nested SKILL.md files under fig/ are not allowed")
        for workflow in REQUIRED_WORKFLOWS:
            workflow_path = fig_dir / workflow / "WORKFLOW.md"
            if not workflow_path.exists():
                errors.append(f"workflow missing: fig/{workflow}/WORKFLOW.md")
            else:
                workflow_text = workflow_path.read_text(encoding="utf-8")
                if "## Agent Role References" not in workflow_text:
                    warnings.append(f"workflow has no Agent Role References section: {workflow}")

    agents_yaml = skill_dir / "agents" / "openai.yaml"
    if not agents_yaml.exists():
        errors.append("agents/openai.yaml is missing")
    else:
        agents_text = agents_yaml.read_text(encoding="utf-8")
        if "$scientific-figure-suite" not in agents_text:
            errors.append("agents/openai.yaml default_prompt should mention $scientific-figure-suite")

    if manifest:
        if manifest.get("name") != "scientific-figure-suite":
            errors.append("manifest name must be scientific-figure-suite")
        if manifest.get("entrypoint") != "SKILL.md":
            errors.append("manifest entrypoint must be SKILL.md")

        version_file = skill_dir.parents[1] / "VERSION"
        if not version_file.exists():
            errors.append("repo VERSION file is missing")
        else:
            version = version_file.read_text(encoding="utf-8").strip()
            if manifest.get("adapter_version") != version:
                errors.append("manifest adapter_version must match repo VERSION")

        workflows = manifest.get("internal_workflows")
        if workflows != REQUIRED_WORKFLOWS:
            errors.append("manifest internal_workflows must match required workflow order")

        check_listed_files(skill_dir, manifest.get("commands", []), "commands", (".md",), errors)
        check_listed_files(skill_dir, manifest.get("shared_protocols", []), "shared", (".md",), errors)
        check_listed_files(skill_dir, manifest.get("templates", []), "templates", (".md", ".json"), errors)
        check_listed_files(skill_dir, manifest.get("examples", []), "examples", (".md",), errors)
        check_manifest_paths(
            skill_dir,
            manifest.get("render_templates", []),
            Path("assets") / "render_templates",
            ("",),
            "render_templates",
            errors,
        )
        check_listed_files(skill_dir, manifest.get("validation_scripts", []), "scripts", ("",), errors)
        check_listed_files(skill_dir, manifest.get("memory_scripts", []), "scripts", ("",), errors)
        check_manifest_paths(skill_dir, manifest.get("root_guides", []), Path(), ("",), "root_guides", errors)
        check_manifest_paths(skill_dir, manifest.get("docs", []), Path("docs"), ("",), "docs", errors)
        check_manifest_paths(
            skill_dir,
            manifest.get("shared_agents", []),
            Path("shared") / "agents",
            (".md",),
            "shared_agents",
            errors,
        )
        check_manifest_paths(
            skill_dir,
            manifest.get("shared_contracts", []),
            Path("shared") / "contracts",
            ("",),
            "shared_contracts",
            errors,
        )

        canonical_agents = manifest.get("canonical_agents")
        if not isinstance(canonical_agents, dict):
            errors.append("manifest canonical_agents must be an object")
        else:
            for workflow in REQUIRED_WORKFLOWS:
                agents = canonical_agents.get(workflow)
                if not isinstance(agents, list) or not agents:
                    errors.append(f"manifest canonical_agents missing list for {workflow}")
                    continue
                for agent in agents:
                    if not isinstance(agent, str):
                        errors.append(f"canonical agent entry for {workflow} must be a string")
                        continue
                    agent_path = skill_dir / "fig" / workflow / "agents" / f"{agent}.md"
                    if not agent_path.exists():
                        errors.append(f"canonical agent file missing: fig/{workflow}/agents/{agent}.md")
            unknown_workflows = set(canonical_agents) - set(REQUIRED_WORKFLOWS)
            for workflow in sorted(unknown_workflows):
                errors.append(f"manifest canonical_agents contains unknown workflow: {workflow}")

    pycache_dirs = list(skill_dir.rglob("__pycache__"))
    if pycache_dirs:
        errors.append("skill package must not include __pycache__ directories")

    todo_hits = []
    placeholder_token = "[" + "TODO" + "]"
    for path in skill_dir.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".md", ".py", ".json", ".yaml", ".yml"}:
            if path.name == "validate_skill.py":
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if placeholder_token in text:
                todo_hits.append(str(path.relative_to(skill_dir)))
    if todo_hits:
        warnings.append("TODO markers found: " + ", ".join(todo_hits))

    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the scientific figure suite skill structure.")
    parser.add_argument("skill_dir", help="Path to skills/scientific-figure-suite")
    args = parser.parse_args()
    try:
        errors, warnings = validate(Path(args.skill_dir))
        exit_with_results(errors, warnings)
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
