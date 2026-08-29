"""Build the advanced scientific figures used in the portfolio gallery."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from bioplt import genome_tracks, pangenome, phylogenomics, theme

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
FIGURES = ROOT / "figures"


def save_both(fig: plt.Figure, stem: str) -> None:
    theme.savefig(fig, FIGURES / f"{stem}.png")
    theme.savefig(fig, FIGURES / f"{stem}.svg")


def main() -> None:
    theme.set_theme()
    FIGURES.mkdir(exist_ok=True)

    edges = pd.read_csv(DATA / "phylo_edges.csv")
    metadata = pd.read_csv(DATA / "phylo_metadata.csv")
    gene_matrix = pd.read_csv(DATA / "phylo_gene_presence.csv")
    fig, _ = phylogenomics.phylogenomics_panel(edges, metadata, gene_matrix)
    save_both(fig, "08_phylogenomics_panel")
    plt.close(fig)

    accumulation = pd.read_csv(DATA / "pangenome_accumulation.csv")
    fig, _ = pangenome.accumulation_curves(accumulation)
    save_both(fig, "09_pangenome_accumulation")
    plt.close(fig)

    genes = pd.read_csv(DATA / "synteny_genes.csv")
    links = pd.read_csv(DATA / "synteny_links.csv")
    fig, _ = genome_tracks.synteny_plot(genes, links)
    save_both(fig, "10_synteny_tracks")
    plt.close(fig)


if __name__ == "__main__":
    main()
