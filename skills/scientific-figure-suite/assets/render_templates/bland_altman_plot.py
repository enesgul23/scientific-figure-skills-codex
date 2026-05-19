from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import pandas as pd


plt.rcParams["svg.fonttype"] = "none"


def main() -> None:
    parser = argparse.ArgumentParser(description="Bland-Altman agreement plot template.")
    parser.add_argument("--csv", required=True)
    parser.add_argument("--method-a", required=True)
    parser.add_argument("--method-b", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    data = pd.read_csv(args.csv)
    mean_value = (data[args.method_a] + data[args.method_b]) / 2.0
    difference = data[args.method_b] - data[args.method_a]
    bias = float(difference.mean())
    sd = float(difference.std(ddof=1))
    upper = bias + 1.96 * sd
    lower = bias - 1.96 * sd

    fig, ax = plt.subplots(figsize=(4.0, 3.2), constrained_layout=True)
    ax.scatter(mean_value, difference, s=20, color="#0072B2", alpha=0.75, edgecolors="none")
    ax.axhline(bias, color="black", linewidth=1.2, label="Bias")
    ax.axhline(upper, color="#D55E00", linewidth=1, linestyle="--", label="95% limits")
    ax.axhline(lower, color="#D55E00", linewidth=1, linestyle="--")
    ax.set_xlabel("Mean of methods")
    ax.set_ylabel("Difference between methods")
    ax.legend(frameon=False, loc="best")
    fig.savefig(args.out, dpi=300, bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    main()
