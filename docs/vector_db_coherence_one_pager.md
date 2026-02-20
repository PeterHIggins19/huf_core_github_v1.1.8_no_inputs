# Vector DB coherence adapter

A **one-page brief** for the Vector DB coherence adapter.

> **No live vector DB required:** export your retrieval results (JSONL/CSV/TSV) and audit the result-set **composition**.

## Canonical links

- **HUF repo:** https://github.com/PeterHiggins19/huf_core_github_v1.1.8_no_inputs
- **Docs:** https://peterhiggins19.github.io/huf_core_github_v1.1.8_no_inputs/

## What the audit answers

- **Dominance:** “Is one namespace / collection / tenant quietly dominating results?”
- **Concentration:** “Do a few items explain most of the mass?”  
  Proof line: `items_to_cover_90pct` (smaller ⇒ more concentrated)
- **Declared discards:** “What fell below threshold, and how much mass was discarded?”

## Artifacts (what to open first)

- `artifact_1_coherence_map.csv`  
  Sort by `rho_global_post` → top regimes (namespaces/collections/tenants) by post-normalized mass.
- `artifact_2_active_set.csv`  
  Sort by `rho_global_post` → your ranked review list (the items that matter most overall).
- `artifact_4_error_budget.json`  
  Look for `discarded_budget_global` → explicitly declared discard mass.
- `artifact_3_trace_report.jsonl`  
  When someone asks “why was this retained?” (provenance + reasoning).

## 60-second run (Windows / repo venv)

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

### One-number “proof line”

After the run, look for:

- `items_to_cover_90pct=<k>`

If `k` is small, **concentration is high**: a small number of retained items explain most of the post-normalized mass.

That’s the retrieval version of: “a few budget lines explain most of the variance.”
