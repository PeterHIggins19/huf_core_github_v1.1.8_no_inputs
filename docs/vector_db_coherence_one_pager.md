\
# Vector DB coherence adapter (one-page brief)

This is a **script-first** description of the Vector DB coherence adapter — designed to be readable by:
- builders (how do I run it?)
- reviewers (what do the artifacts mean?)
- partnerships / DevRel (what problem does it solve?)

> **No live vector DB required:** you feed a JSONL export of retrieval results.

---

## What it audits

**1) Namespace dominance / source dominance**  
“Are my results dominated by one namespace / one source?”

- Answered by: `artifact_1_coherence_map.csv` sorted by `rho_global_post`.

**2) Concentration (long tail) in one number**  
“Do a few items explain most of the mass?”

- Answered by: `items_to_cover_90pct` (printed by `inspect_huf_artifacts.py`).

**3) Tail cut is declared, not hidden**  
“What did we discard and how much budget did we throw away?”

- Answered by: `artifact_4_error_budget.json` (discarded mass) + `artifact_3_trace_report.jsonl` (provenance).

---

## How it works (five steps)

1) **Export retrieval results**  
   Save your retrieval results to JSONL (one JSON object per line).

2) **Choose a regime field**  
   Pick the column used for grouping: `namespace`, `collection`, `tenant`, `source`, etc.

3) **Choose a discard boundary**  
   Set `--tau-global` (global threshold) or a retained target (if your adapter supports it).

4) **Run the adapter**  
   Output goes into an `out/...` folder.

5) **Read the audit artifacts**  
   Coherence map → Active set → Error budget → Trace report.

---

## Input format (JSONL)

### Required fields

- `id` (string): unique id for the item/chunk/document
- `score` (number): similarity/relevance score (**higher is better**)

### Optional fields

Anything you want to group by (regimes), e.g.:

- `namespace`
- `collection`
- `source`
- `tenant`

Example:

```json
{"id":"doc_001","score":0.82,"namespace":"kb","source":"handbook"}
{"id":"doc_002","score":0.63,"namespace":"kb","source":"manual"}
{"id":"doc_101","score":0.77,"namespace":"tickets","source":"ops"}
{"id":"doc_102","score":0.12,"namespace":"tickets","source":"ops"}
```

!!! note "Distance metrics (lower is better)"
    If your system emits **distance** (lower is better), transform it first. Two common choices:

    - `score = 1 / (1 + distance)`
    - `score = -distance`

    Keep the transform explicit so the audit trail stays honest.

---

## Run (Windows PowerShell)

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

.\.venv\Scripts\python scripts/inspect_huf_artifacts.py --out $out
```

!!! warning "PowerShell vs Python"
    If your prompt looks like `>>>`, you are **inside Python**.
    Exit with `exit()` (or Ctrl+Z then Enter), then run commands in PowerShell.

---

## Output artifacts (what each one is for)

### `artifact_1_coherence_map.csv` — regime ranking (“where the budget went”)

Open in Excel and sort by `rho_global_post` descending.

You’re looking for:

- **Dominance:** does the top regime exceed 0.50?
- **Concentration across regimes:** do the top 2–3 regimes cover most mass?
- **Tail cut by regime:** did one regime lose much more than others?

This answers: **“Which groups dominate my retrieval results?”**

### `artifact_2_active_set.csv` — retained items (“the review list”)

Two useful reads:

- **Global triage:** sort by `rho_global_post` → top items overall.
- **Within-regime triage:** filter to one regime and sort by `rho_local_post`.

This answers: **“Which items should I review first?”**

### `artifact_4_error_budget.json` — discard ledger (“what was thrown away”)

Look for a key like `discarded_budget_global`.

This answers: **“How much did we discard, and is that acceptable?”**

### `artifact_3_trace_report.jsonl` — provenance (“how to defend the numbers”)

Use the trace when someone asks:

- “Why is this item retained?”
- “What input fields formed this row?”
- “What exclusions happened?”

This answers: **“Show me the workpapers.”**

---

## Example output (how to interpret it fast)

If your inspector prints:

```text
[tail] items_to_cover_90pct=3

Top regimes by rho_global_post:
  1. kb       rho_post=0.619658
  2. tickets  rho_post=0.380342
```

Read it like this:

- **No monopoly, but clear dominance:** `kb` owns ~62% of the post-normalized mass, `tickets` ~38%.
- **High concentration:** *top 3 items explain 90%* of the retained mass.

A useful “one-liner” to repeat:

> **If the top 3 chunks are stale, 90% of retrieval mass is compromised.**

That’s why this adapter is useful even when your average retrieval metric looks “fine.”

---

## Where this fits in the broader HUF story

This adapter is an easy way to teach **non-linear long-tail reweighting**:

- baseline retrieval set (everything)
- filtered retrieval set (exception-only)
- ranked variance review (what changed, by regime and by item)

See also: **Long tail (accounting lens)** (`docs/long_tail_accounting_lens.md`).

---

## Partnership angle (optional)

If you want to pitch this as an integration, the core message is:

> **“HUF adds an audit layer to retrieval exports: regime ranking + concentration + declared discards + trace.”**

Natural partner categories:

- **Vector DBs** (namespaces/collections map cleanly to regimes): Weaviate, Pinecone, Qdrant, Milvus/Zilliz
- **RAG orchestration** (callbacks/hooks after retrieval): LangChain, LlamaIndex
- **RAG evaluation** (composition audit complements quality metrics): Ragas, Arize, Weights & Biases (RAG tooling)

Keep the demo small: one JSONL file, one command, one headline number (`items_to_cover_90pct`).
