import os, zipfile, textwrap, datetime
from pathlib import Path

md = textwrap.dedent("""\
# Ramsar Pilot: Environmental Governance Audit
*Wetland conservation program governance · ecology as subject domain · open data as substrate*

!!! note "Scope positioning"
    **HUF is not doing ecology modeling.** This case treats ecological indicators as *inputs* to a governance system.
    HUF audits the **governance layer**: whether resources and attention are allocated coherently across regimes,
    whether drift is detected, and whether reporting artifacts remain traceable and accountable.

!!! note "Ethics disclosure"
    AI-assisted drafting/editing may be used for clarity; the operator reviews/curates final wording.
    Domain/performance claims should be treated as hypotheses unless supported by reproducible runs and emitted artifacts.

---

## What this page is

A pilot case study showing how to apply HUF to **environmental governance**: the institutions and workflows that sit on top of ecological data (wetlands, biodiversity, hydrology) and decide how budgets, interventions, and monitoring effort are distributed.

This page is a blueprint. It is designed to be reproducible with your own dataset (national portals, Ramsar site lists, NGO monitoring feeds, etc.).

## Why it matters

Environmental programs often fail *silently*:

- budgets “add up” globally while internal allocation drifts
- reporting completeness varies by region or site, but no one sees the dominance
- exceptions (crashes, die-offs, drought events) get handled ad hoc without a consistent audit trail

HUF helps by making the internal distribution explicit, traceable, and reviewable.

## Classification

- **Primary domain:** Environmental Governance *(same family as Markham governance audits)*
- **Subject domain:** Ecology *(wetlands/biodiversity/hydrology)*
- **Substrate:** Open Data Infrastructure *(reporting → decision trace, portal gaps, dataset completeness)*

## What you’ll see

- How to define **regimes** for a conservation program (regions, authorities, funding streams, reporting channels)
- How to define **items** (sites, interventions, monitoring events, datasets, grants)
- How “unity” works as an audit contract (**Σρ = 1.0** on the chosen accounting view)
- How to interpret the four standard artifacts:
  - coherence map (where the mass is)
  - active set (what was retained)
  - trace report (why it stayed)
  - error budget (what was discarded)

---

## A simple HUF framing for Ramsar-style governance

### Regimes (choose one, keep it stable)
Pick a regime definition that matches your governance question:

- **Region** (e.g., continent, country, basin)
- **Authority** (e.g., ministry, agency, NGO partner)
- **Funding stream** (capex/opex, monitoring vs intervention)
- **Reporting channel** (portal A vs portal B, public vs internal)

> Recommendation: start with **Region** because it’s intuitive and usually available.

### Items
Choose item granularity you can audit:

- wetland site (one row per site per period)
- intervention (restoration project, policy action)
- monitoring event (survey, measurement)
- dataset update (portal publication)

### Weight / score
Pick a score that represents “mass” in the audit view. Common options:

- budget amount (currency)
- monitoring effort (staff-hours, surveys)
- risk-weighted priority (a proxy score)
- “attention share” (e.g., number of published updates)

HUF does not require a perfect score. It requires that you are explicit about what the score means.

---

## Artifacts / outputs

| Artifact | File | What it answers |
|---|---|---|
| 1 | `artifact_1_coherence_map.csv` | Which regimes dominate? How concentrated is governance attention/allocation? |
| 2 | `artifact_2_active_set.csv` | What was retained under the retention policy, and what is each item’s share? |
| 3 | `artifact_3_trace_report.jsonl` | Why each item stayed/discarded (audit trail) |
| 4 | `artifact_4_error_budget.json` | Discarded mass by reason/regime (prevents silent loss) |

---

## Run the example

This pilot is meant to run on your own inputs. The minimal requirement is an **items file** with:

- `item_id`
- `regime`
- `score` (nonnegative)
- optional fields: `year`, `metric`, `source`, `notes`

### Step 1 — Create a tiny synthetic pilot input (for learning)

Save this as `notes/ramsar_pilot/synthetic_ramsar.jsonl`:

```python
import json
from pathlib import Path

Path("notes/ramsar_pilot").mkdir(parents=True, exist_ok=True)

rows = [
  # region, item, score (e.g., budget share or effort proxy)
  ("Europe",   "HR_site_001",  12.0),
  ("Europe",   "HR_site_002",   9.0),
  ("Europe",   "HR_site_003",   7.0),
  ("Africa",   "UG_site_010",   5.0),
  ("Africa",   "UG_site_011",   4.0),
  ("Asia",     "IN_site_020",   8.0),
  ("Asia",     "IN_site_021",   6.0),
  ("Americas", "CA_site_100",  10.0),
  ("Oceania",  "AU_site_200",   3.0),
]

out = Path("notes/ramsar_pilot/synthetic_ramsar.jsonl")
with out.open("w", encoding="utf-8") as f:
  for region, item_id, score in rows:
    f.write(json.dumps({
      "item_id": item_id,
      "regime": region,
      "score": float(score),
      "year": 2025,
      "metric": "allocation_proxy",
      "source": "synthetic"
    }) + "\\n")

print("Wrote:", out)
