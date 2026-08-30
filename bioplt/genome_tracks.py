"""Directional genome tracks and synteny links using Matplotlib patches."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import FancyArrow, Patch, Polygon


def synteny_plot(genes: pd.DataFrame, links: pd.DataFrame) -> tuple[plt.Figure, plt.Axes]:
    """Draw aligned gene arrows and homology links for multiple genomes."""
    gene_required = {"genome", "gene", "family", "start_bp", "end_bp", "strand", "color"}
    link_required = {"source_genome", "source_gene", "target_genome", "target_gene", "identity"}
    missing_genes = sorted(gene_required - set(genes.columns))
    missing_links = sorted(link_required - set(links.columns))
    if missing_genes:
        raise ValueError(f"Missing gene columns: {', '.join(missing_genes)}")
    if missing_links:
        raise ValueError(f"Missing link columns: {', '.join(missing_links)}")
    if genes.empty:
        raise ValueError("genes must contain at least one feature")
    if not genes["strand"].isin(["+", "-"]).all():
        raise ValueError("strand must contain only '+' and '-'")
    if (genes["end_bp"] <= genes["start_bp"]).any():
        raise ValueError("Each end_bp must be greater than start_bp")
    if not links["identity"].between(0, 100).all():
        raise ValueError("identity must be between 0 and 100")

    genome_order = list(dict.fromkeys(genes["genome"]))
    y_positions = {genome: len(genome_order) - index - 1 for index, genome in enumerate(genome_order)}
    indexed = genes.set_index(["genome", "gene"], drop=False)
    max_bp = float(genes["end_bp"].max())
    fig, ax = plt.subplots(figsize=(13, 5.8))

    for link in links.itertuples(index=False):
        source_key = (link.source_genome, link.source_gene)
        target_key = (link.target_genome, link.target_gene)
        if source_key not in indexed.index or target_key not in indexed.index:
            raise ValueError(f"Link references an unknown gene: {source_key} -> {target_key}")
        source = indexed.loc[source_key]
        target = indexed.loc[target_key]
        source_y = y_positions[link.source_genome]
        target_y = y_positions[link.target_genome]
        polygon = Polygon(
            [
                (source["start_bp"] / 1000, source_y - 0.20),
                (source["end_bp"] / 1000, source_y - 0.20),
                (target["end_bp"] / 1000, target_y + 0.20),
                (target["start_bp"] / 1000, target_y + 0.20),
            ],
            closed=True,
            facecolor="#7A7A7A",
            edgecolor="none",
            alpha=0.08 + 0.34 * (link.identity / 100),
            zorder=1,
        )
        ax.add_patch(polygon)

    for genome in genome_order:
        y = y_positions[genome]
        ax.hlines(y, 0, max_bp / 1000, color="#777777", linewidth=1, zorder=2)
        for row in genes[genes["genome"] == genome].itertuples(index=False):
            start = row.start_bp / 1000
            length = (row.end_bp - row.start_bp) / 1000
            x = start if row.strand == "+" else row.end_bp / 1000
            dx = length if row.strand == "+" else -length
            head_length = min(max(length * 0.22, 0.08), 0.32)
            ax.add_patch(
                FancyArrow(
                    x,
                    y,
                    dx,
                    0,
                    width=0.30,
                    head_width=0.45,
                    head_length=head_length,
                    length_includes_head=True,
                    facecolor=row.color,
                    edgecolor="white",
                    linewidth=0.8,
                    zorder=3,
                )
            )
            if length >= 0.45:
                ax.text(start + length / 2, y + 0.32, row.gene, ha="center", va="bottom", fontsize=8)

    ax.set_yticks([y_positions[value] for value in genome_order], genome_order)
    ax.set_ylim(-0.75, len(genome_order) - 0.25)
    ax.set_xlim(-0.1, max_bp / 1000 + 0.2)
    ax.set_xlabel("Genomic coordinate (kb)")
    ax.set_title("Conserved Gene Neighborhood and Synteny")
    unique_families = genes.drop_duplicates("family")[["family", "color"]]
    handles = [
        Patch(facecolor=color, edgecolor="white", label=family)
        for family, color in unique_families.itertuples(index=False)
    ]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=5, frameon=False)
    ax.grid(axis="x", alpha=0.2)
    ax.grid(axis="y", visible=False)
    fig.tight_layout()
    return fig, ax
