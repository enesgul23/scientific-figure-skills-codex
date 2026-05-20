from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import pandas as pd

from text_layout import apply_axis_text, configure_text_defaults


def main() -> None:
    parser = argparse.ArgumentParser(description="Forest plot template.")
    parser.add_argument("--csv", required=True)
    parser.add_argument("--label", required=True)
    parser.add_argument("--estimate", required=True)
    parser.add_argument("--lower", required=True)
    parser.add_argument("--upper", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    configure_text_defaults()

    data = pd.read_csv(args.csv).iloc[::-1].reset_index(drop=True)
    y = range(len(data))
    fig, ax = plt.subplots(figsize=(4.5, max(2.2, 0.32 * len(data))), constrained_layout=True)
    ax.errorbar(
        data[args.estimate],
        y,
        xerr=[data[args.estimate] - data[args.lower], data[args.upper] - data[args.estimate]],
        fmt="o",
        color="black",
        ecolor="black",
        capsize=2,
    )
    ax.axvline(1, color="0.5", linewidth=1, linestyle="--")
    ax.set_yticks(list(y), data[args.label])
    apply_axis_text(ax, xlabel=args.estimate)
    fig.savefig(args.out, dpi=300)


if __name__ == "__main__":
    main()
