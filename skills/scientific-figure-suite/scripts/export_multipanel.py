from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from _common import load_structured_file, parse_csv_arg


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

    canvas = layout.get("canvas", {})
    width_mm = float(canvas.get("width_mm", 180))
    height_mm = float(canvas.get("height_mm", 120))
    panels: list[dict[str, Any]] = layout.get("panels") or [{"id": "a"}, {"id": "b"}]
    count = max(1, len(panels))
    columns = int(layout.get("grid", {}).get("columns") or min(count, 2))
    rows = (count + columns - 1) // columns

    fig, axes = plt.subplots(rows, columns, figsize=(width_mm / 25.4, height_mm / 25.4), squeeze=False)
    for index, ax in enumerate(axes.flat):
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
    fig.tight_layout()

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
