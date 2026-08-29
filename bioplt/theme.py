"""Consistent visual theme used across every figure in this repository."""

from __future__ import annotations

import matplotlib.pyplot as plt

CATEGORY_COLORS = {
    0: "#0072B2",
    1: "#D55E00",
    2: "#009E73",
    3: "#CC79A7",
    4: "#E69F00",
    5: "#56B4E9",
    6: "#F0E442",
    7: "#000000",
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
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
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


def savefig(fig: plt.Figure, path: str, *, transparent: bool = False) -> None:
    """Save a figure with tight bounds in raster or vector formats."""
    fig.savefig(path, dpi=DPI_SAVE, bbox_inches="tight", transparent=transparent)
