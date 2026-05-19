from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import pandas as pd


plt.rcParams["svg.fonttype"] = "none"


def main() -> None:
    parser = argparse.ArgumentParser(description="Dose-response curve template.")
    parser.add_argument("--csv", required=True)
    parser.add_argument("--dose", required=True)
    parser.add_argument("--response", required=True)
    parser.add_argument("--group", default="")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    data = pd.read_csv(args.csv)
    fig, ax = plt.subplots(figsize=(4.2, 3.2), constrained_layout=True)
    if args.group and args.group in data:
        for group, group_data in data.groupby(args.group):
            ordered = group_data.sort_values(args.dose)
            ax.plot(ordered[args.dose], ordered[args.response], marker="o", linewidth=1.4, markersize=4, label=str(group))
        ax.legend(frameon=False, title=args.group)
    else:
        ordered = data.sort_values(args.dose)
        ax.plot(ordered[args.dose], ordered[args.response], marker="o", linewidth=1.4, markersize=4, color="#0072B2")
    ax.set_xscale("log" if (data[args.dose] > 0).all() else "linear")
    ax.set_xlabel(args.dose)
    ax.set_ylabel(args.response)
    fig.savefig(args.out, dpi=300, bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    main()
