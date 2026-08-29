"""Pangenome accumulation figures with replicate-level uncertainty."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from . import theme


def _validate_accumulation(df: pd.DataFrame) -> None:
    required = {"replicate", "n_genomes", "pan_genes", "core_genes"}
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")
    if df.empty:
        raise ValueError("Input data must contain at least one row")
    numeric = df[["n_genomes", "pan_genes", "core_genes"]]
    if (numeric <= 0).any().any():
        raise ValueError("Genome and gene counts must be positive")
    if (df["core_genes"] > df["pan_genes"]).any():
        raise ValueError("core_genes cannot exceed pan_genes")


def summarize_accumulation(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize replicate accumulation curves by mean and 95% interval."""
    _validate_accumulation(df)
    rows = []
    for n_genomes, group in df.groupby("n_genomes", sort=True):
        rows.append(
            {
                "n_genomes": n_genomes,
                "pan_mean": group["pan_genes"].mean(),
                "pan_low": group["pan_genes"].quantile(0.025),
                "pan_high": group["pan_genes"].quantile(0.975),
                "core_mean": group["core_genes"].mean(),
                "core_low": group["core_genes"].quantile(0.025),
                "core_high": group["core_genes"].quantile(0.975),
            }
        )
    return pd.DataFrame(rows)


def accumulation_curves(df: pd.DataFrame) -> tuple[plt.Figure, np.ndarray]:
    """Plot pan- and core-genome curves with replicate and interval layers."""
    summary = summarize_accumulation(df)
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.8), sharex=True)
    specifications = [
        (axes[0], "pan_genes", "pan_mean", "pan_low", "pan_high", "Pan-genome", theme.color_for(0)),
        (axes[1], "core_genes", "core_mean", "core_low", "core_high", "Core genome", theme.color_for(1)),
    ]
    for ax, raw_col, mean_col, low_col, high_col, title, color in specifications:
        for _, replicate in df.groupby("replicate"):
            ax.plot(
                replicate["n_genomes"],
                replicate[raw_col],
                color=color,
                alpha=0.10,
                linewidth=0.8,
            )
        ax.fill_between(
            summary["n_genomes"],
            summary[low_col],
            summary[high_col],
            color=color,
            alpha=0.22,
            label="95% empirical interval",
        )
        ax.plot(
            summary["n_genomes"],
            summary[mean_col],
            color=color,
            linewidth=2.5,
            label="Replicate mean",
        )
        ax.set_title(title)
        ax.set_xlabel("Genomes sampled")
        ax.set_ylabel("Gene families")
        ax.legend(frameon=False)
    fig.suptitle("Pangenome Accumulation with Resampling Uncertainty", fontweight="bold")
    fig.tight_layout()
    return fig, axes
