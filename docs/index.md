# Scientific Figure Engineering with Matplotlib

`bioplt` is a tested collection of low-level Matplotlib components for biology,
genomics, and bioinformatics. It demonstrates how to construct figures whose
layout or geometry must encode scientific structure directly.

## Start here

- [Gallery](gallery.md): ten rendered examples and their design rationale
- [Methods and interpretation](methods.md): transformations, encodings, and limits
- [Setup](setup.md): reproducible installation and validation
- [Data dictionary](https://github.com/mbilal-OU/biology-data-viz-matplotlib/blob/main/data/data_dictionary.md): every generated column
- [Advanced notebook](https://github.com/mbilal-OU/biology-data-viz-matplotlib/blob/main/notebooks/scientific_figure_case_studies.ipynb): three genomics case studies

## What this repository demonstrates

| Capability | Implementation | Example |
|---|---|---|
| Topology-aware alignment | Shared y coordinates from a validated tree | Phylogenomics panel |
| Resampling uncertainty | Replicates, means, empirical intervals | Pangenome accumulation |
| Feature geometry | Directional arrows and link polygons | Synteny tracks |
| Custom coordinates | Wedges and tangent arrows | Plasmid map |
| Multi-panel composition | Nested `GridSpec` | Sequencing QC dashboard |
| Three-dimensional views | `mplot3d` plus 2D tradeoff notes | Docking and enzyme activity |
| Time-dependent output | Deterministic `FuncAnimation` frames | Growth curves |

## Quality contract

Every public plotting function validates its required schema. Continuous
integration regenerates all seeded data, executes both notebooks, renders the
gallery, builds the package and documentation, and enforces at least 95% test
coverage across Python 3.10, 3.12, and 3.14.

The included data are simulations for testing and teaching. They are not
experimental evidence.
