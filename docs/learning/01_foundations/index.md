HUF-DOC: HUF.REL.LRN.MODULE.01_FOUNDATIONS | HUF:1.1.8 | DOC:v0.1.0 | STATUS:draft | LANE:release | RO:Peter Higgins
CODES: LRN, 01_FOUNDATIONS | ART: CM, AS, TR, EB | EVID:E0 | POSTURE:OP | WEIGHTS: OP=0.80 TOOL=0.20 PEER=0.00 | CAP: OP_MIN=0.51 TOOL_MAX=0.49 | CANON:docs/learning/01_foundations/index.md

# Foundations

What this page is:
A plain-language definition of the core quantities HUF uses: regimes, weights, normalization, retention, and “discarded mass”.

Why it matters:
Without crisp definitions, teams talk past each other. This module gives the shared vocabulary.

What you’ll see:
- Minimal symbols and definitions
- A toy example you can compute by hand
- How retention changes interpretation (without hiding loss)

## Definitions (minimal)

Let each item have:
- a **score** (nonnegative weight)
- a **regime label** `r` (tenant/source/category)

Per regime:
- **regime mass:** `w_r = Σ score_i (for items in regime r)`
- **normalized regime share:** `p_r = w_r / Σ w_r`

If you normalize per regime (local view):
- item local share: `ρ_local(i) = score_i / Σ(score_j in same regime)`

If you normalize globally:
- item global share: `ρ_global(i) = score_i / Σ(all scores)`

## Retention (optional, but common)

Retention keeps the most-mass items under a rule (e.g., “keep items until 99% mass retained”).

Key rule:
> Retention must produce an **explicit Error Budget**.

That means:
- discarded items are not “gone”
- they are accounted for (by reason and regime)

## Toy example

Items:

| item | regime | score |
|---|---|---:|
| A | R1 | 80 |
| B | R1 | 20 |
| C | R2 | 9 |
| D | R2 | 1 |

Regime masses:
- `w_R1 = 100`, `w_R2 = 10`
- `p_R1 = 100/110`, `p_R2 = 10/110`

If we retain only items with score ≥ 10:
- kept: A, B, C
- discarded: D (but logged in EB)

Interpretation:
- the retained distribution is tighter
- but the EB shows exactly what was excluded and why

## Run the example (inspect any out folder)

```powershell
.\.venv\Scripts\python scripts\inspect_huf_artifacts.py --out out/traffic_phase_demo
```

Next steps:
- Go to **02 Formal core** to see the conservative mathematical structure (without overclaim).
