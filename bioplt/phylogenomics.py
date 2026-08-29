"""Aligned phylogeny, metadata, and pangenome matrix figures."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Patch, Rectangle

from . import diagrams, theme


def phylogenomics_panel(
    edges: pd.DataFrame,
    metadata: pd.DataFrame,
    gene_matrix: pd.DataFrame,
) -> tuple[plt.Figure, dict[str, plt.Axes]]:
    """Align a branch-length tree with metadata and gene presence-absence.

    ``metadata`` requires ``taxon``, ``lineage``, ``habitat``, and
    ``genome_size_mb``. ``gene_matrix`` requires ``taxon`` followed by binary
    gene-family columns. Tip order is derived from tree topology and applied to
    every panel.
    """
    metadata_required = {"taxon", "lineage", "habitat", "genome_size_mb"}
    missing_metadata = sorted(metadata_required - set(metadata.columns))
    if missing_metadata:
        raise ValueError(f"Missing metadata columns: {', '.join(missing_metadata)}")
    if "taxon" not in gene_matrix.columns:
        raise ValueError("gene_matrix must contain a taxon column")

    layout = diagrams._build_tree_layout(edges)
    tips = layout["leaves"]
    if set(metadata["taxon"]) != set(tips):
        raise ValueError("metadata taxa must match tree tips exactly")
    if set(gene_matrix["taxon"]) != set(tips):
        raise ValueError("gene_matrix taxa must match tree tips exactly")

    metadata_indexed = metadata.set_index("taxon").loc[tips]
    genes_indexed = gene_matrix.set_index("taxon").loc[tips]
    if not np.isin(genes_indexed.to_numpy(), [0, 1]).all():
        raise ValueError("Gene-family columns must contain only 0 and 1")
    variable = genes_indexed.loc[:, genes_indexed.nunique() > 1]
    if variable.empty:
        raise ValueError("At least one variable gene family is required")

    fig = plt.figure(figsize=(14, 7.2))
    grid = GridSpec(1, 3, figure=fig, width_ratios=[2.6, 1.5, 4.2], wspace=0.08)
    ax_tree = fig.add_subplot(grid[0, 0])
    ax_meta = fig.add_subplot(grid[0, 1])
    ax_matrix = fig.add_subplot(grid[0, 2])

    diagrams.phylo_tree(edges, ax_tree, show_tip_labels=False)
    ax_tree.set_title("Core-genome phylogeny")

    lineage_values = sorted(metadata_indexed["lineage"].unique())
    habitat_values = sorted(metadata_indexed["habitat"].unique())
    lineage_colors = {value: theme.color_for(i) for i, value in enumerate(lineage_values)}
    habitat_colors = {
        value: theme.color_for(i + len(lineage_values)) for i, value in enumerate(habitat_values)
    }
    size_min = metadata_indexed["genome_size_mb"].min()
    size_range = metadata_indexed["genome_size_mb"].max() - size_min

    for y, taxon in enumerate(tips):
        row = metadata_indexed.loc[taxon]
        size_fraction = 0.5 if size_range == 0 else (row["genome_size_mb"] - size_min) / size_range
        colors = [
            lineage_colors[row["lineage"]],
            habitat_colors[row["habitat"]],
            plt.cm.Greys(0.25 + 0.65 * size_fraction),
        ]
        for x, color in enumerate(colors):
            ax_meta.add_patch(Rectangle((x - 0.43, y - 0.40), 0.86, 0.80, facecolor=color, edgecolor="white"))

    ax_meta.set_xlim(-0.5, 2.5)
    ax_meta.set_ylim(-0.6, len(tips) - 0.4)
    ax_meta.set_xticks([0, 1, 2], ["Lineage", "Habitat", "Genome size"], rotation=55, ha="right")
    ax_meta.set_yticks(range(len(tips)), [tip.replace("_", " ") for tip in tips], fontsize=9)
    ax_meta.tick_params(axis="y", length=0)
    ax_meta.set_title("Metadata")
    for spine in ax_meta.spines.values():
        spine.set_visible(False)

    ax_matrix.imshow(
        variable.to_numpy(),
        aspect="auto",
        interpolation="nearest",
        origin="lower",
        cmap=plt.matplotlib.colors.ListedColormap(["#F5F5F5", theme.color_for(0)]),
        vmin=0,
        vmax=1,
    )
    ax_matrix.set_ylim(-0.6, len(tips) - 0.4)
    ax_matrix.set_yticks([])
    ax_matrix.set_xticks([])
    ax_matrix.set_xlabel(f"{variable.shape[1]} variable gene families")
    ax_matrix.set_title("Accessory-gene matrix")

    legend_handles = [
        *[Patch(facecolor=color, label=value) for value, color in lineage_colors.items()],
        *[Patch(facecolor=color, label=value) for value, color in habitat_colors.items()],
        Patch(facecolor=theme.color_for(0), label="Gene present"),
        Patch(facecolor="#F5F5F5", edgecolor="#BBBBBB", label="Gene absent"),
    ]
    fig.legend(
        handles=legend_handles, loc="lower center", ncol=5, frameon=False, bbox_to_anchor=(0.58, 0.015)
    )
    fig.suptitle("Phylogeny-Aligned Pangenome Overview", fontsize=15, fontweight="bold", y=0.98)
    fig.subplots_adjust(bottom=0.22, top=0.88)
    return fig, {"tree": ax_tree, "metadata": ax_meta, "matrix": ax_matrix}
