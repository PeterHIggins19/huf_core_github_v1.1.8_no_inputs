# Traffic Phase worked example (Toronto signals)

Run baseline:

```powershell
.\.venv\Scripts\huf traffic --csv cases/traffic_phase/inputs/toronto_traffic_signals_phase_status.csv --out out/traffic_phase
```

Run exception-only:

```powershell
.\.venv\Scripts\huf traffic-anomaly --csv cases/traffic_anomaly/inputs/toronto_traffic_signals_phase_status.csv --out out/traffic_anomaly --status "Green Termination"
```

See:
- [Long tail (accounting lens)](long_tail_accounting_lens.md)
