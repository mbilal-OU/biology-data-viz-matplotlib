"""Custom multi-panel layouts: plt.subplots grids and GridSpec dashboards."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.gridspec import GridSpec

from . import theme


def _jitter(n: int, spread: float = 0.08):
    rng = np.random.default_rng(0)
    return rng.uniform(-spread, spread, n)


def gene_expression_small_multiples(df: pd.DataFrame) -> tuple[plt.Figure, np.ndarray]:
    """One small Axes per gene, each showing control vs. treatment replicates.

    Parameters
    ----------
    df : DataFrame with columns ``gene``, ``condition``, ``replicate``,
        ``expression``.
    """
    genes = sorted(df["gene"].unique())
    n = len(genes)
    ncols = 3
    nrows = -(-n // ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(11, 3.2 * nrows), sharey=False)
    axes = np.atleast_1d(axes).ravel()

    for i, gene in enumerate(genes):
        ax = axes[i]
        sub = df[df["gene"] == gene]
        for j, condition in enumerate(["control", "treatment"]):
            vals = sub[sub["condition"] == condition]["expression"]
            x = np.full(len(vals), j) + _jitter(len(vals))
            ax.scatter(x, vals, color=theme.color_for(j), alpha=0.7, s=18)
            ax.scatter([j], [vals.mean()], color="black", marker="_", s=200, zorder=5)
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["control", "treatment"], fontsize=9)
        ax.set_title(gene, fontsize=11)
        ax.set_xlim(-0.5, 1.5)

    for k in range(n, len(axes)):
        axes[k].axis("off")

    fig.suptitle("Gene Expression, One Panel Per Gene", fontweight="bold", y=1.02)
    fig.tight_layout()
    return fig, axes


def qc_dashboard(df: pd.DataFrame) -> plt.Figure:
    """A single-figure QC dashboard: scatter, two histograms, and a text
    summary panel, laid out with GridSpec.

    Parameters
    ----------
    df : DataFrame with columns ``coverage_mean``, ``duplicates_pct``,
        ``gc_content``, ``q30_pct``, ``batch``.
    """
    fig = plt.figure(figsize=(11, 7))
    gs = GridSpec(2, 3, figure=fig, width_ratios=[2, 1, 1], height_ratios=[1, 1])

    ax_main = fig.add_subplot(gs[:, 0])
    for i, batch in enumerate(sorted(df["batch"].unique())):
        sub = df[df["batch"] == batch]
        ax_main.scatter(
            sub["coverage_mean"], sub["duplicates_pct"],
            color=theme.color_for(i), alpha=0.7, s=25, label=batch,
        )
    ax_main.set_xlabel("Mean coverage (X)")
    ax_main.set_ylabel("PCR duplicates (%)")
    ax_main.set_title("Coverage vs. Duplication")
    ax_main.legend(frameon=False, fontsize=9)

    ax_hist1 = fig.add_subplot(gs[0, 1])
    ax_hist1.hist(df["gc_content"], bins=15, color=theme.color_for(2), edgecolor="white")
    ax_hist1.set_title("GC content", fontsize=10)

    ax_hist2 = fig.add_subplot(gs[0, 2])
    ax_hist2.hist(df["q30_pct"], bins=15, color=theme.color_for(3), edgecolor="white")
    ax_hist2.set_title("Q30 %", fontsize=10)

    ax_text = fig.add_subplot(gs[1, 1:])
    ax_text.axis("off")
    n_low_cov = (df["coverage_mean"] < 30).sum()
    summary = (
        f"n = {len(df)} samples\n"
        f"batches: {df['batch'].nunique()}\n"
        f"mean coverage: {df['coverage_mean'].mean():.1f}x\n"
        f"samples below 30x: {n_low_cov}\n"
        f"mean duplication: {df['duplicates_pct'].mean():.1f}%"
    )
    ax_text.text(0.0, 0.9, "Run Summary", fontsize=12, fontweight="bold", va="top")
    ax_text.text(0.0, 0.65, summary, fontsize=10, va="top", family="monospace")

    fig.suptitle("Sequencing Run QC Dashboard", fontweight="bold", y=0.98)
    fig.tight_layout()
    return fig
