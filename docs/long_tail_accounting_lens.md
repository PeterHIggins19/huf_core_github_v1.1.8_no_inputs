\
# Long tail (accounting lens)

**Disambiguation (important):** this is **not** “ML class imbalance.”  
Here **long tail** means **mass distribution + exception reweighting** — the way a budget, ledger, or log stream becomes *more concentrated* when you filter to exceptions.

If you only read one sentence, read this:

> **Baseline view** (everything) can look stable, while an **exception-only view** becomes sharply concentrated — a few regimes dominate and the review list collapses into a small “top K”.

---

## The accounting story in three lines

1) **Baseline P&L (everything):** most activity is “normal,” spread across many lines.  
2) **Exception-only P&L (filtered):** the tail gets reweighted; small categories can become dominant.  
3) **Ranked variance review:** you review the few items/regimes that explain most of the post-normalized mass.

This is the exact reason Traffic Phase vs Traffic Anomaly is such a good teaching pair.

---

## Why “long tail” matters operationally

In day-to-day operations you want two things at once:

- **Compression:** reduce thousands of lines to a few lines you can actually review.
- **Auditability:** prove where the mass went and why something is retained/discarded.

Long-tail behavior is what makes this hard:

- the baseline distribution is often diffuse (many contributors),
- but exceptions create **non-linear concentration** (a few contributors dominate),
- and naive filtering destroys auditability (“why did we lose 70% of the rows?”).

HUF’s contract is designed to keep this honest.

---

## Traffic Phase vs Traffic Anomaly (the cleanest demo)

### What each command means

- **Traffic Phase** = baseline, “all rows” view (like baseline P&L)
- **Traffic Anomaly** = exception-only view (like exception-only P&L)

For Toronto traffic data:

- baseline: all phase status rows
- anomaly: only rows where `PHASE_STATUS_TEXT == "Green Termination"` (or any status you choose)

### Run the 2‑minute long-tail demo (script-first)

```powershell
.\.venv\Scripts\python scripts/run_long_tail_demo.py --status "Green Termination"
```

This runs **Traffic Phase → Traffic Anomaly**, then prints:

- `Top-10 regimes changed ...`
- **PROOF line:** `items_to_cover_90pct baseline -> exception`
- and (if present) discarded budget diagnostics

**Why the proof line is powerful:**

- `items_to_cover_90pct` answers:  
  “How many retained items explain 90% of the post-normalized mass?”

So when you see something like:

- `PROOF: items_to_cover_90pct 37 -> 12`

you can say (truthfully):

> The exception-only view is **more concentrated**: fewer items explain most of the mass.

That’s long-tail reweighting in one number people can repeat.

---

## How to read the artifacts like an accountant

Every run yields an output folder (e.g. `out/traffic_anomaly_demo/`) with the contract artifacts:

- **Coherence map** — `artifact_1_coherence_map.csv`
- **Active set** — `artifact_2_active_set.csv`
- **Trace report** — `artifact_3_trace_report.jsonl`
- **Error budget** — `artifact_4_error_budget.json` (if emitted)

### 1) Coherence map = “where the budget went”
Open `artifact_1_coherence_map.csv` and sort by `rho_global_post` descending.

You are looking for:

- the **top regimes** (dominant categories)
- how quickly the cumulative share rises (concentration across regimes)
- any regime whose share jumps significantly in the anomaly run

Accounting translation:

- regime ≈ account group / cost center / source / namespace
- `rho_global_post` ≈ “share of the retained (post-pruned) unity budget”

### 2) Active set = “the review list”
Open `artifact_2_active_set.csv` and sort by `rho_global_post` descending.

This is your **ranked variance review list**.

Two practical views:

- **Global triage:** sort by `rho_global_post` (top items overall)
- **Within-regime triage:** filter to one regime, sort by `rho_local_post` (top items inside that regime)

Accounting translation:

- item ≈ transaction line / vendor / document chunk / event id
- `rho_global_post` ≈ “how important is this item overall, after pruning?”
- `rho_local_post` ≈ “how dominant is this item within its regime?”

### 3) Trace report = “how you defend the result”
Open `artifact_3_trace_report.jsonl` when someone asks:

- “Why is this item in the active set?”
- “What input rows produced this?”
- “What was excluded and why?”

Think of the trace report as the supporting workpapers.

### 4) Error budget = “how much you threw away”
If present, open `artifact_4_error_budget.json`.

Look for a field like:

- `discarded_budget_global`

Accounting translation:

- discarded budget ≈ “how much mass we excluded from the review list”
- This makes pruning explicit and defensible.

---

## Non-linear + long-tail: the key intuition (in accounting terms)

### Baseline P&L is not the whole story
A baseline report often has many “small lines” that collectively add up, but individually don’t matter.

### Exception-only P&L changes the weights
Filtering to exceptions does **two things**:

1) It removes a big chunk of baseline mass (normal activity).  
2) It **renormalizes** what remains — the remaining items get larger shares because the budget is re-scaled to 1.0.

This is why concentration can increase dramatically:
- not because the world changed,
- but because your **review lens** changed.

### Ranked variance review is the operational goal
You want a short list you can investigate:

- “Top regimes changed”
- “Top items explain most of the mass”
- “Here’s the trace to justify each retained item”
- “Here’s the declared discarded budget”

That’s the HUF pattern.

---

## Quick “reviewer checklist” (what good looks like)

After running baseline + exception:

1) Coherence map: do the top regimes make sense?
2) Active set: is your review list small enough to act on?
3) Proof line: did `items_to_cover_90pct` shrink in the exception view?
4) Trace: can you defend one retained item end-to-end?
5) Error budget: is the discarded mass declared and acceptable?

---

## If you want the formal math

For equations, fixed points, and information-theory measures (entropy, KL divergence), see:

- **Higgins Unity Framework: Mathematical form and function** (`docs/huf_math_form_and_function.md`)
