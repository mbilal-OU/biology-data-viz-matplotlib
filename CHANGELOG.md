# Changelog

All notable changes to this project are documented here.
Format loosely follows [Keep a Changelog](https://keepachangelog.com/).

## [1.1.0], 2026-08-29

### Added
- Topology-aligned phylogeny, metadata, and accessory-gene panels.
- Pan- and core-genome accumulation curves with resampling uncertainty.
- Directional gene-neighborhood and synteny diagrams.
- Five deterministic genomics tables, an advanced case-study notebook,
  raster and vector gallery exports, and scientific-method notes.
- Strict documentation builds, GitHub Pages deployment, package builds,
  a three-version Python matrix, and a 95% coverage gate.

### Changed
- Plasmid strand arrows follow the circular tangent and include a functional
  legend.
- Phylogenetic tip order follows topology and malformed trees are rejected.
- Public documentation now distinguishes visualization from biological
  inference and documents 3D readability tradeoffs.

## [1.0.0], 2026-08-28

### Added
- Initial release of the repository, built around a tested,
  importable `bioplt` package (`scatter3d`, `panels`, `animation`,
  `surface`, `diagrams` modules).
- 7 simulated datasets in `data/`, 3 shared with the companion
  seaborn-biological-statistics repository (docking_scores,
  gene_expression, qc_metrics) and 4 new (growth_curves,
  enzyme_activity_surface, plasmid_map, phylo_edges), each generated
  deterministically by `scripts/generate_datasets.py` with a
  documented rationale, plus `data/data_dictionary.md`.
- `tests/test_bioplt.py`: 16 tests covering both rendering and
  structural or statistical sanity checks against known ground truth
  (enzyme surface peak location, tree leaf count and connectivity,
  plasmid gene bounds, growth curve plateau behavior).
- `notebooks/matplotlib_beginner_guide.ipynb`: full tutorial covering
  7 techniques, each with biological question, rationale, code, and
  interpretation, executed end-to-end.
- `docs/`: gallery of every figure paired with its exact code, plus a
  documentation home page.
- `figures/workflow_diagram.svg`: repository pipeline diagram.
- Project scaffolding: `LICENSE` (MIT), `CITATION.cff`,
  `CONTRIBUTING.md`, `pyproject.toml`, `requirements.txt`,
  `environment.yml`, `.gitignore`.
- CI (`.github/workflows/ci.yml`): lint with ruff, regenerate datasets
  and diff for determinism, run pytest, execute the notebook.
