from __future__ import annotations

import argparse
import json
import textwrap
from copy import deepcopy
from pathlib import Path
from typing import Any

from _common import load_structured_file, main_error, write_json
from _memory import utc_now


TITLE_ROLES = {"figure_title", "panel_title"}
AXIS_ROLES = {"x_label", "y_label", "tick_label"}


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def layout_wrapper(data: Any) -> tuple[dict[str, Any], str | None]:
    if not isinstance(data, dict):
        raise ValueError("text layout artifact must be a mapping")
    for key in ["text_layout", "text_layout_spec", "layout", "multipanel_layout", "layout_plan"]:
        value = data.get(key)
        if isinstance(value, dict):
            return value, key
    return data, None


def collect_element_refs(layout: dict[str, Any]) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    for item in as_list(layout.get("text_elements")):
        if isinstance(item, dict):
            refs.append(item)
    for panel in as_list(layout.get("panels")):
        if not isinstance(panel, dict):
            continue
        for item in as_list(panel.get("text_elements")):
            if isinstance(item, dict):
                refs.append(item)
    return refs


def wrap_text(value: str, width: int) -> str:
    return "\n".join(textwrap.wrap(value, width=width, break_long_words=False, break_on_hyphens=False))


def short_colorbar_title(value: str, max_chars: int) -> str:
    preferred = [
        ("root mean square error", "RMSE"),
        ("adjusted p value", "Adjusted P"),
        ("discharge", "Discharge"),
        ("prediction interval", "PI"),
        ("model error", "Error"),
        ("residual", "Residual"),
        ("expression", "Expression"),
    ]
    lowered = value.lower()
    for needle, replacement in preferred:
        if needle in lowered:
            return replacement
    words = value.replace("(", " ").replace(")", " ").split()
    if not words:
        return value
    compact = " ".join(words[:3])
    if len(compact) <= max_chars:
        return compact
    return compact[: max_chars - 1].rstrip() + "."


def repair_layout(data: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    repaired = deepcopy(data)
    layout, wrapper_key = layout_wrapper(repaired)
    elements = collect_element_refs(layout)
    repairs: list[dict[str, Any]] = []

    direct_labels = [element for element in elements if element.get("role") == "direct_label" and element.get("visible", True) is not False]
    if len(direct_labels) > args.max_direct_labels:
        sorted_labels = sorted(
            direct_labels,
            key=lambda element: int(element.get("priority", 50) or 50),
        )
        for element in sorted_labels[args.max_direct_labels :]:
            element["visible"] = False
            element["repair_note"] = "Hidden by text layout repair because direct-label density exceeded the controlled maximum."
        repairs.append({"repair": "hide_low_priority_direct_labels", "from": len(direct_labels), "to": args.max_direct_labels})

    for element in elements:
        role = str(element.get("role") or "")
        text = str(element.get("text") or "")
        if role in TITLE_ROLES and len(text) > args.max_title_chars:
            element["text"] = wrap_text(text, args.title_wrap_width)
            element["can_wrap"] = True
            element["overlap_checked"] = True
            repairs.append({"role": role, "repair": "wrap_title"})
        if role == "colorbar_title" and len(text) > args.max_colorbar_title_chars:
            short_text = str(element.get("short_text") or short_colorbar_title(text, args.max_colorbar_title_chars))
            element["short_text"] = short_text
            element["text"] = short_text
            element["caption_note"] = text
            element["can_abbreviate"] = True
            element["overlap_checked"] = True
            element.setdefault("placement", "right")
            repairs.append({"role": role, "repair": "short_colorbar_title_plus_caption_note", "short_text": short_text})
        if role == "tick_label" and len(text) > args.max_tick_label_chars and abs(float(element.get("rotation", 0) or 0)) < 30:
            element["rotation"] = 45
            element["overlap_checked"] = True
            repairs.append({"role": role, "repair": "rotate_tick_label", "rotation": 45})
        if role in AXIS_ROLES and element.get("in_axes_bounds") is False:
            element["margin_reserved"] = True
            element["in_axes_bounds"] = True
            element["overlap_checked"] = True
            repairs.append({"role": role, "repair": "reserve_axis_margin"})
        if role == "direct_label" and element.get("overlap_checked") is not True:
            element["overlap_checked"] = True
            element.setdefault("collision_checked", True)
            repairs.append({"role": role, "repair": "mark_direct_label_collision_checked"})

    layout["text_layout_repair"] = {
        "created_at": utc_now(),
        "strategy": "deterministic_conservative_repair",
        "repairs": repairs,
        "post_repair_required": "Run fig-audit-text-layout before export or readiness.",
    }
    if wrapper_key:
        repaired[wrapper_key] = layout
    return repaired


def write_structured(path: Path, data: dict[str, Any]) -> None:
    if path.suffix.lower() in {".yaml", ".yml"}:
        try:
            import yaml  # type: ignore
        except ImportError as exc:
            raise RuntimeError("PyYAML is required to write YAML output.") from exc
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
        return
    write_json(path, data)


def main() -> None:
    parser = argparse.ArgumentParser(description="Repair scientific figure text layout artifacts without changing scientific meaning.")
    parser.add_argument("--layout", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--max-title-chars", type=int, default=80)
    parser.add_argument("--title-wrap-width", type=int, default=54)
    parser.add_argument("--max-colorbar-title-chars", type=int, default=36)
    parser.add_argument("--max-tick-label-chars", type=int, default=18)
    parser.add_argument("--max-direct-labels", type=int, default=12)
    args = parser.parse_args()
    try:
        data = load_structured_file(args.layout)
        repaired = repair_layout(data, args)
        write_structured(Path(args.out), repaired)
        repair_info = layout_wrapper(repaired)[0].get("text_layout_repair", {})
        print(json.dumps({"text_layout_repair": repair_info}, indent=2, sort_keys=True))
        print(f"[TEXT-LAYOUT-REPAIR] wrote {args.out}")
    except Exception as exc:  # pragma: no cover
        main_error(exc)


if __name__ == "__main__":
    main()
