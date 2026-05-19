from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_MEMORY_REL = Path(".codex") / "scientific-figure-memory"
SCHEMA_VERSION = "0.6.0"
BOUNDARY_HASH_PLACEHOLDER = "000000000000"
BOUNDARY_HASH_MODE = "SFS_CANONICAL_V1"

REQUIRED_JSON_FILES = [
    "memory_manifest.json",
    "project_profile.json",
    "journal_targets.json",
    "figure_passport.json",
    "figure_set_manifest.json",
    "submission_package_index.json",
    "dataset_registry.json",
    "author_visual_style_profile.json",
]

REQUIRED_JSONL_FILES = [
    "visual_claim_ledger.jsonl",
    "quality_audit_history.jsonl",
    "revision_boundary_ledger.jsonl",
    "journal_guideline_verification.jsonl",
    "visual_audit_artifact.jsonl",
    "cross_figure_consistency_history.jsonl",
    "submission_readiness_history.jsonl",
    "figure_decision_log.jsonl",
    "visual_regression_history.jsonl",
    "dependency_plan_history.jsonl",
    "external_data_plan_history.jsonl",
]

VALID_STYLE_STATUSES = {"VERIFIED", "ESTIMATED", "UNVERIFIED"}
VALID_MEMORY_LEVELS = {"LIGHTWEIGHT", "RESEARCH_GRADE", "SUBMISSION_GRADE"}
VALID_VALIDATION_STATUSES = {"PASS", "PASS_WITH_WARNINGS", "FAIL", "NOT_RUN"}
VALID_STYLE_PROFILE_STATUSES = {"NONE", "PARTIAL", "USER_APPROVED", "STALE", "FORGOTTEN"}


def default_pipeline_state() -> dict[str, Any]:
    return {
        "active_stage": None,
        "completed_stages": [],
        "blocked_stages": [],
        "last_artifacts": [],
        "next_actions": [],
        "readiness_summary": "NOT_RUN",
    }


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def slug(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.strip()).strip("-").lower()
    return cleaned or "scientific-figure-project"


def resolve_memory_dir(project_root: str | Path = ".", memory_dir: str | Path | None = None) -> Path:
    if memory_dir is not None:
        return Path(memory_dir).expanduser().resolve()
    return (Path(project_root).expanduser().resolve() / DEFAULT_MEMORY_REL).resolve()


def looks_like_installed_skill_dir(path: Path) -> bool:
    return (
        (path / "SKILL.md").is_file()
        and (path / "manifest.json").is_file()
        and path.name == "scientific-figure-suite"
        and path.parent.name == "skills"
    )


def is_inside_installed_skill_dir(path: Path) -> bool:
    resolved = path.resolve()
    for candidate in [resolved, *resolved.parents]:
        if looks_like_installed_skill_dir(candidate):
            return True
    return False


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    entries: list[dict[str, Any]] = []
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        data = json.loads(line)
        if not isinstance(data, dict):
            raise ValueError(f"{path.name}:{line_number} JSONL entry must be an object")
        entries.append(data)
    return entries


def append_jsonl(path: Path, entry: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(entry, sort_keys=True, separators=(",", ":")) + "\n")


def canonical_json_bytes(data: dict[str, Any]) -> bytes:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def compute_boundary_hash(prior_entries: list[dict[str, Any]], new_entry: dict[str, Any]) -> str:
    boundary_entries = [entry for entry in prior_entries if entry.get("kind") == "boundary"]
    staged = dict(new_entry)
    staged["hash"] = BOUNDARY_HASH_PLACEHOLDER
    staged["hash_mode"] = BOUNDARY_HASH_MODE
    payload = b"".join(canonical_json_bytes(entry) + b"\n" for entry in [*boundary_entries, staged])
    return hashlib.sha256(payload).hexdigest()[:12]


def initial_memory_files(
    project_id: str,
    field: str,
    target_journals: list[str],
    memory_level: str,
) -> dict[str, str]:
    now = utc_now()
    journal_targets = []
    for journal in target_journals:
        journal_targets.append(
            {
                "journal": journal,
                "status": "UNVERIFIED",
                "guideline_source": "unknown",
                "checked_at": None,
                "preferred_formats": [],
                "unresolved_requirements": ["Current official figure guidelines have not been checked."],
                "notes": [],
            }
        )
    if not journal_targets:
        journal_targets.append(
            {
                "journal": "unspecified",
                "status": "UNVERIFIED",
                "guideline_source": "unknown",
                "checked_at": None,
                "preferred_formats": [],
                "unresolved_requirements": ["No target journal has been specified."],
                "notes": [],
            }
        )

    json_files = {
        "memory_manifest.json": {
            "memory_manifest": {
                "schema_version": SCHEMA_VERSION,
                "project_id": project_id,
                "memory_level": memory_level,
                "created_at": now,
                "updated_at": now,
                "active_figure_id": None,
                "current_stage": None,
                "pipeline_state": default_pipeline_state(),
                "validation_status": "NOT_RUN",
                "unresolved_requirements": [],
                "files": {
                    "project_profile": "project_profile.json",
                    "journal_targets": "journal_targets.json",
                    "figure_passport": "figure_passport.json",
                    "figure_set_manifest": "figure_set_manifest.json",
                    "submission_package_index": "submission_package_index.json",
                    "visual_claim_ledger": "visual_claim_ledger.jsonl",
                    "dataset_registry": "dataset_registry.json",
                    "quality_audit_history": "quality_audit_history.jsonl",
                    "revision_boundary_ledger": "revision_boundary_ledger.jsonl",
                    "journal_guideline_verification": "journal_guideline_verification.jsonl",
                    "visual_audit_artifact": "visual_audit_artifact.jsonl",
                    "cross_figure_consistency_history": "cross_figure_consistency_history.jsonl",
                    "submission_readiness_history": "submission_readiness_history.jsonl",
                    "figure_decision_log": "figure_decision_log.jsonl",
                    "visual_regression_history": "visual_regression_history.jsonl",
                    "dependency_plan_history": "dependency_plan_history.jsonl",
                    "external_data_plan_history": "external_data_plan_history.jsonl",
                    "author_visual_style_profile": "author_visual_style_profile.json",
                },
            }
        },
        "project_profile.json": {
            "project_profile": {
                "project_id": project_id,
                "field": field,
                "preferred_language": "English",
                "target_journals": target_journals,
                "figure_style": "minimal, high-density, journal-ready",
                "color_policy": "colorblind-safe",
                "default_export": ["pdf", "svg", "png"],
                "created_at": now,
                "updated_at": now,
                "notes": [],
            }
        },
        "journal_targets.json": {"journal_targets": {"targets": journal_targets}},
        "figure_passport.json": {"figure_passport": {"schema_version": SCHEMA_VERSION, "figures": []}},
        "figure_set_manifest.json": {
            "figure_set_manifest": {
                "schema_version": SCHEMA_VERSION,
                "project_id": project_id,
                "created_at": now,
                "updated_at": now,
                "figures": [],
                "style_consistency_status": "NOT_RUN",
                "readiness_status": "NOT_RUN",
                "unresolved_requirements": [],
            }
        },
        "submission_package_index.json": {
            "submission_package_index": {
                "schema_version": SCHEMA_VERSION,
                "project_id": project_id,
                "created_at": now,
                "updated_at": now,
                "package_root": None,
                "files": [],
                "index_status": "NOT_RUN",
            }
        },
        "dataset_registry.json": {"dataset_registry": {"datasets": []}},
        "author_visual_style_profile.json": {
            "author_visual_style_profile": {
                "status": "NONE",
                "created_at": now,
                "updated_at": now,
                "source_summary": "No user-approved visual style samples have been analyzed.",
                "preferences": {},
                "conflicts": [],
                "application_policy": "Soft preference below truth, reproducibility, accessibility, and journal requirements.",
            }
        },
    }
    jsonl_files = {name: "" for name in REQUIRED_JSONL_FILES}
    return {**{name: json.dumps(data, indent=2, sort_keys=True) + "\n" for name, data in json_files.items()}, **jsonl_files}


def update_manifest_timestamp(memory_dir: Path, validation_status: str | None = None) -> None:
    manifest_path = memory_dir / "memory_manifest.json"
    if not manifest_path.exists():
        return
    data = load_json(manifest_path)
    manifest = data.setdefault("memory_manifest", {})
    manifest["updated_at"] = utc_now()
    if validation_status:
        manifest["validation_status"] = validation_status
    save_json(manifest_path, data)
