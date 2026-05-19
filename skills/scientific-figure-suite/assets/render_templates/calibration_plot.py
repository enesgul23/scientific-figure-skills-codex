from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(description="Calibration curve template from binned predictions.")
    parser.add_argument("--csv", required=True)
    parser.add_argument("--expected", required=True)
    parser.add_argument("--observed", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    data = pd.read_csv(args.csv)
    fig, ax = plt.subplots(figsize=(3.6, 3.0), constrained_layout=True)
    ax.plot(data[args.expected], data[args.observed], marker="o", linewidth=1.5)
    ax.plot([0, 1], [0, 1], color="black", linewidth=1, linestyle="--")
    ax.set_xlabel(args.expected)
    ax.set_ylabel(args.observed)
    fig.savefig(args.out, dpi=300)


if __name__ == "__main__":
    main()
