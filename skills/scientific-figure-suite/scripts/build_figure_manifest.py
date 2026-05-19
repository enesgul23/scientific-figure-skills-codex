from __future__ import annotations

import argparse
from datetime import datetime, timezone

from _common import parse_csv_arg, write_json


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a scientific figure submission manifest.")
    parser.add_argument("--figure-id", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--files", default="", help="Comma-separated output files")
    parser.add_argument("--data-sources", default="", help="Comma-separated data source paths")
    parser.add_argument("--code-sources", default="", help="Comma-separated code source paths")
    parser.add_argument("--style-status", default="UNVERIFIED", choices=["VERIFIED", "ESTIMATED", "UNVERIFIED"])
    parser.add_argument("--quality-report", default="")
    parser.add_argument("--design-only", action="store_true")
    parser.add_argument("--environment-note", default="")
    args = parser.parse_args()

    manifest = {
        "figure_id": args.figure_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "files": parse_csv_arg(args.files),
        "data_sources": parse_csv_arg(args.data_sources),
        "code_sources": parse_csv_arg(args.code_sources),
        "style_status": args.style_status,
        "quality_report": args.quality_report,
        "design_only": args.design_only,
        "environment_note": args.environment_note,
    }
    write_json(args.out, manifest)
    print(f"[PASS] wrote manifest: {args.out}")


if __name__ == "__main__":
    main()
