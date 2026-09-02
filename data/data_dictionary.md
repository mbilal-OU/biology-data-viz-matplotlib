# Data Dictionary

All datasets in this repository are simulated (not real experimental
data) using [`scripts/generate_datasets.py`](../scripts/generate_datasets.py),
with a fixed random seed (`np.random.default_rng(42)`) so results are
exactly reproducible. Three datasets use the same generation logic as
the companion Seaborn repository, seaborn-biological-statistics, so the
same biological scenario can be compared across both libraries. Nine
additional tables support low-level Matplotlib techniques and advanced
genomics case studies.

---

### `docking_scores.csv` (360 rows), shared with seaborn-biological-statistics
Simulated virtual-screening results against 3 protein targets.

| Column | Type | Description |
|---|---|---|
| `target` | str | Protein target (`Kinase_A`, `Protease_B`, `GPCR_C`) |
| `ligand_id` | str | Unique ligand identifier |
| `logP` | float | Simulated lipophilicity |
| `molecular_weight` | float | Simulated molecular weight (Da) |
| `ring_count` | int | Number of ring systems |
| `vina_score` | float | Docking score, kcal/mol (more negative means stronger binding) |

Used here for a 3D scatter plot (logP, molecular weight, vina score).
The 3D view is treated as exploratory and paired with a discussion of
its perspective and occlusion tradeoffs.

### `gene_expression.csv` (180 rows), shared with seaborn-biological-statistics
log2 expression for 6 genes, control vs. treatment, 15 replicates per condition.

| Column | Type | Description |
|---|---|---|
| `gene` | str | Gene symbol |
| `direction` | str | Ground-truth simulated direction: `up`, `down`, `unchanged` |
| `condition` | str | `control` or `treatment` |
| `replicate` | int | Replicate index |
| `expression` | float | Simulated log2 expression |

Used here for a small-multiples figure, one Matplotlib Axes per gene.

### `qc_metrics.csv` (96 rows), shared with seaborn-biological-statistics
Per-sample sequencing QC for a 96-sample batch across 3 sub-batches.

| Column | Type | Description |
|---|---|---|
| `sample_id` | str | Sample identifier |
| `batch` | str | `batch_1`, `batch_2`, `batch_3` |
| `coverage_mean` | float | Mean sequencing coverage (X) |
| `duplicates_pct` | float | PCR duplication rate (%) |
| `gc_content` | float | GC content (%) |
| `q30_pct` | float | Fraction of bases with Q30+ quality (%) |

Used here for a custom GridSpec dashboard combining a scatter, two
histograms, and a text summary panel in one figure.

### `growth_curves.csv` (240 rows), new
Bacterial growth curves (OD600) for 3 strains over 24 hours, logistic
growth model with strain-specific rate, carrying capacity, and lag.

| Column | Type | Description |
|---|---|---|
| `strain` | str | `WT`, `MutantA_fast`, `MutantB_slow` |
| `replicate` | int | Replicate index (4 per strain) |
| `time_h` | float | Hours since inoculation |
| `OD600` | float | Simulated optical density at 600nm |

Used to drive a FuncAnimation showing the curves diverge over time.

### `enzyme_activity_surface.csv` (625 rows), new
Enzyme activity sampled on a 25x25 grid of pH and temperature.

| Column | Type | Description |
|---|---|---|
| `pH` | float | Buffer pH (4.0 to 10.0) |
| `temperature_C` | float | Reaction temperature (10 to 70C) |
| `activity_pct` | float | Simulated relative activity (%), peak near pH 7.4, 37C |

Used for a 3D surface plot and matching contour plot.

### `plasmid_map.csv` (7 rows), new
A synthetic 5400bp expression plasmid's gene layout.

| Column | Type | Description |
|---|---|---|
| `gene` | str | Gene name |
| `category` | str | `ori`, `resistance`, `reporter`, `promoter`, `MCS` |
| `start_bp` | int | Start position (bp) |
| `end_bp` | int | End position (bp) |
| `strand` | str | `+` or `-` |
| `color` | str | Hex color used for the category |

Used to draw a circular plasmid map with Matplotlib Wedge patches.

### `phylo_edges.csv` (14 rows), new
A small phylogenetic tree for 8 taxa, encoded as edges.

| Column | Type | Description |
|---|---|---|
| `parent` | str | Parent node name (internal node or `root`) |
| `child` | str | Child node name (internal node or a `Taxon_X` leaf) |
| `branch_length` | float | Branch length from parent to child |

Used to draw a dendrogram manually from line segments rather than
through a library dendrogram function.

### `phylo_metadata.csv` (8 rows)
Metadata aligned to the tips in `phylo_edges.csv`.

| Column | Type | Description |
|---|---|---|
| `taxon` | str | Tip identifier; must match the phylogeny exactly |
| `lineage` | str | Simulated lineage assignment |
| `habitat` | str | Simulated isolation habitat |
| `genome_size_mb` | float | Simulated genome size in megabases |

### `phylo_gene_presence.csv` (8 rows)
Binary pangenome matrix aligned to the same eight taxa.

| Column | Type | Description |
|---|---|---|
| `taxon` | str | Tip identifier; must match the phylogeny exactly |
| `GF_000` to `GF_031` | int | Gene-family presence (`1`) or absence (`0`) |

The plotting API validates taxa and binary values, removes invariant families
from the displayed accessory matrix, and applies topology-derived tip order to
all panels. It does not infer a tree or gene families.

### `pangenome_accumulation.csv` (900 rows)
Pan- and core-genome trajectories from 30 simulated resampling replicates.

| Column | Type | Description |
|---|---|---|
| `replicate` | int | Resampling replicate identifier |
| `n_genomes` | int | Number of genomes included |
| `pan_genes` | int | Number of unique gene families observed |
| `core_genes` | int | Number of gene families shared by all included genomes |

Thin trajectories preserve individual resamples; the summary curves use the
replicate mean and empirical 2.5 to 97.5 percentile interval. These bands show
sampling sensitivity, not model-based confidence intervals.

### `synteny_genes.csv` (18 rows)
Gene features for three simulated genome neighborhoods.

| Column | Type | Description |
|---|---|---|
| `genome` | str | Genome or region identifier |
| `gene` | str | Feature name |
| `family` | str | Functional family used for color mapping |
| `start_bp` | int | Feature start coordinate |
| `end_bp` | int | Feature end coordinate |
| `strand` | str | Forward (`+`) or reverse (`-`) strand |
| `color` | str | Hex color for the functional family |

### `synteny_links.csv` (11 rows)
Explicit pairwise links between features in adjacent neighborhoods.

| Column | Type | Description |
|---|---|---|
| `source_genome` | str | Upper region identifier |
| `source_gene` | str | Feature in the upper region |
| `target_genome` | str | Lower region identifier |
| `target_gene` | str | Linked feature in the lower region |
| `identity` | float | Simulated pairwise identity percentage |

The figure renders supplied relationships and maps identity to link opacity. It
does not perform alignment, orthology inference, or synteny detection.
