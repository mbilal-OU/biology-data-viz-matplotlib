# Data Dictionary

All datasets in this repository are simulated (not real experimental
data) using [`scripts/generate_datasets.py`](../scripts/generate_datasets.py),
with a fixed random seed (`np.random.default_rng(42)`) so results are
exactly reproducible. Three datasets use the same generation logic as
the companion Seaborn repository, biology-data-viz-seaborn, so the
same biological scenario can be compared across both libraries. Four
are new, chosen specifically to need a Matplotlib-only technique.

---

### `docking_scores.csv` (360 rows), shared with biology-data-viz-seaborn
Simulated virtual-screening results against 3 protein targets.

| Column | Type | Description |
|---|---|---|
| `target` | str | Protein target (`Kinase_A`, `Protease_B`, `GPCR_C`) |
| `ligand_id` | str | Unique ligand identifier |
| `logP` | float | Simulated lipophilicity |
| `molecular_weight` | float | Simulated molecular weight (Da) |
| `ring_count` | int | Number of ring systems |
| `vina_score` | float | Docking score, kcal/mol (more negative means stronger binding) |

Used here for a 3D scatter plot (logP, molecular weight, vina score),
a view a 2D plot cannot show directly.

### `gene_expression.csv` (180 rows), shared with biology-data-viz-seaborn
log2 expression for 6 genes, control vs. treatment, 15 replicates per condition.

| Column | Type | Description |
|---|---|---|
| `gene` | str | Gene symbol |
| `direction` | str | Ground-truth simulated direction: `up`, `down`, `null` |
| `condition` | str | `control` or `treatment` |
| `replicate` | int | Replicate index |
| `expression` | float | Simulated log2 expression |

Used here for a small-multiples figure, one Matplotlib Axes per gene.

### `qc_metrics.csv` (96 rows), shared with biology-data-viz-seaborn
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
