from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

from _common import exit_with_results, main_error
from _memory import append_jsonl, read_jsonl, resolve_memory_dir, utc_now


HASH_RE = re.compile(r"^[0-9a-f]{12}$")


def find_boundary(entries: list[dict[str, Any]], hash_value: str) -> dict[str, Any] | None:
    for entry in entries:
        if entry.get("kind") == "boundary" and entry.get("hash") == hash_value:
            return entry
    return None


def resume(memory_dir: Path, hash_value: str, override_next_stage: str | None) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not HASH_RE.match(hash_value):
        return ["resume hash must be 12 lowercase hex characters"], warnings

    ledger_path = memory_dir / "revision_boundary_ledger.jsonl"
    if not ledger_path.exists():
        return [f"revision boundary ledger missing: {ledger_path}"], warnings

    entries = read_jsonl(ledger_path)
    boundary = find_boundary(entries, hash_value)
    if boundary is None:
        return [f"boundary hash not found: {hash_value}"], warnings

    for entry in entries:
        if entry.get("kind") == "resume" and entry.get("consumes_hash") == hash_value:
            return [f"boundary hash already consumed: {hash_value}"], warnings

    verification_status = boundary.get("verification_status")
    if verification_status in {"STALE", "UNVERIFIED"}:
        warnings.append(f"boundary verification_status is {verification_status}; re-check required inputs before final output")

    next_stage = override_next_stage or boundary.get("next_stage")
    resume_entry = {
        "kind": "resume",
        "created_at": utc_now(),
        "consumes_hash": hash_value,
        "figure_id": boundary.get("figure_id"),
        "next_stage": next_stage,
        "source_completed_stage": boundary.get("completed_stage"),
    }
    append_jsonl(ledger_path, resume_entry)
    print("Resume Acknowledged")
    print(f"- hash: {hash_value}")
    print(f"- figure_id: {boundary.get('figure_id')}")
    print(f"- recovered_version: {boundary.get('to_version')}")
    print(f"- next_stage: {next_stage}")
    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Resume a scientific figure project from a Figure Passport boundary hash.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--memory-dir", default=None)
    parser.add_argument("--hash", required=True)
    parser.add_argument("--next-stage")
    args = parser.parse_args()
    try:
        memory_dir = resolve_memory_dir(args.project_root, args.memory_dir)
        errors, warnings = resume(memory_dir, args.hash, args.next_stage)
        exit_with_results(errors, warnings)
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
