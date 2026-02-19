# Start Here (Developer)

This page assumes you already have the repo locally (git clone or GitHub Desktop).  
Goal: get a working `.venv`, fetch inputs, run demos.

> Run commands from the repo root (folder containing `pyproject.toml`).

---

## Windows (PowerShell)

### Create venv + install
```powershell
python scripts\bootstrap.py
.\.venv\Scripts\python -m pip install -e .
```

### Ensure the venv `huf` wins over conda
```powershell
$env:Path = "$PWD\.venv\Scripts;$env:Path"
huf --help
```

### Fetch inputs
```powershell
.\.venv\Scripts\python scripts\fetch_data.py --markham --toronto --yes
```

### Run demos
```powershell
huf markham --xlsx cases\markham2018\inputs\2018-Budget-Allocation-of-Revenue-and-Expenditure-by-Fund.xlsx --out out\markham2018
huf traffic --csv cases\traffic_phase\inputs\toronto_traffic_signals_phase_status.csv --out out\traffic_phase
huf traffic-anomaly --csv cases\traffic_anomaly\inputs\toronto_traffic_signals_phase_status.csv --out out\traffic_anomaly --status "Green Termination" --tau-global 0.0005
```

### Planck (optional)
```powershell
.\.venv\Scripts\python -m pip install astropy
.\.venv\Scripts\python scripts\fetch_data.py --planck-guide
# (place the FITS at cases\planck70\inputs\LFI_SkyMap_070_1024_R3.00_full.fits)
huf planck --fits cases\planck70\inputs\LFI_SkyMap_070_1024_R3.00_full.fits --out out\planck70 --retained-target 0.97 --nside-out 64
```

---

## macOS / Linux (bash/zsh)

```bash
python3 scripts/bootstrap.py
./.venv/bin/python -m pip install -e .

./.venv/bin/python scripts/fetch_data.py --markham --toronto --yes

./.venv/bin/huf markham --xlsx cases/markham2018/inputs/2018-Budget-Allocation-of-Revenue-and-Expenditure-by-Fund.xlsx --out out/markham2018
./.venv/bin/huf traffic --csv cases/traffic_phase/inputs/toronto_traffic_signals_phase_status.csv --out out/traffic_phase
./.venv/bin/huf traffic-anomaly --csv cases/traffic_anomaly/inputs/toronto_traffic_signals_phase_status.csv --out out/traffic_anomaly --status "Green Termination" --tau-global 0.0005
```

### Makefile (optional convenience)
If you have `make` installed (common on macOS/Linux):
```bash
make fetch-data
```
