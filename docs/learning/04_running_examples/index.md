HUF-DOC: HUF.REL.LRN.MODULE.04_RUNNING_EXAMPLES | HUF:1.1.8 | DOC:v0.1.0 | STATUS:draft | LANE:release | RO:Peter Higgins
CODES: LRN, 04_RUNNING_EXAMPLES | ART: CM, AS, TR, EB | EVID:E0 | POSTURE:OP | WEIGHTS: OP=0.80 TOOL=0.20 PEER=0.00 | CAP: OP_MIN=0.51 TOOL_MAX=0.49 | CANON:docs/learning/04_running_examples/index.md

# Running examples

What this page is:
How to run the canonical examples and what each one demonstrates.

Why it matters:
Examples create intuition fast — especially for the “retention can strengthen what remains” inversion.

What you’ll see:
- Traffic baseline vs anomaly (long tail)
- Markham (civic budgets)
- Planck (scientific dataset)
- Vector DB coherence (retrieval regimes)

## Traffic: baseline vs exception-only

```powershell
python scripts/bootstrap.py
.\.venv\Scripts\python scripts/fetch_data.py --toronto --yes
.\.venv\Scripts\python scripts/run_long_tail_demo.py --status "Green Termination"
```

Look for:
- tightened concentration in exception-only view
- EB showing discarded mass explicitly

## Markham (civic budget)

```powershell
.\.venv\Scripts\python -m huf --case markham
```

## Planck (optional / large input)

Planck inputs may be large; see the Planck case page in docs before running.

## Vector DB coherence

```powershell
.\.venv\Scripts\python examples/run_vector_db_demo.py
```

Next steps:
- **05 Case studies** for how to read and package a case.
