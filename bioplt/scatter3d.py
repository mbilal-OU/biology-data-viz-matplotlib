"""3D plots: something Seaborn has no direct equivalent for."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from . import theme


def docking_scatter_3d(df: pd.DataFrame) -> tuple[plt.Figure, plt.Axes]:
    """3D scatter of logP, molecular weight, and docking score, by target.

    Parameters
    ----------
    df : DataFrame with columns ``logP``, ``molecular_weight``,
        ``vina_score``, ``target``.
    """
    fig = plt.figure(figsize=(8, 6.5))
    ax = fig.add_subplot(111, projection="3d")

    targets = df["target"].unique()
    for i, target in enumerate(targets):
        sub = df[df["target"] == target]
        ax.scatter(
            sub["logP"],
            sub["molecular_weight"],
            sub["vina_score"],
            label=target,
            color=theme.color_for(i),
            alpha=0.7,
            s=30,
        )

    ax.set_xlabel("logP")
    ax.set_ylabel("Molecular weight (Da)")
    ax.set_zlabel("Vina score (kcal/mol)")
    ax.set_title("Docking Landscape in 3D: logP x MW x Binding Score")
    ax.invert_zaxis()
    ax.legend(loc="upper left", bbox_to_anchor=(1.05, 1.0), frameon=False)
    ax.view_init(elev=20, azim=-60)
    return fig, ax
