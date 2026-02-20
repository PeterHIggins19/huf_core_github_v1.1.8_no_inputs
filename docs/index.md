# Higgins Unity Framework (HUF) — HUF Core docs

HUF Core is a runnable, **artifact-first** toolkit: you run a case, then you read the outputs it produced.

## Where to start

- **Learning Path**: follow the “do-this-next” flow in the left sidebar.  
  → [Learning Path](learning_path.md)
- **Beginner (no Git)**: point-and-click setup, then copy/paste commands.  
  → [Start Here → Zero GitHub Knowledge](get_started_zero_github.md)
- **Developer**: bootstrap a repo venv + run docs locally.  
  → [Start Here → Developer](start_here.md)
- **If anything breaks**: Windows/Conda fixes.  
  → [Troubleshooting](troubleshooting.md)

## One-minute demo (Windows PowerShell)

After you have created the repo virtual environment (`.venv`) and installed dependencies:

```powershell
.\.venv\Scripts\python scripts/fetch_data.py --markham --toronto --yes
.\.venv\Scripts\huf markham --xlsx cases/markham2018/inputs/2018-Budget-Allocation-of-Revenue-and-Expenditure-by-Fund.xlsx --out out/markham2018
.\.venv\Scripts\huf traffic --csv cases/traffic_phase/inputs/toronto_traffic_signals_phase_status.csv --out out/traffic_phase
.\.venv\Scripts\huf traffic-anomaly --csv cases/traffic_anomaly/inputs/toronto_traffic_signals_phase_status.csv --out out/traffic_anomaly --status "Green Termination"
```

Then open:

- `out/markham2018/artifact_1_coherence_map.csv` (regimes)
- `out/markham2018/artifact_2_active_set.csv` (retained set)
- `out/markham2018/artifact_3_trace_report.jsonl` (audit trail)

## Run the docs site locally (Windows)

```powershell
.\.venv\Scripts\python -m mkdocs serve
```

Tip: If copy/paste ever seems “weird” on Windows, prefer **forward slashes** in file paths (e.g., `scripts/fetch_data.py`, `cases/...`) and only use backslashes for the venv executables (e.g., `.\.venv\Scripts\python`).
