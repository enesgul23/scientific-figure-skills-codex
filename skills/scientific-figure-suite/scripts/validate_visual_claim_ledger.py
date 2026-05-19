from __future__ import annotations

import argparse
from typing import Any

from _common import exit_with_results, load_structured_file, main_error


VALID_SUPPORT = {"supported", "partially_supported", "unsupported", "unverifiable"}
HIGH_RISK_TYPES = {"causal", "mechanistic"}


def validate_claim(claim: dict[str, Any], index: int) -> list[str]:
    errors: list[str] = []
    prefix = f"claim {claim.get('id', index + 1)}"

    if not claim.get("claim_text"):
        errors.append(f"{prefix}: claim_text is required")
    support = claim.get("support_status")
    if support not in VALID_SUPPORT:
        errors.append(f"{prefix}: support_status must be one of {sorted(VALID_SUPPORT)}")
    if not claim.get("visual_element"):
        errors.append(f"{prefix}: visual_element is required")
    if "caption_alignment" not in claim:
        errors.append(f"{prefix}: caption_alignment is required")

    risk = claim.get("risk_level")
    required_fix = str(claim.get("required_fix") or "").strip()
    if support in {"unsupported", "unverifiable"} and not required_fix:
        errors.append(f"{prefix}: unsupported or unverifiable claims require required_fix")
    if risk == "high" and not required_fix:
        errors.append(f"{prefix}: high-risk claims require required_fix")

    claim_type = claim.get("claim_type")
    if claim_type in HIGH_RISK_TYPES and support != "supported" and not required_fix:
        errors.append(f"{prefix}: causal/mechanistic claims need support or a fix")

    return errors


def validate(data: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    ledger = data.get("visual_claim_ledger", data)
    if not isinstance(ledger, dict):
        return ["visual_claim_ledger must be a mapping"], warnings
    if not ledger.get("figure_id"):
        errors.append("figure_id is required")

    claims = ledger.get("claims")
    if not isinstance(claims, list) or not claims:
        errors.append("claims must be a non-empty list")
    else:
        for index, claim in enumerate(claims):
            if not isinstance(claim, dict):
                errors.append(f"claim {index + 1}: must be a mapping")
                continue
            errors.extend(validate_claim(claim, index))
            if not claim.get("data_source") and claim.get("support_status") == "supported":
                warnings.append(f"claim {claim.get('id', index + 1)} is supported but has no data_source")

    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a visual claim ledger YAML/JSON file.")
    parser.add_argument("ledger")
    args = parser.parse_args()
    try:
        data = load_structured_file(args.ledger)
        if not isinstance(data, dict):
            raise ValueError("ledger must be a mapping")
        errors, warnings = validate(data)
        exit_with_results(errors, warnings)
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
