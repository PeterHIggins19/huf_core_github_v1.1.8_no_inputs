# Data Sources & Fetching

HUF Core demos use a mix of **bundled** inputs and **fetched** inputs.

## Recommended rule (Windows/Conda)

After the repo venv exists, always run fetch via:

```powershell
.\.venv\Scripts\python scripts/fetch_data.py --help
```

## Markham (2018 Budget Allocation workbook)

Fetch:

```powershell
.\.venv\Scripts\python scripts/fetch_data.py --markham
```

Expected file:

- `cases/markham2018/inputs/2018-Budget-Allocation-of-Revenue-and-Expenditure-by-Fund.xlsx`

## Toronto (Traffic signals timing → CSV)

Non-interactive (best for copy/paste):

```powershell
.\.venv\Scripts\python scripts/fetch_data.py --toronto --yes
```

Expected files:

- `cases/traffic_phase/inputs/toronto_traffic_signals_phase_status.csv`
- `cases/traffic_anomaly/inputs/toronto_traffic_signals_phase_status.csv`

## Planck 70 GHz (guided/manual)

Planck files are large; HUF prints a copy/paste guide instead of downloading automatically:

```powershell
.\.venv\Scripts\python scripts/fetch_data.py --planck-guide
```

You will download a 70 GHz FITS file into:

- `cases/planck70/inputs/`

Then run:

```powershell
.\.venv\Scripts\huf planck --fits cases/planck70/inputs/YOUR_70GHZ_MAP.fits --out out/planck70
```
