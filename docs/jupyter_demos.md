HUF-DOC: HUF.REL.DOCS.PAGE.JUPYTER_DEMOS | HUF:1.1.8 | DOC:v0.1.0 | STATUS:release | LANE:release | RO:Peter Higgins
CODES: DOCS | ART: CM, AS, TR, EB | EVID:E1 | POSTURE:OP | WEIGHTS: OP=0.80 TOOL=0.20 PEER=0.00 | CAP: OP_MIN=0.51 TOOL_MAX=0.49 | CANON:docs/jupyter_demos.md

# Jupyter demos (optional)

Jupyter is optional. It’s useful when you want to **read and summarize artifacts** interactively.

## Install + launch (Windows PowerShell)

```powershell
.\.venv\Scripts\python -m pip install notebook pandas
.\.venv\Scripts\python -m notebook
```

A browser window opens. Create a new notebook (Python).

## Important: PowerShell is not Python

If you type `import pandas as pd` at a **PowerShell** prompt, it will fail.

Run Python code:
- in a notebook cell, or
- inside `python` interactive (`.\.venv\Scripts\python`), or
- from a script file.

## Suggested notebook pattern

### Cell 1 — run a case (CLI)
```python
import subprocess, sys
subprocess.check_call([sys.executable, "-m", "huf_core.cli", "--help"])
```

(Or just run the case in PowerShell first, then open artifacts in the next cells.)

### Cell 2 — open artifacts (Markham)
```python
import pandas as pd

coh = pd.read_csv("out/markham2018/artifact_1_coherence_map.csv")
active = pd.read_csv("out/markham2018/artifact_2_active_set.csv").sort_values("rank")

coh.sort_values("rho_global_post", ascending=False).head(10)
```

### Cell 3 — “how many items cover 90%?”
```python
active["cum"] = active["rho_global_post"].cumsum()
active.loc[active["cum"] >= 0.90, ["rank","item_id","cum"]].head(1)
```

### Cell 4 — open artifacts (Traffic Phase)
```python
import pandas as pd

coh = pd.read_csv("out/traffic_phase/artifact_1_coherence_map.csv")
active = pd.read_csv("out/traffic_phase/artifact_2_active_set.csv").sort_values("rank")

coh.sort_values("rho_global_post", ascending=False).head(15)
```

## Export
You can export notebooks to HTML/PDF from the Jupyter UI (File → Download).
