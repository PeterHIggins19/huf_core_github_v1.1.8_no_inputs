# Quick Run (copy/paste)

Goal: create a local `.venv`, fetch inputs, and run the included demos.

> Run these commands from the repo root (the folder that contains `pyproject.toml`).

---

## Windows (PowerShell)

### 1) Bootstrap + install
```powershell
python scripts\bootstrap.py
.\.venv\Scripts\python -m pip install -e .
```

### 2) Fetch Markham + Toronto inputs
```powershell
.\.venv\Scripts\python scripts\fetch_data.py --markham --toronto --yes
```

### 3) Run the demos
```powershell
.\.venv\Scripts\huf markham `
  --xlsx cases\markham2018\inputs\2018-Budget-Allocation-of-Revenue-and-Expenditure-by-Fund.xlsx `
  --out out\markham2018

.\.venv\Scripts\huf traffic `
  --csv cases\traffic_phase\inputs\toronto_traffic_signals_phase_status.csv `
  --out out\traffic_phase

.\.venv\Scripts\huf traffic-anomaly `
  --csv cases\traffic_anomaly\inputs\toronto_traffic_signals_phase_status.csv `
  --out out\traffic_anomaly `
  --status "Green Termination" `
  --tau-global 0.0005
```

### 4) Optional: Planck (FITS is large)
Install FITS support:
```powershell
.\.venv\Scripts\python -m pip install astropy
```

Download the repo’s example FITS to the expected path (resume-friendly):
```powershell
$dest = "cases\planck70\inputs\LFI_SkyMap_070_1024_R3.00_full.fits"
New-Item -ItemType Directory -Force (Split-Path $dest) | Out-Null
$src  = "https://irsa.ipac.caltech.edu/data/Planck/release_3/all-sky-maps/maps/LFI_SkyMap_070_1024_R3.00_full.fits"
Start-BitsTransfer -Source $src -Destination $dest
```

Run:
```powershell
.\.venv\Scripts\huf planck `
  --fits cases\planck70\inputs\LFI_SkyMap_070_1024_R3.00_full.fits `
  --out out\planck70 `
  --retained-target 0.97 `
  --nside-out 64
```

---

## macOS / Linux (bash/zsh)

### 1) Bootstrap + install
```bash
python3 scripts/bootstrap.py
./.venv/bin/python -m pip install -e .
```

### 2) Fetch Markham + Toronto inputs
```bash
./.venv/bin/python scripts/fetch_data.py --markham --toronto --yes
```

### 3) Run the demos
```bash
./.venv/bin/huf markham --xlsx cases/markham2018/inputs/2018-Budget-Allocation-of-Revenue-and-Expenditure-by-Fund.xlsx --out out/markham2018
./.venv/bin/huf traffic --csv cases/traffic_phase/inputs/toronto_traffic_signals_phase_status.csv --out out/traffic_phase
./.venv/bin/huf traffic-anomaly --csv cases/traffic_anomaly/inputs/toronto_traffic_signals_phase_status.csv --out out/traffic_anomaly --status "Green Termination" --tau-global 0.0005
```

### Makefile (optional convenience)
If you have `make` installed:
```bash
make fetch-data
```

---

## Output sanity check

Each run writes artifacts to your `--out` folder, including:
- `artifact_1_coherence_map.csv`
- `artifact_2_active_set.csv`
- `artifact_3_trace_report.jsonl`
- `artifact_4_error_budget.json`
- `run_stamp.json`, `meta.json`, `stability_packet.csv`


---

## Preview the docs locally

```powershell
.\.venv\Scripts\python -m mkdocs serve
```
