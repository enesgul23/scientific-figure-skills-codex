from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.image as mpimg
import matplotlib.pyplot as plt


def main() -> None:
    parser = argparse.ArgumentParser(description="Raster multipanel composer template.")
    parser.add_argument("--panel", action="append", required=True, help="Panel image path; repeat for each panel")
    parser.add_argument("--label", action="append", default=[])
    parser.add_argument("--cols", type=int, default=2)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    panels = [Path(item) for item in args.panel]
    rows = (len(panels) + args.cols - 1) // args.cols
    fig, axes = plt.subplots(rows, args.cols, figsize=(3.4 * args.cols, 3.0 * rows), constrained_layout=True)
    axes_list = axes.ravel() if hasattr(axes, "ravel") else [axes]
    for index, ax in enumerate(axes_list):
        ax.axis("off")
        if index >= len(panels):
            continue
        ax.imshow(mpimg.imread(panels[index]))
        label = args.label[index] if index < len(args.label) else chr(ord("a") + index)
        ax.text(0.01, 0.99, label, transform=ax.transAxes, ha="left", va="top", fontweight="bold")
    fig.savefig(args.out, dpi=300)


if __name__ == "__main__":
    main()
