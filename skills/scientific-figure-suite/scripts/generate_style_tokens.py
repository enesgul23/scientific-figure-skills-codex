from __future__ import annotations

import argparse
from pathlib import Path

from _common import load_structured_file, write_json


def main() -> None:
    parser = argparse.ArgumentParser(description="Copy a stored style token profile to a working JSON file.")
    parser.add_argument("--profile", required=True, help="Profile name, for example nature_estimated")
    parser.add_argument("--out", required=True, help="Output JSON path")
    parser.add_argument("--status", choices=["VERIFIED", "ESTIMATED", "UNVERIFIED"], default="")
    args = parser.parse_args()

    skill_dir = Path(__file__).resolve().parents[1]
    token_path = skill_dir / "assets" / "style_tokens" / f"{args.profile}.json"
    if not token_path.exists():
        raise SystemExit(f"[FAIL] unknown style token profile: {args.profile}")

    token = load_structured_file(token_path)
    if not isinstance(token, dict):
        raise SystemExit("[FAIL] style token must be a mapping")

    if args.status:
        if args.status == "VERIFIED" and token.get("requires_live_verification") is True:
            raise SystemExit("[FAIL] cannot mark stored profile VERIFIED without current official or user-provided guidelines")
        token["status"] = args.status

    write_json(args.out, token)
    print(f"[PASS] wrote style token: {args.out}")


if __name__ == "__main__":
    main()
