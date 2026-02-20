# Learning path

HUF is easiest to learn by **running a case**, then **reading the artifacts** it produces.
This path is designed so the left sidebar is a “do-this-next” guide.

!!! tip "Windows / Conda rule"
    After the repo venv exists, always run tools via the repo executables:

    ```powershell
    .\.venv\Scripts\python -V
    .\.venv\Scripts\huf --help
    .\.venv\Scripts\python -m mkdocs serve
    ```

## Step 1 — Install + first run

Choose one:

- Start here (developer): **Start Here → Developer**
- Start here (beginner): **Start Here → Zero GitHub Knowledge**

Goal: you can run `.\.venv\Scripts\huf --help` and you can produce an `out/.../run_stamp.json`.

## Step 2 — Run the “two core” cases

1) **Markham (budget allocation)** → then read:
- **Worked examples → Markham**

2) **Traffic Phase (signal phases)** → then read:
- **Worked examples → Traffic phase**

These two are the best introductions to how HUF turns a raw table into:

- a *coherence map* (regimes),
- an *active set* (retained items),
- and a *trace report* (auditable, line-by-line).

## Step 3 — Try an adapter-style use case

- **Adapters → Vector DB coherence**

This shows how HUF can “explain” retrieval results by grouping **where the score mass comes from**
(namespaces, sources, etc.) and what gets excluded by `tau_global`.

## Step 4 — Optional: big-data / scientific demo

- Planck LFI/HFI 70 GHz (optional): see **Start Here → Developer** (Planck section)

## Step 5 — Optional: notebooks

- **Jupyter demos** (optional)

If you want plots + interactive exploration, notebooks are a nice fit.
