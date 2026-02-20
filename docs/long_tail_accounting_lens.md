# Long tail (accounting lens)

**Not ML class imbalance:** here “long tail” means **mass distribution + exception reweighting** (baseline vs filtered view).  
In practice: baseline ledger → exception-only sub-ledger → ranked variance review.

---

## Why the “tail” becomes the story

1) **Long-tail reweighting**  
   Many small contributors don’t matter… until you filter to a rare event type. Then the tail can dominate the review list.

2) **Non-linear concentration**  
   A small share of rows can concentrate into a few regimes and dominate operational risk.

3) **Auditability**  
   You get a ranked “where the mass is” map plus a trace report you can defend.

---

## Two-minute demo (script-first)

```powershell
.\.venv\Scripts\python scripts/run_long_tail_demo.py --status "Green Termination"
```

Look for:

- `PROOF: items_to_cover_90pct 37 -> 12` (example)
