from pathlib import Path

FIGURES = [
    "01_docking_3d.png",
    "02_gene_expression_panels.png",
    "03_qc_dashboard.png",
    "04_growth_curves.gif",
    "05_enzyme_surface.png",
    "06_plasmid_map.png",
    "07_phylo_tree.png",
    "08_phylogenomics_panel.png",
    "09_pangenome_accumulation.png",
    "10_synteny_tracks.png",
]


def test_every_gallery_figure_links_to_a_tutorial() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")
    guide = Path("docs/figure-tutorials.md").read_text(encoding="utf-8")

    for figure in FIGURES:
        assert f"figures/{figure})](docs/figure-tutorials.md#" in readme

    assert guide.count("**Use when:**") == len(FIGURES)
    assert guide.count("**Inputs and code:**") == len(FIGURES)
    assert guide.count("**Use your own data:**") == len(FIGURES)
    assert guide.count("**Interpret:**") == len(FIGURES)
