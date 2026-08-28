# %% [markdown]
# # Biology Data Visualization with Matplotlib
#
# A tutorial focused on what Matplotlib can do that a figure-level
# Seaborn call cannot: 3D plots, animation, custom multi-panel
# layouts, and manually drawn diagrams. Three datasets (docking
# scores, gene expression, sequencing QC) are shared with the
# companion Seaborn repo, biology-data-viz-seaborn, so the same
# biological scenario can be compared across both libraries. Four
# datasets are new, chosen specifically because they need a
# Matplotlib-only technique.
#
# Each section follows the same structure: biological question, why
# this technique needs raw Matplotlib, code, and interpretation.

# %%
import sys
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path.cwd().parent))
from bioplt import theme, scatter3d, panels, animation, surface, diagrams

theme.set_theme()
DATA = Path.cwd().parent / "data"
FIGS = Path.cwd().parent / "figures"
FIGS.mkdir(exist_ok=True)

# %% [markdown]
# ## 1. 3D Scatter: Docking Landscape in Three Dimensions
#
# **Biological question:** How do lipophilicity (logP), molecular
# weight, and docking score relate together across three drug targets?
# A 2D scatter (as used in the Seaborn version of this dataset) has to
# pick two of these three variables; does the third add anything?
#
# **Why this needs raw Matplotlib:** Seaborn has no 3D plotting
# function. A true 3D scatter needs `mpl_toolkits.mplot3d`, accessed
# directly through Matplotlib's `Axes3D` projection.

# %%
df_dock = pd.read_csv(DATA / "docking_scores.csv")
fig, ax = scatter3d.docking_scatter_3d(df_dock)
theme.savefig(fig, FIGS / "01_docking_3d.png")
plt.show()

# %% [markdown]
# **Interpretation:** The 3D view shows that molecular weight adds
# little extra separation beyond what logP already explains: the
# best-scoring points cluster in the same logP band regardless of
# molecular weight, meaning weight is not an independent driver of
# affinity in this simulated screen. That is itself a useful negative
# result, and it's a conclusion that's easier to see in 3D than by
# eyeballing two separate 2D plots.

# %% [markdown]
# ## 2. Small Multiples: One Panel Per Gene
#
# **Biological question:** Which genes shift between control and
# treatment, and by how much does each individual replicate move?
#
# **Why this needs raw Matplotlib:** `plt.subplots` gives direct
# control over a grid of independent Axes, useful when each panel
# needs its own scale or annotation rather than sharing one set of
# axes like a faceted Seaborn plot would.

# %%
df_expr = pd.read_csv(DATA / "gene_expression.csv")
fig, axes = panels.gene_expression_small_multiples(df_expr)
theme.savefig(fig, FIGS / "02_gene_expression_panels.png")
plt.show()

# %% [markdown]
# **Interpretation:** `MYC` and `IL6` show a clear upward shift with
# little overlap between conditions. `TP53` and `CDKN1A` shift down
# the same way. `GAPDH` and `ACTB` show heavily overlapping
# distributions, consistent with them being simulated as unaffected
# housekeeping genes. The individual replicate dots (not just a
# summary bar) make it clear these patterns hold across the whole
# replicate set, not just the mean.

# %% [markdown]
# ## 3. Custom Dashboard: Sequencing QC in One Figure
#
# **Biological question:** What's the overall health of a sequencing
# run: coverage, duplication, GC content, quality, and a quick summary
# all at a glance?
#
# **Why this needs raw Matplotlib:** `GridSpec` allows Axes of
# different sizes and aspect ratios to sit in one figure (a large
# scatter next to two small histograms next to a text panel), a layout
# no single Seaborn function produces.

# %%
df_qc = pd.read_csv(DATA / "qc_metrics.csv")
fig = panels.qc_dashboard(df_qc)
theme.savefig(fig, FIGS / "03_qc_dashboard.png")
plt.show()

# %% [markdown]
# **Interpretation:** The scatter panel again shows the
# coverage-versus-duplication artifact seen in the Seaborn version of
# this dataset (low coverage tracking with high duplication), while
# the dashboard format adds an at-a-glance numeric summary that a
# reader could act on immediately, for example flagging the exact
# count of samples below a 30x coverage threshold.

# %% [markdown]
# ## 4. Animation: Bacterial Growth Curves Over Time
#
# **Biological question:** How do three bacterial strains differ in
# growth rate and lag phase as they grow toward carrying capacity?
#
# **Why this needs raw Matplotlib:** `FuncAnimation` is the only way
# to show a process unfolding over time rather than a single finished
# state. Watching the curves race apart frame by frame makes the lag
# phase and growth-rate differences far more immediate than reading a
# static endpoint plot.

# %%
df_growth = pd.read_csv(DATA / "growth_curves.csv")
anim, anim_fig = animation.growth_curve_animation(df_growth, n_frames=40)
anim.save(FIGS / "04_growth_curves.gif", writer="pillow", fps=12)
plt.close(anim_fig)
print("saved figures/04_growth_curves.gif")

# %% [markdown]
# **Interpretation:** `MutantA_fast` pulls ahead almost immediately
# and plateaus early at a lower final density. `MutantB_slow` has a
# visibly longer lag phase before it starts climbing, but ultimately
# reaches the highest carrying capacity of the three strains. Neither
# of those two facts (early speed versus final yield being different
# strains) is obvious from endpoint data alone; the animation makes
# the trade-off visible as it happens.

# %% [markdown]
# ## 5. 3D Surface and Contour: Enzyme Activity Response Surface
#
# **Biological question:** How does enzyme activity depend jointly on
# pH and temperature, and where is the optimum?
#
# **Why this needs raw Matplotlib:** A heatmap (the Seaborn approach)
# flattens a true 2D-input, 1D-output relationship onto a single 2D
# color grid. `plot_surface` shows the actual shape of the response,
# including how sharply activity falls off away from the optimum in
# each direction, which a flat heatmap makes harder to judge by eye.

# %%
df_surf = pd.read_csv(DATA / "enzyme_activity_surface.csv")
fig = surface.enzyme_activity_surface(df_surf)
theme.savefig(fig, FIGS / "05_enzyme_surface.png")
plt.show()

# %%
peak = df_surf.loc[df_surf["activity_pct"].idxmax()]
print(peak)

# %% [markdown]
# **Interpretation:** The surface has a single, fairly narrow peak
# near pH 7.4 and 37C, consistent with a typical mesophilic enzyme
# operating near physiological conditions. The contour panel beside it
# marks that peak directly, and shows the surface is more sensitive to
# temperature than to pH: the contour lines are more tightly packed
# along the temperature axis, meaning a given deviation in temperature
# costs more activity than the same-sized deviation in pH.

# %% [markdown]
# ## 6. Manually Drawn Diagram: Circular Plasmid Map
#
# **Biological question:** What does the gene layout of a small
# expression plasmid look like: which genes are present, where, and on
# which strand?
#
# **Why this needs raw Matplotlib:** There is no Seaborn function for
# this at all. Drawing it requires placing `Wedge` patches at specific
# angles computed from base-pair positions, plus manual label and
# arrow placement, a diagram type that has to be built from primitive
# shapes.

# %%
df_plasmid = pd.read_csv(DATA / "plasmid_map.csv")
fig, ax = diagrams.plasmid_map(df_plasmid)
theme.savefig(fig, FIGS / "06_plasmid_map.png")
plt.show()

# %% [markdown]
# **Interpretation:** The map lays out an origin of replication, two
# resistance markers, a reporter, and their associated promoters
# around the circle in their correct relative positions and strand
# orientations. This is the same kind of diagram produced by dedicated
# plasmid-mapping software (e.g. SnapGene), built here entirely from
# Matplotlib primitives.

# %% [markdown]
# ## 7. Manually Drawn Diagram: Phylogenetic Tree
#
# **Biological question:** What are the evolutionary relationships and
# relative divergence times among 8 taxa?
#
# **Why this needs raw Matplotlib:** Rather than calling a dendrogram
# function (as SciPy or Seaborn's clustermap would), this draws the
# tree from a plain parent-child-branch-length table using line
# segments, to show the layout algorithm itself: computing each node's
# horizontal position from cumulative branch length, and each internal
# node's vertical position from the mean of its children.

# %%
df_tree = pd.read_csv(DATA / "phylo_edges.csv")
fig, ax = diagrams.phylo_tree(df_tree)
theme.savefig(fig, FIGS / "07_phylo_tree.png")
plt.show()

# %% [markdown]
# **Interpretation:** Taxon A and Taxon B are each other's closest
# relatives, joining at the shallowest branch length in the tree.
# Taxon C is the deepest-branching member of its clade, splitting off
# before the E/F/G/H group diversifies further. The x-axis position of
# each tip directly encodes cumulative evolutionary distance from the
# root, which is exactly what a phylogenetic tree diagram is meant to
# show.

# %% [markdown]
# ## Summary
#
# | # | Technique | Dataset | Shared with Seaborn repo | Why Matplotlib only |
# |---|-----------|---------|---------------------------|----------------------|
# | 1 | 3D scatter | docking_scores | yes | no 3D in Seaborn |
# | 2 | Small multiples | gene_expression | yes | direct subplot grid control |
# | 3 | GridSpec dashboard | qc_metrics | yes | mixed panel sizes in one figure |
# | 4 | Animation | growth_curves | no, new | shows change over time |
# | 5 | 3D surface + contour | enzyme_activity_surface | no, new | true 2D-input response surface |
# | 6 | Manual diagram | plasmid_map | no, new | no equivalent plotting function |
# | 7 | Manual diagram | phylo_edges | no, new | manual layout algorithm |
#
# Next steps: see `CONTRIBUTING.md` to add a new technique or dataset,
# or explore `bioplt/` directly to reuse these functions in your own
# analysis. For the Seaborn-based version of the shared datasets, see
# the companion repository, biology-data-viz-seaborn.
