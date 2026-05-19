from __future__ import annotations

import argparse

from _common import exit_with_results, main_error
from _memory import append_jsonl, resolve_memory_dir, utc_now


VALID_SUPPORT = {"supported", "partially_supported", "unsupported", "unverifiable"}


def append_claim(args: argparse.Namespace) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if args.support_status not in VALID_SUPPORT:
        errors.append(f"--support-status must be one of {sorted(VALID_SUPPORT)}")
    if args.support_status in {"unsupported", "unverifiable"} and not args.required_fix:
        errors.append("unsupported or unverifiable claims require --required-fix")
    if errors:
        return errors, warnings

    memory_dir = resolve_memory_dir(args.project_root, args.memory_dir)
    entry = {
        "created_at": utc_now(),
        "claim_id": args.claim_id,
        "figure_id": args.figure_id,
        "panel_id": args.panel_id,
        "claim_text": args.claim_text,
        "claim_type": args.claim_type,
        "visual_element": args.visual_element,
        "data_source": args.data_source,
        "computation_source": args.computation_source,
        "support_status": args.support_status,
        "uncertainty_shown": args.uncertainty_shown,
        "caption_alignment": args.caption_alignment,
        "risk_level": args.risk_level,
        "required_fix": args.required_fix,
    }
    append_jsonl(memory_dir / "visual_claim_ledger.jsonl", entry)
    print(f"[VISUAL-CLAIM] {args.claim_id} figure={args.figure_id}")
    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Append a project-local visual claim ledger entry.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--memory-dir", default=None)
    parser.add_argument("--claim-id", required=True)
    parser.add_argument("--figure-id", required=True)
    parser.add_argument("--panel-id")
    parser.add_argument("--claim-text", required=True)
    parser.add_argument("--claim-type", default="descriptive")
    parser.add_argument("--visual-element", required=True)
    parser.add_argument("--data-source")
    parser.add_argument("--computation-source")
    parser.add_argument("--support-status", default="unverifiable")
    parser.add_argument("--uncertainty-shown", default="not_applicable")
    parser.add_argument("--caption-alignment", default="not_checked")
    parser.add_argument("--risk-level", default="medium")
    parser.add_argument("--required-fix")
    args = parser.parse_args()
    try:
        errors, warnings = append_claim(args)
        exit_with_results(errors, warnings)
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
