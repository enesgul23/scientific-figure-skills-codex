from __future__ import annotations

import argparse
import shutil

from _common import exit_with_results, main_error
from _memory import append_jsonl, resolve_memory_dir, save_json, update_manifest_timestamp, utc_now


def forget(args: argparse.Namespace) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not args.confirm:
        return ["forget_memory requires --confirm"], warnings

    memory_dir = resolve_memory_dir(args.project_root, args.memory_dir)
    if not memory_dir.exists():
        return [f"memory directory missing: {memory_dir}"], warnings

    now = utc_now()
    if args.scope == "author_visual_style_profile":
        save_json(
            memory_dir / "author_visual_style_profile.json",
            {
                "author_visual_style_profile": {
                    "status": "FORGOTTEN",
                    "created_at": now,
                    "updated_at": now,
                    "source_summary": "Redacted by explicit forget request.",
                    "preferences": {},
                    "conflicts": [],
                    "application_policy": "No author visual style memory is active.",
                }
            },
        )
    elif args.scope == "visual_claim_ledger":
        (memory_dir / "visual_claim_ledger.jsonl").write_text("", encoding="utf-8")
    elif args.scope == "quality_audit_history":
        (memory_dir / "quality_audit_history.jsonl").write_text("", encoding="utf-8")
    elif args.scope == "all":
        shutil.rmtree(memory_dir)
        print(f"[FORGET] removed {memory_dir}")
        return errors, warnings
    else:
        return [f"unknown scope: {args.scope}"], warnings

    append_jsonl(
        memory_dir / "revision_boundary_ledger.jsonl",
        {
            "kind": "forget",
            "created_at": now,
            "scope": args.scope,
            "reason": args.reason or "Explicit user forget request.",
        },
    )
    update_manifest_timestamp(memory_dir)
    print(f"[FORGET] scope={args.scope}")
    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Forget selected project-local scientific figure memory.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--memory-dir", default=None)
    parser.add_argument("--scope", required=True, choices=["author_visual_style_profile", "visual_claim_ledger", "quality_audit_history", "all"])
    parser.add_argument("--reason")
    parser.add_argument("--confirm", action="store_true")
    args = parser.parse_args()
    try:
        errors, warnings = forget(args)
        exit_with_results(errors, warnings)
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
