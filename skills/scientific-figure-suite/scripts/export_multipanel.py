from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from _common import load_structured_file, parse_csv_arg


def layout_root(data: dict[str, Any]) -> dict[str, Any]:
    for key in ["multipanel_layout", "layout_plan"]:
        value = data.get(key)
        if isinstance(value, dict):
            return value
    return data


def parse_bbox(value: Any) -> list[float] | None:
    if isinstance(value, list) and len(value) == 4:
        return [float(item) for item in value]
    if not isinstance(value, dict):
        return None
    x0 = float(value.get("x0", value.get("left", value.get("x", 0.0))))
    y0 = float(value.get("y0", value.get("bottom", value.get("y", 0.0))))
    if "width" in value:
        width = float(value["width"])
    elif "w" in value:
        width = float(value["w"])
    elif "x1" in value:
        width = float(value["x1"]) - x0
    else:
        return None
    if "height" in value:
        height = float(value["height"])
    elif "h" in value:
        height = float(value["h"])
    elif "y1" in value:
        height = float(value["y1"]) - y0
    else:
        return None
    return [x0, y0, width, height]


def panel_bbox(panel: dict[str, Any]) -> list[float] | None:
    for key in ["bbox", "axis_box", "panel_box", "bounds", "rect"]:
        bbox = parse_bbox(panel.get(key))
        if bbox is not None:
            return bbox
    return None


def colorbar_specs(layout: dict[str, Any], panels: list[dict[str, Any]]) -> list[dict[str, Any]]:
    specs: list[dict[str, Any]] = []
    for panel in panels:
        raw = panel.get("colorbar")
        if raw is True:
            raw = {}
        if isinstance(raw, dict):
            specs.append(raw)
    raw_colorbars = layout.get("colorbars")
    if isinstance(raw_colorbars, list):
        specs.extend(item for item in raw_colorbars if isinstance(item, dict))
    return specs


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a simple labeled multipanel layout proof from a layout YAML/JSON file.")
    parser.add_argument("--layout", required=True)
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--formats", default="pdf,png")
    parser.add_argument("--dpi", type=int, default=300)
    args = parser.parse_args()

    import matplotlib.pyplot as plt

    layout = load_structured_file(args.layout)
    if not isinstance(layout, dict):
        raise SystemExit("[FAIL] layout must be a mapping")
    layout = layout_root(layout)

    canvas = layout.get("canvas", {})
    width_mm = float(canvas.get("width_mm", 180))
    height_mm = float(canvas.get("height_mm", 120))
    panels: list[dict[str, Any]] = layout.get("panels") or [{"id": "a"}, {"id": "b"}]
    count = max(1, len(panels))
    columns = int(layout.get("grid", {}).get("columns") or min(count, 2))
    rows = (count + columns - 1) // columns

    fig = plt.figure(figsize=(width_mm / 25.4, height_mm / 25.4))
    manual_boxes = [panel_bbox(panel) for panel in panels]
    axes = []
    if all(box is not None for box in manual_boxes):
        axes = [fig.add_axes(box) for box in manual_boxes if box is not None]
    else:
        grid_axes = fig.subplots(rows, columns, squeeze=False)
        fig.subplots_adjust(left=0.06, right=0.97, bottom=0.08, top=0.94, wspace=0.10, hspace=0.12)
        axes = list(grid_axes.flat)

    for index, ax in enumerate(axes):
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color("#2f3542")
            spine.set_linewidth(0.75)
        if index < count:
            panel = panels[index]
            label = panel.get("id", chr(ord("a") + index))
            role = panel.get("role", "panel")
            ax.text(0.02, 0.98, str(label), transform=ax.transAxes, va="top", ha="left", fontweight="bold")
            ax.text(0.5, 0.5, str(role), transform=ax.transAxes, va="center", ha="center", fontsize=8)
        else:
            ax.set_visible(False)

    for spec in colorbar_specs(layout, panels):
        bbox = panel_bbox(spec)
        if bbox is None:
            continue
        cax = fig.add_axes(bbox)
        cax.imshow([[0], [1]], cmap="viridis", aspect="auto", origin="lower")
        cax.set_xticks([])
        cax.set_yticks([])
        label = spec.get("short_label") or spec.get("label") or spec.get("title")
        if label:
            cax.set_title(str(label), fontsize=6, pad=2)

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    basename = layout.get("layout_name", "multipanel_layout")
    for fmt in parse_csv_arg(args.formats):
        output = outdir / f"{basename}.{fmt}"
        kwargs = {"bbox_inches": "tight", "facecolor": "white"}
        if fmt.lower() in {"png", "tif", "tiff", "jpg", "jpeg"}:
            kwargs["dpi"] = args.dpi
        fig.savefig(output, **kwargs)
        print(f"[PASS] wrote {output}")


if __name__ == "__main__":
    main()
