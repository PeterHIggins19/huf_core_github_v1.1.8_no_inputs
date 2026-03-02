HUF-DOC: HUF.REL.LRN.MODULE.07_ADVANCED_MATH | HUF:1.1.8 | DOC:v0.1.0 | STATUS:draft | LANE:release | RO:Peter Higgins
CODES: LRN, 07_ADVANCED_MATH | ART: CM, AS, TR, EB | EVID:E0 | POSTURE:OP | WEIGHTS: OP=0.80 TOOL=0.20 PEER=0.00 | CAP: OP_MIN=0.51 TOOL_MAX=0.49 | CANON:docs/learning/07_advanced_math/index.md

# Advanced math (practical)

What this page is:
A practical summary of “advanced” metrics used in HUF runs (concentration, dominance, drift), without claiming formal universality.

Why it matters:
The *same artifacts* become more useful when you know what signals to look for.

What you’ll see:
- concentration measures (e.g., “items to cover 90%”)
- dominance/delta comparisons between views
- drift framing (conservative)

## Concentration

A common headline metric:
- **items_to_cover_90pct**
  - smaller means more concentrated
  - compare baseline vs exception-only

## Dominance / drift

Look at how top regimes reorder between runs:
- CM shows the regime ranking
- AS shows what items drive it

## Reading posture (conservative)

Use these signals as:
- **evidence** for where to look
- not as proofs of causality

If you want deeper formal work:
- see `docs/books/advanced_mathematics/index.md`

Next steps:
- Re-run a case and write a short reviewer note using CM/AS/TR/EB.
