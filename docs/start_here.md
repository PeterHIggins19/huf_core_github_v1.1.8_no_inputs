# Start Here (Developer)

This page assumes you're comfortable editing files and running commands, but it still prioritizes **copy/paste success**.

## 1) Clone or download the repo

- Git: `git clone ...`
- Or use GitHub Desktop
- Or download the ZIP from GitHub and unzip it

You are in the right folder if you can see `pyproject.toml`.

## 2) Create the repo virtual environment (`.venv`)

Recommended (works on Windows/macOS/Linux):

```powershell
python scripts/bootstrap.py
```

After bootstrap, **always** call the repo executables explicitly:

```powershell
.\.venv\Scripts\python -V
.\.venv\Scripts\huf --help
```

!!! note "Conda users"
    Conda is fine, but avoid installing HUF into a global Conda environment.
    Bootstrap once, then run `.\.venv\Scripts\python` / `.\.venv\Scripts\huf` explicitly so you never “accidentally” execute `miniconda3\Scripts\huf.exe`.

## 3) Fetch demo inputs (Markham + Toronto)

```powershell
.\.venv\Scripts\python scripts/fetch_data.py --markham --toronto --yes
```

## 4) Run a case

```powershell
.\.venv\Scripts\huf markham --xlsx cases/markham2018/inputs/2018-Budget-Allocation-of-Revenue-and-Expenditure-by-Fund.xlsx --out out/markham2018
```

## 5) Run the docs site locally

Docs preview command (always):

```powershell
.\.venv\Scripts\python -m mkdocs serve
```

Strict build check (CI-style):

```powershell
.\.venv\Scripts\python -m mkdocs build --strict
```

## 6) Planck (optional, large file)

Planck files are large and are intentionally **guided/manual**:

```powershell
.\.venv\Scripts\python scripts/fetch_data.py --planck-guide
```

Then run:

```powershell
.\.venv\Scripts\huf planck --fits cases/planck70/inputs/YOUR_70GHZ_MAP.fits --out out/planck70
```

(Use the filename you actually downloaded; the Planck adapter accepts common 70 GHz products.)
