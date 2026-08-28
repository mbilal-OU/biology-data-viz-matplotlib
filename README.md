# biology-data-viz-matplotlib

[![CI](https://github.com/mbilal-OU/biology-data-viz-matplotlib/actions/workflows/ci.yml/badge.svg)](https://github.com/mbilal-OU/biology-data-viz-matplotlib/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](pyproject.toml)
[![Matplotlib](https://img.shields.io/badge/matplotlib-%E2%89%A53.8-informational)](https://matplotlib.org)

**biology-data-viz-matplotlib** is a tested Matplotlib tutorial and
reusable plotting toolkit, focused specifically on techniques a
figure-level Seaborn call cannot do: 3D plots, animation, custom
multi-panel layouts, and manually drawn diagrams.
> **From a seeded simulation, to a tested plotting package, to a narrative notebook, to publication-ready figures, all checked in CI.**

![Pipeline](figures/workflow_diagram.svg)

**Jump to:** [Full tutorial (every plot, explained)](#full-tutorial-every-plot-explained) · [Quick start](#quick-start) · [Repository structure](#repository-structure) · [Reproducibility](#reproducibility)

---

## At a glance

This repo is the companion to
[biology-data-viz-seaborn](https://github.com/mbilal-OU/biology-data-viz-seaborn),
covering the techniques Seaborn does not: 3D visualization, animation,
custom GridSpec layouts, and diagrams drawn from primitive shapes.
Three datasets (docking scores, gene expression, sequencing QC) are
shared with that repo, so the same biological scenario can be compared
across both libraries side by side. Four datasets are new, chosen
because they specifically need a Matplotlib-only technique.

| You provide | This repo returns |
|---|---|
| nothing, just clone it | 7 simulated datasets with documented biological rationale |
| `python scripts/generate_datasets.py` | byte-identical, reproducible CSVs (seeded) |
| a dataset from `data/` | a tested `bioplt` function that plots it correctly-styled |
| the tutorial below (or the notebook) | biological question, why this needs raw Matplotlib, code, interpretation, and how to reuse it, for 7 techniques |
| `pytest tests/` | rendering checks and statistical/structural sanity checks against known ground truth |

It deliberately stays a **teaching and reference toolkit**, not a
general-purpose visualization library. Each tutorial section below
tells you exactly what column structure you need to point it at your
own DataFrame.

---

## Quick start

```bash
git clone https://github.com/mbilal-OU/biology-data-viz-matplotlib.git
cd biology-data-viz-matplotlib

python -m venv .venv && source .venv/bin/activate   # optional
pip install -r requirements.txt
pip install -e .
```

```bash
jupyter notebook notebooks/matplotlib_beginner_guide.ipynb
```

Conda users: `conda env create -f environment.yml && conda activate bioplt`.

---

## Full Tutorial: Every Plot, Explained

For each technique below: what it is for, the biological question it answers here, the exact code that produces it, an interpretation of the actual result, and what you'd need to use it on your own data. This mirrors `notebooks/matplotlib_beginner_guide.ipynb` exactly. Every snippet below is executed end-to-end in CI on every push.

```python
import pandas as pd
import matplotlib.pyplot as plt
from bioplt import theme, scatter3d, panels, animation, surface, diagrams

theme.set_theme()
```

---

### 1. 3D Scatter: Docking Landscape in Three Dimensions

**Plot type:** 3D scatter (mpl_toolkits.mplot3d)

**Dataset origin:** Shared with biology-data-viz-seaborn (same dataset, new dimension).

**What this technique is for:** Seaborn has no 3D plotting function at all. A true 3D scatter needs `mpl_toolkits.mplot3d`, accessed directly through Matplotlib's `Axes3D` projection, giving full control over elevation, azimuth, and three independent numeric axes at once.

**Biological question:** How do lipophilicity (logP), molecular weight, and docking score relate together across three drug targets? A 2D scatter has to pick two of these three variables. Does the third add anything?

**Dataset:** `data/docking_scores.csv`. 360 rows. Simulated virtual-screening results against 3 protein targets.

**Create this figure:**

```python
df = pd.read_csv("data/docking_scores.csv")
fig, ax = scatter3d.docking_scatter_3d(df)
```

![3D Scatter: Docking Landscape in Three Dimensions](figures/01_docking_3d.png)

**Interpretation:** The 3D view shows that molecular weight adds little extra separation beyond what logP already explains: the best-scoring points cluster in the same logP band regardless of molecular weight, meaning weight is not an independent driver of affinity in this simulated screen. That is itself a useful negative result, and it is easier to see in 3D than by eyeballing two separate 2D plots.

**Requirements to use this on your own data:**

- three continuous numeric columns (x, y, z)
- optionally: a categorical column to color and label groups

**Adapted code for your own DataFrame:**

```python
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.scatter(my_df["x"], my_df["y"], my_df["z"], c=my_df["group_codes"])
```

---

### 2. Small Multiples: One Panel Per Gene

**Plot type:** plt.subplots grid

**Dataset origin:** Shared with biology-data-viz-seaborn (same dataset, different layout).

**What this technique is for:** `plt.subplots` gives direct control over a grid of independent Axes, useful when each panel needs its own scale, title, or annotation rather than sharing one set of axes the way a faceted Seaborn plot would.

**Biological question:** Which genes shift between control and treatment, and by how much does each individual replicate move?

**Dataset:** `data/gene_expression.csv`. 180 rows. log2 expression for 6 genes, control vs. treatment, 15 replicates each.

**Create this figure:**

```python
df = pd.read_csv("data/gene_expression.csv")
fig, axes = panels.gene_expression_small_multiples(df)
```

![Small Multiples: One Panel Per Gene](figures/02_gene_expression_panels.png)

**Interpretation:** `MYC` and `IL6` show a clear upward shift with little overlap between conditions. `TP53` and `CDKN1A` shift down the same way. `GAPDH` and `ACTB` show heavily overlapping distributions, consistent with them being simulated as unaffected housekeeping genes. Plotting every replicate dot, not just a summary bar, makes clear these patterns hold across the whole replicate set.

**Requirements to use this on your own data:**

- a grouping column to split into panels (one Axes per group)
- one categorical x column and one continuous y column within each panel

**Adapted code for your own DataFrame:**

```python
groups = my_df["panel_column"].unique()
fig, axes = plt.subplots(nrows, ncols, figsize=(11, 3 * nrows))
for ax, group in zip(axes.ravel(), groups):
    sub = my_df[my_df["panel_column"] == group]
    ax.scatter(sub["x"], sub["y"])
    ax.set_title(group)
```

---

### 3. Custom Dashboard: Sequencing QC in One Figure

**Plot type:** GridSpec multi-panel dashboard

**Dataset origin:** Shared with biology-data-viz-seaborn (same dataset, different layout).

**What this technique is for:** `GridSpec` allows Axes of different sizes and aspect ratios to sit in one figure, for example a large scatter next to two small histograms next to a text panel, a layout no single Seaborn function produces.

**Biological question:** What is the overall health of a sequencing run: coverage, duplication, GC content, quality, and a quick summary all at a glance?

**Dataset:** `data/qc_metrics.csv`. 96 rows. Per-sample sequencing QC for a 96-sample batch across 3 sub-batches.

**Create this figure:**

```python
df = pd.read_csv("data/qc_metrics.csv")
fig = panels.qc_dashboard(df)
```

![Custom Dashboard: Sequencing QC in One Figure](figures/03_qc_dashboard.png)

**Interpretation:** The scatter panel shows the same coverage-versus-duplication artifact seen in the Seaborn version of this dataset (low coverage tracking with high duplication), while the dashboard format adds an at-a-glance numeric summary a reader could act on immediately, for example the exact count of samples below a 30x coverage threshold.

**Requirements to use this on your own data:**

- several numeric columns for the scatter and histograms
- a categorical column for the scatter's color grouping

**Adapted code for your own DataFrame:**

```python
fig = plt.figure(figsize=(11, 7))
gs = GridSpec(2, 3, figure=fig, width_ratios=[2, 1, 1])
ax_main = fig.add_subplot(gs[:, 0])
ax_hist1 = fig.add_subplot(gs[0, 1])
ax_hist2 = fig.add_subplot(gs[0, 2])
ax_text = fig.add_subplot(gs[1, 1:])
```

---

### 4. Animation: Bacterial Growth Curves Over Time

**Plot type:** FuncAnimation

**Dataset origin:** New dataset, no Seaborn equivalent at all.

**What this technique is for:** `FuncAnimation` is the only way to show a process unfolding over time rather than a single finished state. Each frame redraws the line data with one more timepoint revealed, so change over time is genuinely visible rather than implied.

**Biological question:** How do three bacterial strains differ in growth rate and lag phase as they grow toward carrying capacity?

**Dataset:** `data/growth_curves.csv`. 240 rows. OD600 growth curves for 3 strains over 24h, 4 replicates each, logistic growth model.

**Create this figure:**

```python
df = pd.read_csv("data/growth_curves.csv")
anim, fig = animation.growth_curve_animation(df, n_frames=40)
anim.save("growth_curves.gif", writer="pillow", fps=12)
```

![Animation: Bacterial Growth Curves Over Time](figures/04_growth_curves.gif)

**Interpretation:** `MutantA_fast` pulls ahead almost immediately and plateaus early at a lower final density. `MutantB_slow` has a visibly longer lag phase before it starts climbing, but ultimately reaches the highest carrying capacity of the three strains. Neither of those facts, an early speed and final yield trade-off, is obvious from endpoint data alone; the animation makes it visible as it happens.

**Requirements to use this on your own data:**

- an ordered x variable (usually time)
- one or more y series to animate, grouped by a category column
- install `pillow` to export as GIF, or use `writer="ffmpeg"` for MP4

**Adapted code for your own DataFrame:**

```python
fig, ax = plt.subplots()
(line,) = ax.plot([], [])

def update(frame):
    line.set_data(x[:frame], y[:frame])
    return [line]

anim = FuncAnimation(fig, update, frames=len(x))
anim.save("output.gif", writer="pillow", fps=12)
```

---

### 5. 3D Surface and Contour: Enzyme Activity Response Surface

**Plot type:** plot_surface + contourf

**Dataset origin:** New dataset, no Seaborn equivalent at all.

**What this technique is for:** A heatmap flattens a true 2D-input, 1D-output relationship onto a single flat color grid. `plot_surface` shows the actual shape of the response, including how sharply activity falls off away from the optimum in each direction, which is harder to judge by eye on a flat map.

**Biological question:** How does enzyme activity depend jointly on pH and temperature, and where is the optimum?

**Dataset:** `data/enzyme_activity_surface.csv`. 625 rows. Enzyme activity sampled on a 25x25 grid of pH and temperature.

**Create this figure:**

```python
df = pd.read_csv("data/enzyme_activity_surface.csv")
fig = surface.enzyme_activity_surface(df)
```

![3D Surface and Contour: Enzyme Activity Response Surface](figures/05_enzyme_surface.png)

**Interpretation:** The surface has a single, fairly narrow peak near pH 7.4 and 37C, consistent with a typical mesophilic enzyme operating near physiological conditions. The contour panel beside it marks that peak directly, and shows the surface is more sensitive to temperature than to pH: the contour lines are more tightly packed along the temperature axis, meaning a given temperature deviation costs more activity than the same-sized pH deviation.

**Requirements to use this on your own data:**

- two continuous independent variables sampled on a grid
- one continuous response variable
- pivot to a 2D grid first (`pivot_table`), then use `np.meshgrid`

**Adapted code for your own DataFrame:**

```python
piv = my_df.pivot_table(index="y_var", columns="x_var", values="z_var")
x_grid, y_grid = np.meshgrid(piv.columns, piv.index)
ax = fig.add_subplot(projection="3d")
ax.plot_surface(x_grid, y_grid, piv.to_numpy(), cmap="viridis")
```

---

### 6. Manually Drawn Diagram: Circular Plasmid Map

**Plot type:** Wedge patches, manual layout

**Dataset origin:** New dataset, no Seaborn equivalent at all.

**What this technique is for:** There is no Seaborn function for this at all. Drawing it requires placing `Wedge` patches at specific angles computed from base-pair positions, plus manual label and arrow placement: a diagram type built entirely from primitive shapes rather than a single plotting call.

**Biological question:** What does the gene layout of a small expression plasmid look like: which genes are present, where, and on which strand?

**Dataset:** `data/plasmid_map.csv`. 7 rows. A synthetic 5400bp expression plasmid's gene layout.

**Create this figure:**

```python
df = pd.read_csv("data/plasmid_map.csv")
fig, ax = diagrams.plasmid_map(df)
```

![Manually Drawn Diagram: Circular Plasmid Map](figures/06_plasmid_map.png)

**Interpretation:** The map lays out an origin of replication, two resistance markers, a reporter gene, and their associated promoters around the circle in their correct relative positions and strand orientations. This is the same kind of diagram produced by dedicated plasmid-mapping software, built here entirely from Matplotlib primitives.

**Requirements to use this on your own data:**

- gene name, start position, end position, and strand columns
- a total sequence length to convert positions into angles

**Adapted code for your own DataFrame:**

```python
from matplotlib.patches import Wedge

def bp_to_angle(bp, total_length):
    return 90 - (bp / total_length) * 360

for _, gene in my_df.iterrows():
    theta1 = bp_to_angle(gene["end_bp"], total_length)
    theta2 = bp_to_angle(gene["start_bp"], total_length)
    ax.add_patch(Wedge((0, 0), 1.0, theta1, theta2, width=0.15))
```

---

### 7. Manually Drawn Diagram: Phylogenetic Tree

**Plot type:** Line segments, manual layout algorithm

**Dataset origin:** New dataset, no Seaborn equivalent at all.

**What this technique is for:** Rather than calling a dendrogram function, this draws the tree from a plain parent-child-branch-length table using line segments, showing the layout algorithm itself: each node's horizontal position comes from cumulative branch length, and each internal node's vertical position from the mean of its children.

**Biological question:** What are the evolutionary relationships and relative divergence times among 8 taxa?

**Dataset:** `data/phylo_edges.csv`. 14 rows. A small phylogenetic tree for 8 taxa, encoded as parent-child edges.

**Create this figure:**

```python
df = pd.read_csv("data/phylo_edges.csv")
fig, ax = diagrams.phylo_tree(df)
```

![Manually Drawn Diagram: Phylogenetic Tree](figures/07_phylo_tree.png)

**Interpretation:** Taxon A and Taxon B are each other's closest relatives, joining at the shallowest branch length in the tree. Taxon C is the deepest-branching member of its clade, splitting off before the E/F/G/H group diversifies further. The x-axis position of each tip directly encodes cumulative evolutionary distance from the root, which is exactly what a phylogenetic tree diagram is meant to show.

**Requirements to use this on your own data:**

- a parent column, a child column, and a branch length column
- exactly one root node (present as a parent but never as a child)

**Adapted code for your own DataFrame:**

```python
# compute cumulative depth from root by walking the edge table,
# then for each parent-child pair draw an L-shaped connector:
ax.plot([x_parent, x_parent], [y_parent, y_child], color="black")
ax.plot([x_parent, x_child], [y_child, y_child], color="black")
```

---


## Using `bioplt` on your own data: general pattern

Every example above follows the same shape: read your CSV, call one
`bioplt` function, get back a Matplotlib `Figure`. To adapt any of
them:

```python
import pandas as pd
from bioplt import theme, surface   # or scatter3d / panels / animation / diagrams

theme.set_theme()

my_df = pd.read_csv("your_data.csv")
fig = surface.enzyme_activity_surface(my_df)   # works on any x/y/z grid data
fig.savefig("my_figure.png", dpi=300, bbox_inches="tight")
```

If your columns don't match the exact names `bioplt` expects, either
rename them (`my_df.rename(columns={...})`) before calling the
function, or use the "adapted code" snippet under each technique
above, which shows the raw Matplotlib calls with placeholder column
names you can swap in directly.

---

## Repository structure

```
biology-data-viz-matplotlib/
├── bioplt/                       # Reusable, tested plotting package
│   ├── theme.py                  #   consistent styling
│   ├── scatter3d.py              #   3D scatter plots
│   ├── panels.py                 #   plt.subplots grids and GridSpec dashboards
│   ├── animation.py              #   FuncAnimation
│   ├── surface.py                #   3D surface and contour plots
│   └── diagrams.py               #   manually drawn diagrams (plasmid map, tree)
├── data/
│   ├── *.csv                     # 7 simulated datasets
│   └── data_dictionary.md        # column definitions and simulation rationale
├── scripts/
│   ├── generate_datasets.py          # deterministic (seeded) data generation, with rationale docstrings
│   └── _build_readme_gallery.py      # generates the tutorial section of this README
├── notebooks/
│   ├── matplotlib_beginner_guide.py     # tutorial, authored as a Jupytext script
│   └── matplotlib_beginner_guide.ipynb  # executed notebook (source of truth for output)
├── figures/                      # publication-quality exported figures (300 DPI), one GIF, and workflow_diagram.svg
├── docs/
│   ├── index.md                  # docs home
│   └── gallery.md                # mirror of the tutorial below, as a standalone page
├── tests/
│   └── test_bioplt.py            # rendering smoke tests and statistical/structural sanity checks
├── .github/workflows/
│   └── ci.yml                    # lint, determinism check, tests, notebook execution
├── requirements.txt / environment.yml / pyproject.toml
├── CHANGELOG.md / CONTRIBUTING.md / CITATION.cff / LICENSE (MIT)
```

---

## Scope and guardrails

**This repo does:**
- simulate every dataset deterministically, with a documented
  biological and statistical rationale, not arbitrary numbers;
- ship plotting code as a tested, importable package rather than
  copy-paste notebook cells;
- verify quantitative and structural claims against the data's actual
  ground truth (for example, that the enzyme activity surface's peak
  lands near the simulated optimum), not just that a plot renders;
- re-execute the tutorial notebook in CI on every push, so committed
  output always matches the code;
- focus specifically on techniques that need raw Matplotlib, not
  reimplement what Seaborn already does well.

**This repo does not:**
- duplicate the Seaborn repository's coverage of standard 2D
  statistical plots. See
  [biology-data-viz-seaborn](https://github.com/mbilal-OU/biology-data-viz-seaborn)
  for scatter, line, box, violin, heatmap, and pairplot tutorials;
- ingest or validate real experimental data on your behalf. Data
  cleaning is out of scope; bring your own tidy DataFrame;
- cover interactive/web-based visualization (Plotly, Bokeh) or
  genome-browser-style tracks. This is a static-figure and
  local-animation tutorial.

---

## Reproducibility

- All data is generated deterministically (`np.random.default_rng(42)`);
  `python scripts/generate_datasets.py` regenerates byte-identical CSVs.
- CI regenerates the datasets on every push and diffs them against
  what's committed, so a silent nondeterminism bug fails the build.
- `pytest tests/ -v` runs 16 tests: rendering smoke tests for every
  plotting function, plus statistical and structural sanity checks
  (the enzyme surface peak lands near the simulated optimum, the
  phylogenetic tree has the correct leaf count and is fully connected,
  the plasmid genes stay within the plasmid length, growth curves
  plateau as expected).
- The notebook is executed end-to-end in CI (`ExecutePreprocessor`,
  180s timeout), so a broken cell fails the build, not just a local run.

```bash
pytest tests/ -v
```

---

## Documentation

- [Documentation home](docs/index.md)
- [Plot gallery (standalone page)](docs/gallery.md)
- [Data dictionary](data/data_dictionary.md)
- [Changelog](CHANGELOG.md)
- Companion repository: [biology-data-viz-seaborn](https://github.com/mbilal-OU/biology-data-viz-seaborn)

## Contributing

New techniques, datasets, and clearer explanations are welcome. See
[`CONTRIBUTING.md`](CONTRIBUTING.md) for dataset-generation conventions,
test requirements, and how to re-execute the notebook before a PR.

## Citation

Citation metadata is in [`CITATION.cff`](CITATION.cff). GitHub renders
a "Cite this repository" button automatically.

## License

[MIT](LICENSE)

## Tags

`matplotlib` · `python` · `bioinformatics` · `biology` · `data-visualization` · `animation` · `3d-plots` · `tutorial` · `reproducible-research`
