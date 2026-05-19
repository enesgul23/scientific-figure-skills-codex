from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


plt.rcParams["svg.fonttype"] = "none"


def curve_points(labels: np.ndarray, scores: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    thresholds = np.r_[np.inf, np.sort(np.unique(scores))[::-1], -np.inf]
    tpr: list[float] = []
    fpr: list[float] = []
    precision: list[float] = []
    recall: list[float] = []
    positives = max(float((labels == 1).sum()), 1.0)
    negatives = max(float((labels == 0).sum()), 1.0)
    for threshold in thresholds:
        predicted = scores >= threshold
        tp = float(((predicted == 1) & (labels == 1)).sum())
        fp = float(((predicted == 1) & (labels == 0)).sum())
        fn = float(((predicted == 0) & (labels == 1)).sum())
        tpr.append(tp / positives)
        fpr.append(fp / negatives)
        precision.append(tp / max(tp + fp, 1.0))
        recall.append(tp / max(tp + fn, 1.0))
    return np.asarray(fpr), np.asarray(tpr), np.asarray(recall), np.asarray(precision)


def main() -> None:
    parser = argparse.ArgumentParser(description="ROC and precision-recall curve template.")
    parser.add_argument("--csv", required=True)
    parser.add_argument("--y-true", required=True)
    parser.add_argument("--score", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    data = pd.read_csv(args.csv)
    labels = data[args.y_true].astype(int).to_numpy()
    scores = data[args.score].astype(float).to_numpy()
    fpr, tpr, recall, precision = curve_points(labels, scores)
    order = np.argsort(fpr)
    trapezoid = getattr(np, "trapezoid", None) or np.trapz
    roc_auc = float(trapezoid(tpr[order], fpr[order]))

    fig, axes = plt.subplots(1, 2, figsize=(6.4, 3.1), constrained_layout=True)
    axes[0].plot(fpr, tpr, color="#0072B2", linewidth=1.6)
    axes[0].plot([0, 1], [0, 1], color="0.65", linewidth=1, linestyle="--")
    axes[0].set_xlabel("False positive rate")
    axes[0].set_ylabel("True positive rate")
    axes[0].set_title(f"ROC AUC = {roc_auc:.2f}")
    axes[0].set_xlim(0, 1)
    axes[0].set_ylim(0, 1)

    axes[1].plot(recall, precision, color="#D55E00", linewidth=1.6)
    axes[1].set_xlabel("Recall")
    axes[1].set_ylabel("Precision")
    axes[1].set_title("Precision-recall")
    axes[1].set_xlim(0, 1)
    axes[1].set_ylim(0, 1)
    fig.savefig(args.out, dpi=300, bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    main()
