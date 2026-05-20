from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from text_layout import apply_axis_text, configure_text_defaults


configure_text_defaults()


def main() -> None:
    parser = argparse.ArgumentParser(description="Raincloud-style distribution plot template.")
    parser.add_argument("--csv", required=True)
    parser.add_argument("--group", required=True)
    parser.add_argument("--value", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    data = pd.read_csv(args.csv)
    groups = [str(item) for item in data[args.group].dropna().unique()]
    values = [data.loc[data[args.group].astype(str) == group, args.value].dropna().astype(float).to_numpy() for group in groups]
    positions = np.arange(1, len(groups) + 1)
    rng = np.random.default_rng(7)

    fig, ax = plt.subplots(figsize=(max(3.6, 0.72 * len(groups)), 3.2), constrained_layout=True)
    violins = ax.violinplot(values, positions=positions, widths=0.7, showmeans=False, showmedians=False, showextrema=False)
    for body in violins["bodies"]:
        body.set_facecolor("#56B4E9")
        body.set_edgecolor("none")
        body.set_alpha(0.35)
    ax.boxplot(values, positions=positions, widths=0.18, patch_artist=True, showfliers=False, boxprops={"facecolor": "white", "edgecolor": "black"}, medianprops={"color": "black"})
    for position, group_values in zip(positions, values):
        jitter = rng.normal(0, 0.045, size=len(group_values))
        ax.scatter(np.full(len(group_values), position) + jitter, group_values, s=12, alpha=0.65, color="#0072B2", edgecolors="none")
    ax.set_xticks(positions, groups)
    apply_axis_text(ax, xlabel=args.group, ylabel=args.value)
    fig.savefig(args.out, dpi=300, bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    main()
