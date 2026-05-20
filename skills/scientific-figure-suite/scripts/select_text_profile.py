from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from _common import exit_with_results, load_structured_file, main_error, write_json
from _memory import utc_now


def norm(value: str | None) -> str:
    return str(value or "").strip().lower().replace("_", "-")


def load_profiles(path: Path) -> list[dict[str, Any]]:
    data = load_structured_file(path)
    root = data.get("text_style_profiles", data) if isinstance(data, dict) else {}
    profiles = root.get("profiles") if isinstance(root, dict) else None
    if not isinstance(profiles, list):
        raise ValueError("text_style_profiles.profiles must be a list")
    return [profile for profile in profiles if isinstance(profile, dict)]


def score_profile(profile: dict[str, Any], domain: str, chart_type: str) -> int:
    score = 0
    domains = {norm(item) for item in profile.get("domains", [])}
    chart_types = {norm(item) for item in profile.get("chart_types", [])}
    profile_id = norm(profile.get("profile_id"))
    if domain and (domain in domains or domain == profile_id):
        score += 10
    if chart_type and chart_type in chart_types:
        score += 8
    if domain and any(domain in item or item in domain for item in domains):
        score += 2
    if chart_type and any(chart_type in item or item in chart_type for item in chart_types):
        score += 2
    return score


def select_profile(profiles: list[dict[str, Any]], domain: str, chart_type: str) -> tuple[dict[str, Any], list[str]]:
    warnings: list[str] = []
    scored = [(score_profile(profile, domain, chart_type), profile) for profile in profiles]
    scored.sort(key=lambda item: item[0], reverse=True)
    if scored and scored[0][0] > 0:
        return scored[0][1], warnings
    for profile in profiles:
        if profile.get("profile_id") == "statistical_plots":
            warnings.append("no exact text profile match; using statistical_plots fallback")
            return profile, warnings
    raise ValueError("no usable text profile found")


def build_selection(args: argparse.Namespace, skill_dir: Path) -> dict[str, Any]:
    domain = norm(args.domain)
    chart_type = norm(args.chart_type)
    profiles = load_profiles(skill_dir / args.profiles)
    profile, warnings = select_profile(profiles, domain, chart_type)
    selection = {
        "text_profile_selection": {
            "created_at": utc_now(),
            "domain": args.domain or None,
            "chart_type": args.chart_type or None,
            "journal_status": args.journal_status,
            "profile_id": profile.get("profile_id"),
            "source": "bundled_domain_profiles",
            "live_web_required": False,
            "canonical_axis_labels": profile.get("canonical_axis_labels", {}),
            "title_patterns": profile.get("title_patterns", []),
            "unit_formatting": profile.get("unit_formatting", {}),
            "abbreviation_rules": profile.get("abbreviation_rules", []),
            "forbidden_vague_labels": profile.get("forbidden_vague_labels", []),
            "caption_expansion_suggestions": profile.get("caption_expansion_suggestions", []),
            "warnings": warnings,
        }
    }
    return selection


def main() -> None:
    parser = argparse.ArgumentParser(description="Select a bundled scientific figure text style profile.")
    parser.add_argument("--skill-dir", default=".")
    parser.add_argument("--profiles", default="assets/text_profiles/domain_text_profiles.json")
    parser.add_argument("--domain", default="")
    parser.add_argument("--chart-type", default="")
    parser.add_argument("--journal-status", default="UNVERIFIED", choices=["VERIFIED", "ESTIMATED", "UNVERIFIED"])
    parser.add_argument("--out", default="")
    args = parser.parse_args()
    try:
        skill_dir = Path(args.skill_dir).resolve()
        selection = build_selection(args, skill_dir)
        if args.out:
            write_json(args.out, selection)
            print(f"[TEXT-PROFILE] wrote {args.out}")
        payload = selection["text_profile_selection"]
        print(f"[TEXT-PROFILE] {payload['profile_id']}")
        exit_with_results([], payload.get("warnings", []))
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
