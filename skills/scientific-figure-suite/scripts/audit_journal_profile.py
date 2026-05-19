from __future__ import annotations

import argparse
from typing import Any

from _common import VALID_STYLE_STATUSES, exit_with_results, flatten_strings, load_structured_file, main_error


FORBIDDEN_WHEN_UNVERIFIED = ["compliant", "submission-ready", "submission ready"]


def find_profile(data: dict[str, Any]) -> dict[str, Any]:
    profile = data.get("journal_style") or data.get("target_journal") or data
    if not isinstance(profile, dict):
        raise ValueError("journal profile must be a mapping")
    return profile


def validate(data: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    profile = find_profile(data)

    target = profile.get("target") or profile.get("name") or data.get("target")
    if not target:
        errors.append("journal target is required")

    status = profile.get("status") or profile.get("style_status")
    if status not in VALID_STYLE_STATUSES:
        errors.append(f"style status must be one of {sorted(VALID_STYLE_STATUSES)}")

    text = flatten_strings(data).lower()
    if status != "VERIFIED":
        for forbidden in FORBIDDEN_WHEN_UNVERIFIED:
            if forbidden in text:
                errors.append(f"forbidden compliance language for non-VERIFIED status: {forbidden}")

    unresolved = profile.get("unresolved_requirements")
    if status in {"ESTIMATED", "UNVERIFIED"} and not unresolved:
        warnings.append("unresolved_requirements should be listed for ESTIMATED or UNVERIFIED status")

    source = profile.get("guideline_source")
    if status == "VERIFIED" and source not in {"live_official", "user_provided"}:
        errors.append("VERIFIED status requires guideline_source live_official or user_provided")

    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit journal style profile status and language.")
    parser.add_argument("journal_profile")
    args = parser.parse_args()
    try:
        data = load_structured_file(args.journal_profile)
        if not isinstance(data, dict):
            raise ValueError("journal profile must be a mapping")
        errors, warnings = validate(data)
        exit_with_results(errors, warnings)
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
