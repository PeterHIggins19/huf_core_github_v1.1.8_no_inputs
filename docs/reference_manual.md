# HUF Reference Manual

**Updated:** 2026-02-17

This manual is the “how to run it” companion to the handbook. It’s written for:

- **GUI-only** users (download a ZIP, double-click a Windows starter),
- researchers who live in **Excel + theory**,
- anyone who wants **reproducible artifacts** without learning Git on day one.

---

## 1) Quick Start (Windows, no Git required)

### Option A — easiest: GitHub Release ZIP

1. Download the ZIP from the project’s GitHub Releases page.
2. Unzip it somewhere simple (Desktop is fine).
3. Double-click: **`START_HERE_WINDOWS.bat`**

What it does:

- creates a local virtual environment in `.venv`
- installs HUF in editable mode (local)
- fetches Markham + Toronto inputs (unless you skip)
- prints the exact commands to run the demos

> Tip: If Windows shows a security warning the first time, click “More info” → “Run anyway”.

### Option B — GitHub Desktop (recommended once you’re comfortable)

Use GitHub Desktop to keep your folder synced with GitHub.

Day-to-day:

- **Fetch** checks for updates.
- **Pull** downloads updates.
- **Commit** records your changes.
- **Push/Sync** uploads your changes.

---

## 2) Fetching input data (real public sources)

Run these from the repo root (the folder that contains `pyproject.toml`).

### Markham (2018 Budget Allocation XLSX)

```powershell
.\.venv\Scripts\python scripts/fetch_data.py --markham
```

Expected file:

- `cases/markham2018/inputs/2018-Budget-Allocation-of-Revenue-and-Expenditure-by-Fund.xlsx`

### Toronto (Traffic signals timing → CSV)

Non-interactive default selection:

```powershell
.\.venv\Scripts\python scripts/fetch_data.py --toronto --yes
```

Expected files:

- `cases/traffic_phase/inputs/toronto_traffic_signals_phase_status.csv`
- `cases/traffic_anomaly/inputs/toronto_traffic_signals_phase_status.csv`

Toronto schema expected by HUF traffic adapters:

- **required**: `TCS`, `PHASE`
- **optional**: `PHASE_STATUS_TEXT`, `PHASE_CALL_TEXT`

### Planck (guided/manual)

```powershell
.\.venv\Scripts\python scripts/fetch_data.py --planck-guide
```

You’ll end up with a FITS file such as:

- `cases/planck70/inputs/...70...fits`

---

## 3) Running the included cases (Windows PowerShell)

### A) Markham 2018 (fund-weighted expenditures)

```powershell
.\.venv\Scripts\huf markham --xlsx cases/markham2018/inputs/2018-Budget-Allocation-of-Revenue-and-Expenditure-by-Fund.xlsx --out out/markham2018
```

### B) Toronto traffic phase (band extraction)

```powershell
.\.venv\Scripts\huf traffic --csv cases/traffic_phase/inputs/toronto_traffic_signals_phase_status.csv --out out/traffic_phase
```

### C) Toronto traffic anomaly (share + hotspots)

```powershell
.\.venv\Scripts\huf traffic-anomaly --csv cases/traffic_anomaly/inputs/toronto_traffic_signals_phase_status.csv --out out/traffic_anomaly --status "Green Termination"
```

### D) Planck 70 GHz (map → coherence → stability)

```powershell
.\.venv\Scripts\huf planck --fits cases/planck70/inputs/YOUR_70GHZ_MAP.fits --out out/planck70
```

---

## 4) Understanding `run_stamp.json` (your reproducibility receipt)

HUF writes a stamp like:

```json
{
  "dataset_id": "...",
  "code_hash": "...",
  "param_hash": "...",
  "created_utc": "...",
  "run_id": "..."
}
```

Interpretation:

- `dataset_id` — identifier derived from the input file(s)
- `code_hash` — identifier for the code state that produced artifacts
- `param_hash` — identifier for your parameterization (τ grid, budgets, etc.)
- `run_id` — unique run identifier

If two runs have the same `dataset_id + code_hash + param_hash`, their artifacts should match (modulo timestamps).

---

## 5) Troubleshooting (Windows-focused)

### “SSL: CERTIFICATE_VERIFY_FAILED”

Try:

```powershell
.\.venv\Scripts\python -V
.\.venv\Scripts\python -m pip install certifi
.\.venv\Scripts\python scripts/fetch_data.py --toronto --yes
```

### “HTTP Error 404” during Toronto fetch

Default:

- `https://open.toronto.ca/api/3/action`

Override explicitly:

```powershell
.\.venv\Scripts\python scripts/fetch_data.py --toronto --yes --toronto-ckan https://open.toronto.ca/api/3/action
```

### “File not found … cases/.../inputs/...”

Run fetch first:

```powershell
.\.venv\Scripts\python scripts/fetch_data.py --markham --toronto --yes
```

---

## 6) Build / preview the docs site

```powershell
.\.venv\Scripts\python -m mkdocs serve
```

Strict build check:

```powershell
.\.venv\Scripts\python -m mkdocs build --strict
```
