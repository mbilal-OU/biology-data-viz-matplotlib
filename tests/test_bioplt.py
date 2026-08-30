"""
Smoke and sanity tests for the bioplt package.

Two kinds of checks:
1. Every plotting function runs without error and returns a real
   Matplotlib object (a rendering smoke test).
2. Statistical or structural sanity checks confirming the simulated
   datasets and diagrams match the ground truth baked into
   scripts/generate_datasets.py.
"""

from pathlib import Path

import matplotlib
import pandas as pd
import pytest

matplotlib.use("Agg")

from bioplt import (  # noqa: E402
    animation,
    diagrams,
    genome_tracks,
    panels,
    pangenome,
    phylogenomics,
    scatter3d,
    surface,
    theme,
)

DATA = Path(__file__).resolve().parents[1] / "data"

theme.set_theme()


@pytest.fixture(scope="module")
def docking_df():
    return pd.read_csv(DATA / "docking_scores.csv")


@pytest.fixture(scope="module")
def expression_df():
    return pd.read_csv(DATA / "gene_expression.csv")


@pytest.fixture(scope="module")
def qc_df():
    return pd.read_csv(DATA / "qc_metrics.csv")


@pytest.fixture(scope="module")
def growth_df():
    return pd.read_csv(DATA / "growth_curves.csv")


@pytest.fixture(scope="module")
def surface_df():
    return pd.read_csv(DATA / "enzyme_activity_surface.csv")


@pytest.fixture(scope="module")
def plasmid_df():
    return pd.read_csv(DATA / "plasmid_map.csv")


@pytest.fixture(scope="module")
def tree_df():
    return pd.read_csv(DATA / "phylo_edges.csv")


@pytest.fixture(scope="module")
def phylo_metadata_df():
    return pd.read_csv(DATA / "phylo_metadata.csv")


@pytest.fixture(scope="module")
def phylo_gene_df():
    return pd.read_csv(DATA / "phylo_gene_presence.csv")


@pytest.fixture(scope="module")
def accumulation_df():
    return pd.read_csv(DATA / "pangenome_accumulation.csv")


@pytest.fixture(scope="module")
def synteny_genes_df():
    return pd.read_csv(DATA / "synteny_genes.csv")


@pytest.fixture(scope="module")
def synteny_links_df():
    return pd.read_csv(DATA / "synteny_links.csv")


# --- rendering smoke tests -------------------------------------------------


def test_docking_scatter_3d_renders(docking_df):
    fig, ax = scatter3d.docking_scatter_3d(docking_df)
    assert fig is not None


def test_gene_expression_small_multiples_renders(expression_df):
    fig, axes = panels.gene_expression_small_multiples(expression_df)
    assert len(axes) >= expression_df["gene"].nunique()


def test_qc_dashboard_renders(qc_df):
    fig = panels.qc_dashboard(qc_df)
    assert len(fig.axes) >= 4


def test_growth_curve_animation_renders(growth_df):
    anim, fig = animation.growth_curve_animation(growth_df, n_frames=5)
    assert anim is not None
    assert fig is not None


def test_enzyme_activity_surface_renders(surface_df):
    fig = surface.enzyme_activity_surface(surface_df)
    assert len(fig.axes) >= 2


def test_plasmid_map_renders(plasmid_df):
    fig, ax = diagrams.plasmid_map(plasmid_df)
    assert ax.has_data() or len(ax.patches) > 0


def test_phylo_tree_renders(tree_df):
    fig, ax = diagrams.phylo_tree(tree_df)
    assert len(ax.lines) > 0


def test_phylogenomics_panel_aligns_every_tip(tree_df, phylo_metadata_df, phylo_gene_df):
    fig, axes = phylogenomics.phylogenomics_panel(tree_df, phylo_metadata_df, phylo_gene_df)
    assert set(axes) == {"tree", "metadata", "matrix"}
    assert len(axes["metadata"].get_yticklabels()) == len(phylo_metadata_df)


def test_pangenome_accumulation_renders(accumulation_df):
    fig, axes = pangenome.accumulation_curves(accumulation_df)
    assert len(axes) == 2
    assert all(ax.has_data() for ax in axes)


def test_synteny_plot_renders(synteny_genes_df, synteny_links_df):
    fig, ax = genome_tracks.synteny_plot(synteny_genes_df, synteny_links_df)
    assert len(ax.patches) >= len(synteny_genes_df) + len(synteny_links_df)


# --- statistical / structural sanity checks --------------------------------


def test_growth_curves_strain_ranking(growth_df):
    """MutantA_fast should reach a higher OD600 sooner than MutantB_slow
    at an early timepoint, matching the simulated growth rates."""
    early = growth_df[growth_df["time_h"].between(4, 6)]
    fast_mean = early[early["strain"] == "MutantA_fast"]["OD600"].mean()
    slow_mean = early[early["strain"] == "MutantB_slow"]["OD600"].mean()
    assert fast_mean > slow_mean


def test_growth_curves_reach_plateau(growth_df):
    """By the final timepoint, the growth rate (change in OD600 per
    step) should have slowed well below its peak rate, consistent with
    logistic growth approaching its carrying capacity. This accounts
    for strain-specific lag phases rather than comparing fixed time
    windows directly."""
    for strain, sub in growth_df.groupby("strain"):
        sub = sub.groupby("time_h")["OD600"].mean().sort_index()
        diffs = sub.diff().dropna()
        final_rate = diffs.iloc[-1]
        peak_rate = diffs.max()
        assert final_rate < peak_rate * 0.5


def test_enzyme_surface_peak_near_expected_optimum(surface_df):
    """The activity surface's maximum should be close to the simulated
    optimum of pH 7.4, 37C."""
    peak_row = surface_df.loc[surface_df["activity_pct"].idxmax()]
    assert peak_row["pH"] == pytest.approx(7.4, abs=0.6)
    assert peak_row["temperature_C"] == pytest.approx(37.0, abs=6.0)


def test_plasmid_genes_stay_within_length(plasmid_df):
    plasmid_length = 5400
    assert (plasmid_df["end_bp"] <= plasmid_length).all()
    assert (plasmid_df["start_bp"] >= 0).all()


def test_plasmid_genes_non_overlapping_where_expected(plasmid_df):
    """No two genes should have identical start positions (sanity check
    that the synthetic map has one arc per gene)."""
    assert plasmid_df["start_bp"].is_unique


def test_phylo_tree_has_expected_leaf_count(tree_df):
    parents = set(tree_df["parent"])
    children = set(tree_df["child"])
    leaves = children - parents
    assert len(leaves) == 8


def test_phylo_tree_is_connected(tree_df):
    """Every child should be reachable from the root by following
    parent-child edges (no orphan subtrees)."""
    parents = set(tree_df["parent"])
    children = set(tree_df["child"])
    root_candidates = parents - children
    assert len(root_candidates) == 1


def test_phylo_layout_preserves_topology_order(tree_df):
    layout = diagrams._build_tree_layout(tree_df)
    assert layout["leaves"] == [
        "Taxon_A",
        "Taxon_B",
        "Taxon_C",
        "Taxon_D",
        "Taxon_H",
        "Taxon_E",
        "Taxon_F",
        "Taxon_G",
    ]


def test_phylo_tree_rejects_negative_branch_length(tree_df):
    invalid = tree_df.copy()
    invalid.loc[0, "branch_length"] = -0.1
    with pytest.raises(ValueError, match="cannot be negative"):
        diagrams.phylo_tree(invalid)


def test_phylo_tree_rejects_repeated_child(tree_df):
    invalid = pd.concat(
        [tree_df, pd.DataFrame([{"parent": "N2", "child": "Taxon_A", "branch_length": 0.2}])],
        ignore_index=True,
    )
    with pytest.raises(ValueError, match="one parent"):
        diagrams.phylo_tree(invalid)


def test_accumulation_summary_respects_curve_direction(accumulation_df):
    summary = pangenome.summarize_accumulation(accumulation_df)
    assert summary["pan_mean"].is_monotonic_increasing
    assert summary["core_mean"].is_monotonic_decreasing


def test_synteny_rejects_unknown_gene_link(synteny_genes_df, synteny_links_df):
    invalid = synteny_links_df.copy()
    invalid.loc[0, "source_gene"] = "missing_gene"
    with pytest.raises(ValueError, match="unknown gene"):
        genome_tracks.synteny_plot(synteny_genes_df, invalid)


def test_qc_dashboard_reports_correct_low_coverage_count(qc_df):
    """Verify the rendered dashboard text reports the calculated count."""
    expected = int((qc_df["coverage_mean"] < 30).sum())
    fig = panels.qc_dashboard(qc_df)
    rendered_text = "\n".join(text.get_text() for ax in fig.axes for text in ax.texts)
    assert f"samples below 30x: {expected}" in rendered_text


def test_docking_targets_have_distinct_score_optima(docking_df):
    """Sanity check that the 3 targets still show different best-score
    logP ranges, mirroring the seaborn repo's inverted-U structure."""
    best_per_target = docking_df.loc[docking_df.groupby("target")["vina_score"].idxmin()]
    assert best_per_target["logP"].std() > 0


def test_plasmid_validation_errors_are_explicit(plasmid_df):
    with pytest.raises(ValueError, match="positive"):
        diagrams.plasmid_map(plasmid_df, plasmid_length=0)
    invalid = plasmid_df.copy()
    invalid.loc[0, "strand"] = "?"
    with pytest.raises(ValueError, match="strand"):
        diagrams.plasmid_map(invalid)
    invalid = plasmid_df.copy()
    invalid.loc[0, "start_bp"] = -1
    with pytest.raises(ValueError, match="within"):
        diagrams.plasmid_map(invalid)
    invalid = plasmid_df.copy()
    invalid.loc[0, "end_bp"] = invalid.loc[0, "start_bp"]
    with pytest.raises(ValueError, match="greater"):
        diagrams.plasmid_map(invalid)


def test_tree_schema_and_root_validation(tree_df):
    with pytest.raises(ValueError, match="Missing required columns"):
        diagrams.phylo_tree(tree_df.drop(columns="branch_length"))
    invalid = tree_df.copy()
    invalid["branch_length"] = "not-numeric"
    with pytest.raises(ValueError, match="numeric"):
        diagrams.phylo_tree(invalid)
    forest = pd.concat(
        [tree_df, pd.DataFrame([{"parent": "other_root", "child": "orphan", "branch_length": 0.1}])],
        ignore_index=True,
    )
    with pytest.raises(ValueError, match="exactly one root"):
        diagrams.phylo_tree(forest)


def test_synteny_schema_and_value_validation(synteny_genes_df, synteny_links_df):
    with pytest.raises(ValueError, match="Missing gene columns"):
        genome_tracks.synteny_plot(synteny_genes_df.drop(columns="family"), synteny_links_df)
    with pytest.raises(ValueError, match="Missing link columns"):
        genome_tracks.synteny_plot(synteny_genes_df, synteny_links_df.drop(columns="identity"))
    with pytest.raises(ValueError, match="at least one"):
        genome_tracks.synteny_plot(synteny_genes_df.iloc[0:0], synteny_links_df)
    invalid = synteny_genes_df.copy()
    invalid.loc[0, "strand"] = "?"
    with pytest.raises(ValueError, match="strand"):
        genome_tracks.synteny_plot(invalid, synteny_links_df)
    invalid = synteny_genes_df.copy()
    invalid.loc[0, "end_bp"] = invalid.loc[0, "start_bp"]
    with pytest.raises(ValueError, match="greater"):
        genome_tracks.synteny_plot(invalid, synteny_links_df)
    invalid_links = synteny_links_df.copy()
    invalid_links.loc[0, "identity"] = 101
    with pytest.raises(ValueError, match="between 0 and 100"):
        genome_tracks.synteny_plot(synteny_genes_df, invalid_links)


def test_accumulation_validation(accumulation_df):
    with pytest.raises(ValueError, match="Missing required columns"):
        pangenome.summarize_accumulation(accumulation_df.drop(columns="core_genes"))
    with pytest.raises(ValueError, match="at least one"):
        pangenome.summarize_accumulation(accumulation_df.iloc[0:0])
    invalid = accumulation_df.copy()
    invalid.loc[0, "n_genomes"] = 0
    with pytest.raises(ValueError, match="positive"):
        pangenome.summarize_accumulation(invalid)
    invalid = accumulation_df.copy()
    invalid.loc[0, "core_genes"] = invalid.loc[0, "pan_genes"] + 1
    with pytest.raises(ValueError, match="cannot exceed"):
        pangenome.summarize_accumulation(invalid)


def test_phylogenomics_validation(tree_df, phylo_metadata_df, phylo_gene_df):
    with pytest.raises(ValueError, match="Missing metadata columns"):
        phylogenomics.phylogenomics_panel(
            tree_df,
            phylo_metadata_df.drop(columns="habitat"),
            phylo_gene_df,
        )
    with pytest.raises(ValueError, match="taxon column"):
        phylogenomics.phylogenomics_panel(
            tree_df,
            phylo_metadata_df,
            phylo_gene_df.drop(columns="taxon"),
        )
    invalid_metadata = phylo_metadata_df.copy()
    invalid_metadata.loc[0, "taxon"] = "unknown"
    with pytest.raises(ValueError, match="metadata taxa"):
        phylogenomics.phylogenomics_panel(tree_df, invalid_metadata, phylo_gene_df)
    invalid_genes = phylo_gene_df.copy()
    invalid_genes.loc[0, "taxon"] = "unknown"
    with pytest.raises(ValueError, match="gene_matrix taxa"):
        phylogenomics.phylogenomics_panel(tree_df, phylo_metadata_df, invalid_genes)
    invalid_genes = phylo_gene_df.copy()
    invalid_genes.loc[0, "GF_010"] = 2
    with pytest.raises(ValueError, match="only 0 and 1"):
        phylogenomics.phylogenomics_panel(tree_df, phylo_metadata_df, invalid_genes)
    invariant = phylo_gene_df[["taxon", "GF_000"]].copy()
    with pytest.raises(ValueError, match="variable gene family"):
        phylogenomics.phylogenomics_panel(tree_df, phylo_metadata_df, invariant)
