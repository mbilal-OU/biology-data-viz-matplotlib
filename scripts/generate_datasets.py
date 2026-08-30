"""
generate_datasets.py
=====================
Simulates all datasets used in this repository. Three datasets
(docking_scores, gene_expression, qc_metrics) use the same generation
logic as the companion Seaborn repo (biology-data-viz-seaborn), so the
same biological scenario can be viewed through both libraries. The
remaining tables support low-level Matplotlib techniques and advanced
genomics case studies.

Usage:
    python scripts/generate_datasets.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

RNG = np.random.default_rng(42)
OUT = Path(__file__).resolve().parents[1] / "data"
OUT.mkdir(exist_ok=True)


def save(df: pd.DataFrame, name: str) -> None:
    path = OUT / name
    df.to_csv(path, index=False)
    print(f"wrote {path}  ({len(df)} rows, {len(df.columns)} cols)")


# ---------------------------------------------------------------------------
# Shared datasets (same logic as biology-data-viz-seaborn)
# ---------------------------------------------------------------------------
def gen_docking_scores(n_per_target: int = 120) -> pd.DataFrame:
    """
    Virtual screening campaign against 3 protein targets. vina_score
    (kcal/mol, more negative is better binding) depends on logP with a
    target-specific optimum, plus noise. Used here for a 3D scatter
    (logP, molecular_weight, vina_score), a view that a 2D Seaborn
    scatter cannot show directly.
    """
    targets = {"Kinase_A": -7.5, "Protease_B": -6.8, "GPCR_C": -8.2}
    rows = []
    for target, best_score in targets.items():
        logP = RNG.normal(2.5, 1.3, n_per_target)
        optimal_logP = 2.8 if target != "GPCR_C" else 3.6
        penalty = 0.35 * (logP - optimal_logP) ** 2
        vina = best_score + penalty + RNG.normal(0, 0.6, n_per_target)
        ring_count = RNG.poisson(2.2, n_per_target) + 1
        mw = RNG.normal(380, 60, n_per_target).clip(180, 600)
        rows.append(
            pd.DataFrame(
                {
                    "target": target,
                    "ligand_id": [f"{target[:3].upper()}_{i:04d}" for i in range(n_per_target)],
                    "logP": logP.round(2),
                    "molecular_weight": mw.round(1),
                    "ring_count": ring_count,
                    "vina_score": vina.round(2),
                }
            )
        )
    return pd.concat(rows, ignore_index=True)


def gen_gene_expression(n_replicates: int = 15) -> pd.DataFrame:
    """
    log2 expression for 6 genes under control vs. treatment, with
    known up/down/unchanged ground truth. Used here for a small-multiples
    figure (one Axes per gene via plt.subplots), a layout Matplotlib
    controls directly rather than through a plotting function.
    """
    genes = {
        "TP53": ("down", -1.2),
        "MYC": ("up", 1.6),
        "GAPDH": ("unchanged", 0.0),
        "IL6": ("up", 2.1),
        "ACTB": ("unchanged", 0.05),
        "CDKN1A": ("down", -0.8),
    }
    rows = []
    for gene, (direction, effect) in genes.items():
        baseline = RNG.normal(8.0, 0.4)
        for condition, delta in [("control", 0.0), ("treatment", effect)]:
            expr = baseline + delta + RNG.normal(0, 0.35, n_replicates)
            rows.append(
                pd.DataFrame(
                    {
                        "gene": gene,
                        "direction": direction,
                        "condition": condition,
                        "replicate": np.arange(n_replicates),
                        "expression": expr.round(3),
                    }
                )
            )
    return pd.concat(rows, ignore_index=True)


def gen_qc_metrics(n_samples: int = 96) -> pd.DataFrame:
    """
    Per-sample sequencing QC for a 96-sample batch, with coverage and
    duplication negatively correlated (a real low-input artifact).
    Used here for a custom multi-panel dashboard built with
    GridSpec: histogram, scatter, and a text summary combined in one
    figure, a layout Seaborn's figure-level functions do not offer.
    """
    input_quality = RNG.beta(5, 2, n_samples)
    coverage_mean = 25 + 55 * input_quality + RNG.normal(0, 4, n_samples)
    duplicates_pct = 35 - 25 * input_quality + RNG.normal(0, 3, n_samples)
    gc_content = RNG.normal(41, 2.5, n_samples)
    q30_pct = 88 + 8 * input_quality + RNG.normal(0, 1.5, n_samples)
    batch = RNG.choice(["batch_1", "batch_2", "batch_3"], n_samples)

    return pd.DataFrame(
        {
            "sample_id": [f"SMP{idx:03d}" for idx in range(n_samples)],
            "batch": batch,
            "coverage_mean": coverage_mean.clip(5, None).round(2),
            "duplicates_pct": duplicates_pct.clip(1, 60).round(2),
            "gc_content": gc_content.round(2),
            "q30_pct": q30_pct.clip(60, 99.9).round(2),
        }
    )


# ---------------------------------------------------------------------------
# New datasets, chosen for Matplotlib-specific techniques
# ---------------------------------------------------------------------------
def gen_growth_curves(n_timepoints: int = 20, n_replicates: int = 4) -> pd.DataFrame:
    """
    Bacterial growth curves (OD600) for 3 strains over time, following
    a logistic growth model with strain-specific growth rate and
    carrying capacity. Used to drive a FuncAnimation: each frame reveals
    one more timepoint, so the curves visibly race toward their
    plateaus, something a static plot cannot show.
    """
    hours = np.linspace(0, 24, n_timepoints)
    strains = {
        "WT": dict(r=0.55, k=1.4, lag=1.0),
        "MutantA_fast": dict(r=0.85, k=1.2, lag=0.5),
        "MutantB_slow": dict(r=0.35, k=1.6, lag=2.5),
    }
    rows = []
    for strain, p in strains.items():
        for rep in range(n_replicates):
            od0 = 0.02 + RNG.normal(0, 0.003)
            r = p["r"] * RNG.normal(1.0, 0.05)
            k = p["k"] * RNG.normal(1.0, 0.04)
            t_shifted = np.clip(hours - p["lag"], 0, None)
            od = k / (1 + ((k - od0) / od0) * np.exp(-r * t_shifted))
            od += RNG.normal(0, 0.01, n_timepoints)
            od = np.clip(od, 0.005, None)
            rows.append(
                pd.DataFrame(
                    {
                        "strain": strain,
                        "replicate": rep,
                        "time_h": hours.round(2),
                        "OD600": od.round(4),
                    }
                )
            )
    return pd.concat(rows, ignore_index=True)


def gen_enzyme_activity_surface(n_ph: int = 25, n_temp: int = 25) -> pd.DataFrame:
    """
    Enzyme activity as a function of pH and temperature, sampled on a
    grid. Activity follows a 2D Gaussian-like response surface with a
    single optimum (pH 7.4, 37C), typical of a mesophilic enzyme.
    Used for a 3D surface plot and a matching contour plot side by
    side, a genuinely 3D relationship that a heatmap alone flattens.
    """
    ph = np.linspace(4.0, 10.0, n_ph)
    temp = np.linspace(10.0, 70.0, n_temp)
    ph_grid, temp_grid = np.meshgrid(ph, temp)

    ph_opt, temp_opt = 7.4, 37.0
    ph_width, temp_width = 1.1, 12.0
    activity = 100 * np.exp(
        -(((ph_grid - ph_opt) ** 2) / (2 * ph_width**2))
        - (((temp_grid - temp_opt) ** 2) / (2 * temp_width**2))
    )
    activity += RNG.normal(0, 1.5, activity.shape)
    activity = np.clip(activity, 0, None)

    return pd.DataFrame(
        {
            "pH": ph_grid.ravel().round(3),
            "temperature_C": temp_grid.ravel().round(2),
            "activity_pct": activity.ravel().round(2),
        }
    )


def gen_plasmid_map(n_genes: int = 7, plasmid_length: int = 5400) -> pd.DataFrame:
    """
    A synthetic plasmid gene map: gene name, start/end position (bp),
    strand, and functional category. Used to draw a circular plasmid
    map with Matplotlib patches (Wedge), a diagram type with no
    equivalent Seaborn function at all.
    """
    categories = {
        "ori": "#8899AA",
        "resistance": "#C0504D",
        "reporter": "#4F81BD",
        "promoter": "#9BBB59",
        "MCS": "#8064A2",
    }
    genes = [
        ("ori", "ori", 0, 600, "+"),
        ("AmpR", "resistance", 700, 1550, "-"),
        ("lacZ_promoter", "promoter", 1600, 1750, "+"),
        ("MCS", "MCS", 1760, 1860, "+"),
        ("GFP", "reporter", 1900, 2650, "+"),
        ("T7_promoter", "promoter", 2700, 2830, "-"),
        ("KanR", "resistance", 3000, 3800, "+"),
    ]
    rows = []
    for name, cat, start, end, strand in genes[:n_genes]:
        rows.append(
            dict(
                gene=name,
                category=cat,
                start_bp=start,
                end_bp=min(end, plasmid_length),
                strand=strand,
                color=categories[cat],
            )
        )
    df = pd.DataFrame(rows)
    df.attrs["plasmid_length"] = plasmid_length
    return df


def gen_phylo_edges() -> pd.DataFrame:
    """
    A small phylogenetic tree encoded as parent-child edges with
    branch lengths, for 8 taxa. Used to draw a dendrogram manually
    with line segments and text labels rather than a library
    dendrogram function, to show low-level layout control.
    """
    edges = [
        ("root", "N1", 0.1),
        ("root", "N2", 0.15),
        ("N1", "N3", 0.2),
        ("N1", "N4", 0.25),
        ("N2", "Taxon_E", 0.4),
        ("N2", "N5", 0.2),
        ("N3", "Taxon_A", 0.3),
        ("N3", "Taxon_B", 0.35),
        ("N4", "Taxon_C", 0.45),
        ("N4", "N6", 0.15),
        ("N5", "Taxon_F", 0.3),
        ("N5", "Taxon_G", 0.28),
        ("N6", "Taxon_D", 0.2),
        ("N6", "Taxon_H", 0.22),
    ]
    return pd.DataFrame(edges, columns=["parent", "child", "branch_length"])


def gen_phylogenomics_tables() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Create tree-tip metadata and a matched gene presence-absence matrix."""
    taxa = [f"Taxon_{letter}" for letter in "ABCDEFGH"]
    lineage = {
        "Taxon_A": "Lineage_1",
        "Taxon_B": "Lineage_1",
        "Taxon_C": "Lineage_1",
        "Taxon_D": "Lineage_1",
        "Taxon_H": "Lineage_1",
        "Taxon_E": "Lineage_2",
        "Taxon_F": "Lineage_2",
        "Taxon_G": "Lineage_2",
    }
    metadata = pd.DataFrame(
        {
            "taxon": taxa,
            "lineage": [lineage[taxon] for taxon in taxa],
            "habitat": ["Host", "Host", "Water", "Soil", "Host", "Water", "Soil", "Water"],
            "genome_size_mb": [4.8, 4.7, 5.1, 4.5, 4.3, 5.0, 4.9, 4.6],
        }
    )

    matrix = np.ones((len(taxa), 32), dtype=int)
    for column in range(10, 20):
        associated = "Lineage_1" if column < 15 else "Lineage_2"
        for row, taxon in enumerate(taxa):
            probability = 0.88 if lineage[taxon] == associated else 0.12
            matrix[row, column] = RNG.binomial(1, probability)
    matrix[:, 20:] = RNG.binomial(1, 0.30, size=(len(taxa), 12))
    gene_matrix = pd.DataFrame(matrix, columns=[f"GF_{index:03d}" for index in range(32)])
    gene_matrix.insert(0, "taxon", taxa)
    return metadata, gene_matrix


def gen_pangenome_accumulation(
    n_genomes: int = 30,
    n_replicates: int = 30,
) -> pd.DataFrame:
    """Simulate resampled pan- and core-genome accumulation curves."""
    sample_sizes = np.arange(1, n_genomes + 1)
    rows = []
    for replicate in range(n_replicates):
        pan_scale = RNG.normal(1.0, 0.025)
        core_scale = RNG.normal(1.0, 0.018)
        pan = (3100 + 520 * sample_sizes**0.55) * pan_scale
        core = (3200 - 500 * np.log1p(sample_sizes)) * core_scale
        pan += RNG.normal(0, 35, len(sample_sizes))
        core += RNG.normal(0, 22, len(sample_sizes))
        pan = np.maximum.accumulate(np.rint(pan)).astype(int)
        core = np.minimum.accumulate(np.rint(core)).astype(int)
        rows.append(
            pd.DataFrame(
                {
                    "replicate": replicate,
                    "n_genomes": sample_sizes,
                    "pan_genes": pan,
                    "core_genes": core,
                }
            )
        )
    return pd.concat(rows, ignore_index=True)


def gen_synteny_tables() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Create three related gene neighborhoods and pairwise homology links."""
    colors = {
        "recombination": "#0072B2",
        "chaperone": "#D55E00",
        "island": "#009E73",
        "topoisomerase": "#CC79A7",
        "transcription": "#E69F00",
        "efflux": "#56B4E9",
        "novel": "#777777",
    }
    specifications = {
        "Genome_Alpha": [
            ("recA", "recombination", 500, 1300, "+"),
            ("dnaK", "chaperone", 1500, 2450, "+"),
            ("islandA", "island", 2700, 3400, "+"),
            ("gyrB", "topoisomerase", 3650, 4550, "-"),
            ("rpoB", "transcription", 4800, 5900, "+"),
            ("efflux", "efflux", 6200, 7200, "+"),
        ],
        "Genome_Beta": [
            ("recA", "recombination", 400, 1200, "+"),
            ("dnaK", "chaperone", 1400, 2350, "+"),
            ("islandA", "island", 2550, 3250, "-"),
            ("gyrB", "topoisomerase", 3500, 4400, "-"),
            ("rpoB", "transcription", 4650, 5750, "+"),
            ("efflux", "efflux", 6000, 7000, "+"),
        ],
        "Genome_Gamma": [
            ("recA", "recombination", 600, 1400, "+"),
            ("dnaK", "chaperone", 1620, 2570, "+"),
            ("novelX", "novel", 2750, 3300, "+"),
            ("islandA", "island", 3500, 4200, "+"),
            ("gyrB", "topoisomerase", 4450, 5350, "-"),
            ("rpoB", "transcription", 5600, 6700, "+"),
        ],
    }
    rows = []
    for genome, features in specifications.items():
        for gene, family, start, end, strand in features:
            rows.append(
                {
                    "genome": genome,
                    "gene": gene,
                    "family": family,
                    "start_bp": start,
                    "end_bp": end,
                    "strand": strand,
                    "color": colors[family],
                }
            )
    genes = pd.DataFrame(rows)

    links = []
    for source_genome, target_genome in [
        ("Genome_Alpha", "Genome_Beta"),
        ("Genome_Beta", "Genome_Gamma"),
    ]:
        source_genes = set(genes.loc[genes["genome"] == source_genome, "gene"])
        target_genes = set(genes.loc[genes["genome"] == target_genome, "gene"])
        for index, gene in enumerate(sorted(source_genes & target_genes)):
            links.append(
                {
                    "source_genome": source_genome,
                    "source_gene": gene,
                    "target_genome": target_genome,
                    "target_gene": gene,
                    "identity": 86 + (index * 2) % 13,
                }
            )
    return genes, pd.DataFrame(links)


def main() -> None:
    save(gen_docking_scores(), "docking_scores.csv")
    save(gen_gene_expression(), "gene_expression.csv")
    save(gen_qc_metrics(), "qc_metrics.csv")
    save(gen_growth_curves(), "growth_curves.csv")
    save(gen_enzyme_activity_surface(), "enzyme_activity_surface.csv")
    save(gen_plasmid_map(), "plasmid_map.csv")
    save(gen_phylo_edges(), "phylo_edges.csv")
    metadata, gene_matrix = gen_phylogenomics_tables()
    save(metadata, "phylo_metadata.csv")
    save(gene_matrix, "phylo_gene_presence.csv")
    save(gen_pangenome_accumulation(), "pangenome_accumulation.csv")
    synteny_genes, synteny_links = gen_synteny_tables()
    save(synteny_genes, "synteny_genes.csv")
    save(synteny_links, "synteny_links.csv")


if __name__ == "__main__":
    main()
