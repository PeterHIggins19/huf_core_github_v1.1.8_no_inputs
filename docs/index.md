---
title: HUF Core
# HUF-DOC: HUF.REL.DOCS.PAGE.INDEX | HUF:1.1.8 | DOC:v0.2.0 | STATUS:release | LANE:release | RO:Peter Higgins
# CODES: DOCS, HOME | ART: CM, AS, TR, EB | EVID:E1 | POSTURE:OP | WEIGHTS: OP=0.80 TOOL=0.20 PEER=0.00 | CAP: OP_MIN=0.51 TOOL_MAX=0.49 | CANON:docs/index.md
---

# Higgins Unity Framework (HUF)

HUF is an artifact-first compression + audit framework for long-tail distributions (budgets, logs, exceptions).

It produces review-first artifacts on every run:

- **Coherence map** (`artifact_1_coherence_map.csv`) — where the mass is (ranked regimes)
- **Active set** (`artifact_2_active_set.csv`) — retained items + global/local shares
- **Trace report** (`artifact_3_trace_report.jsonl`) — provenance + why it stayed
- **Error budget** (`artifact_4_error_budget.json`) — discarded mass by reason and regime

---

## Quick links

- **Quick run (copy/paste):** [quick_run.md](quick_run.md)
- **Learning (graduated track):** [learning/index.md](learning/index.md)
- **Books (library):** [books/index.md](books/index.md)
- **Field guide:** [field_guide.md](field_guide.md)
- **Partners & case studies:** [partners/index.md](partners/index.md)

---

## Run locally (one-click starters)

These scripts live at the repo root. MkDocs cannot link to them as local docs files, so use the GitHub links:

- Windows: https://github.com/PeterHiggins19/huf_core/blob/main/START_HERE_WINDOWS.bat
- macOS: https://github.com/PeterHiggins19/huf_core/blob/main/START_HERE_MAC.command
- Linux: https://github.com/PeterHiggins19/huf_core/blob/main/start_here_linux.sh

---

## Common next steps

- **Developer start:** [start_here.md](start_here.md)
- **Data sources & fetching:** [data_sources.md](data_sources.md)
- **Troubleshooting:** [troubleshooting.md](troubleshooting.md)
- **Reference manual:** [reference_manual.md](reference_manual.md)

Repo scripts (external links):
- Fetch inputs: https://github.com/PeterHiggins19/huf_core/blob/main/scripts/fetch_data.py
- Bootstrap helper: https://github.com/PeterHiggins19/huf_core/blob/main/scripts/bootstrap.py

---

## If you have no GitHub experience

- [get_started_zero_github.md](get_started_zero_github.md)

---

## Cases catalog

- [partners/case_studies/index.md](partners/case_studies/index.md)

