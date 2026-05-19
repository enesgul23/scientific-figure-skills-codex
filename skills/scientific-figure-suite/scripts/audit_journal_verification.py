from __future__ import annotations

import argparse
from typing import Any

from _common import exit_with_results, main_error
from _memory import append_jsonl, load_json, resolve_memory_dir, save_json, utc_now


VALID_SOURCES = {"live_official", "user_provided", "stored_estimate", "unknown"}
VALID_STATUSES = {"VERIFIED", "ESTIMATED", "UNVERIFIED"}


def update_target(targets: list[dict[str, Any]], journal: str, status: str, source_type: str, source_ref: str | None) -> None:
    for target in targets:
        if target.get("journal") == journal:
            target["status"] = status
            target["guideline_source"] = source_type
            target["checked_at"] = utc_now()
            target["source_ref"] = source_ref
            if status == "VERIFIED":
                target["unresolved_requirements"] = []
            return
    targets.append(
        {
            "journal": journal,
            "status": status,
            "guideline_source": source_type,
            "checked_at": utc_now(),
            "source_ref": source_ref,
            "preferred_formats": [],
            "unresolved_requirements": [] if status == "VERIFIED" else ["Current official figure guidelines remain unresolved."],
            "notes": [],
        }
    )


def audit(args: argparse.Namespace) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if args.source_type not in VALID_SOURCES:
        errors.append(f"--source-type must be one of {sorted(VALID_SOURCES)}")
    if args.status not in VALID_STATUSES:
        errors.append(f"--status must be one of {sorted(VALID_STATUSES)}")
    if args.status == "VERIFIED" and args.source_type not in {"live_official", "user_provided"}:
        errors.append("VERIFIED journal status requires live_official or user_provided source")
    if args.status == "VERIFIED" and not args.source_ref:
        errors.append("VERIFIED journal status requires --source-ref")
    if errors:
        return errors, warnings

    memory_dir = resolve_memory_dir(args.project_root, args.memory_dir)
    ledger_path = memory_dir / "journal_guideline_verification.jsonl"
    entry = {
        "created_at": utc_now(),
        "journal": args.journal,
        "source_type": args.source_type,
        "status": args.status,
        "source_ref": args.source_ref,
        "requirements": {
            "figure_size": args.figure_size,
            "formats": args.format,
            "resolution": args.resolution,
            "color_space": args.color_space,
            "font": args.font,
        },
        "checked_by": "scientific-figure-suite",
        "notes": args.note,
    }
    append_jsonl(ledger_path, entry)

    targets_path = memory_dir / "journal_targets.json"
    if targets_path.exists():
        data = load_json(targets_path)
        targets = data.setdefault("journal_targets", {}).setdefault("targets", [])
        if isinstance(targets, list):
            update_target(targets, args.journal, args.status, args.source_type, args.source_ref)
            save_json(targets_path, data)
        else:
            errors.append("journal_targets.targets must be a list")

    print(f"[JOURNAL-VERIFICATION] {args.journal} {args.status} source={args.source_type}")
    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Append journal guideline verification memory.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--memory-dir", default=None)
    parser.add_argument("--journal", required=True)
    parser.add_argument("--source-type", required=True)
    parser.add_argument("--status", required=True)
    parser.add_argument("--source-ref")
    parser.add_argument("--figure-size")
    parser.add_argument("--format", action="append", default=[])
    parser.add_argument("--resolution")
    parser.add_argument("--color-space")
    parser.add_argument("--font")
    parser.add_argument("--note", action="append", default=[])
    args = parser.parse_args()
    try:
        errors, warnings = audit(args)
        exit_with_results(errors, warnings)
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
