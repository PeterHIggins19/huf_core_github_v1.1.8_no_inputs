# HUF Reference Manual

**Updated:** 2026-02-17

This manual is the “how to run it” companion to the handbook. It’s written for:
- **GUI-only** users (download a ZIP, double-click a Windows starter),
- researchers who live in **Excel + theory**, and
- anyone who wants **reproducible artifacts** without learning Git on day one.

---

## 1) Quick Start (Windows, no Git required)

### Option A — easiest: GitHub Release ZIP
1. Open the project Release page on GitHub and download the ZIP (the asset attached to the release).
2. Unzip it somewhere simple (Desktop is fine).
3. Double-click: **`START_HERE_WINDOWS.bat`**

What it does:
- creates a local virtual environment in `.venv`
- installs HUF in editable mode (local)
- fetches **Markham + Toronto** civic inputs automatically
- prints the *exact commands* to run the demos

> Tip: If Windows shows a security warning the first time, click “More info” → “Run anyway”.

### Option B — GitHub Desktop (recommended once you’re comfortable)
Use GitHub Desktop to keep your folder synced with GitHub. Day-to-day:
- **Fetch** checks for updates.
- **Pull** downloads updates.
- **Commit** records your changes.
- **Push/Sync** uploads your changes.

---

## 2) Fetching input data (real public sources)

Run these from the repo root (the folder that contains `pyproject.toml`).

### Markham (2018 Budget Allocation XLSX)
```powershell
.\.venv\Scripts\python scripts\fetch_data.py --markham
```
Expected file:
- `cases\markham2018\inputs\2018-Budget-Allocation-of-Revenue-and-Expenditure-by-Fund.xlsx`

### Toronto (Traffic signals timing → CSV)
Non-interactive default selection:
```powershell
.\.venv\Scripts\python scripts\fetch_data.py --toronto --yes
```

Interactive mode (lets you choose among matching datasets):
```powershell
.\.venv\Scripts\python scripts\fetch_data.py --toronto
```

Expected files:
- `cases\traffic_phase\inputs\toronto_traffic_signals_phase_status.csv`
- `cases\traffic_anomaly\inputs\toronto_traffic_signals_phase_status.csv`

Toronto schema expected by HUF traffic adapters:
- **required**: `TCS`, `PHASE`
- **optional**: `PHASE_STATUS_TEXT`, `PHASE_CALL_TEXT`

### Planck (guided/manual)
Planck maps are *large*; users often want to choose **PLA** vs **IRSA** mirrors and which products to pull.

Guidance:
```powershell
.\.venv\Scripts\python scripts\fetch_data.py --planck-guide
```

You’ll end up with a FITS file such as:
- `cases\planck70\inputs\LFI_SkyMap_070_1024_R3.00_full.fits`

---

## 3) Running the included cases

### A) Markham 2018 (fund-weighted expenditures)
```powershell
.\.venv\Scripts\huf markham ^
  --xlsx cases\markham2018\inputs\2018-Budget-Allocation-of-Revenue-and-Expenditure-by-Fund.xlsx ^
  --out out\markham2018
```

What you should see:
- `out\markham2018\run_stamp.json`
- `out\markham2018\artifacts\markham_fund_weights.png`
- tabular artifacts suitable for Excel inspection

Open the image to sanity-check weights:
- `docs\assets\markham_fund_weights.png`

### B) Toronto traffic phase (band extraction)
```powershell
.\.venv\Scripts\huf traffic ^
  --csv cases\traffic_phase\inputs\toronto_traffic_signals_phase_status.csv ^
  --out out\traffic_phase
```

Key outputs:
- normalized element table
- UBH artifacts and stability packet

### C) Toronto traffic anomaly (share + hotspots)
```powershell
.\.venv\Scripts\huf traffic-anomaly ^
  --csv cases\traffic_anomaly\inputs\toronto_traffic_signals_phase_status.csv ^
  --out out\traffic_anomaly
```

Sanity-check visualization:
- `docs\assets\traffic_anomaly_share.png`

### D) Planck 70 GHz (map → coherence → stability)
```powershell
.\.venv\Scripts\huf planck ^
  --fits cases\planck70\inputs\LFI_SkyMap_070_1024_R3.00_full.fits ^
  --out out\planck70
```

Expect:
- coherence maps and stability sweep artifacts in `out\planck70\artifacts\...`
- (optionally) a stability sweep report describing retained set vs τ

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
- `dataset_id` — identifier derived from the *input file(s)* (so you can prove what data you ran)
- `code_hash` — identifier for the *code state* that produced artifacts
- `param_hash` — identifier for your parameterization (τ grid, budgets, etc.)
- `run_id` — unique run identifier (useful when repeating sweeps)

If two runs have the same `dataset_id + code_hash + param_hash`, their artifacts should match (modulo timestamps).

---

## 5) Troubleshooting (Windows-focused)

### “SSL: CERTIFICATE_VERIFY_FAILED”
This is usually a **Python installation / certificate store** issue (common with very new Python builds or locked-down machines).

Try:
1. Ensure you are using the repo venv Python:
   ```powershell
   .\.venv\Scripts\python -V
   ```
2. Install certifi into the venv:
   ```powershell
   .\.venv\Scripts\python -m pip install certifi
   ```
3. Re-run fetch:
   ```powershell
   .\.venv\Scripts\python scripts\fetch_data.py --toronto --yes
   ```

If it still fails, your network may be intercepting TLS (corporate proxy). In that case, download the Toronto ZIP manually from the browser and place the extracted CSV into:
- `cases\traffic_phase\inputs\toronto_traffic_signals_phase_status.csv`

### “HTTP Error 404” during Toronto fetch
This usually means the CKAN base URL is wrong. Use the default:
- `https://open.toronto.ca/api/3/action`

You can override explicitly:
```powershell
.\.venv\Scripts\python scripts\fetch_data.py --toronto --yes --toronto-ckan https://open.toronto.ca/api/3/action
```

### “File not found … cases\…\inputs\…”
Run the fetch step first:
```powershell
.\.venv\Scripts\python scripts\fetch_data.py --markham --toronto --yes
```

---

## 6) “Where is that file on GitHub?” (finding images + artifacts)

Example file you asked about:
`cases/markham2018/markham_fund_weights.png`

On GitHub.com:
1. Go to the repo home page
2. Click **Code** (file list)
3. Click **cases**
4. Click **markham2018**
5. Click **markham_fund_weights.png**

You can also use GitHub’s search box and type: `markham_fund_weights.png`

---

## 7) Data sources (what is shipped vs fetched)

See **Data Sources** in the docs navigation for:
- Markham Open Data link(s)
- Toronto Open Data link(s)
- Planck PLA + IRSA links and “how to pick the right file”

---

