# Contributing

Contributions are welcome: new techniques, new datasets, clearer
explanations, or bug fixes.

## Setup

```bash
git clone https://github.com/mbilal-OU/matplotlib-genomic-figures.git
cd matplotlib-genomic-figures
pip install -r requirements.txt
pip install -e .
```

## Repository conventions

- **Datasets** are generated, not hand-written. If you add or change a
  dataset, do it in `scripts/generate_datasets.py`, with a docstring
  explaining the biological scenario and the statistical rationale
  behind the simulation (distribution choices, effect sizes, noise
  model). Regenerate with `python scripts/generate_datasets.py` and
  update `data/data_dictionary.md` to match.
- **Plotting code** lives in `bioplt/`, organized by technique
  (`scatter3d.py`, `panels.py`, `animation.py`, `surface.py`,
  `diagrams.py`). Every public function needs a docstring describing
  its parameters and what it returns.
- **New techniques should need real Matplotlib, not duplicate
  Seaborn.** Before adding a plot type here, check whether it already
  has a good Seaborn equivalent. If it does, it belongs in the
  companion repository, seaborn-biological-statistics, instead. This repo
  is specifically for what Seaborn cannot do directly: 3D, animation,
  custom multi-Axes layouts, and manually drawn diagrams.
- **Tests**: add both a rendering smoke test and, where the data has
  a known ground truth, a statistical or structural sanity check to
  `tests/test_bioplt.py`. Run tests with:

  ```bash
  pytest tests/ -v
  ```

- **Notebook**: the tutorial notebook is authored as a Jupytext
  "percent" script at `notebooks/matplotlib_beginner_guide.py` and
  converted to `.ipynb`. To edit it:

  ```bash
  jupytext --to notebook notebooks/matplotlib_beginner_guide.py -o notebooks/matplotlib_beginner_guide.ipynb
  jupyter nbconvert --to notebook --execute --inplace notebooks/matplotlib_beginner_guide.ipynb
  ```

  Please re-execute the notebook before committing so committed output
  matches the code (CI checks this, see `.github/workflows/ci.yml`).

## Adding a new technique

1. Add or extend a dataset generator in `scripts/generate_datasets.py`
   with a clear rationale docstring.
2. Add a plotting function to the appropriate `bioplt/*.py` module.
3. Add a rendering test (and a sanity check if applicable) to
   `tests/test_bioplt.py`.
4. Add a section to the tutorial notebook following the existing
   structure: biological question, why this needs raw Matplotlib,
   code, and interpretation.
5. Regenerate the README's tutorial section:

   ```bash
   python scripts/_build_readme_gallery.py > /tmp/gallery_section.md
   ```

   then merge it into `README.md` and `docs/gallery.md`.

## Pull requests

- Keep PRs focused on one change.
- Make sure `pytest tests/ -v` passes locally before opening a PR.
- Describe the biological motivation for any new dataset or technique
  in the PR description.
