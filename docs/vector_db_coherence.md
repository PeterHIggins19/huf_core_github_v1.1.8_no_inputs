# Vector DB coherence with HUF (auditable rerank lens)

This page shows a practical way to apply HUF to **vector database retrieval results**.

HUF is **not** a vector index (HNSW/IVF/FAISS/Pinecone handle retrieval).
HUF acts *after retrieval* as an **audit + normalization + exclusion lens** that can help you:
- normalize scores to a unity budget (mass frame)
- group results into regimes (namespace / collection / cluster)
- exclude low-mass items (`tau`)
- produce artifacts explaining *why* items/regimes dominated

## 1) Export retrieval results

Export your top-k retrieval list as **JSONL** (recommended) or **CSV/TSV**.

Minimum required fields:
- `id` (string)
- `score` (float)

Optional fields:
- `namespace` (or `collection`, `cluster`, `source`) — used to form regimes
- any other metadata you want to keep in `trace_path`

Example JSONL:

```jsonl
{"id":"doc_001","score":0.82,"namespace":"kb","source":"handbook"}
{"id":"doc_101","score":0.77,"namespace":"tickets","source":"ops"}
{"id":"doc_102","score":0.12,"namespace":"tickets","source":"ops"}
```

## 2) Run the demo

```bash
python examples/run_vector_db_demo.py \
  --in path/to/retrieval.jsonl \
  --out out/vector_db_demo \
  --tau-global 0.02
```

Outputs:
- `artifact_1_coherence_map.csv`
- `artifact_2_active_set.csv`
- `artifact_3_trace_report.jsonl`
- `artifact_4_error_budget.json`
- plus `meta.json` (adapter metadata)

## 3) Choosing `tau`

Think of `tau` as the minimum “budget share” an item must keep to stay in the active set.

- Too high: you may exclude everything (especially if the list spreads mass across many items)
- Too low: you keep too many low-signal results

Start with:
- `0.01` for top-k ~ 100–200
- `0.02` if you want stronger pruning

## 4) Similarity vs distance (important)

HUF expects **larger value = more mass**.
If your system outputs **distance** (smaller is better), convert it before HUF, e.g.:
- `score = max(distance) - distance`
- or `score = 1 / (1 + distance)`

If your similarity scores can be negative, use:
- `--nonneg-mode clip` (negatives -> 0), or
- `--nonneg-mode shift` (subtract minimum)

## 5) What HUF adds (the non-hype version)

Vector DBs retrieve “what’s close”.
HUF helps you answer:
- which regimes dominated the budget
- what got excluded and why
- how sensitive results are to a chosen threshold

This makes retrieval behavior easier to explain and debug.
