\
# Data Sources & Fetching (record copy)

This page exists for older links. The **canonical** page is:

- `Data Sources & Fetching` → `/data_sources/`

Everything below mirrors the canonical content, but prefer `/data_sources/` when linking.

---

## Fetch the small inputs (recommended path)

```powershell
.\.venv\Scripts\python scripts/fetch_data.py --markham --toronto --yes
```

If you haven't created the venv yet, run:

```powershell
python scripts/bootstrap.py
```

---

## Planck LFI 70 GHz (PR3) — guide only

Print the guide:

```powershell
.\.venv\Scripts\python scripts/fetch_data.py --planck-guide
```

IRSA direct URL (PR3 all-sky maps):

`https://irsa.ipac.caltech.edu/data/Planck/release_3/all-sky-maps/maps/LFI_SkyMap_070_1024_R3.00_full.fits`

PowerShell note: use `curl.exe` (PowerShell `curl` is `Invoke-WebRequest`):

```powershell
curl.exe -L -o "cases/planck70/inputs/LFI_SkyMap_070_1024_R3.00_full.fits" "https://irsa.ipac.caltech.edu/data/Planck/release_3/all-sky-maps/maps/LFI_SkyMap_070_1024_R3.00_full.fits"
```

---

## Docs preview

```powershell
.\.venv\Scripts\python -m mkdocs serve
```
