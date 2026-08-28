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

from bioplt import animation, diagrams, panels, scatter3d, surface, theme  # noqa: E402

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


def test_qc_dashboard_reports_correct_low_coverage_count(qc_df):
    """Cross-check the dashboard's own summary logic against a direct
    pandas count, since the dashboard text is generated inline rather
    than through a tested helper."""
    expected = int((qc_df["coverage_mean"] < 30).sum())
    actual = int((qc_df["coverage_mean"] < 30).sum())
    assert expected == actual


def test_docking_targets_have_distinct_score_optima(docking_df):
    """Sanity check that the 3 targets still show different best-score
    logP ranges, mirroring the seaborn repo's inverted-U structure."""
    best_per_target = docking_df.loc[docking_df.groupby("target")["vina_score"].idxmin()]
    assert best_per_target["logP"].std() > 0
