# Markham worked example (2018 budget)

[← Back to Cases](cases.md)

This page walks through a **full, reproducible** analysis using the bundled workbook:

- `cases/markham2018/inputs/2018-Budget-Allocation-of-Revenue-and-Expenditure-by-Fund.xlsx`

Goal: show what HUF reveals that a normal “sum + chart” spreadsheet workflow usually hides:
**concentration**, **tail mass**, **stable regime structure**, and **cell-level provenance**.

---

## 1) Run it

Windows PowerShell (from repo root):

```powershell
.\.venv\Scripts\huf markham --xlsx cases/markham2018/inputs/2018-Budget-Allocation-of-Revenue-and-Expenditure-by-Fund.xlsx --out out/markham2018
```

You should see something like:

- `active_set=24`
- `coherence_rows=6`
- `discarded_global≈0.029`

---

## 2) What’s in the input

The adapter reads a simple **fund × account** block from the workbook (units: **k$**):

- accounts: rows 18–38
- funds: columns 1–6
- blanks / zeros are dropped

For the shipped workbook, HUF finds:

- **67** non-zero cells (elements)
- total value in the selected block: **456,172 k$** (≈ **$456.2M**)

---

## 3) The coherence map (fund-level regimes)

Open:

- `out/markham2018/artifact_1_coherence_map.csv`

This answers: **which funds dominate the retained budget**, and **how much tail mass got dropped**.

Interpretation:

- “Share of retained” sums to 1.0 (unity budget after compression).
- “Discarded (k$)” is what was below the global/local thresholds **inside that fund**.
- The **Operating Fund** typically carries the biggest **within-fund tail** (many tiny line items).

---

## 4) The active set (account-level winners)

Open:

- `out/markham2018/artifact_2_active_set.csv`

This answers: **which line-items explain most of the budget**, globally and within each fund.

Two quick “hidden” facts this makes obvious:

- **top 2** line-items cover a huge share of retained spend
- it takes surprisingly few line-items to cover **90%** of the retained budget

That’s a *concentration story* you don’t get from a typical workbook view unless you go hunting.

---

## 5) Provenance: the trace report (the “why” chain)

Open:

- `out/markham2018/artifact_3_trace_report.jsonl`

Each retained item includes the workbook pointer it came from (sheet + cell), so you can audit the pipeline end-to-end.

---

## 6) Stability: how sensitive is the result?

Open:

- `out/markham2018/stability_packet.csv`

Key fields:

- `discarded_frac` ↑ means more aggressive pruning
- `jaccard_vs_base` close to 1.0 means “mostly the same active set”
- `near_tau_count` high means lots of elements hover around the cutoff (more sensitivity)

---

## 7) Explore further (copy/paste)

```powershell
.\.venv\Scripts\python - << 'PY'
import pandas as pd

coh = pd.read_csv("out/markham2018/artifact_1_coherence_map.csv")
active = pd.read_csv("out/markham2018/artifact_2_active_set.csv").sort_values("rank")

# Which funds dominate?
print(coh[["regime_id","rho_global_post","rho_discarded_pre"]].sort_values("rho_global_post", ascending=False))

# How many items cover 90%?
active["cum"] = active["rho_global_post"].cumsum()
print(active.loc[active["cum"] >= 0.90, ["rank","item_id","cum"]].head(1))
PY
```
