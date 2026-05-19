from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(description="Observed-vs-predicted parity scatter template.")
    parser.add_argument("--csv", required=True)
    parser.add_argument("--observed", required=True)
    parser.add_argument("--predicted", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    data = pd.read_csv(args.csv)
    fig, ax = plt.subplots(figsize=(3.5, 3.5), constrained_layout=True)
    ax.scatter(data[args.observed], data[args.predicted], s=18, alpha=0.75, edgecolors="none")
    lower = min(data[args.observed].min(), data[args.predicted].min())
    upper = max(data[args.observed].max(), data[args.predicted].max())
    ax.plot([lower, upper], [lower, upper], color="black", linewidth=1)
    ax.set_xlabel(args.observed)
    ax.set_ylabel(args.predicted)
    ax.set_aspect("equal", adjustable="box")
    fig.savefig(args.out, dpi=300)


if __name__ == "__main__":
    main()
