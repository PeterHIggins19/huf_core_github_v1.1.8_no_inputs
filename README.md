# HUF Core Snapshot (v1.1.8)

**HUF is an artifact-first compression + audit framework for long-tail distributions** (budgets, logs, exceptions).

It produces three “review-first” artifacts on every run:

- **Coherence map** (`artifact_1_coherence_map.csv`) — *where the mass is* (ranked regimes)
- **Active set** (`artifact_2_active_set.csv`) — retained items + global/local shares
- **Trace report** (`artifact_3_trace_report.jsonl`) — provenance + “why it stayed”

Docs site: https://peterhiggins19.github.io/huf_core_github_v1.1.8_no_inputs/

---

## 60-second long-tail demo (Windows/Conda copy/paste)

This runs **Traffic Phase** (baseline) then **Traffic Anomaly** (exception-only) and prints:

- top regimes by `rho_global_post` (top 10)
- “items to cover 90%”
- discarded budget
- “top regimes changed + concentration increased” summary

```powershell
python scripts/bootstrap.py
.\.venv\Scripts\python scripts/fetch_data.py --toronto --yes
.\.venv\Scripts\python scripts/run_long_tail_demo.py --status "Green Termination"
```

Outputs are written to:

- `out/traffic_phase_demo/`
- `out/traffic_anomaly_demo/`

Quick inspect any run:

```powershell
.\.venv\Scripts\python scripts/inspect_huf_artifacts.py --out out/traffic_anomaly_demo
```

More explanation (accounting lens): `docs/long_tail_accounting_lens.md`

---

## New to GitHub?

If you’re starting from **zero GitHub knowledge**, begin here:

- **Start here (MkDocs page):** `docs/get_started_zero_github.md`

One‑click setup scripts (repo root):

- Windows: `START_HERE_WINDOWS.bat`
- macOS: `START_HERE_MAC.command`
- Linux: `start_here_linux.sh`

These create a local Python environment, install dependencies, and can fetch **Markham + Toronto** inputs.

Planck is guided/manual because the FITS files are very large.

---

## What’s in this repo

Start with:

1) **Handbook**: `docs/handbook.md`  
2) **Reference Manual**: `docs/reference_manual.md`  
3) **Cases**: `cases/*`

### DOCX exports (record-keeping)

For users who aren’t GitHub-native, this release also includes **DOCX** copies of key docs (generated from the Markdown sources):

- `docs/handbook.docx`
- `docs/reference_manual.docx`
- `docs/data_sources.docx`
- `docs/gui_quickstart.docx`

### Inputs policy

Upstream inputs (Planck FITS / Markham workbook / Toronto traffic CSV) are **real public data** and may be **not bundled**.
See `DATA_SOURCES.md` for download locations and expected paths.
