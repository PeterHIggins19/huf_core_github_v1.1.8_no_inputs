# Traffic Phase worked example (Toronto signals)

[← Back to Cases](cases.md)

This page is a **guided artifact-reading flow** for the Traffic Phase case:

- `cases/traffic_phase/inputs/toronto_traffic_signals_phase_status.csv`

Goal: show what HUF reveals that a typical “count rows / pivot table” workflow usually hides:
**a ranked, auditable “where the mass is” map**, **per-intersection signatures**, and **stable compression knobs (tau)**.

---

## 1) Run it

Windows PowerShell (from repo root):

```powershell
.\.venv\Scripts\huf traffic --csv cases/traffic_phase/inputs/toronto_traffic_signals_phase_status.csv --out out/traffic_phase
```

---

## 2) What’s in the input

HUF expects a **Toronto traffic phase status** CSV with at least:

- `TCS` (signal controller / intersection id)
- `PHASE` (phase number)

---

## 3) What the adapter does (finite elements)

The Traffic Phase adapter compresses raw rows into **finite elements**:

- **Regime (group):** `TCS=` (one regime per intersection)
- **Element (inside a regime):** `PHASE_BAND=`

Where `PHASE_BAND` is a deliberate, human-readable grouping:

- `MajorEven(2,4,6,8)`
- `MinorOdd(1,3,5,7)`
- `Other(9-12)`

So each intersection becomes a 2–3 element “signature vector”:

```
TCS= -> [MajorEven share, MinorOdd share, Other share]
```

---

## 4) The outputs (what to open first)

A run writes to `out/traffic_phase/`:

1) `artifact_1_coherence_map.csv` — **Intersection ranking** (one row per `TCS`) + discard reporting  
2) `artifact_2_active_set.csv` — **Retained elements** (bands that survived tau)  
3) `artifact_3_trace_report.jsonl` — **Provenance chain** (how each item was formed)  
4) `artifact_4_error_budget.json` — single-number discard summary  
5) `stability_packet.csv` — small sweep showing sensitivity to tau

---

## 5) Next step: the diagnostic lens (Traffic Anomaly)

Traffic Phase is the **baseline** case. The anomaly case is the **exception** case.

**Accounting analogy:**

- Traffic Phase = whole ledger (stable allocation picture)
- Traffic Anomaly = filtered sub-ledger (refunds / overrides / exceptions)

Run it:

```powershell
.\.venv\Scripts\huf traffic-anomaly --csv cases/traffic_anomaly/inputs/toronto_traffic_signals_phase_status.csv --out out/traffic_anomaly --status "Green Termination"
```

What to look for:

- Do the top regimes change (which intersections jump up)?
- Does concentration increase (fewer regimes explain most mass)?
- Does the long tail shrink or expand inside the exception status?

That’s the “non-linear + long-tail” story: rare events often re-weight the system in ways that a baseline pivot table won’t show clearly.
