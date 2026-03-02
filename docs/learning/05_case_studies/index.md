HUF-DOC: HUF.REL.LRN.MODULE.05_CASE_STUDIES | HUF:1.1.8 | DOC:v0.1.0 | STATUS:draft | LANE:release | RO:Peter Higgins
CODES: LRN, 05_CASE_STUDIES | ART: CM, AS, TR, EB | EVID:E0 | POSTURE:OP | WEIGHTS: OP=0.80 TOOL=0.20 PEER=0.00 | CAP: OP_MIN=0.51 TOOL_MAX=0.49 | CANON:docs/learning/05_case_studies/index.md

# Case studies

What this page is:
How HUF case studies are structured and how to read them like a reviewer.

Why it matters:
A case is where you prove “this is reproducible” and “nothing disappeared silently”.

What you’ll see:
- Case folder anatomy
- What “reproducible” means in HUF terms
- A reading order (fast)

## Case anatomy

Typical layout:

- `inputs/` (documented)
- `artifact_1_*.csv` (CM)
- `artifact_2_*.csv` (AS)
- `artifact_3_*.jsonl` (TR)
- `artifact_4_*.json` (EB)
- `meta.json` / `run_stamp.json` (run metadata)

## Fast reading order

1) EB — what was discarded (and why)
2) CM — where the mass is
3) AS — what remained and shares
4) TR — decision log for edge cases

Next steps:
- **06 Partner pilots** for “how to do this with a real organization”
