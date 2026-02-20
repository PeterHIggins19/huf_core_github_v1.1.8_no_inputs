# Quick Run (copy/paste)

This page is the fastest way to get a successful run on **Windows + Conda**.

## 1) Bootstrap the repo venv

From the repo root (the folder that contains `pyproject.toml`):

```powershell
python scripts/bootstrap.py
```

Confirm you are using the repo venv:

```powershell
.\.venv\Scripts\python -V
.\.venv\Scripts\huf --help
```

## 2) Fetch inputs (Markham + Toronto)

```powershell
.\.venv\Scripts\python scripts/fetch_data.py --markham --toronto --yes
```

## 3) Run the two core demos

```powershell
.\.venv\Scripts\huf markham --xlsx cases/markham2018/inputs/2018-Budget-Allocation-of-Revenue-and-Expenditure-by-Fund.xlsx --out out/markham2018
.\.venv\Scripts\huf traffic --csv cases/traffic_phase/inputs/toronto_traffic_signals_phase_status.csv --out out/traffic_phase
```

## 4) Run the diagnostic demo (Traffic Anomaly)

```powershell
.\.venv\Scripts\huf traffic-anomaly --csv cases/traffic_anomaly/inputs/toronto_traffic_signals_phase_status.csv --out out/traffic_anomaly --status "Green Termination"
```

## 5) Preview the docs site locally

Always run MkDocs via the repo venv:

```powershell
.\.venv\Scripts\python -m mkdocs serve
```

Optional strict check (useful before a commit):

```powershell
.\.venv\Scripts\python -m mkdocs build --strict
```

## Notes

- Prefer **forward slashes** in file paths (`cases/...`, `scripts/fetch_data.py`). Windows PowerShell accepts them and it avoids `\t` / `\f` escape surprises in YAML and other contexts.
- If `python` is not found, try `py -3 scripts/bootstrap.py` instead.
