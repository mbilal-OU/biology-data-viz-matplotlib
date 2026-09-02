# Setup

## macOS and Linux

```bash
git clone https://github.com/mbilal-OU/matplotlib-genomic-figures.git
cd matplotlib-genomic-figures
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
```

## Windows PowerShell

```powershell
git clone https://github.com/mbilal-OU/matplotlib-genomic-figures.git
Set-Location matplotlib-genomic-figures
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
```

If PowerShell blocks activation for the current session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Validate the installation

```bash
python scripts/generate_datasets.py
python scripts/build_advanced_gallery.py
pytest -q
ruff check bioplt scripts tests
mkdocs build --strict
```

The data generator is deterministic. A clean checkout should show no data diff
after it runs.
