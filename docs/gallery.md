# Plot Gallery

Every figure in this repository, shown next to the exact `bioplt` call that produced it. All code below is copy-pasteable, and it matches [`notebooks/matplotlib_beginner_guide.ipynb`](../notebooks/matplotlib_beginner_guide.ipynb) exactly, which is executed end-to-end in CI, so these snippets are guaranteed to run.

```python
import pandas as pd
import matplotlib.pyplot as plt
from bioplt import theme, scatter3d, panels, animation, surface, diagrams

theme.set_theme()
DATA = "data"
```

---

## 1 . 3D Scatter: Docking Landscape in Three Dimensions

**3D scatter (mpl_toolkits.mplot3d).** Shared with biology-data-viz-seaborn (same dataset, new dimension).

**Question:** How do lipophilicity (logP), molecular weight, and docking score relate together across three drug targets? A 2D scatter has to pick two of these three variables. Does the third add anything?

```python
df = pd.read_csv(f"{DATA}/docking_scores.csv")
fig, ax = scatter3d.docking_scatter_3d(df)
```

![3D Scatter: Docking Landscape in Three Dimensions](../figures/01_docking_3d.png)

The 3D view shows that molecular weight adds little extra separation beyond what logP already explains: the best-scoring points cluster in the same logP band regardless of molecular weight, meaning weight is not an independent driver of affinity in this simulated screen. That is itself a useful negative result, and it is easier to see in 3D than by eyeballing two separate 2D plots.

---

## 2 . Small Multiples: One Panel Per Gene

**plt.subplots grid.** Shared with biology-data-viz-seaborn (same dataset, different layout).

**Question:** Which genes shift between control and treatment, and by how much does each individual replicate move?

```python
df = pd.read_csv(f"{DATA}/gene_expression.csv")
fig, axes = panels.gene_expression_small_multiples(df)
```

![Small Multiples: One Panel Per Gene](../figures/02_gene_expression_panels.png)

`MYC` and `IL6` show a clear upward shift with little overlap between conditions. `TP53` and `CDKN1A` shift down the same way. `GAPDH` and `ACTB` show heavily overlapping distributions, consistent with them being simulated as unaffected housekeeping genes. Plotting every replicate dot, not just a summary bar, makes clear these patterns hold across the whole replicate set.

---

## 3 . Custom Dashboard: Sequencing QC in One Figure

**GridSpec multi-panel dashboard.** Shared with biology-data-viz-seaborn (same dataset, different layout).

**Question:** What is the overall health of a sequencing run: coverage, duplication, GC content, quality, and a quick summary all at a glance?

```python
df = pd.read_csv(f"{DATA}/qc_metrics.csv")
fig = panels.qc_dashboard(df)
```

![Custom Dashboard: Sequencing QC in One Figure](../figures/03_qc_dashboard.png)

The scatter panel shows the same coverage-versus-duplication artifact seen in the Seaborn version of this dataset (low coverage tracking with high duplication), while the dashboard format adds an at-a-glance numeric summary a reader could act on immediately, for example the exact count of samples below a 30x coverage threshold.

---

## 4 . Animation: Bacterial Growth Curves Over Time

**FuncAnimation.** New dataset, no Seaborn equivalent at all.

**Question:** How do three bacterial strains differ in growth rate and lag phase as they grow toward carrying capacity?

```python
df = pd.read_csv(f"{DATA}/growth_curves.csv")
anim, fig = animation.growth_curve_animation(df, n_frames=40)
anim.save("growth_curves.gif", writer="pillow", fps=12)
```

![Animation: Bacterial Growth Curves Over Time](../figures/04_growth_curves.gif)

`MutantA_fast` pulls ahead almost immediately and plateaus early at a lower final density. `MutantB_slow` has a visibly longer lag phase before it starts climbing, but ultimately reaches the highest carrying capacity of the three strains. Neither of those facts, an early speed and final yield trade-off, is obvious from endpoint data alone; the animation makes it visible as it happens.

---

## 5 . 3D Surface and Contour: Enzyme Activity Response Surface

**plot_surface + contourf.** New dataset, no Seaborn equivalent at all.

**Question:** How does enzyme activity depend jointly on pH and temperature, and where is the optimum?

```python
df = pd.read_csv(f"{DATA}/enzyme_activity_surface.csv")
fig = surface.enzyme_activity_surface(df)
```

![3D Surface and Contour: Enzyme Activity Response Surface](../figures/05_enzyme_surface.png)

The surface has a single, fairly narrow peak near pH 7.4 and 37C, consistent with a typical mesophilic enzyme operating near physiological conditions. The contour panel beside it marks that peak directly, and shows the surface is more sensitive to temperature than to pH: the contour lines are more tightly packed along the temperature axis, meaning a given temperature deviation costs more activity than the same-sized pH deviation.

---

## 6 . Manually Drawn Diagram: Circular Plasmid Map

**Wedge patches, manual layout.** New dataset, no Seaborn equivalent at all.

**Question:** What does the gene layout of a small expression plasmid look like: which genes are present, where, and on which strand?

```python
df = pd.read_csv(f"{DATA}/plasmid_map.csv")
fig, ax = diagrams.plasmid_map(df)
```

![Manually Drawn Diagram: Circular Plasmid Map](../figures/06_plasmid_map.png)

The map lays out an origin of replication, two resistance markers, a reporter gene, and their associated promoters around the circle in their correct relative positions and strand orientations. This is the same kind of diagram produced by dedicated plasmid-mapping software, built here entirely from Matplotlib primitives.

---

## 7 . Manually Drawn Diagram: Phylogenetic Tree

**Line segments, manual layout algorithm.** New dataset, no Seaborn equivalent at all.

**Question:** What are the evolutionary relationships and relative divergence times among 8 taxa?

```python
df = pd.read_csv(f"{DATA}/phylo_edges.csv")
fig, ax = diagrams.phylo_tree(df)
```

![Manually Drawn Diagram: Phylogenetic Tree](../figures/07_phylo_tree.png)

Taxon A and Taxon B are each other's closest relatives, joining at the shallowest branch length in the tree. Taxon C is the deepest-branching member of its clade, splitting off before the E/F/G/H group diversifies further. The x-axis position of each tip directly encodes cumulative evolutionary distance from the root, which is exactly what a phylogenetic tree diagram is meant to show.

---

**Regenerate every figure above from scratch:**

```bash
python scripts/generate_datasets.py
jupyter nbconvert --to notebook --execute --inplace notebooks/matplotlib_beginner_guide.ipynb
```
