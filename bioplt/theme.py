"""Consistent visual theme used across every figure in this repository."""

from __future__ import annotations

import matplotlib.pyplot as plt

CATEGORY_COLORS = {
    0: "#4C72B0",
    1: "#DD8452",
    2: "#55A868",
    3: "#C44E52",
    4: "#8172B2",
    5: "#937860",
}
SEQUENTIAL_CMAP = "viridis"
DIVERGING_CMAP = "vlag"
FIGSIZE_DEFAULT = (7, 5)
DPI_SAVE = 300


def set_theme() -> None:
    """Apply the repository-wide Matplotlib theme.

    Call this once at the top of a notebook or script before plotting.
    """
    plt.rcParams.update(
        {
            "figure.figsize": FIGSIZE_DEFAULT,
            "figure.dpi": 100,
            "savefig.dpi": DPI_SAVE,
            "savefig.bbox": "tight",
            "axes.titleweight": "bold",
            "axes.titlesize": 13,
            "axes.labelsize": 11,
            "axes.grid": True,
            "grid.alpha": 0.3,
            "axes.axisbelow": True,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "font.size": 10.5,
        }
    )


def color_for(index: int) -> str:
    """Return a themed color for the given category index, cycling if needed."""
    return CATEGORY_COLORS[index % len(CATEGORY_COLORS)]


def savefig(fig: plt.Figure, path: str) -> None:
    """Save a figure at publication resolution with a tight bounding box."""
    fig.savefig(path, dpi=DPI_SAVE, bbox_inches="tight")
