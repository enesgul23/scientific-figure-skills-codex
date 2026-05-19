from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(description="Survival curve template from precomputed survival probabilities.")
    parser.add_argument("--csv", required=True)
    parser.add_argument("--time", required=True)
    parser.add_argument("--survival", required=True)
    parser.add_argument("--group")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    data = pd.read_csv(args.csv)
    fig, ax = plt.subplots(figsize=(4.2, 3.2), constrained_layout=True)
    if args.group:
        for name, group in data.groupby(args.group):
            ax.step(group[args.time], group[args.survival], where="post", label=str(name))
        ax.legend(frameon=False)
    else:
        ax.step(data[args.time], data[args.survival], where="post")
    ax.set_xlabel(args.time)
    ax.set_ylabel(args.survival)
    ax.set_ylim(0, 1.02)
    fig.savefig(args.out, dpi=300)


if __name__ == "__main__":
    main()
