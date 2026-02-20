# Long tail (accounting lens)

This page explains why people get excited about “long tail” in HUF — **not** as ML class-imbalance,
but as an **audit + prioritization lens** for real-world distributions:

- budgets (many small line items),
- logs (many small sources),
- exceptions (rare events that concentrate differently).

The key idea:

> In the baseline view, the tail is usually “noise”.  
> In the exception view, the tail can become the story — **non-linearly**.

---

## Traffic Phase vs Traffic Anomaly (baseline P&L → exception-only P&L)

Both cases use the *same CSV*, but they answer different questions:

- **Traffic Phase (baseline):** “What does normal operation look like, and where is most of the mass?”
- **Traffic Anomaly (exception-only):** “Within a specific status, where is the mass now — and what changed?”

Accounting analogy:

- **Traffic Phase = the whole ledger.**  
  Stable allocation across cost centers.
- **Traffic Anomaly = a filtered sub-ledger.**  
  Only refunds / overrides / write-offs / policy exceptions.

Why this matters:

1) **Long-tail reweighting**  
   Many small contributors do not matter… until you filter to a rare event type. Then “the tail” can dominate the review list.

2) **Non-linear concentration**  
   A small share of rows can concentrate into a few regimes (intersections / cost centers) and dominate operational risk.

3) **Auditability**  
   HUF doesn’t just show a chart — it produces an **audit trail** (trace report) you can defend in a review.

---

## The three artifacts to read (always)

Every run produces:

- **Coherence map** (`artifact_1_coherence_map.csv`)  
  “Where the mass is” (ranked regimes; e.g., intersections, funds, namespaces)

- **Active set** (`artifact_2_active_set.csv`)  
  Retained items + global/local shares

- **Trace report** (`artifact_3_trace_report.jsonl`)  
  Provenance: why each item stayed, what it came from, and what got excluded

---

## 60-second long-tail demo (script-first)

This demo runs baseline + exception-only and prints:

- top 10 regimes by `rho_global_post`
- items-to-cover-90%
- discarded budget
- “top regimes changed + concentration increased”

```powershell
.\.venv\Scripts\python scripts/run_long_tail_demo.py --status "Green Termination"
```

If the Toronto CSV is missing, fetch it first:

```powershell
.\.venv\Scripts\python scripts/fetch_data.py --toronto --yes
```

---

## Inspect any run (quick dashboard)

```powershell
.\.venv\Scripts\python scripts/inspect_huf_artifacts.py --out out/traffic_phase
.\.venv\Scripts\python scripts/inspect_huf_artifacts.py --out out/traffic_anomaly
```

What you’re looking for:

- **Top regimes changed:** which regimes enter/exit the top list between baseline and exception
- **Concentration increased:** fewer regimes/items cover 90% (exception views often tighten)
- **Discarded budget:** how much mass was dropped by thresholds (stability sensitivity)

---

## Manual commands (if you prefer explicit runs)

Baseline:

```powershell
.\.venv\Scripts\huf traffic --csv cases/traffic_phase/inputs/toronto_traffic_signals_phase_status.csv --out out/traffic_phase
```

Exception-only:

```powershell
.\.venv\Scripts\huf traffic-anomaly --csv cases/traffic_anomaly/inputs/toronto_traffic_signals_phase_status.csv --out out/traffic_anomaly --status "Green Termination"
```
