# Vector DB coherence (from retrieval results)

This adapter analyzes a set of retrieval hits (e.g., from a vector database) and answers:

- **Which regimes dominate** the retrieved set? (e.g., `namespace`, `tenant`, `source`, …)
- **How concentrated** is the set? (e.g., “how many items explain 90% of the mass?”)

If you’re coming from outside “advanced computation”: think of this as a **retrieval audit** that turns a pile of ranked results into a small, explainable report.

> If you ever see PowerShell “doing weird things” when you paste commands, start with **[Running examples on Windows/macOS/Linux](running_examples.md)**.

---

## Why run this

Run this when you want to validate that:

- Your retrieval isn’t silently dominated by one bucket (a single namespace/tenant/source)
- Small parameter changes (like `tau`) don’t create unstable, misleading concentration

---

## Input: retrieval export (`.jsonl`)

The demo input is a JSON Lines file (one JSON object per line) containing:

- `id` (string)
- `score` (float)
- a **regime field** such as `namespace`

Example line:

```json
{"id":"doc_001","score":0.82,"namespace":"kb","source":"handbook"}
```

---

## Run the demo

### 1) Set paths

=== "Windows (PowerShell)"

    ```powershell
    $py  = ".\\.venv\\Scripts\\python.exe"
    $in  = "cases/vector_db/inputs/retrieval.jsonl"
    $out = "out/vector_db_demo"
    ```

=== "macOS / Linux (bash/zsh)"

    ```bash
    py="./.venv/bin/python"
    in="cases/vector_db/inputs/retrieval.jsonl"
    out="out/vector_db_demo"
    ```

### 2) Create a tiny demo input (optional)

If you already have a retrieval export, skip this.

=== "Windows (PowerShell)"

    ```powershell
    New-Item -ItemType Directory -Force (Split-Path $in) | Out-Null

    @'
    {"id":"doc_001","score":0.82,"namespace":"kb","source":"handbook"}
    {"id":"doc_002","score":0.63,"namespace":"kb","source":"manual"}
    {"id":"doc_101","score":0.77,"namespace":"tickets","source":"ops"}
    {"id":"doc_102","score":0.12,"namespace":"tickets","source":"ops"}
    '@ | Set-Content -Encoding utf8 $in
    ```

=== "macOS / Linux (bash/zsh)"

    ```bash
    mkdir -p "$(dirname "$in")"
    cat > "$in" <<'JSONL'
    {"id":"doc_001","score":0.82,"namespace":"kb","source":"handbook"}
    {"id":"doc_002","score":0.63,"namespace":"kb","source":"manual"}
    {"id":"doc_101","score":0.77,"namespace":"tickets","source":"ops"}
    {"id":"doc_102","score":0.12,"namespace":"tickets","source":"ops"}
    JSONL
    ```

### 3) Run the example

=== "Windows (PowerShell)"

    ```powershell
    New-Item -ItemType Directory -Force $out | Out-Null

    & $py examples/run_vector_db_demo.py `
      --in $in `
      --out $out `
      --tau-global 0.02 `
      --regime-field namespace
    ```

=== "macOS / Linux (bash/zsh)"

    ```bash
    mkdir -p "$out"

    "$py" examples/run_vector_db_demo.py \
      --in "$in" \
      --out "$out" \
      --tau-global 0.02 \
      --regime-field namespace
    ```

### What you should see

```text
[OK] Wrote artifacts to: out\vector_db_demo
```

Artifacts are written to:

- `out/vector_db_demo/`

---

## Inspect the artifacts (recommended)

**Why:** this is the fastest way to verify the run produced *real* numbers and to find the CSV files you can open in Excel / pandas.

=== "Windows (PowerShell)"

    ```powershell
    & $py scripts/inspect_huf_artifacts.py --out $out
    ```

=== "macOS / Linux (bash/zsh)"

    ```bash
    "$py" scripts/inspect_huf_artifacts.py --out "$out"
    ```

### Expected output (example)

```text
[out] ...\out\vector_db_demo
[tail] items_to_cover_90pct=3

Top regimes by rho_global_post:
  1. kb       rho_post=0.619658
  2. tickets  rho_post=0.380342
```

---

## Compare two tau values (concentration delta)

**Why:** check whether your concentration headline is stable.

=== "Windows (PowerShell)"

    ```powershell
    $out = "out/vector_db_delta"

    & $py scripts/run_vector_db_concentration_delta.py `
      --in $in `
      --out $out `
      --tau-a 0.005 `
      --tau-b 0.02 `
      --regime-field namespace
    ```

=== "macOS / Linux (bash/zsh)"

    ```bash
    out="out/vector_db_delta"

    "$py" scripts/run_vector_db_concentration_delta.py \
      --in "$in" \
      --out "$out" \
      --tau-a 0.005 \
      --tau-b 0.02 \
      --regime-field namespace
    ```

What you should see:

- Two sub‑runs under `out/vector_db_delta/` (one per tau)
- A headline like:

```text
Concentration unchanged: items_to_cover_90pct 3 -> 3
```

---

## Plots (optional, but great for presentations)

If you want charts, install matplotlib:

=== "Windows"

    ```powershell
    & .\.venv\Scripts\python.exe -m pip install matplotlib
    ```

=== "macOS / Linux"

    ```bash
    ./.venv/bin/python -m pip install matplotlib
    ```

Then generate plots for any output folder:

```bash
python scripts/plot_huf_artifacts.py --out out/vector_db_demo
```

This writes images under `<out>/plots/`.

Example charts (from the tiny demo input):

![Example: coherence by regime](assets/plots/vector_db_coherence_by_regime.png)

![Example: concentration curve](assets/plots/vector_db_concentration_curve.png)

---

## Common pitfalls

- **PowerShell is not Python.** If you type `import pandas as pd` at `PS C:\...>` it will fail.
- **`python - <<'PY'` is bash‑only.** On Windows PowerShell, use the here‑string pattern from `running_examples.md`.
- If you see `Unable to initialize device PRN`, you likely ran `print(...)` in PowerShell instead of Python.

