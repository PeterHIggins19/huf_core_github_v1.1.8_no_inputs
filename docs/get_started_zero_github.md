HUF-DOC: HUF.REL.DOCS.PAGE.GET_STARTED_ZERO_GITHUB | HUF:1.1.8 | DOC:v0.1.0 | STATUS:release | LANE:release | RO:Peter Higgins
CODES: DOCS | ART: CM, AS, TR, EB | EVID:E1 | POSTURE:OP | WEIGHTS: OP=0.80 TOOL=0.20 PEER=0.00 | CAP: OP_MIN=0.51 TOOL_MAX=0.49 | CANON:docs/get_started_zero_github.md

# Start Here (Zero GitHub Knowledge)

You can run HUF without learning command-line git.

The goal is:

- you can run `.\.venv\Scripts\huf --help`
- you can produce `out/.../run_stamp.json`

## Option 1 — easiest (recommended): the one-click starter

From the repo folder:

- Windows: double-click `START_HERE_WINDOWS.bat`
- macOS: right-click `START_HERE_MAC.command` → **Open**
- Linux: `./start_here_linux.sh`

This creates a local `.venv` and installs what you need.

## Option 2 — manual (Windows PowerShell)

From the repo root:

### 1) Create a repo virtual environment

> If you plan to run the docs locally, install `.[dev,docs]` (MkDocs is pinned in the `docs` extra).

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip setuptools wheel
.\.venv\Scripts\python -m pip install -e ".[dev,docs]"
```

### 2) Fetch the civic inputs (Markham + Toronto)

```powershell
.\.venv\Scripts\python scripts/fetch_data.py --markham --toronto --yes
```

### 3) Run the demo cases

```powershell
.\.venv\Scripts\huf markham --xlsx cases/markham2018/inputs/2018-Budget-Allocation-of-Revenue-and-Expenditure-by-Fund.xlsx --out out/markham2018
.\.venv\Scripts\huf traffic --csv cases/traffic_phase/inputs/toronto_traffic_signals_phase_status.csv --out out/traffic_phase
.\.venv\Scripts\huf traffic-anomaly --csv cases/traffic_anomaly/inputs/toronto_traffic_signals_phase_status.csv --out out/traffic_anomaly --status "Green Termination"
```

### 4) Preview the docs locally (optional)

Always run MkDocs through the repo venv:

```powershell
.\.venv\Scripts\python -m mkdocs serve
```

## Important Windows note: slashes

- Use **forward slashes** for file paths in docs and commands: `scripts/fetch_data.py`, `cases/...`, `out/...`
- Use backslashes only for the venv executables: `.\.venv\Scripts\python`, `.\.venv\Scripts\huf`
