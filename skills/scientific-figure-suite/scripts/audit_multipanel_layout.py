from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from _common import exit_with_results, load_structured_file, main_error, write_json
from _memory import append_jsonl, resolve_memory_dir, utc_now


AUTO_LAYOUT_ENGINES = {"auto", "automatic", "constrained_layout", "tight_layout", "matplotlib_auto"}
CONTROLLED_LABEL_POLICIES = {"controlled", "curated", "representative_subset", "indexed_subset"}
MAP_SCATTER_TYPES = {"map", "geospatial", "geospatial_map", "station_map", "scatter", "parity_scatter"}


def layout_root(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError("layout artifact must be a mapping")
    for key in ["multipanel_layout", "layout_plan"]:
        value = data.get(key)
        if isinstance(value, dict):
            return value
    return data


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def parse_bbox(value: Any) -> dict[str, float] | None:
    if value is None:
        return None
    if isinstance(value, list) and len(value) == 4:
        x0, y0, width, height = [float(item) for item in value]
    elif isinstance(value, dict):
        x0 = float(value.get("x0", value.get("left", value.get("x", 0.0))))
        y0 = float(value.get("y0", value.get("bottom", value.get("y", 0.0))))
        if "width" in value:
            width = float(value["width"])
        elif "w" in value:
            width = float(value["w"])
        elif "x1" in value:
            width = float(value["x1"]) - x0
        elif "right" in value:
            width = float(value["right"]) - x0
        else:
            return None
        if "height" in value:
            height = float(value["height"])
        elif "h" in value:
            height = float(value["h"])
        elif "y1" in value:
            height = float(value["y1"]) - y0
        elif "top" in value:
            height = float(value["top"]) - y0
        else:
            return None
    else:
        return None
    return {"x0": x0, "y0": y0, "width": width, "height": height, "x1": x0 + width, "y1": y0 + height}


def get_bbox(item: dict[str, Any]) -> dict[str, float] | None:
    for key in ["bbox", "axis_box", "panel_box", "bounds", "rect"]:
        bbox = parse_bbox(item.get(key))
        if bbox is not None:
            return bbox
    return None


def colorbar_entries(layout: dict[str, Any], panels: list[dict[str, Any]]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for panel in panels:
        raw = panel.get("colorbar")
        if raw is True or panel.get("uses_colorbar") is True:
            raw = {} if raw is True else raw
        if isinstance(raw, dict):
            entry = dict(raw)
            entry.setdefault("panel_id", panel.get("id", panel.get("panel_id")))
            entries.append(entry)
    for raw in as_list(layout.get("colorbars")):
        if isinstance(raw, dict):
            entries.append(dict(raw))
    return entries


def normalized_color(value: Any) -> str:
    return str(value or "").strip().lower()


def collect_color_bindings(panel: dict[str, Any]) -> dict[str, str]:
    bindings: dict[str, str] = {}
    for key in ["color_bindings", "semantic_color_map", "semantic_colors"]:
        value = panel.get(key)
        if isinstance(value, dict):
            for category, color in value.items():
                if color not in (None, ""):
                    bindings[str(category)] = str(color)
    return bindings


def label_count(label_spec: Any) -> int:
    if isinstance(label_spec, list):
        return len(label_spec)
    if isinstance(label_spec, dict):
        if isinstance(label_spec.get("labels"), list):
            return len(label_spec["labels"])
        if label_spec.get("count") is not None:
            return int(label_spec["count"])
        if label_spec.get("enabled") is True or label_spec.get("allowed") is True:
            return 1
    return 0


def label_spec_for(panel: dict[str, Any]) -> Any:
    for key in ["direct_labels", "station_labels", "point_labels"]:
        if key in panel:
            return panel.get(key)
    return None


def plot_kind(panel: dict[str, Any]) -> str:
    for key in ["plot_type", "kind", "type", "role"]:
        if panel.get(key):
            return str(panel[key]).lower()
    return ""


def overlap_area(first: dict[str, float], second: dict[str, float]) -> float:
    width = min(first["x1"], second["x1"]) - max(first["x0"], second["x0"])
    height = min(first["y1"], second["y1"]) - max(first["y0"], second["y0"])
    if width <= 0 or height <= 0:
        return 0.0
    return width * height


def check_result(checks: list[dict[str, Any]], name: str, errors: list[str], warnings: list[str], start_e: int, start_w: int) -> None:
    if len(errors) > start_e:
        result = "FAIL"
    elif len(warnings) > start_w:
        result = "PASS_WITH_WARNINGS"
    else:
        result = "PASS"
    checks.append({"check": name, "result": result, "new_blockers": len(errors) - start_e, "new_warnings": len(warnings) - start_w})


def audit_layout(layout: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    checks: list[dict[str, Any]] = []

    panels = [panel for panel in as_list(layout.get("panels")) if isinstance(panel, dict)]
    layout_name = str(layout.get("layout_name") or layout.get("name") or "multipanel_layout")
    layout_engine = str(layout.get("layout_engine") or layout.get("engine") or "").strip().lower()
    manual_fallback = bool(layout.get("manual_axes_fallback") or layout.get("fallback_to_manual_axes"))

    start_e, start_w = len(errors), len(warnings)
    if not panels:
        errors.append("layout must contain at least one panel")
    panel_ids = [str(panel.get("id", panel.get("panel_id", ""))) for panel in panels]
    if len([item for item in panel_ids if item]) != len(panels):
        errors.append("every panel requires id or panel_id")
    duplicates = sorted({item for item in panel_ids if item and panel_ids.count(item) > 1})
    if duplicates:
        errors.append("duplicate panel ids: " + ", ".join(duplicates))
    check_result(checks, "panel_inventory", errors, warnings, start_e, start_w)

    bboxes: list[tuple[str, dict[str, float]]] = []
    start_e, start_w = len(errors), len(warnings)
    for panel, panel_id in zip(panels, panel_ids):
        bbox = get_bbox(panel)
        if bbox is None:
            warnings.append(f"{panel_id}: panel bbox is missing; optical grid cannot be fully audited")
            continue
        if bbox["width"] <= 0 or bbox["height"] <= 0:
            errors.append(f"{panel_id}: panel bbox width and height must be positive")
        for coord in ["x0", "y0", "x1", "y1"]:
            if bbox[coord] < -args.tolerance or bbox[coord] > 1 + args.tolerance:
                errors.append(f"{panel_id}: panel bbox {coord} is outside normalized figure bounds")
        bboxes.append((panel_id, bbox))
    for index, (left_id, left_box) in enumerate(bboxes):
        for right_id, right_box in bboxes[index + 1 :]:
            if overlap_area(left_box, right_box) > args.tolerance:
                errors.append(f"panel boxes overlap: {left_id} and {right_id}")
    check_result(checks, "panel_box_geometry", errors, warnings, start_e, start_w)

    start_e, start_w = len(errors), len(warnings)
    if len(bboxes) >= 2:
        rows: list[list[tuple[str, dict[str, float]]]] = []
        for item in sorted(bboxes, key=lambda pair: pair[1]["y1"], reverse=True):
            for row in rows:
                if abs(item[1]["y1"] - row[0][1]["y1"]) <= args.row_tolerance:
                    row.append(item)
                    break
            else:
                rows.append([item])
        for row in rows:
            if len(row) < 2:
                continue
            top_span = max(item[1]["y1"] for item in row) - min(item[1]["y1"] for item in row)
            bottom_span = max(item[1]["y0"] for item in row) - min(item[1]["y0"] for item in row)
            ids = ", ".join(item[0] for item in row)
            if top_span > args.row_tolerance or bottom_span > args.row_tolerance:
                errors.append(f"panel row boxes do not share top/bottom bounds within tolerance: {ids}")
    else:
        warnings.append("not enough explicit panel boxes to audit row top/bottom alignment")
    check_result(checks, "panel_row_top_bottom_alignment", errors, warnings, start_e, start_w)

    colorbars = colorbar_entries(layout, panels)
    start_e, start_w = len(errors), len(warnings)
    if colorbars:
        if not layout_engine:
            errors.append("colorbar layouts require explicit layout_engine")
        if layout_engine in AUTO_LAYOUT_ENGINES and not manual_fallback:
            errors.append("colorbar layouts cannot rely only on automatic/constrained layout; add manual_axes_fallback or use manual_axes")
        for index, colorbar in enumerate(colorbars, start=1):
            label = str(colorbar.get("label") or colorbar.get("title") or "").strip()
            short_label = str(colorbar.get("short_label") or "").strip()
            if not label:
                errors.append(f"colorbar {index}: label or title is required")
            if len(label) > args.max_colorbar_label_chars and not short_label and colorbar.get("label_strategy") not in {"short_title", "short_label"}:
                errors.append(f"colorbar {index}: long label requires short_label or label_strategy=short_title")
            if not (colorbar.get("label_overlap_checked") is True or colorbar.get("overlap_checked") is True):
                errors.append(f"colorbar {index}: label overlap check is required")
            if not (colorbar.get("label_spacing_checked") is True or colorbar.get("spacing_checked") is True):
                errors.append(f"colorbar {index}: label spacing check is required")
            if get_bbox(colorbar) is None:
                errors.append(f"colorbar {index}: explicit bbox is required for spacing audit")
    check_result(checks, "colorbar_layout_control", errors, warnings, start_e, start_w)

    start_e, start_w = len(errors), len(warnings)
    global_map = layout.get("semantic_color_map") or layout.get("color_semantics") or {}
    global_map = global_map if isinstance(global_map, dict) else {}
    seen: dict[str, tuple[str, str]] = {}
    for panel, panel_id in zip(panels, panel_ids):
        bindings = collect_color_bindings(panel)
        for category, color in bindings.items():
            normalized = normalized_color(color)
            if category in global_map and normalized != normalized_color(global_map[category]):
                errors.append(f"{panel_id}: semantic color for {category} differs from global map")
            if category in seen and normalized != seen[category][0]:
                errors.append(f"{panel_id}: semantic category {category} changes color from panel {seen[category][1]}")
            else:
                seen[category] = (normalized, panel_id)
        if panel.get("semantic_categories") and not bindings:
            warnings.append(f"{panel_id}: semantic_categories listed without explicit color_bindings")
    if len(seen) > 0 and not global_map:
        warnings.append("semantic colors are panel-local; consider adding root semantic_color_map for renderer handoff")
    check_result(checks, "semantic_color_consistency", errors, warnings, start_e, start_w)

    start_e, start_w = len(errors), len(warnings)
    for panel, panel_id in zip(panels, panel_ids):
        kind = plot_kind(panel)
        if not any(token in kind for token in MAP_SCATTER_TYPES):
            continue
        spec = label_spec_for(panel)
        count = label_count(spec)
        if count <= 0:
            continue
        if not isinstance(spec, dict):
            errors.append(f"{panel_id}: direct labels require a policy object, not an unlabeled list")
            continue
        policy = str(spec.get("policy") or "").lower()
        if policy not in CONTROLLED_LABEL_POLICIES:
            errors.append(f"{panel_id}: direct station/point labels require a controlled label policy")
        if spec.get("collision_checked") is not True and spec.get("overlap_checked") is not True:
            errors.append(f"{panel_id}: direct station/point labels require collision_checked=true")
        max_count = int(spec.get("max_count") or args.max_direct_labels)
        if count > min(max_count, args.max_direct_labels):
            errors.append(f"{panel_id}: direct station/point label count exceeds controlled maximum ({count})")
    check_result(checks, "map_scatter_direct_label_control", errors, warnings, start_e, start_w)

    start_e, start_w = len(errors), len(warnings)
    if layout_engine in AUTO_LAYOUT_ENGINES and not manual_fallback:
        warnings.append("automatic layout has no manual_axes_fallback rule for poor optical grid results")
    if not bboxes:
        warnings.append("optical grid review is limited because no explicit panel boxes were supplied")
    check_result(checks, "manual_fallback_and_optical_grid_review", errors, warnings, start_e, start_w)

    result = "FAIL" if errors else ("PASS_WITH_WARNINGS" if warnings else "PASS")
    return {
        "multipanel_layout_audit": {
            "created_at": utc_now(),
            "layout_name": layout_name,
            "result": result,
            "layout_engine": layout_engine or None,
            "panel_count": len(panels),
            "colorbar_count": len(colorbars),
            "checks": checks,
            "blockers": errors,
            "warnings": warnings,
        }
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit multi-panel scientific figure layout geometry, colorbar spacing, semantic colors, and optical grid quality.")
    parser.add_argument("--layout", required=True, help="Layout YAML/JSON file.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--memory-dir", default=None)
    parser.add_argument("--out", default="")
    parser.add_argument("--append-memory", action="store_true")
    parser.add_argument("--tolerance", type=float, default=0.002)
    parser.add_argument("--row-tolerance", type=float, default=0.015)
    parser.add_argument("--max-colorbar-label-chars", type=int, default=36)
    parser.add_argument("--max-direct-labels", type=int, default=12)
    args = parser.parse_args()
    try:
        layout = layout_root(load_structured_file(args.layout))
        report = audit_layout(layout, args)
        payload = report["multipanel_layout_audit"]
        if args.out:
            write_json(args.out, report)
            print(f"[MULTIPANEL-LAYOUT-AUDIT] wrote {args.out}")
        if args.append_memory:
            memory_dir = resolve_memory_dir(args.project_root, args.memory_dir)
            append_jsonl(memory_dir / "multipanel_layout_history.jsonl", report)
        print(f"[MULTIPANEL-LAYOUT-AUDIT] {payload['result']}")
        exit_with_results(payload["blockers"], payload["warnings"])
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
