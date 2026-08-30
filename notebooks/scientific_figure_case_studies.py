# %% [markdown]
# # Scientific Figure Engineering with Matplotlib
#
# These case studies use low-level Matplotlib layout, patches, coordinate
# systems, and shared axes to build figures that are difficult to express with
# a high-level statistical plotting call.

# %%
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, str(Path.cwd().parent))
from bioplt import genome_tracks, pangenome, phylogenomics, theme

theme.set_theme()
DATA = Path.cwd().parent / "data"

# %% [markdown]
# ## 1. Phylogeny-aligned pangenome overview
#
# Tip order comes from tree topology and is applied to metadata and gene-content
# panels. The tree root is the single node with no parent, branch lengths map to
# the horizontal axis, and accessory genes are displayed as a binary matrix.

# %%
edges = pd.read_csv(DATA / "phylo_edges.csv")
metadata = pd.read_csv(DATA / "phylo_metadata.csv")
gene_matrix = pd.read_csv(DATA / "phylo_gene_presence.csv")
fig, axes = phylogenomics.phylogenomics_panel(edges, metadata, gene_matrix)
plt.show()

# %% [markdown]
# ## 2. Pangenome accumulation and uncertainty
#
# Thin lines show individual resampling replicates. The strong line is the
# replicate mean, and the band is the empirical 2.5 to 97.5 percentile interval.
# This makes sampling sensitivity visible instead of presenting one genome order
# as definitive.

# %%
accumulation = pd.read_csv(DATA / "pangenome_accumulation.csv")
fig, axes = pangenome.accumulation_curves(accumulation)
plt.show()

# %% [markdown]
# ## 3. Gene neighborhoods and synteny
#
# Arrow direction encodes strand. Translucent polygons connect homologous genes
# between adjacent regions, and opacity represents sequence identity. The gray
# feature is a lineage-specific insertion rather than a failed match.

# %%
genes = pd.read_csv(DATA / "synteny_genes.csv")
links = pd.read_csv(DATA / "synteny_links.csv")
fig, ax = genome_tracks.synteny_plot(genes, links)
plt.show()
