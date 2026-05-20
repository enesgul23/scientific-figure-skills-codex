from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import pandas as pd

from text_layout import add_right_colorbar, configure_text_defaults


def main() -> None:
    parser = argparse.ArgumentParser(description="Matrix heatmap template.")
    parser.add_argument("--csv", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    configure_text_defaults()

    matrix = pd.read_csv(args.csv, index_col=0)
    fig, ax = plt.subplots(figsize=(4.5, 3.8), constrained_layout=True)
    image = ax.imshow(matrix.values, aspect="auto", cmap="viridis")
    ax.set_xticks(range(matrix.shape[1]), matrix.columns, rotation=90)
    ax.set_yticks(range(matrix.shape[0]), matrix.index)
    add_right_colorbar(fig, ax, image, label="Value")
    fig.savefig(args.out, dpi=300)


if __name__ == "__main__":
    main()
