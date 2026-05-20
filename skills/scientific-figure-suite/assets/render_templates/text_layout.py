from __future__ import annotations

import textwrap
from typing import Any


def configure_text_defaults() -> None:
    import matplotlib.pyplot as plt

    plt.rcParams.update(
        {
            "svg.fonttype": "none",
            "font.size": 8,
            "axes.titlesize": 8,
            "axes.labelsize": 8,
            "xtick.labelsize": 7,
            "ytick.labelsize": 7,
            "legend.fontsize": 7,
            "legend.title_fontsize": 7,
        }
    )


def compact_label(value: str, max_chars: int = 48) -> str:
    text = str(value).strip().replace("_", " ")
    if len(text) <= max_chars:
        return text
    wrapped = textwrap.wrap(text, width=max_chars, break_long_words=False, break_on_hyphens=False)
    return "\n".join(wrapped[:2]) if wrapped else text[:max_chars]


def apply_axis_text(ax: Any, xlabel: str | None = None, ylabel: str | None = None, title: str | None = None) -> None:
    if xlabel:
        ax.set_xlabel(compact_label(xlabel), labelpad=4)
    if ylabel:
        ax.set_ylabel(compact_label(ylabel), labelpad=5)
    if title:
        ax.set_title(compact_label(title, max_chars=54), pad=6)


def add_right_colorbar(fig: Any, ax: Any, mappable: Any, label: str | None = None, shrink: float = 0.82) -> Any:
    colorbar = fig.colorbar(mappable, ax=ax, shrink=shrink, location="right", pad=0.025)
    if label:
        colorbar.set_label(compact_label(label, max_chars=30), labelpad=6)
    return colorbar
