# Scientific Figure Engineering with Matplotlib

[![CI](https://github.com/mbilal-OU/biology-data-viz-matplotlib/actions/workflows/ci.yml/badge.svg)](https://github.com/mbilal-OU/biology-data-viz-matplotlib/actions/workflows/ci.yml)
[![Docs](https://github.com/mbilal-OU/biology-data-viz-matplotlib/actions/workflows/docs.yml/badge.svg)](https://github.com/mbilal-OU/biology-data-viz-matplotlib/actions/workflows/docs.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB)](pyproject.toml)
[![License: MIT](https://img.shields.io/badge/license-MIT-2E7D32)](LICENSE)

A tested portfolio of custom scientific figures for biology, genomics, and
bioinformatics. It focuses on the work below a high-level plotting call:
coordinate systems, topology-aware layouts, patches, shared axes, GridSpec,
animation, vector export, validation, and reproducible figure construction.

All included datasets are seeded simulations with documented structure. They
exist to test figure behavior and do not represent experimental evidence.

## Flagship case studies

### Phylogeny-aligned pangenome overview

![Aligned phylogeny, metadata, and pangenome matrix](figures/08_phylogenomics_panel.png)

The rectangular phylogram is rooted from the edge table and scaled by cumulative
branch length. Tree topology determines tip order, which is then applied to the
metadata tracks and binary gene matrix. Input validation rejects negative branch
lengths, repeated children, multiple roots, disconnected nodes, mismatched taxa,
and non-binary gene values.

### Pangenome accumulation with uncertainty

![Pan and core genome accumulation curves](figures/09_pangenome_accumulation.png)

Thin lines preserve individual resampling replicates. Strong lines report the
replicate mean, and shaded regions report empirical 95% intervals. This avoids
presenting one genome order as a definitive accumulation trajectory.

### Gene neighborhoods and synteny

![Directional genes and homology links](figures/10_synteny_tracks.png)

Gene arrows encode strand direction. Translucent polygons connect homologous
features between adjacent genomes, with opacity mapped to identity. Insertions,
inversions, missing genes, coordinate scale, and functional families remain
visible in one compact figure.

## Demonstrated capabilities

| Figure-engineering task | Implementation | Biological example |
|---|---|---|
| Align heterogeneous panels | Shared topology-derived y coordinates and GridSpec | Phylogeny, metadata, pangenome |
| Display sampling uncertainty | Replicate layers, mean curve, empirical interval | Pan/core accumulation |
| Draw directional features | `FancyArrow`, `Polygon`, explicit coordinates | Gene neighborhoods and synteny |
| Construct circular diagrams | Wedges, tangent arrows, functional legend | Plasmid map |
| Build dashboards | Nested GridSpec and summary text | Sequencing QC |
| Compare many groups | Small multiples with controlled axes | Gene expression |
| Show a response surface | 3D surface paired with a 2D contour | Enzyme activity |
| Animate temporal data | `FuncAnimation` with deterministic frames | Bacterial growth |
| Inspect three continuous axes | 3D scatter plus documented 2D tradeoff | Docking landscape |

The repository also covers annotation, z-order, clipping, legends, colorbars,
accessible colors, raster and vector export, reusable APIs, and semantic tests.

## Quick start

```bash
git clone https://github.com/mbilal-OU/biology-data-viz-matplotlib.git
cd biology-data-viz-matplotlib
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install -e .
jupyter lab
```

Windows instructions are available in [`docs/setup.md`](docs/setup.md). Start
with
[`notebooks/scientific_figure_case_studies.ipynb`](notebooks/scientific_figure_case_studies.ipynb).
The original technique-by-technique notebook remains available at
[`notebooks/matplotlib_beginner_guide.ipynb`](notebooks/matplotlib_beginner_guide.ipynb).

## Reusable API

```python
import pandas as pd
from bioplt import phylogenomics, theme

theme.set_theme()

edges = pd.read_csv("data/phylo_edges.csv")
metadata = pd.read_csv("data/phylo_metadata.csv")
genes = pd.read_csv("data/phylo_gene_presence.csv")

fig, axes = phylogenomics.phylogenomics_panel(edges, metadata, genes)
theme.savefig(fig, "phylogenomics.svg")
```

Synteny is built from explicit gene and link tables:

```python
from bioplt import genome_tracks

features = pd.read_csv("data/synteny_genes.csv")
links = pd.read_csv("data/synteny_links.csv")
fig, ax = genome_tracks.synteny_plot(features, links)
```

## Scientific and visual guardrails

- A phylogenetic root is inferred only when exactly one parentless node exists.
- Branch length controls horizontal distance; rectangular placement does not
  imply time unless the input tree is time calibrated.
- Tip order follows topology, not alphabetical sorting.
- Accumulation bands describe resampling sensitivity, not model-based confidence
  unless a model is explicitly fitted.
- 3D graphics are paired with or compared against 2D views because perspective
  and occlusion can reduce quantitative readability.
- Homology links encode supplied relationships; the plotting function does not
  infer orthology or synteny.

## Reproducibility and quality checks

```bash
python scripts/generate_datasets.py
python scripts/build_advanced_gallery.py
pytest -q
ruff check bioplt scripts tests
mkdocs build --strict
```

Continuous integration checks deterministic data generation, semantic and
rendering tests, at least 95% package coverage, notebook execution, strict
documentation links, linting, and package construction. The theme supports
300-DPI PNG and TIFF plus vector SVG and PDF output with editable text.

## Repository map

```text
bioplt/       reusable low-level scientific figure components
data/         deterministic figure inputs and data dictionary
figures/      rendered raster, vector, and animated gallery
notebooks/    narrative core and advanced case studies
scripts/      deterministic data and gallery builders
tests/        rendering, geometry, schema, and biological sanity checks
docs/         documentation site source
```

## Scope

This repository demonstrates custom static and animated scientific figures.
Statistical visualization, Seaborn semantics, differential-expression displays,
ordination, and compositional-data examples are covered in the companion
[biology-data-viz-seaborn](https://github.com/mbilal-OU/biology-data-viz-seaborn)
repository.

## Citation and license

Citation metadata are provided in [`CITATION.cff`](CITATION.cff). The code is
released under the [MIT License](LICENSE).
