# Vector DB coherence (one‑pager)

This is the quickest way to run the “retrieval audit” demo and confirm the output is real.

If you want the deeper explanation, plots, and tau‑sensitivity checks, go to **[Vector DB coherence](vector_db_coherence.md)**.

---

## Run

=== "Windows (PowerShell)"

    ```powershell
    $py  = ".\\.venv\\Scripts\\python.exe"
    $in  = "cases/vector_db/inputs/retrieval.jsonl"
    $out = "out/vector_db_demo"

    & $py examples/run_vector_db_demo.py `
      --in $in `
      --out $out `
      --tau-global 0.02 `
      --regime-field namespace

    & $py scripts/inspect_huf_artifacts.py --out $out
    ```

=== "macOS / Linux (bash/zsh)"

    ```bash
    py="./.venv/bin/python"
    in="cases/vector_db/inputs/retrieval.jsonl"
    out="out/vector_db_demo"

    "$py" examples/run_vector_db_demo.py \
      --in "$in" \
      --out "$out" \
      --tau-global 0.02 \
      --regime-field namespace

    "$py" scripts/inspect_huf_artifacts.py --out "$out"
    ```

## What you should see

- `[OK] Wrote artifacts to: out\vector_db_demo`
- A short dashboard including:

  - `items_to_cover_90pct=...`
  - “Top regimes by rho_global_post”

---

## If paste behaves strangely (Windows)

See **[Running examples on Windows/macOS/Linux](running_examples.md)** for the PSReadLine fix and safe multi‑line patterns.

