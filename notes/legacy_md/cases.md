# Included cases

These cases are ready-to-run from a fresh clone.

## Quick commands (Windows PowerShell)

```powershell
.\.venv\Scripts\python scripts/fetch_data.py --markham --toronto --yes

.\.venv\Scripts\huf markham --xlsx cases/markham2018/inputs/2018-Budget-Allocation-of-Revenue-and-Expenditure-by-Fund.xlsx --out out/markham2018
.\.venv\Scripts\huf traffic --csv cases/traffic_phase/inputs/toronto_traffic_signals_phase_status.csv --out out/traffic_phase
.\.venv\Scripts\huf traffic-anomaly --csv cases/traffic_anomaly/inputs/toronto_traffic_signals_phase_status.csv --out out/traffic_anomaly --status "Green Termination"
```

---

## Two-minute long-tail demo

```powershell
.\.venv\Scripts\python scripts/run_long_tail_demo.py --status "Green Termination"
```

Look for:

- `PROOF: items_to_cover_90pct 37 -> 12` (example)

---

## Traffic Phase vs Traffic Anomaly (accounting lens)

**Not ML class imbalance:** here “long tail” means **mass distribution + exception reweighting** (baseline vs filtered view).

Full explainer:
- [Long tail (accounting lens)](long_tail_accounting_lens.md)
