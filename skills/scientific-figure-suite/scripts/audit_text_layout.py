from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from _common import exit_with_results, load_structured_file, main_error, write_json
from _memory import append_jsonl, resolve_memory_dir, utc_now


ALLOWED_ROLES = {
    "figure_title",
    "panel_title",
    "x_label",
    "y_label",
    "tick_label",
    "legend_title",
    "legend_label",
    "colorbar_title",
    "colorbar_tick_label",
    "panel_label",
    "direct_label",
    "annotation",
}

AXIS_BOUND_ROLES = {"x_label", "y_label", "tick_label", "colorbar_title", "colorbar_tick_label"}
TITLE_ROLES = {"figure_title", "panel_title"}
VISIBLE_FALSE = {False, "false", "False", "no", "NO", 0}


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def layout_root(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError("text layout artifact must be a mapping")
    for key in ["text_layout", "text_layout_spec", "layout", "multipanel_layout", "layout_plan"]:
        value = data.get(key)
        if isinstance(value, dict):
            return value
    return data


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


def overlap_area(first: dict[str, float], second: dict[str, float]) -> float:
    width = min(first["x1"], second["x1"]) - max(first["x0"], second["x0"])
    height = min(first["y1"], second["y1"]) - max(first["y0"], second["y0"])
    if width <= 0 or height <= 0:
        return 0.0
    return width * height


def min_gap_violation(first: dict[str, float], second: dict[str, float], min_gap: float) -> bool:
    if overlap_area(first, second) > 0:
        return True
    horizontal_gap = max(second["x0"] - first["x1"], first["x0"] - second["x1"], 0.0)
    vertical_gap = max(second["y0"] - first["y1"], first["y0"] - second["y1"], 0.0)
    same_band = first["y0"] < second["y1"] and second["y0"] < first["y1"]
    same_column = first["x0"] < second["x1"] and second["x0"] < first["x1"]
    return (same_band and horizontal_gap < min_gap) or (same_column and vertical_gap < min_gap)


def collect_text_elements(layout: dict[str, Any]) -> list[dict[str, Any]]:
    elements: list[dict[str, Any]] = []
    for item in as_list(layout.get("text_elements")):
        if isinstance(item, dict):
            elements.append(dict(item))
    for panel in as_list(layout.get("panels")):
        if not isinstance(panel, dict):
            continue
        panel_id = panel.get("id", panel.get("panel_id"))
        for item in as_list(panel.get("text_elements")):
            if isinstance(item, dict):
                element = dict(item)
                element.setdefault("panel_id", panel_id)
                elements.append(element)
        for key, role in [("title", "panel_title"), ("xlabel", "x_label"), ("ylabel", "y_label")]:
            raw = panel.get(key)
            if isinstance(raw, dict):
                element = dict(raw)
                element.setdefault("role", role)
                element.setdefault("panel_id", panel_id)
                elements.append(element)
    return elements


def load_forbidden_labels(args: argparse.Namespace, layout: dict[str, Any]) -> tuple[str | None, set[str], list[str]]:
    warnings: list[str] = []
    profile_id: str | None = None
    forbidden = {str(item).strip().lower() for item in as_list(layout.get("forbidden_vague_labels")) if str(item).strip()}
    profile_obj = layout.get("terminology_profile")
    if isinstance(profile_obj, dict):
        profile_id = str(profile_obj.get("profile_id") or "") or None
        forbidden.update(str(item).strip().lower() for item in as_list(profile_obj.get("forbidden_vague_labels")) if str(item).strip())
    if args.text_profile:
        data = load_structured_file(args.text_profile)
        selection = data.get("text_profile_selection", data) if isinstance(data, dict) else {}
        if isinstance(selection, dict):
            profile_id = str(selection.get("profile_id") or profile_id or "") or None
            forbidden.update(str(item).strip().lower() for item in as_list(selection.get("forbidden_vague_labels")) if str(item).strip())
        else:
            warnings.append("text profile file did not contain a usable object")
    if layout.get("terminology_profile_id") and profile_id is None:
        profile_id = str(layout.get("terminology_profile_id"))
    return profile_id, forbidden, warnings


def add_check(checks: list[dict[str, Any]], name: str, errors: list[str], warnings: list[str], start_e: int, start_w: int) -> None:
    if len(errors) > start_e:
        result = "FAIL"
    elif len(warnings) > start_w:
        result = "PASS_WITH_WARNINGS"
    else:
        result = "PASS"
    checks.append({"check": name, "result": result, "new_blockers": len(errors) - start_e, "new_warnings": len(warnings) - start_w})


def element_label(element: dict[str, Any], index: int) -> str:
    role = element.get("role", "unknown_role")
    panel_id = element.get("panel_id", "figure")
    text = str(element.get("text", "")).replace("\n", " ").strip()
    text = text[:36] + ("..." if len(text) > 36 else "")
    return f"{panel_id}:{role}:{index}:{text}"


def audit_layout(layout: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    repairs: list[dict[str, Any]] = []
    checks: list[dict[str, Any]] = []

    figure_id = str(layout.get("figure_id") or layout.get("layout_name") or layout.get("name") or "unknown_figure")
    elements = collect_text_elements(layout)
    profile_id, forbidden_labels, profile_warnings = load_forbidden_labels(args, layout)
    warnings.extend(profile_warnings)

    start_e, start_w = len(errors), len(warnings)
    normalized: list[tuple[int, dict[str, Any], dict[str, float]]] = []
    if not elements:
        errors.append("text layout must contain at least one text element")
    for index, element in enumerate(elements, start=1):
        role = str(element.get("role") or "").strip()
        if role not in ALLOWED_ROLES:
            errors.append(f"text element {index}: invalid or missing role")
        if not str(element.get("text") or "").strip():
            errors.append(f"text element {index}: text is required")
        bbox = parse_bbox(element.get("bbox"))
        if bbox is None:
            errors.append(f"text element {index}: bbox is required")
            continue
        if bbox["width"] <= 0 or bbox["height"] <= 0:
            errors.append(f"text element {index}: bbox width and height must be positive")
        normalized.append((index, element, bbox))
    add_check(checks, "text_element_inventory", errors, warnings, start_e, start_w)

    start_e, start_w = len(errors), len(warnings)
    for index, element, bbox in normalized:
        label = element_label(element, index)
        allow_outside = element.get("allow_outside") is True or element.get("role") == "caption_text"
        if not allow_outside:
            for coord in ["x0", "y0", "x1", "y1"]:
                if bbox[coord] < -args.bounds_tolerance or bbox[coord] > 1 + args.bounds_tolerance:
                    errors.append(f"{label}: text bbox {coord} exceeds normalized figure bounds")
        if element.get("in_axes_bounds") is False and element.get("role") in AXIS_BOUND_ROLES:
            errors.append(f"{label}: axis or colorbar text is outside its allocated bounds")
            repairs.append({"element": label, "repair": "reserve_margin_or_shorten_label"})
    add_check(checks, "text_bounds_and_axis_overflow", errors, warnings, start_e, start_w)

    start_e, start_w = len(errors), len(warnings)
    visible = [(i, element, bbox) for i, element, bbox in normalized if element.get("visible", True) not in VISIBLE_FALSE]
    for offset, (left_index, left, left_box) in enumerate(visible):
        if left.get("allow_overlap") is True:
            continue
        for right_index, right, right_box in visible[offset + 1 :]:
            if right.get("allow_overlap") is True:
                continue
            if min_gap_violation(left_box, right_box, args.min_gap):
                errors.append(f"text overlap or insufficient spacing: {element_label(left, left_index)} vs {element_label(right, right_index)}")
                repairs.append({"elements": [element_label(left, left_index), element_label(right, right_index)], "repair": "move_wrap_or_reduce_lower_priority_text"})
    add_check(checks, "text_overlap_and_spacing", errors, warnings, start_e, start_w)

    start_e, start_w = len(errors), len(warnings)
    for index, element, _bbox in normalized:
        label = element_label(element, index)
        font_size = element.get("font_size_pt")
        if font_size is None:
            warnings.append(f"{label}: font_size_pt is missing")
        else:
            try:
                if float(font_size) < args.min_font_size_pt:
                    errors.append(f"{label}: font size is below {args.min_font_size_pt:g} pt")
            except (TypeError, ValueError):
                errors.append(f"{label}: font_size_pt must be numeric")
        rotation = float(element.get("rotation", 0) or 0)
        if abs(rotation) > args.max_rotation:
            errors.append(f"{label}: rotation exceeds {args.max_rotation:g} degrees")
        elif abs(rotation) > 60 and element.get("role") == "tick_label":
            warnings.append(f"{label}: tick label rotation is high; confirm readability")
    add_check(checks, "font_size_and_rotation", errors, warnings, start_e, start_w)

    start_e, start_w = len(errors), len(warnings)
    for index, element, _bbox in normalized:
        text = str(element.get("text") or "").strip()
        role = str(element.get("role") or "")
        label = element_label(element, index)
        if role in TITLE_ROLES and len(text) > args.max_title_chars and element.get("can_wrap") is not True:
            errors.append(f"{label}: long title requires can_wrap=true or a shorter title")
            repairs.append({"element": label, "repair": "wrap_title"})
        if role == "colorbar_title":
            if len(text) > args.max_colorbar_title_chars and not element.get("short_text") and element.get("can_abbreviate") is not True:
                errors.append(f"{label}: long colorbar title requires short_text or can_abbreviate=true")
                repairs.append({"element": label, "repair": "short_colorbar_title_plus_caption_note"})
            placement = str(element.get("placement") or "right").strip().lower()
            if placement not in {"right", "panel_right", "group_right"}:
                errors.append(f"{label}: colorbar title placement must default to right or audited group_right")
            if placement == "group_right":
                if element.get("shared_scale") is not True and element.get("group_shared_scale") is not True:
                    errors.append(f"{label}: group colorbar requires shared_scale=true")
                if element.get("compresses_panels") is True:
                    errors.append(f"{label}: group colorbar must not compress panel boxes")
                if element.get("overlap_checked") is not True:
                    errors.append(f"{label}: group colorbar requires overlap_checked=true")
    add_check(checks, "title_and_colorbar_text_policy", errors, warnings, start_e, start_w)

    start_e, start_w = len(errors), len(warnings)
    direct_labels = [item for item in normalized if item[1].get("role") == "direct_label" and item[1].get("visible", True) not in VISIBLE_FALSE]
    if len(direct_labels) > args.max_direct_labels:
        errors.append(f"direct label count exceeds controlled maximum ({len(direct_labels)} > {args.max_direct_labels})")
        repairs.append({"repair": "hide_low_priority_direct_labels", "current_count": len(direct_labels), "target_count": args.max_direct_labels})
    for index, element, _bbox in direct_labels:
        label = element_label(element, index)
        if element.get("overlap_checked") is not True and element.get("collision_checked") is not True:
            errors.append(f"{label}: direct labels require overlap_checked=true or collision_checked=true")
    add_check(checks, "direct_label_control", errors, warnings, start_e, start_w)

    start_e, start_w = len(errors), len(warnings)
    if forbidden_labels:
        for index, element, _bbox in normalized:
            text = str(element.get("text") or "").strip().lower()
            if text in forbidden_labels:
                errors.append(f"{element_label(element, index)}: vague label is forbidden by text profile")
                repairs.append({"element": element_label(element, index), "repair": "replace_with_domain_specific_label"})
    add_check(checks, "academic_terminology", errors, warnings, start_e, start_w)

    result = "FAIL" if errors else ("PASS_WITH_WARNINGS" if warnings else "PASS")
    return {
        "text_layout_report": {
            "created_at": utc_now(),
            "figure_id": figure_id,
            "result": result,
            "terminology_profile_id": profile_id,
            "colorbar_policy": str(layout.get("colorbar_policy") or "right_default_shared_group_when_audited"),
            "text_element_count": len(elements),
            "checks": checks,
            "blockers": errors,
            "warnings": warnings,
            "repairs_suggested": repairs,
        }
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit text overlap, clipping, alignment, colorbar titles, and terminology for scientific figures.")
    parser.add_argument("--layout", required=True, help="Text layout YAML/JSON artifact.")
    parser.add_argument("--text-profile", default="", help="Optional text profile selection JSON.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--memory-dir", default=None)
    parser.add_argument("--out", default="")
    parser.add_argument("--append-memory", action="store_true")
    parser.add_argument("--bounds-tolerance", type=float, default=0.002)
    parser.add_argument("--min-gap", type=float, default=0.002)
    parser.add_argument("--min-font-size-pt", type=float, default=6.0)
    parser.add_argument("--max-rotation", type=float, default=90.0)
    parser.add_argument("--max-title-chars", type=int, default=80)
    parser.add_argument("--max-colorbar-title-chars", type=int, default=36)
    parser.add_argument("--max-direct-labels", type=int, default=12)
    args = parser.parse_args()
    try:
        layout = layout_root(load_structured_file(args.layout))
        report = audit_layout(layout, args)
        payload = report["text_layout_report"]
        if args.out:
            write_json(args.out, report)
            print(f"[TEXT-LAYOUT-AUDIT] wrote {args.out}")
        if args.append_memory:
            memory_dir = resolve_memory_dir(args.project_root, args.memory_dir)
            append_jsonl(memory_dir / "text_layout_history.jsonl", report)
        print(f"[TEXT-LAYOUT-AUDIT] {payload['result']}")
        exit_with_results(payload["blockers"], payload["warnings"])
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
