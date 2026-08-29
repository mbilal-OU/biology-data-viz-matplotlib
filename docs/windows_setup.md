# Windows setup

The README quick start uses the POSIX activation command `source .venv/bin/activate`, which works on Linux and macOS. On Windows, create the same virtual environment and activate it with the shell-specific command below.

## PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .
```

If PowerShell blocks local activation scripts, you can avoid changing the machine-wide execution policy and run the environment's Python directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m jupyter notebook notebooks/matplotlib_beginner_guide.ipynb
```

## Command Prompt

```bat
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
pip install -e .
```

After activation, launch the tutorial with:

```text
jupyter notebook notebooks/matplotlib_beginner_guide.ipynb
```

This keeps the dependency set identical to the main installation path while making the tutorial reproducible for Windows users.
