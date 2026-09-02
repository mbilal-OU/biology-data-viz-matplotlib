# Figure Gallery

All figures are generated from versioned CSV inputs and reusable functions in
`bioplt`. PNG files support fast review; the advanced static figures are also
exported as editable SVG.

## Advanced genomics case studies

### Phylogeny-aligned pangenome overview

![Phylogeny-aligned pangenome overview](https://raw.githubusercontent.com/mbilal-OU/matplotlib-genomic-figures/main/figures/08_phylogenomics_panel.png)

Tree topology determines tip order across the phylogram, metadata tracks, and
binary accessory-gene matrix. Horizontal branch length is preserved.

```python
fig, axes = phylogenomics.phylogenomics_panel(edges, metadata, gene_matrix)
```

### Pangenome accumulation

![Pangenome accumulation](https://raw.githubusercontent.com/mbilal-OU/matplotlib-genomic-figures/main/figures/09_pangenome_accumulation.png)

Individual resampling trajectories remain visible beneath their means and
empirical 95% intervals.

```python
fig, axes = pangenome.accumulation_curves(accumulation)
```

### Gene neighborhoods and synteny

![Synteny tracks](https://raw.githubusercontent.com/mbilal-OU/matplotlib-genomic-figures/main/figures/10_synteny_tracks.png)

Arrow direction encodes strand; link opacity encodes supplied sequence identity.

```python
fig, ax = genome_tracks.synteny_plot(genes, links)
```

## Core technique gallery

| Figure | Technique | Scientific use |
|---|---|---|
| [Docking landscape](https://raw.githubusercontent.com/mbilal-OU/matplotlib-genomic-figures/main/figures/01_docking_3d.png) | 3D scatter | Inspect three continuous variables |
| [Gene expression](https://raw.githubusercontent.com/mbilal-OU/matplotlib-genomic-figures/main/figures/02_gene_expression_panels.png) | Small multiples | Preserve replicate-level distributions |
| [Sequencing QC](https://raw.githubusercontent.com/mbilal-OU/matplotlib-genomic-figures/main/figures/03_qc_dashboard.png) | `GridSpec` dashboard | Combine diagnostics and summary text |
| [Growth curves](https://raw.githubusercontent.com/mbilal-OU/matplotlib-genomic-figures/main/figures/04_growth_curves.gif) | Animation | Reveal temporal divergence |
| [Enzyme response](https://raw.githubusercontent.com/mbilal-OU/matplotlib-genomic-figures/main/figures/05_enzyme_surface.png) | Surface plus contour | Locate a joint optimum |
| [Plasmid map](https://raw.githubusercontent.com/mbilal-OU/matplotlib-genomic-figures/main/figures/06_plasmid_map.png) | Patches and polar geometry | Show coordinates and strand |
| [Phylogenetic tree](https://raw.githubusercontent.com/mbilal-OU/matplotlib-genomic-figures/main/figures/07_phylo_tree.png) | Validated tree layout | Preserve topology and branch length |

## Regenerate the gallery

```bash
python scripts/generate_datasets.py
python scripts/_build_readme_gallery.py
python scripts/build_advanced_gallery.py
```

See [Methods and interpretation](methods.md) before treating any encoding as a
biological inference.
