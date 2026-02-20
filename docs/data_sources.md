# Data Sources & Fetching

This repo ships small inputs for Markham and Toronto via `scripts/fetch_data.py`.
Planck is guide-only because the file is large.

---

## Fetch Markham + Toronto inputs

```powershell
.\.venv\Scripts\python scripts/fetch_data.py --markham --toronto --yes
```

If you haven't created the venv yet:

```powershell
python scripts/bootstrap.py
```

---

## Docs preview

```powershell
.\.venv\Scripts\python -m mkdocs serve
```
