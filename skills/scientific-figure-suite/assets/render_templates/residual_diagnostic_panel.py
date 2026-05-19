from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(description="Residual diagnostic panel template.")
    parser.add_argument("--csv", required=True)
    parser.add_argument("--fitted", required=True)
    parser.add_argument("--residual", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    data = pd.read_csv(args.csv)
    fig, axes = plt.subplots(1, 2, figsize=(6.8, 3.0), constrained_layout=True)
    axes[0].scatter(data[args.fitted], data[args.residual], s=14, alpha=0.7)
    axes[0].axhline(0, color="black", linewidth=1)
    axes[0].set_xlabel(args.fitted)
    axes[0].set_ylabel(args.residual)
    axes[1].hist(data[args.residual].dropna(), bins=30, color="#4c78a8")
    axes[1].set_xlabel(args.residual)
    axes[1].set_ylabel("Count")
    fig.savefig(args.out, dpi=300)


if __name__ == "__main__":
    main()
