HUF-DOC: HUF.REL.LRN.MODULE.00_ORIENTATION | HUF:1.1.8 | DOC:v0.1.0 | STATUS:draft | LANE:release | RO:Peter Higgins
CODES: LRN, 00_ORIENTATION | ART: CM, AS, TR, EB | EVID:E0 | POSTURE:OP | WEIGHTS: OP=0.80 TOOL=0.20 PEER=0.00 | CAP: OP_MIN=0.51 TOOL_MAX=0.49 | CANON:docs/learning/00_orientation/index.md

# Orientation

What this page is:
A 10-minute introduction to what HUF *does* and how to recognize when you’re already inside a HUF-shaped problem.

Why it matters:
If your work has **regimes** (tenants, departments, sources, categories) and you need to understand **where the mass is** and **what got discarded**, HUF provides a repeatable audit lens.

What you’ll see:
- The core pipeline (regimes → accounting → retention → coherence → artifacts)
- What the four artifacts mean
- A first runnable demo

## The pipeline (mental model)

1) **Regimes**: split items by a label (tenant/source/category).
2) **Mass accounting**: compute total weight per regime and a normalized distribution.
3) **Retention (optional)**: keep the most-mass items; log discards; renormalize explicitly.
4) **Coherence / concentration**: measure dominance and drift.
5) **Artifacts out**: write CM/AS/TR/EB.

## What “HUF” outputs every run

- **CM — Coherence Map:** ranked regimes + dominance signals  
- **AS — Active Set:** retained items + global/local shares  
- **TR — Trace Report:** “why it stayed” and provenance  
- **EB — Error Budget:** what was discarded (by reason/regime)

## Run the example

From repo root:

```powershell
python scripts/bootstrap.py
.\.venv\Scripts\python scripts/fetch_data.py --toronto --yes
.\.venv\Scripts\python scripts/run_long_tail_demo.py --status "Green Termination"
```

What to expect:
- An `out/...` folder with four artifacts
- A console line like `PROOF: items_to_cover_90pct 37 -> 12` (your numbers may differ)

Interpretation:
- If the exception-only view tightens (fewer items cover 90%), that’s a practical long-tail signal.

Next steps:
- Proceed to **01 Foundations** to define regimes, normalization, and retention precisely.
