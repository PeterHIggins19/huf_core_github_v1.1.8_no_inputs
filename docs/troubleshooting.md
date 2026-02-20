# Troubleshooting

**Updated:** 2026-02-17

This page collects common “Windows reality” problems people hit when they’re new to Python tooling.

---

## 1) “.venv exists but commands run the wrong Python”

If you see paths like `miniconda3\Scripts\huf.exe`, you’re running a *global* install, not the repo venv.

Use the venv explicitly:

```powershell
.\.venv\Scripts\python -V
.\.venv\Scripts\huf --help
```

---

## 2) SSL certificate errors (CERTIFICATE_VERIFY_FAILED)

Fix:

```powershell
.\.venv\Scripts\python -m pip install certifi
.\.venv\Scripts\python scripts/fetch_data.py --toronto --yes
```

---

## 3) Toronto fetch gets HTTP 404

Use the default CKAN base:

- `https://open.toronto.ca/api/3/action`

Explicit override:

```powershell
.\.venv\Scripts\python scripts/fetch_data.py --toronto --yes --toronto-ckan https://open.toronto.ca/api/3/action
```

---

## 4) “File not found” for case inputs

Run fetch first:

```powershell
.\.venv\Scripts\python scripts/fetch_data.py --markham --toronto --yes
```
