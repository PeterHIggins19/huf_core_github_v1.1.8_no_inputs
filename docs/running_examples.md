# Running examples on Windows, macOS, and Linux

This project is **cross‑platform**, but the *shell syntax* is not. Most “it broke when I pasted it” problems come from mixing:

- **PowerShell commands** (Windows) vs **bash/zsh commands** (macOS/Linux)
- **Shell commands** vs the **Python REPL** (`>>>` prompt)

This page gives copy/paste‑safe patterns and explains *why* each one exists.

---

## Which terminal should I use?

=== "Windows"

    Recommended:

    - **Windows Terminal** + **PowerShell 7+** (best copy/paste behavior)
    - PowerShell 5.1 also works, but line continuations and paste handling are fussier.

    If pasting turns `.` into `[` or auto‑enters mid‑paste, update PSReadLine (this fixes most “weird paste” bugs):

    ```powershell
    Install-Module PSReadLine -Scope CurrentUser -Force -AllowClobber
    # close the terminal completely, then open a NEW PowerShell session
    ```

=== "macOS / Linux"

    Use your default terminal with **bash** or **zsh**.

    - Most docs and one‑liners online assume bash/zsh.
    - `python - <<'PY' ... PY` (heredoc) works here, **not** in PowerShell.

---

## Shell vs Python: how to tell what you’re typing into

- If your prompt looks like:

  - `PS C:\...>` → you are in **PowerShell**
  - `$` → you are in **bash/zsh**
  - `>>>` → you are in **Python** (the REPL)

**Rule:**

- Run `huf ...` and `python some_script.py ...` **in the shell**.
- Run `import ...` and `print(...)` **inside Python**, or via `python -c` / a script.

Why this matters:

- In PowerShell, `print` is *not* Python — it’s a shell command/alias that tries to print to a printer (the “PRN” device), which is why you saw:

  ```
  Unable to initialize device PRN
  ```

---

## Recommended pattern: run the provided scripts (not pasted Python)

The repo includes helper scripts like:

- `scripts/inspect_huf_artifacts.py` (quick dashboard)
- `scripts/run_vector_db_concentration_delta.py` (compare tau settings)

These are intentionally **paste‑friendly** and avoid REPL confusion.

---

## Multi‑line Python snippets (when you really need them)

### Option A (recommended): save a `.py` file

This is the most reliable approach for beginners and teams.

### Option B: pipe a here‑string / heredoc into `python -`

=== "Windows (PowerShell)"

    PowerShell does **not** support bash heredocs (`<<'PY'`). Use a **here‑string** piped into Python:

    ```powershell
    $py = ".\\.venv\\Scripts\\python.exe"

    @'
    import sys
    print("Hello from stdin", sys.version)
    '@ | & $py -
    ```

=== "macOS / Linux (bash/zsh)"

    ```bash
    ./.venv/bin/python - <<'PY'
    import sys
    print("Hello from stdin", sys.version)
    PY
    ```

What to expect:

- `python -` means “read the program from **stdin**”.
- If you see syntax errors *before* Python starts, it’s a shell syntax mismatch.

---

## Worked examples

Below are the three examples most people start with. Each one has:

- **Why run it** (what question it answers)
- **How to run it** (Windows + macOS/Linux)
- **What you should see** (expected outputs)
- **How to inspect/plot results**

---

### Example 1 — Vector DB coherence (retrieval audit)

**Why run it:**

- Check whether a retrieval result set is dominated by one **namespace/source/tenant**.
- Quantify *concentration* (“how many items explain 90% of the mass?”).

See the full walkthrough: **[Vector DB coherence](vector_db_coherence.md)**.

---

### Example 2 — Concentration delta (tau sensitivity)

**Why run it:**

- Compare two `tau` settings to see if concentration is stable or sensitive.

What you should expect:

- It runs two sub‑runs (A and B) and reports whether the “items_to_cover_90pct” headline changes.

---

### Example 3 — Planck 70 GHz (FITS → HUF)

**Why run it:**

- A “real physics” example that produces a non‑toy output and demonstrates the pipeline on scientific data.

See the worked page: **[Planck LFI 70 GHz worked example](partners/case_studies/planck_lfi_70ghz.md)**.

---

## Plots and visual sanity checks

If you want charts (recommended when presenting results), install matplotlib:

=== "Windows"

    ```powershell
    & .\.venv\Scripts\python.exe -m pip install matplotlib
    ```

=== "macOS / Linux"

    ```bash
    ./.venv/bin/python -m pip install matplotlib
    ```

Then generate plots from any output folder:

```bash
python scripts/plot_huf_artifacts.py --out out/vector_db_demo
```

Outputs (saved under `<out>/plots/`):

- `coherence_by_regime.png` — bar chart of `rho_global_post` by regime
- `concentration_curve.png` — cumulative coverage curve + the 90% cutoff

