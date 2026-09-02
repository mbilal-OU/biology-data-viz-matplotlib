# Matplotlib figure tutorials for genomics

These tutorials focus on the reason to use low-level Matplotlib, the required
data, the exact constructor, adaptation to personal data, and a defensible
interpretation. All bundled data are seeded simulations.

```python
import pandas as pd
from bioplt import animation, diagrams, genome_tracks, panels, pangenome, phylogenomics, scatter3d, surface, theme

theme.set_theme()
```

## 01 3D docking landscape

- **Use when:** three continuous attributes must be inspected together and an
  interactive rotation is not required in the final output.
- **Inputs and code:** [`docking_scores.csv`](../data/docking_scores.csv) and
  [`scatter3d.docking_scatter_3d`](../bioplt/scatter3d.py).
- **Use your own data:** pass a DataFrame containing the documented docking
  score, lipophilicity, molecular-weight, and target columns. Update labels if
  your variables differ.
- **Interpret:** look for group overlap, gradients, and occlusion. Docking score
  is a computational ranking, not measured affinity. Confirm any apparent 3D
  separation in 2D projections.

## 02 Gene-expression panels

- **Use when:** identical group comparisons across several genes need aligned
  axes and consistent panel geometry.
- **Inputs and code:** [`gene_expression.csv`](../data/gene_expression.csv) and
  [`panels.gene_expression_small_multiples`](../bioplt/panels.py).
- **Use your own data:** keep one row per biological replicate with explicit gene,
  condition, and value columns. Pass the DataFrame to the constructor.
- **Interpret:** compare within-gene group location and variation. Do not infer
  differential expression from visual separation alone.

## 03 Sequencing-QC dashboard

- **Use when:** related library metrics and review thresholds should be combined
  in one compact diagnostic page.
- **Inputs and code:** [`qc_metrics.csv`](../data/qc_metrics.csv) and
  [`panels.qc_dashboard`](../bioplt/panels.py).
- **Use your own data:** provide one row per library using the data dictionary.
  Change thresholds to match the assay, instrument, and downstream analysis.
- **Interpret:** identify samples and metric combinations requiring review.
  Dashboard flags are not automatic exclusion decisions.

## 04 Animated growth curves

- **Use when:** the order in which time-course trajectories emerge is the main
  communication goal.
- **Inputs and code:** [`growth_curves.csv`](../data/growth_curves.csv) and
  [`animation.growth_curve_animation`](../bioplt/animation.py).
- **Use your own data:** supply time, replicate, condition, and response columns,
  then save the returned animation with a supported writer.
- **Interpret:** stable axes permit honest frame-to-frame comparison. Animation
  supports communication but should be accompanied by a static figure for exact
  values and accessibility.

## 05 Enzyme-response surface

- **Use when:** a response depends jointly on two continuous experimental
  variables and both a surface and contour view are useful.
- **Inputs and code:** [`enzyme_activity_surface.csv`](../data/enzyme_activity_surface.csv)
  and [`surface.enzyme_activity_surface`](../bioplt/surface.py).
- **Use your own data:** provide a complete or suitably interpolated grid with
  the two predictors and response. Document any interpolation or smoothing.
- **Interpret:** peaks identify observed or interpolated response regions, not
  necessarily a causal optimum outside the sampled grid.

## 06 Circular plasmid map

- **Use when:** annotated genomic features, strands, and coordinates should be
  displayed around a circular molecule.
- **Inputs and code:** [`plasmid_map.csv`](../data/plasmid_map.csv) and
  [`diagrams.plasmid_map`](../bioplt/diagrams.py).
- **Use your own data:** provide feature start, end, strand, label, and function,
  plus the true plasmid length. Validate wrapped features at the origin.
- **Interpret:** the map displays supplied annotation. It does not infer gene
  function, operons, replication origin, or circularity.

## 07 Phylogenetic tree

- **Use when:** custom branch geometry and metadata styling must be controlled
  directly with Matplotlib Artists.
- **Inputs and code:** [`phylo_edges.csv`](../data/phylo_edges.csv),
  [`phylo_metadata.csv`](../data/phylo_metadata.csv), and
  [`diagrams.phylo_tree`](../bioplt/diagrams.py).
- **Use your own data:** export a rooted edge table with consistent node IDs,
  branch lengths, and tip metadata. The validator requires one root.
- **Interpret:** topology and lengths come from upstream inference. Horizontal
  distance is time only for a valid time-calibrated tree.

## 08 Phylogeny-aligned pangenome

- **Use when:** a tree, sample annotations, and a gene presence-absence matrix
  must share exact tip order.
- **Inputs and code:** [`phylo_edges.csv`](../data/phylo_edges.csv),
  [`phylo_metadata.csv`](../data/phylo_metadata.csv),
  [`phylo_gene_presence.csv`](../data/phylo_gene_presence.csv), and
  [`phylogenomics.phylogenomics_panel`](../bioplt/phylogenomics.py).
- **Use your own data:** ensure every tree tip appears exactly once in metadata
  and the binary matrix. Join by stable identifiers, never incidental row order.
- **Interpret:** aligned patterns show where supplied gene calls occur on the
  tree. They do not establish gain, loss, or horizontal transfer without an
  explicit evolutionary model.

## 09 Pangenome accumulation

- **Use when:** pan and core gene-family counts should be summarized across many
  randomized genome-addition orders.
- **Inputs and code:** [`pangenome_accumulation.csv`](../data/pangenome_accumulation.csv)
  and [`pangenome.accumulation_curves`](../bioplt/pangenome.py).
- **Use your own data:** retain replicate-level permutation results with genome
  count, order ID, pan count, and core count. Do not provide only one order.
- **Interpret:** bands show resampling sensitivity. Curve shape alone does not
  establish an open or closed pangenome.

## 10 Synteny and gene neighborhoods

- **Use when:** directional gene tracks and supplied homology links must be
  compared across genomes.
- **Inputs and code:** [`synteny_genes.csv`](../data/synteny_genes.csv),
  [`synteny_links.csv`](../data/synteny_links.csv), and
  [`genome_tracks.synteny_plot`](../bioplt/genome_tracks.py).
- **Use your own data:** export genome, start, end, strand, family, and label for
  features, plus explicit source-target homology links. Use consistent coordinate
  conventions.
- **Interpret:** conserved order and orientation support a synteny description.
  The plotting code does not infer orthology, rearrangements, or transfer.

## Reproduce the gallery

```bash
python scripts/generate_datasets.py
python scripts/build_advanced_gallery.py
pytest -q
```

See the [data dictionary](../data/data_dictionary.md) for exact columns.
