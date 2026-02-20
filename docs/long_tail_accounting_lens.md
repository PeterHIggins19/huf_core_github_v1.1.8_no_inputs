# Long tail (accounting lens)

**Two-line disambiguation (for skimmers):**

- Not ML class imbalance. Here “long tail” means **mass distribution + exception reweighting** (baseline vs filtered view).  
- In practice: **baseline ledger → exception-only sub-ledger → ranked variance review**.

HUF makes that workflow reproducible by writing artifacts (CSVs/JSON) that answer:

- **Where is the mass?** (coherence map)
- **What do we keep for review?** (active set)
- **What did we discard, explicitly?** (error budget)
- **Why did this row/item survive?** (trace)

---

## Why the “tail” becomes the story

### 1) Long-tail reweighting

In a baseline ledger, most categories look “small” and ignorable.

But the moment you filter to a **rare event type** (exceptions), the distribution reweights:

- a small set of rows can dominate the review list
- regimes you barely noticed can become the story

This is the accounting intuition behind “the long tail”: **exceptions make the tail visible**.

### 2) Non-linear concentration

Filtering is non-linear.

When you discard rows (tighten the review boundary), probability mass doesn’t shrink uniformly — it **concentrates**.

HUF exposes this concentration with one repeatable headline:

> `items_to_cover_90pct = k`  
> The top **k retained items** explain **90%** of post-normalized mass.

Smaller `k` ⇒ more concentrated ⇒ a tiny set dominates.

### 3) Auditability

Exception review is only useful if you can defend it.

HUF provides:

- a regime ranking (who dominates)
- a ranked review list (what to look at first)
- a discard ledger (what was dropped, and how much “budget” that represents)
- a trace report (why retained)

---

## Traffic Phase vs Traffic Anomaly

This is the simplest “accounting-style” teaching example in the repo.

### Baseline view (Traffic Phase)

Traffic Phase is like baseline P&L:

- you observe routine operations
- mass is spread across many rows
- the “tail” looks harmless

### Exception view (Traffic Anomaly)

Traffic Anomaly is like exception-only P&L:

- you filter to a rare/important condition (an anomaly)
- the distribution reweights
- mass concentrates into fewer regimes/items

### Ranked variance review

Once you have baseline and exception views, the operational question is:

> **What changed the most, and where should we look first?**

HUF’s artifacts answer that with ranking + a proof line.

---

## Two-minute demo (script-first, Windows-safe)

!!! warning "Run in PowerShell (not inside Python)"
    If your prompt shows `>>>`, exit Python with `exit()`.

```powershell
.\.venv\Scripts\python scripts/run_long_tail_demo.py --status "Green Termination"
```

What the demo does:

1) Runs **Traffic Phase** (baseline)
2) Runs **Traffic Anomaly** (exception)
3) Prints a repeatable summary you can paste into an email/issue

Look for these lines:

- `Top regimes changed: ...`  
- `PROOF: Concentration increased: items_to_cover_90pct X -> Y`

Interpretation:

- **Top regimes changed**: your exception filter changed “who dominates”
- **Concentration increased** (Y smaller): the exception view is dominated by fewer items → higher operational risk if those items are wrong/stale

---

## Accounting example (same pattern, different nouns)

Imagine an accounts payable ledger.

### Baseline ledger (monthly close)

Rows: all invoices.  
Regimes: cost center, vendor, GL account.

You expect dispersion: many vendors, many cost centers.

### Exception-only sub-ledger (audit filter)

Filter rows to:

- invoices above a threshold
- invoices with a policy exception code
- invoices paid outside terms

Now the tail becomes visible:

- a “small” vendor becomes dominant
- one cost center suddenly explains most of the exception mass

### Ranked variance review (what to inspect first)

You don’t want a spreadsheet you scroll.

You want:

- **regime ranking** (who dominates exceptions)
- **active set** (which invoices dominate)
- **discard ledger** (what got dropped, explicitly)

That’s exactly what HUF writes.

---

## What to look for in the artifacts

This is the “open in Excel and circle the row” guide.

### artifact_1_coherence_map.csv (regime ranking)

Sort by `rho_global_post` descending.

Watch for:

- top regime > 0.50 (dominance)
- top 2–3 regimes cover most of mass (concentration by group)

### artifact_2_active_set.csv (ranked review list)

Sort by `rho_global_post` descending.

This is your global review list.

Then filter by `regime_id` and sort by `rho_local_post` for “top inside regime.”

### artifact_4_error_budget.json (declared discards)

Find:

- `discarded_budget_global` (or similarly named key)

This is the explicit “what we dropped” ledger.

If discarded budget is large, your threshold is aggressively pruning.

---

## Make it future-proof (how teams extend this)

Once a team “gets” this page, they usually want:

1) **Multi-run drift**
   - run daily/weekly on the same queries
   - track top regimes and `items_to_cover_90pct` over time

2) **Two-tau sensitivity**
   - run tau A vs tau B
   - print “concentration increased” as a regression guardrail

3) **Compliance / isolation checks**
   - treat tenant/namespace as regimes
   - detect dominance bleed across boundaries

If you’re already using the Vector DB coherence adapter, this is the same mental model — only the nouns change.

See also:

- `vector_db_coherence.md` (regimes, artifacts, and the same “proof line”)
- `math_form_and_function.md` (equations + column mapping)
