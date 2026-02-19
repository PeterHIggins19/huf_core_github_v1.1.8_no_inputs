# Data Sources

**Updated:** 2026-02-18

HUF ships **code + documentation + small derived artifacts**, but it does **not** ship large public datasets (or huge binaries) inside the repo or release ZIPs.

This page tells you where each “real data” demo comes from and how to fetch it.

---

## Markham (Ontario) — 2018 Budget Allocation (XLSX)

Used by: `huf markham ...`

Preferred public sources (these are more stable than “portal” links):

- Markham Open Data listing (document page):
  - https://data-markham.opendata.arcgis.com/documents/81a5dda0ccab4fea8e9ea13433964164
- Markham hosted file endpoint (what `fetch_data.py` uses today):
  - https://maps.markham.ca/OpenDataSite_Tables/Markham_Consolidated_Budget_By_Dept_and_Funding_Source_2018.xlsx

HUF fetch command:
```powershell
.\.venv\Scripts\python scriptsetch_data.py --markham
```

Expected local path:
- `cases\markham2018\inputs\2018-Budget-Allocation-of-Revenue-and-Expenditure-by-Fund.xlsx`

Notes:
- If Markham changes the hosting URL, update `scripts/fetch_data.py` and this page to match.

---

## Toronto (Ontario) — Traffic signals timing (ZIP → CSV)

Used by: `huf traffic ...` and `huf traffic-anomaly ...`

Public source:
- City of Toronto Open Data portal (CKAN-backed): https://open.toronto.ca/

HUF fetch command (non-interactive, recommended):
```powershell
.\.venv\Scripts\python scriptsetch_data.py --toronto --yes
```

Expected local paths (HUF writes the same CSV into both case folders):
- `cases\traffic_phase\inputs\toronto_traffic_signals_phase_status.csv`
- `cases\traffic_anomaly\inputs\toronto_traffic_signals_phase_status.csv`

Toronto schema expected by HUF traffic adapters:
- required columns: `TCS`, `PHASE`
- optional columns: `PHASE_STATUS_TEXT`, `PHASE_CALL_TEXT`

---

## Planck (ESA / NASA) — All-sky maps (FITS)

Used by: `huf planck ...`

Planck maps are **very large** (hundreds of MB to multiple GB). HUF does not ship them.

### Option A — ESA Planck Legacy Archive (PLA)
Portal:
- https://pla.esac.esa.int/

Typical workflow:
1. Open PLA
2. Choose the product family (maps / frequency)
3. Select the release (e.g., PR3)
4. Download the FITS product(s)

### Option B — NASA/IPAC IRSA mirror
IRSA Planck landing page:
- https://irsa.ipac.caltech.edu/Missions/planck.html

Example file used in this repo:
- 70 GHz (LFI) full-sky map (PR3):
  - Preview page: https://irsa.ipac.caltech.edu/data/Planck/release_3/all-sky-maps/previews/LFI_SkyMap_070_1024_R3.00_full/index.html
  - Direct file URL (large): https://irsa.ipac.caltech.edu/data/Planck/release_3/all-sky-maps/maps/LFI_SkyMap_070_1024_R3.00_full.fits

HUF guidance (prints manual download instructions):
```powershell
.\.venv\Scripts\python scriptsetch_data.py --planck-guide
```

Expected local path:
- `cases\planck70\inputs\LFI_SkyMap_070_1024_R3.00_full.fits`

Windows download (resume-friendly):
```powershell
$dest = "cases\planck70\inputs\LFI_SkyMap_070_1024_R3.00_full.fits"
New-Item -ItemType Directory -Force (Split-Path $dest) | Out-Null
$src  = "https://irsa.ipac.caltech.edu/data/Planck/release_3/all-sky-maps/maps/LFI_SkyMap_070_1024_R3.00_full.fits"
Start-BitsTransfer -Source $src -Destination $dest
```

---

## Synthetic data policy (what “toy” means)

- **Worked cases (Planck / Markham / Toronto):** real public data.
- **Toy/synthetic examples (if any):** small vectors strictly for smoke-testing core logic, always labeled as synthetic.
