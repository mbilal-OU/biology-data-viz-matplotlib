"""
bioplt
======
A small, importable Matplotlib plotting toolkit for biology and
bioinformatics visualization. Companion package to `bioviz` in the
biology-data-viz-seaborn repository, focused specifically on
techniques that need raw Matplotlib: 3D plots, animation, custom
multi-panel layouts (GridSpec), and manually drawn diagrams that have
no equivalent Seaborn function.

Example
-------
>>> import pandas as pd
>>> from bioplt import theme, scatter3d
>>> theme.set_theme()
>>> df = pd.read_csv("data/docking_scores.csv")
>>> fig, ax = scatter3d.docking_scatter_3d(df)
"""

from . import genome_tracks, pangenome, phylogenomics, theme  # noqa: F401
from ._version import __version__  # noqa: F401

__all__ = ["genome_tracks", "pangenome", "phylogenomics", "theme", "__version__"]
