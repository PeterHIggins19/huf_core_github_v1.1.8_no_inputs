# Inputs (not bundled)

This case reuses the same Toronto phase-status CSV as `traffic_phase` but filters to a specific anomaly subset.

## Required file
Place the CSV at:

- `cases/traffic_anomaly/inputs/toronto_traffic_signals_phase_status.csv`

## Where to download
See `cases/traffic_phase/inputs/README.md` and `DATA_SOURCES.md`.

## After download
Run:

```bash
huf traffic-anomaly --input cases/traffic_anomaly/inputs/toronto_traffic_signals_phase_status.csv
```
