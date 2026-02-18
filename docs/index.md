# HUF Core

[Start Here](start_here/){ .md-button .md-button--primary }
[Reference Manual](reference_manual/){ .md-button }
[Handbook](handbook/){ .md-button }
[Data Sources](data_sources/){ .md-button }
[GitHub for Beginners](github_for_beginners/){ .md-button }

---

## Get the project

[Download latest release (ZIP)](https://github.com/PeterHIggins19/huf_core_github_v1.1.8_no_inputs/releases/latest){ .md-button .md-button--primary }
[View on GitHub](https://github.com/PeterHIggins19/huf_core_github_v1.1.8_no_inputs){ .md-button }

---

## One-minute demo commands (after running Start Here)

Markham:
```powershell
.\.venv\Scripts\huf markham --xlsx cases\markham2018\inputs\2018-Budget-Allocation-of-Revenue-and-Expenditure-by-Fund.xlsx --out out\markham2018
```

Toronto traffic:
```powershell
.\.venv\Scripts\huf traffic --csv cases\traffic_phase\inputs\toronto_traffic_signals_phase_status.csv --out out\traffic_phase
```

Planck guidance:
```powershell
.\.venv\Scripts\python scripts\fetch_data.py --planck-guide
```
