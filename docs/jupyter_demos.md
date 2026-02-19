\
# Jupyter demos (optional)

Jupyter notebooks are a great way to **read HUF artifacts interactively** (tables + plots in one place).
They're optional — everything in this repo can be run from the CLI.

!!! warning "PowerShell vs Python"
    `import pandas as pd` is **Python**, not PowerShell.
    If you paste Python into PowerShell you'll see errors like `The term 'import' is not recognized...`.

---

## Install Jupyter in the repo venv

```powershell
.\.venv\Scripts\python -m pip install notebook pandas matplotlib
```

## Launch

```powershell
.\.venv\Scripts\python -m notebook
```

A browser window will open. Create a new notebook and point it at your artifact folder, e.g.:

- `out/markham2018/`
- `out/traffic_phase/`
- `out/planck70/`

---

## Minimal “artifact reader” snippet (copy/paste into a notebook cell)

```python
import pandas as pd

coh = pd.read_csv("out/markham2018/artifact_1_coherence_map.csv")
active = pd.read_csv("out/markham2018/artifact_2_active_set.csv").sort_values("rank")

display(coh.head())
display(active.head(10))
```

---

## Prefer one-liners instead of notebooks?

You can run quick inspections without opening Jupyter:

```powershell
.\.venv\Scripts\python -c "import pandas as pd; df=pd.read_csv('out/markham2018/artifact_1_coherence_map.csv'); print(df.sort_values('rho_global_post', ascending=False).head(10).to_string(index=False))"
```
