"""3D surface and contour plots: showing a full 2D response surface."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from . import theme


def enzyme_activity_surface(df: pd.DataFrame) -> plt.Figure:
    """3D surface plot and matching 2D contour of enzyme activity vs. pH
    and temperature, side by side.

    Parameters
    ----------
    df : DataFrame with columns ``pH``, ``temperature_C``, ``activity_pct``.
    """
    piv = df.pivot_table(index="temperature_C", columns="pH", values="activity_pct")
    ph_vals = piv.columns.to_numpy()
    temp_vals = piv.index.to_numpy()
    ph_grid, temp_grid = np.meshgrid(ph_vals, temp_vals)
    activity_grid = piv.to_numpy()

    fig = plt.figure(figsize=(13, 5.5))

    ax3d = fig.add_subplot(1, 2, 1, projection="3d")
    surf = ax3d.plot_surface(
        ph_grid,
        temp_grid,
        activity_grid,
        cmap=theme.SEQUENTIAL_CMAP,
        linewidth=0,
        antialiased=True,
        alpha=0.95,
    )
    ax3d.set_xlabel("pH")
    ax3d.set_ylabel("Temperature (C)")
    ax3d.set_zlabel("Activity (%)")
    ax3d.set_title("Enzyme Activity Surface")
    ax3d.view_init(elev=25, azim=-55)
    fig.colorbar(surf, ax=ax3d, shrink=0.6, label="Activity (%)")

    ax2d = fig.add_subplot(1, 2, 2)
    contour = ax2d.contourf(ph_grid, temp_grid, activity_grid, levels=20, cmap=theme.SEQUENTIAL_CMAP)
    ax2d.set_xlabel("pH")
    ax2d.set_ylabel("Temperature (C)")
    ax2d.set_title("Same Surface, Top-Down View")
    fig.colorbar(contour, ax=ax2d, label="Activity (%)")

    peak_idx = np.unravel_index(np.argmax(activity_grid), activity_grid.shape)
    ax2d.scatter(
        ph_grid[peak_idx],
        temp_grid[peak_idx],
        color="white",
        edgecolor="black",
        s=80,
        zorder=5,
        marker="*",
    )

    fig.tight_layout()
    return fig
