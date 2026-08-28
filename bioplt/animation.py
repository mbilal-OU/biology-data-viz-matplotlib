"""Animation: something with no Seaborn equivalent at all."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.animation import FuncAnimation

from . import theme


def growth_curve_animation(df: pd.DataFrame, n_frames: int = 40) -> tuple[FuncAnimation, plt.Figure]:
    """Animate bacterial growth curves revealing one more timepoint per frame.

    Parameters
    ----------
    df : DataFrame with columns ``strain``, ``replicate``, ``time_h``, ``OD600``.
    n_frames : number of animation frames.

    Returns
    -------
    (anim, fig) : the FuncAnimation and its parent Figure. Save with
    ``anim.save("path.gif", writer="pillow", fps=12)``, then close
    ``fig`` when done.
    """
    strains = sorted(df["strain"].unique())
    means = (
        df.groupby(["strain", "time_h"])["OD600"]
        .mean()
        .reset_index()
        .pivot(index="time_h", columns="strain", values="OD600")
    )
    times = means.index.to_numpy()
    n_points = len(times)
    frame_indices = np.linspace(1, n_points, n_frames, dtype=int)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.set_xlim(times.min(), times.max())
    ax.set_ylim(0, means.to_numpy().max() * 1.1)
    ax.set_xlabel("Time (h)")
    ax.set_ylabel("OD600")
    ax.set_title("Bacterial Growth Curves")

    lines = {}
    for i, strain in enumerate(strains):
        (line,) = ax.plot([], [], color=theme.color_for(i), linewidth=2, label=strain)
        lines[strain] = line
    ax.legend(loc="upper left", frameon=False)

    def update(frame_num):
        cutoff = frame_indices[frame_num]
        for strain in strains:
            lines[strain].set_data(times[:cutoff], means[strain].to_numpy()[:cutoff])
        return list(lines.values())

    anim = FuncAnimation(fig, update, frames=n_frames, interval=80, blit=True)
    return anim, fig
