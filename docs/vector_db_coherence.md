# Vector DB coherence (from retrieval results)

This adapter turns **retrieval results** into a HUF run so you can audit **composition** (not just “quality”):

- **Regime dominance:** which namespace / collection / tenant / source dominates the kept set
- **Concentration:** do a few items explain most of the kept mass?
- **Declared discards:** what fell below threshold, and how much mass was discarded (no silent drops)
- **Trace:** why an item is retained (provenance + reasoning)

> No live vector DB required. You provide a JSONL/CSV/TSV export of retrieval results.

**Disambiguation:** this is *not* “ML class imbalance.”  
Here “long tail” means **mass distribution + exception reweighting** — exactly how logs/ledgers/budgets become more concentrated when you filter to exceptions.

!!! warning "PowerShell vs Python: run commands in the shell"
    If your prompt looks like `>>>`, you are **inside Python**.  
    Exit back to PowerShell with **`exit()`** (or **Ctrl+Z then Enter**), then run the commands below.

---

## Start here

If you want the shortest entry, see:

- **Vector DB coherence adapter (one-page brief)**: `vector_db_coherence_one_pager.md`

If you want the full walkthrough and “what to look for,” you are on the right page.

---

## When to use this

Use this when you want to answer questions like:

- “Are results dominated by one namespace / one tenant / one collection?”
- “Is my retrieval **too concentrated** (a tiny set dominates)?”
- “After filtering to an exception (one tenant/namespace), did the ranking regime change?”
- “If I tighten the threshold, does concentration increase?”

This pairs naturally with **Traffic Phase vs Traffic Anomaly** (teaches baseline → exception-only → ranked review).  
It also pairs with **Long tail (accounting lens)**: baseline view → exception view → ranked variance review.

---

## Concepts (the minimum you need)

### Regimes
A **regime** is the grouping you care about: `namespace`, `collection`, `tenant`, `source`, etc.

You choose it via `--regime-field`.

### Tau (global threshold)
`--tau-global` sets the discard boundary in the **mass** frame.

- Larger `tau` = stricter threshold = more discards (often *more concentration*)
- Smaller `tau` = looser threshold = fewer discards (often *less concentration*)

### The proof line: items_to_cover_90pct
`items_to_cover_90pct = k` means:

> The **top k retained items** explain **90%** of the post-normalized mass.

Smaller `k` ⇒ more concentrated ⇒ a tiny set dominates retrieval.

---

## Input format (JSONL)

One JSON object per line.

### Required fields

- `id` (string): unique item id (document id, chunk id, ticket id, etc.)
- `score` (number): similarity / relevance score (**higher = better**)

### Optional fields (regimes)

Include any grouping fields you want to audit by, e.g.:

- `namespace`
- `collection`
- `source`
- `tenant`
- `index`

Example (`cases/vector_db/inputs/retrieval.jsonl`):

```json
{"id":"doc_001","score":0.82,"namespace":"kb","source":"handbook"}
{"id":"doc_002","score":0.63,"namespace":"kb","source":"manual"}
{"id":"doc_101","score":0.77,"namespace":"tickets","source":"ops"}
{"id":"doc_102","score":0.12,"namespace":"tickets","source":"ops"}
```

---

## 60-second run (Windows PowerShell)

PowerShell note: use **backticks** for line continuation (not `\`).

```powershell
$py  = ".\.venv\Scripts\python.exe"
$in  = "cases/vector_db/inputs/retrieval.jsonl"
$out = "out/vector_db_demo"

New-Item -ItemType Directory -Force (Split-Path $in) | Out-Null
New-Item -ItemType Directory -Force $out | Out-Null

@'
{"id":"doc_001","score":0.82,"namespace":"kb","source":"handbook"}
{"id":"doc_002","score":0.63,"namespace":"kb","source":"manual"}
{"id":"doc_101","score":0.77,"namespace":"tickets","source":"ops"}
{"id":"doc_102","score":0.12,"namespace":"tickets","source":"ops"}
'@ | Set-Content -Encoding utf8 $in

& $py examples/run_vector_db_demo.py `
  --in $in `
  --out $out `
  --tau-global 0.02 `
  --regime-field namespace

& $py scripts/inspect_huf_artifacts.py --out $out
```

Expected console output looks like:

```text
[tail] items_to_cover_90pct=3

Top regimes by rho_global_post:
  1. kb       rho_post=0.619658
  2. tickets  rho_post=0.380342
```

Interpretation:

- `kb` dominates (~62%) but `tickets` is still significant (~38%).
- `items_to_cover_90pct=3` ⇒ **high concentration** (top 3 retained items explain 90% of mass).

---

## Two-tau delta (the repeatable headline)

Sometimes you want one line a teammate can repeat:

> **Concentration increased: items_to_cover_90pct X -> Y**

Run the same input twice (tau A and tau B):

```powershell
$py  = ".\.venv\Scripts\python.exe"
$in  = "cases/vector_db/inputs/retrieval.jsonl"
$out = "out/vector_db_delta"

& $py scripts/run_vector_db_concentration_delta.py `
  --in $in `
  --out $out `
  --tau-a 0.005 `
  --tau-b 0.02 `
  --regime-field namespace
```

Example headline output:

```text
Concentration increased: items_to_cover_90pct 37 -> 12
```

Interpretation: fewer retained items explain 90% of post-normalized mass (**more concentrated**).

---

## Artifacts (the contract)

A valid run folder should contain at least:

- `artifact_1_coherence_map.csv` (regime ranking)
- `artifact_2_active_set.csv` (retained items)
- `artifact_4_error_budget.json` (declared discards)

Optional but strongly recommended:

- `artifact_3_trace_report.jsonl` (why retained)
- `meta.json`, `run_stamp.json`

---

## How to read the artifacts (screenshot-style walkthrough)

Think of this as “what you would point at on a screenshot.”

### Step 0 — sanity check

In File Explorer (or `dir`), confirm the contract files exist.  
If any are missing, treat the run as **not comparable**.

### Step 1 — `artifact_1_coherence_map.csv` (regime ranking)

Open in Excel and sort **descending** by `rho_global_post`.

You’re looking for rows like:

- `regime_id` (e.g., `kb`, `tickets`)
- `rho_global_post` (post-normalized mass share)

What to look for:

- **Dominance:** does the top regime exceed 0.50?
- **Regime concentration:** do top 2–3 regimes cover most of the mass?
- **Tail cut:** if discard columns exist, did one regime lose far more than others?

This answers: **“Which groups dominate my retrieval results?”**

### Step 2 — `artifact_2_active_set.csv` (the ranked review list)

Open in Excel and sort **descending** by `rho_global_post`.

What to do:

- Sort by `rho_global_post` ⇒ global “review list”
- Filter to one `regime_id`, then sort by `rho_local_post` ⇒ top items *within* a regime

This answers: **“Which retained items matter most overall, and within each regime?”**

### Step 3 — `artifact_4_error_budget.json` (declared discards)

Open the JSON and look for:

- `discarded_budget_global` (or similar key)

This answers: **“How much mass did we discard, explicitly?”**  
If this is large, your threshold is doing substantial pruning.

### Step 4 — `artifact_3_trace_report.jsonl` (why retained)

Use this when someone asks:

- “Why did this item make the cut?”
- “Which fields influenced grouping / trace?”

This is the audit trail.

---

## Common patterns (what you’ll see in real systems)

- **Tenant bleed / namespace monopoly:** one regime quietly dominates most results.
- **Over-concentration:** `items_to_cover_90pct` becomes very small (risk: staleness of top chunks).
- **Regime drift:** top regime changes after filtering, or over time (new content, new index behavior).
- **Tail collapse under strict tau:** tightening `tau` shrinks the review list sharply.

---

## Common issues

### “I typed `huf traffic ...` and got `SyntaxError`”

If you see:

- `>>> huf traffic ...`
- `SyntaxError: invalid syntax`

…you typed a **shell command inside Python**.

Fix: exit Python (`exit()`), then run in PowerShell:

```powershell
.\.venv\Scripts\huf traffic --csv cases/traffic_phase/inputs/toronto_traffic_signals_phase_status.csv --out out/traffic_phase
```

### “My scores are distances (lower is better)”

HUF assumes **higher score = better**. If your tool emits distance where lower is better, transform it *explicitly* before auditing, e.g.:

- `score = 1 / (1 + distance)`
- or `score = -distance` (only if your adapter allows negatives)

Keep the transform explicit so the audit trail stays honest.

---

## Where this goes next (future interest)

If you care about this topic long-term, the natural next steps are:

- **Multi-run comparisons:** compare yesterday vs today (regime drift, concentration drift).
- **Per-tenant audit packs:** same query across tenants → detect isolation failures.
- **Evaluation hooks:** run coherence after each retrieval call in CI (regression detection).
- **Math appendix mapping:** jump from formula → artifact column (e.g., `rho_global_post`).

See also:

- **HUF math form and function** (derivations + column mapping)
- **Long tail (accounting lens)** (baseline → exception-only → ranked variance review)
