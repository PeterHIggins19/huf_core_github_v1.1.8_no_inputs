# Quick Run (copy/paste)

Goal: create a local `.venv`, fetch inputs, and run the included demos.

> Run these commands from the repo root (the folder that contains `pyproject.toml`).

---

## Windows (PowerShell)

### 1) Bootstrap + install

```powershell
python scripts/bootstrap.py
.\.venv\Scripts\python -m pip install -e .
```

### 2) Fetch Markham + Toronto inputs

```powershell
.\.venv\Scripts\python scripts/fetch_data.py --markham --toronto --yes
```

### 3) Run the demos

```powershell
.\.venv\Scripts\huf markham --xlsx cases/markham2018/inputs/2018-Budget-Allocation-of-Revenue-and-Expenditure-by-Fund.xlsx --out out/markham2018
.\.venv\Scripts\huf traffic --csv cases/traffic_phase/inputs/toronto_traffic_signals_phase_status.csv --out out/traffic_phase
.\.venv\Scripts\huf traffic-anomaly --csv cases/traffic_anomaly/inputs/toronto_traffic_signals_phase_status.csv --out out/traffic_anomaly --status "Green Termination" --tau-global 0.0005
```

### 4) Two-minute long-tail demo (recommended)

```powershell
.\.venv\Scripts\python scripts/run_long_tail_demo.py --status "Green Termination"
```

### 5) Docs site (local)

Always:

```powershell
.\.venv\Scripts\python -m mkdocs serve
```

Strict check:

```powershell
.\.venv\Scripts\python -m mkdocs build --strict
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
