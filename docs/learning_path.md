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
- Start here (beginner): **Start Here → Zero GitHub knowledge**

Goal: you can run `.\.venv\Scripts\huf --help` and produce an `out/.../run_stamp.json`.

## Step 2 — Run the “two core” cases

1) **Markham (budget allocation)** → then read:
- **Worked examples → Markham**

2) **Traffic Phase (signal phases)** → then read:
- **Worked examples → Traffic phase**

## Step 3 — Understand the “long tail” story (accounting lens)

- **Long tail (accounting lens)**

Then run the 2‑minute demo:

```powershell
.\.venv\Scripts\python scripts/run_long_tail_demo.py --status "Green Termination"
```

## Step 4 — Try an adapter-style use case

- **Adapters → Vector DB coherence**

## Step 5 — Optional: notebooks

- **Jupyter demos** (optional)
