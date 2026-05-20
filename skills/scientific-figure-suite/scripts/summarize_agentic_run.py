from __future__ import annotations

import argparse
from pathlib import Path

from _common import load_structured_file, main_error
from validate_agentic_runbook import root


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize an agentic Scientific Figure Suite runbook.")
    parser.add_argument("runbook")
    args = parser.parse_args()
    try:
        runbook = root(load_structured_file(Path(args.runbook)))
        print(f"Runbook: {runbook.get('run_id')}")
        print(f"Project: {runbook.get('project_id')}")
        action = runbook.get("next_action", {})
        print(f"Next action: {action.get('alias')} - {action.get('reason')}")
        for stage in runbook.get("stages", []):
            print(f"- {stage.get('stage')}: {stage.get('status')}")
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
