from __future__ import annotations

import argparse
import math
import re
from pathlib import Path
from typing import Any

from _common import exit_with_results, main_error, parse_csv_arg
from _memory import append_jsonl, resolve_memory_dir, sha256_file, utc_now


RASTER_FORMATS = {"png", "jpg", "jpeg", "tif", "tiff"}
SVG_TEXT_RE = re.compile(r"<text\b|aria-label=|<title\b", re.IGNORECASE)


def raster_stats(path: Path) -> tuple[int | None, int | None, float | None, list[str]]:
    notes: list[str] = []
    try:
        from PIL import Image  # type: ignore
        import numpy as np  # type: ignore

        with Image.open(path) as image:
            array = np.asarray(image.convert("RGB"), dtype=float)
            return int(image.width), int(image.height), float(array.var()), notes
    except ImportError:
        notes.append("Pillow or numpy unavailable; trying matplotlib image reader.")
    except Exception as exc:
        notes.append(f"Pillow image audit failed: {exc}")
    try:
        import matplotlib.image as mpimg  # type: ignore
        import numpy as np  # type: ignore

        array = mpimg.imread(path)
        height, width = array.shape[:2]
        return int(width), int(height), float(np.asarray(array, dtype=float).var()), notes
    except Exception as exc:
        notes.append(f"raster pixel audit unavailable: {exc}")
        return None, None, None, notes


def audit_file(path: Path, args: argparse.Namespace) -> tuple[dict[str, Any], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    suffix = path.suffix.lower().lstrip(".")
    result: dict[str, Any] = {
        "path": str(path),
        "format": suffix,
        "exists": path.is_file(),
        "sha256": None,
        "byte_size": None,
        "width_px": None,
        "height_px": None,
        "pixel_variance": None,
        "svg_text_present": None,
        "baseline_status": "NOT_RUN",
        "notes": [],
    }
    if not path.is_file():
        errors.append(f"render file missing: {path}")
        return result, errors, warnings

    result["sha256"] = sha256_file(path)
    result["byte_size"] = path.stat().st_size
    if result["byte_size"] <= 0:
        errors.append(f"render file is empty: {path}")

    if suffix in RASTER_FORMATS:
        width, height, variance, notes = raster_stats(path)
        result["width_px"] = width
        result["height_px"] = height
        result["pixel_variance"] = variance
        result["notes"].extend(notes)
        warnings.extend(notes)
        if width is not None and width < args.min_width:
            errors.append(f"raster width below minimum for {path}: {width} < {args.min_width}")
        if height is not None and height < args.min_height:
            errors.append(f"raster height below minimum for {path}: {height} < {args.min_height}")
        if variance is not None and (math.isnan(variance) or variance < args.min_variance):
            errors.append(f"raster appears blank or near-blank for {path}: variance={variance}")
    elif suffix == "svg":
        text = path.read_text(encoding="utf-8", errors="ignore")
        has_text = bool(SVG_TEXT_RE.search(text))
        result["svg_text_present"] = has_text
        if not has_text:
            message = f"SVG text/title elements not detected: {path}"
            if args.require_svg_text:
                errors.append(message)
            else:
                warnings.append(message)

    if args.baseline_dir:
        baseline = Path(args.baseline_dir).resolve() / path.name
        if baseline.is_file():
            result["baseline_status"] = "MATCH" if sha256_file(baseline) == result["sha256"] else "DIFF"
            if result["baseline_status"] == "DIFF":
                warnings.append(f"baseline hash differs: {path.name}")
        else:
            result["baseline_status"] = "MISSING"
            warnings.append(f"baseline file missing: {baseline}")
    return result, errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit rendered scientific figure files for visual QA and regression sanity.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--memory-dir", default=None)
    parser.add_argument("--figure-id", default="unknown")
    parser.add_argument("--file", action="append", required=True)
    parser.add_argument("--expected-formats", default="")
    parser.add_argument("--baseline-dir", default="")
    parser.add_argument("--min-width", type=int, default=120)
    parser.add_argument("--min-height", type=int, default=120)
    parser.add_argument("--min-variance", type=float, default=1.0)
    parser.add_argument("--require-svg-text", action="store_true")
    parser.add_argument("--append-memory", action="store_true")
    args = parser.parse_args()
    try:
        project_root = Path(args.project_root).expanduser().resolve()
        files = [(project_root / item).resolve() if not Path(item).is_absolute() else Path(item).resolve() for item in args.file]
        errors: list[str] = []
        warnings: list[str] = []
        file_results: list[dict[str, Any]] = []
        for path in files:
            result, file_errors, file_warnings = audit_file(path, args)
            file_results.append(result)
            errors.extend(file_errors)
            warnings.extend(file_warnings)

        expected_formats = {item.lower().lstrip(".") for item in parse_csv_arg(args.expected_formats)}
        if expected_formats:
            actual_formats = {item.get("format") for item in file_results if item.get("exists")}
            missing = sorted(expected_formats - actual_formats)
            if missing:
                errors.append("expected render formats missing: " + ", ".join(missing))

        result_status = "FAIL" if errors else ("PASS_WITH_WARNINGS" if warnings else "PASS")
        report = {
            "visual_regression_report": {
                "created_at": utc_now(),
                "figure_id": args.figure_id,
                "result": result_status,
                "files": file_results,
                "blockers": errors,
                "warnings": warnings,
                "baseline_dir": args.baseline_dir or None,
            }
        }
        if args.append_memory:
            memory_dir = resolve_memory_dir(project_root, args.memory_dir)
            append_jsonl(memory_dir / "visual_regression_history.jsonl", report)
        print(f"[RENDER-QUALITY] {result_status}")
        exit_with_results(errors, warnings)
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
