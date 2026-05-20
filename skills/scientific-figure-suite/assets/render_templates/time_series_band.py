from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from text_layout import apply_axis_text, configure_text_defaults


configure_text_defaults()


def main() -> None:
    parser = argparse.ArgumentParser(description="Time-series line with optional uncertainty band template.")
    parser.add_argument("--csv", required=True)
    parser.add_argument("--time", required=True)
    parser.add_argument("--value", required=True)
    parser.add_argument("--lower", default="")
    parser.add_argument("--upper", default="")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    data = pd.read_csv(args.csv)
    parsed_time = pd.to_datetime(data[args.time], errors="coerce")
    if parsed_time.isna().any():
        x = np.arange(len(data))
    else:
        x = parsed_time.to_numpy()
    fig, ax = plt.subplots(figsize=(5.2, 3.0), constrained_layout=True)
    if args.lower and args.upper and args.lower in data and args.upper in data:
        ax.fill_between(x, data[args.lower].astype(float).to_numpy(), data[args.upper].astype(float).to_numpy(), color="#56B4E9", alpha=0.25, linewidth=0)
    ax.plot(x, data[args.value].astype(float).to_numpy(), color="#0072B2", linewidth=1.6)
    apply_axis_text(ax, xlabel=args.time, ylabel=args.value)
    fig.autofmt_xdate(rotation=30, ha="right")
    fig.savefig(args.out, dpi=300, bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    main()
