HUF-DOC: HUF.REL.LRN.MODULE.03_ARTIFACTS | HUF:1.1.8 | DOC:v0.1.0 | STATUS:draft | LANE:release | RO:Peter Higgins
CODES: LRN, 03_ARTIFACTS | ART: CM, AS, TR, EB | EVID:E0 | POSTURE:OP | WEIGHTS: OP=0.80 TOOL=0.20 PEER=0.00 | CAP: OP_MIN=0.51 TOOL_MAX=0.49 | CANON:docs/learning/03_artifacts/index.md

# Artifacts

What this page is:
A reviewer-oriented guide to the four artifacts produced by HUF.

Why it matters:
HUF is “artifact-first”: it’s designed to be audited, not just executed.

What you’ll see:
- What each artifact is for
- How to read it
- Common interpretation mistakes

## Artifact 1 — Coherence Map (CM)

File: `artifact_1_coherence_map.csv`

Purpose:
- Rank regimes by post-normalization dominance
- Show concentration signals (where mass lives)

Read it like:
- “Which regimes explain most of the mass?”
- “Did the dominant regimes change between baseline and exception-only?”

## Artifact 2 — Active Set (AS)

File: `artifact_2_active_set.csv`

Purpose:
- Show retained items and their normalized shares

Read it like:
- global share answers “how much of the whole”
- local share answers “how much within its regime”

## Artifact 3 — Trace Report (TR)

File: `artifact_3_trace_report.jsonl`

Purpose:
- Explain why items stayed or left
- Provide provenance for decisions

Read it like:
- a decision log that can be audited line-by-line

## Artifact 4 — Error Budget (EB)

File: `artifact_4_error_budget.json`

Purpose:
- Log discarded mass by reason and regime
- Guarantee “loss never disappears silently”

If you only read one thing for accountability, read EB.

## Run the example (open artifacts quickly)

```powershell
.\.venv\Scripts\python scripts\inspect_huf_artifacts.py --out out/traffic_anomaly_demo
```

Next steps:
- **04 Running examples** for hands-on workflows
