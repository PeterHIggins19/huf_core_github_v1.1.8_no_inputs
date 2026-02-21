# Case studies

!!! note "Ethics & authorship"
    This page was drafted with AI assistance as an editing and structuring tool. The author reviewed and curated all formal claims; any numerical results shown here are either reproduced by code in this repository or explicitly labeled as illustrative.

## What this page is
A catalog of the included case studies, with their regimes and penalty terms at a glance.

## Why it matters
It lets you pick a case by *shape* (regimes, penalties, detection goal) instead of by domain hype.

## What you’ll see
- A table summarizing each case.
- Links to the runnable pages.

## Artifacts / outputs
- Each case includes a Python script and emits a JSONL trace.

## Run the example
Open any case and run its script.

## What to expect
You’ll get a printed summary plus a trace you can plot.

## Interpretation
Use this catalog to choose the regime structure that matches your own problem.

## Next steps
Start with the simplest case, then add nested regimes.

---

## Catalog table (converted from HTML)

| Case | Domain | Regimes | Penalty term | Detection | Post C(ℋ) | Δ drift |
| --- | --- | --- | --- | --- | --- | --- |
| Planck LFI 70 GHz | Science / ESA | 7 freq channels | φ·F\_r (foreground) | Cosine d>0.12 | 0.968 | −27% |
| City of Markham | Civic / Municipal | 5 budget cats | ε·|ρ−ρ^approved| | Euclidean d>0.10 | 0.958 | −21% |
| Traffic Phase | Infrastructure | 3 phases × corridors | π·P\_r (compliance) | Euclidean ‖e‖>7 | 0.943 | −18% |
| Weaviate VDB | Vector DB | Tenants / States | β·S(s\_r) (state) | Cosine | 0.925 | −15.1% |
| Qdrant VDB | Vector DB | Fallback/Dedicated | T(s\_r) + M(s\_r) | Cosine | 0.926 | −13.5% |
| Pinecone VDB | Vector DB | Namespaces | μ·(1−A\_r) | Activity decay | 0.922 | −14.2% |

!!! note "About the numbers"
    If the table includes `Post C(ℋ)` or `Δ drift`, treat them as **illustrative** unless the corresponding case script reproduces them.
