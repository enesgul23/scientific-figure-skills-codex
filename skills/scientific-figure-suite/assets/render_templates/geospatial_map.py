from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import pandas as pd

from text_layout import add_right_colorbar, apply_axis_text, configure_text_defaults


def main() -> None:
    parser = argparse.ArgumentParser(description="Point-based geospatial map template.")
    parser.add_argument("--csv", required=True)
    parser.add_argument("--lon", required=True)
    parser.add_argument("--lat", required=True)
    parser.add_argument("--value")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    configure_text_defaults()

    data = pd.read_csv(args.csv)
    fig, ax = plt.subplots(figsize=(4.2, 3.8), constrained_layout=True)
    color = data[args.value] if args.value else "#4c78a8"
    points = ax.scatter(data[args.lon], data[args.lat], c=color, s=18, alpha=0.85)
    if args.value:
        add_right_colorbar(fig, ax, points, label=args.value)
    apply_axis_text(ax, xlabel=args.lon, ylabel=args.lat)
    ax.set_aspect("equal", adjustable="datalim")
    fig.savefig(args.out, dpi=300)


if __name__ == "__main__":
    main()
