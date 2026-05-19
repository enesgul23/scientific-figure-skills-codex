from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(description="Volcano plot template.")
    parser.add_argument("--csv", required=True)
    parser.add_argument("--log2fc", required=True)
    parser.add_argument("--pvalue", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    data = pd.read_csv(args.csv)
    y = -np.log10(data[args.pvalue].clip(lower=np.finfo(float).tiny))
    fig, ax = plt.subplots(figsize=(4.0, 3.2), constrained_layout=True)
    ax.scatter(data[args.log2fc], y, s=8, alpha=0.6, edgecolors="none")
    ax.axvline(0, color="0.5", linewidth=1)
    ax.set_xlabel(args.log2fc)
    ax.set_ylabel(f"-log10({args.pvalue})")
    fig.savefig(args.out, dpi=300)


if __name__ == "__main__":
    main()
