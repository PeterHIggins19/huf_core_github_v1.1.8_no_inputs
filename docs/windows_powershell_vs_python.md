# PowerShell vs Python (Windows-safe)

---

## Windows note: PowerShell does not support `<<'PY'` heredocs

If you see examples like this on the internet:

```bash
python - <<'PY'
print("hello")
PY
```

That is **bash** syntax, not PowerShell.

### Do this instead (PowerShell + repo venv)

**Option A — run a helper script (recommended):**

```powershell
.\.venv\Scripts\python scripts/inspect_artifact_tables.py --out out/planck70 --top 10
```

**Option B — start Python explicitly, then type Python:**

```powershell
$py = ".\.venv\Scripts\python.exe"
& $py
```

Now your prompt changes to `>>>` and you can run:

```python
import sys
print(sys.executable)
```

!!! tip "Why you saw `Unable to initialize device PRN`"
    In PowerShell, `print` is a **Windows command** (printer), not Python.
    If you run `print(...)` *in PowerShell*, it tries to print to `PRN`.
