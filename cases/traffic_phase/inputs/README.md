# Inputs (not bundled)

These cases use **real City of Toronto** traffic-signal phase status data exported from the City’s Open Data portal.

The full CSV can be several MB+ depending on the export window, so it is **not included** here.

## Required file
Place the CSV at:

- `cases/traffic_phase/inputs/toronto_traffic_signals_phase_status.csv`

## Where to download
1. Go to the City of Toronto Open Data portal.
2. Search the catalogue for **Traffic Signal Phase Status** (or similar wording).
3. Download/export as CSV.
4. Rename to match the required filename above (or update your CLI `--input`).

See `DATA_SOURCES.md` (repo root) for links.

## After download
Run:

```bash
huf traffic-phase --input cases/traffic_phase/inputs/toronto_traffic_signals_phase_status.csv
```
