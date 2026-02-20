\
# CLI: HUF command lists, labels, terminology

This page is a “single place” to answer:
- what commands exist,
- what files they expect,
- what artifacts they emit,
- and what words mean (regime, τ, active set…).

## Windows/Conda rule (copy/paste reliability)

After the repo venv exists, **always** run tools via the repo executables:

```powershell
.\.venv\Scripts\python -V
.\.venv\Scripts\huf --help
.\.venv\Scripts\python -m mkdocs serve
```

For file paths inside commands and docs, prefer **forward slashes**:
- ✅ `scripts/fetch_data.py`
- ✅ `cases/traffic_phase/inputs/...`
- Only use backslashes for the venv executables: `.\.venv\Scripts\python`

## 1) Discover commands (don’t guess)

Canonical command lists come from `--help`:

```powershell
.\.venv\Scripts\huf --help
.\.venv\Scripts\huf traffic --help
.\.venv\Scripts\huf traffic-anomaly --help
```

If a flag name differs between versions, **trust `--help`** over any doc page.

## 2) Commands in this repo (common entry points)

### `huf markham` (budget allocation workbook → UBH artifacts)
**Input:** an XLSX workbook fetched by `scripts/fetch_data.py --markham`  
**Typical:**
```powershell
.\.venv\Scripts\huf markham --xlsx cases/markham2018/inputs/2018-Budget-Allocation-of-Revenue-and-Expenditure-by-Fund.xlsx --out out/markham2018
```

### `huf traffic` (phase status table → baseline coherence)
**Input:** CSV fetched by `scripts/fetch_data.py --toronto --yes`  
**Typical:**
```powershell
.\.venv\Scripts\huf traffic --csv cases/traffic_phase/inputs/toronto_traffic_signals_phase_status.csv --out out/traffic_phase
```

### `huf traffic-anomaly` (exception view + hotspots)
**Input:** CSV fetched by `scripts/fetch_data.py --toronto --yes`  
**Typical:**
```powershell
.\.venv\Scripts\huf traffic-anomaly --csv cases/traffic_anomaly/inputs/toronto_traffic_signals_phase_status.csv --out out/traffic_anomaly --status "Green Termination" --tau-global 0.0005
```

### `huf planck` (HEALPix FITS → energy-budget run)
**Input:** FITS file placed under `cases/planck70/inputs/` (guided)  
**Typical:**
```powershell
.\.venv\Scripts\python scripts/fetch_data.py --planck-guide
.\.venv\Scripts\huf planck --fits cases/planck70/inputs/YOUR_70GHZ_MAP.fits --out out/planck70
```

## 3) Common flags (pattern-level, not exhaustive)

| Flag | Meaning | Notes |
|---|---|---|
| `--out PATH` | Output folder for the run | Always produce a new folder per run when comparing |
| `--tau-global FLOAT` | Global exclusion threshold τ | Often used to make tail behavior explicit |
| `--tau-local FLOAT` | Local (regime-level) threshold τ | Useful when regimes have very different scales |
| `--status "TEXT"` | Filter condition (traffic anomaly) | Exception view = “rare event type” |
| `--csv PATH` / `--xlsx PATH` / `--fits PATH` | Input type + path | Command-dependent |

Again: run `.\.venv\Scripts\huf <cmd> --help` for the authoritative list.

## 4) Output artifacts (the contract)

Every valid HUF run emits the “contract artifacts” in the run output folder:

- `artifact_1_coherence_map.csv`  
  “Where the budget went” by regime (ranked).
- `artifact_2_active_set.csv`  
  The retained set (what survived exclusion), with shares/ranks.
- `artifact_3_trace_report.jsonl`  
  Line-by-line trace records (why each retained row exists).
- `artifact_4_error_budget.json`  
  Explicit discarded budget + summary diagnostics.

If any of these are missing, treat the run as **non-auditable**.

## 5) Labels and columns you’ll see a lot

The exact column list depends on the adapter, but common meanings:

- `rho_*` columns: a unity-budget share (mass or energy)
  - `rho_global_*`: share in the global distribution
  - `rho_local_*`: share within a regime
- `rank`: descending sort position (largest share first)
- `regime_id` / `regime_label`: grouping identity
- `item_id` / `element_id`: finite element identity

## 6) Terminology (plain-English)

- **Finite element**: smallest auditable unit you agree to defend (row, pixel, log event).
- **Regime**: named grouping (nestable) used to interpret where mass went.
- **Unity budget**: the “sum must be 1.0” invariant after normalization.
- **Coherence map**: regime-level share table (“who dominates”).
- **Active set**: the retained items after exclusion (the set you can justify).
- **Trace report**: the audit trail from outputs back to inputs.
- **τ (tau)**: exclusion threshold; makes long-tail behavior explicit.
- **Discarded budget**: the mass you threw away (must be explicit and reported).

## 7) Helper scripts (artifact inspection)

This repo also includes script-first helpers (Windows-friendly) to inspect runs.

If you have:
- `scripts/run_long_tail_demo.py` — runs Traffic Phase → Traffic Anomaly and prints the “PROOF” headline
- `scripts/inspect_huf_artifacts.py` — prints a quick dashboard for any `out/...` folder

Run them via the venv Python:
```powershell
.\.venv\Scripts\python scripts/run_long_tail_demo.py --status "Green Termination"
.\.venv\Scripts\python scripts/inspect_huf_artifacts.py --out out/traffic_anomaly
```

## Next
- If you want the formal math spine behind these terms, see:
  - **Mathematical form and function** (`docs/huf_math_form_and_function.md`)
