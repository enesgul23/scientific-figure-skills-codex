from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from _common import exit_with_results, main_error
from _memory import append_jsonl, resolve_memory_dir, update_manifest_timestamp, utc_now


def main() -> None:
    parser = argparse.ArgumentParser(description="Append a project-local scientific figure decision entry.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--memory-dir", default=None)
    parser.add_argument("--decision-type", required=True)
    parser.add_argument("--decision", required=True)
    parser.add_argument("--figure-id", default=None)
    parser.add_argument("--rationale", default="")
    parser.add_argument("--artifact", action="append", default=[])
    parser.add_argument("--actor", default="codex")
    args = parser.parse_args()
    try:
        memory_dir = resolve_memory_dir(Path(args.project_root), args.memory_dir)
        if not memory_dir.is_dir():
            raise FileNotFoundError(f"memory directory missing: {memory_dir}")
        entry: dict[str, Any] = {
            "figure_decision": {
                "created_at": utc_now(),
                "decision_type": args.decision_type,
                "decision": args.decision,
                "figure_id": args.figure_id,
                "rationale": args.rationale,
                "artifact_refs": args.artifact,
                "actor": args.actor,
            }
        }
        append_jsonl(memory_dir / "figure_decision_log.jsonl", entry)
        update_manifest_timestamp(memory_dir)
        print(f"[FIGURE-DECISION] {args.decision_type}: {args.decision}")
        exit_with_results([], [])
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
