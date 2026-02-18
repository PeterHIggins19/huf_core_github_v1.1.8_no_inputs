# Data Sources

**Updated:** 2026-02-17

HUF ships **code + documentation + small derived artifacts**, but it does **not** ship large public datasets (or huge binaries) inside the repo or release ZIPs.

This page tells you exactly where each “real data” demo comes from and how to fetch it.

---

## Markham (Ontario) — 2018 Budget Allocation (XLSX)

Used by: `huf markham ...`

Public source:
- City of Markham website (budget document):
  - `https://www.markham.ca/wps/portal/home/city-hall/budget-and-finance/budget/2018budget/03-2018-Budget-Allocation-of-Revenue-and-Expenditure-by-Fund.xlsx`

HUF fetch command:
```powershell
.\.venv\Scripts\python scripts\fetch_data.py --markham
```

Expected local path:
- `cases\markham2018\inputs\2018-Budget-Allocation-of-Revenue-and-Expenditure-by-Fund.xlsx`

Notes:
- If Markham changes the URL, use the Markham site search for the same filename and update `scripts/fetch_data.py` accordingly.

---

## Toronto (Ontario) — Traffic signals timing (ZIP → CSV)

Used by: `huf traffic ...` and `huf traffic-anomaly ...`

Public source:
- City of Toronto Open Data portal (CKAN-backed): `https://open.toronto.ca/`

HUF fetch command (non-interactive, recommended):
```powershell
.\.venv\Scripts\python scripts\fetch_data.py --toronto --yes
```

What HUF downloads:
- A ZIP from Toronto’s CKAN portal (the exact URL may change as resources are updated).
- The fetch script extracts and normalizes a CSV into the case folders:
  - `cases\traffic_phase\inputs\toronto_traffic_signals_phase_status.csv`
  - `cases\traffic_anomaly\inputs\toronto_traffic_signals_phase_status.csv`

If you prefer manual download:
1. Go to `https://open.toronto.ca/`
2. Search for **Traffic signals timing**
3. Download the ZIP
4. Extract and place/rename the CSV to the paths above

---

## Planck (ESA / NASA) — All-sky maps (FITS)

Used by: `huf planck ...`

Planck maps are **very large** (hundreds of MB to multiple GB). HUF does not ship them.

### Option A — ESA Planck Legacy Archive (PLA)
Portal:
- `https://pla.esac.esa.int/`

Typical workflow:
1. Open PLA
2. Choose the product family (maps / frequency)
3. Select the release (e.g., PR3)
4. Download the FITS product(s)

### Option B — NASA/IPAC IRSA mirror
IRSA Planck page:
- `https://irsa.ipac.caltech.edu/Missions/planck.html`

Example file used in this repo:
- 70 GHz (LFI) full-sky map (PR3):
  - `https://irsa.ipac.caltech.edu/data/Planck/release_3/all-sky-maps/maps/LFI/LFI_SkyMap_070_1024_R3.00_full.fits`

HUF guidance:
```powershell
.\.venv\Scripts\python scripts\fetch_data.py --planck-guide
```

Expected local path:
- `cases\planck70\inputs\LFI_SkyMap_070_1024_R3.00_full.fits`

---

## Synthetic data policy (what is “toy”)

Small toy datasets may exist for:
- unit tests
- “hello world” demonstrations
- quick CI sanity checks

All “headline” cases described above (Markham / Toronto / Planck) are **real public datasets**.

