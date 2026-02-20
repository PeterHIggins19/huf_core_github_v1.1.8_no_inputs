# Included cases

These cases are **ready-to-run** from a fresh clone.

## Inputs

- ✅ Markham XLSX: shipped in `cases/markham2018/inputs/`
- ✅ Toronto traffic CSV: shipped in `cases/traffic_phase/inputs/` and `cases/traffic_anomaly/inputs/`
- ❌ Planck FITS: **not shipped** (large). Use `.\.venv\Scripts\python scripts/fetch_data.py --planck-guide` for a copy/paste download guide.

## Outputs

- New runs write to `out/` (recommended).
- Each run produces the core artifacts:

  - `artifact_1_coherence_map.csv`
  - `artifact_2_active_set.csv`
  - `artifact_3_trace_report.jsonl`
  - `artifact_4_error_budget.json`
  - plus `meta.json` and `run_stamp.json`

## Quick commands (Windows PowerShell)

Fetch (optional refresh of shipped inputs):

```powershell
.\.venv\Scripts\python scripts/fetch_data.py --markham --toronto --yes
```

Run Markham:

```powershell
.\.venv\Scripts\huf markham --xlsx cases/markham2018/inputs/2018-Budget-Allocation-of-Revenue-and-Expenditure-by-Fund.xlsx --out out/markham2018
```

Run Traffic Phase:

```powershell
.\.venv\Scripts\huf traffic --csv cases/traffic_phase/inputs/toronto_traffic_signals_phase_status.csv --out out/traffic_phase
```

Run Traffic Anomaly:

```powershell
.\.venv\Scripts\huf traffic-anomaly --csv cases/traffic_anomaly/inputs/toronto_traffic_signals_phase_status.csv --out out/traffic_anomaly --status "Green Termination"
```

Planck guide (prints download steps, does **not** download automatically):

```powershell
.\.venv\Scripts\python scripts/fetch_data.py --planck-guide
```

---

## 60-second long-tail demo

```powershell
.\.venv\Scripts\python scripts/run_long_tail_demo.py --status "Green Termination"
```

This runs **Traffic Phase → Traffic Anomaly** and prints “top regimes changed + concentration increased”.

---

## Traffic Phase vs Traffic Anomaly
### A practical “accounting lens” on non-linear + long-tail behavior

**Traffic Phase** and **Traffic Anomaly** use the *same input CSV*, but they answer different questions:

- **Traffic Phase** (baseline): “What does normal operation look like, and where is most of the mass?”
- **Traffic Anomaly** (diagnostic): “Within a specific exception status, where is the mass now — and what changed?”

If you’re coming from accounting, map it like this:

- **Traffic Phase = the whole ledger.**  
  You look at all transactions and build a stable picture of allocation across cost centers.
- **Traffic Anomaly = a filtered sub-ledger.**  
  For example: *only refunds*, *only manual journal entries*, *only write-offs*, or *only policy exceptions*.

Why this is powerful:

1) **Long-tail**: In real systems, you usually have *many small contributors*.  
   Most of them don’t matter operationally — until you filter to a rare event type. Then the “tail” can become the story.

2) **Non-linear**: The impact is not proportional to row counts.  
   A small fraction of records (or a rare status) can concentrate into a few regimes (intersections / cost centers) and dominate your risk or operational burden.

3) **Auditability**: HUF gives you the “where the mass is” ranking *plus* a trace report.  
   That means you can justify **why** “these 12 intersections” or “these 7 accounts” are your top review list, without hand-waving.

**How to use both cases together:**

- Run **Traffic Phase** to establish the stable baseline distribution.
- Run **Traffic Anomaly** for a named status (e.g., `"Green Termination"`) and compare:
  - which regimes jump up the ranking,
  - how concentrated the retained set becomes,
  - and how much mass sits “near tau” (stability sensitivity).

This is the same workflow as: baseline P&L → exception-only P&L → ranked variance review.

For a deeper walkthrough + the “why this works” story, see:
- **Long tail (accounting lens)** → `docs/long_tail_accounting_lens.md`

---

## Verify a run quickly

After any run, check the output folder has at least:

- `run_stamp.json`
- `artifact_1_coherence_map.csv`
- `artifact_2_active_set.csv`

Example:

```powershell
Test-Path out/markham2018/run_stamp.json
Test-Path out/markham2018/artifact_1_coherence_map.csv
```
