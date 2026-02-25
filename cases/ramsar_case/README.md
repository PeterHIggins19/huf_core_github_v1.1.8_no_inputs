# Ramsar Partner Case (Scaffold)

**Status:** Scaffold only (no partner data committed).  
**Policy:** No data enters this folder without operator sign-off.

## Directory layout

- `data/raw/` — source inputs (operator-authorized only)
- `data/processed/` — derived datasets (reproducible)
- `code/` — pipelines, transforms, loaders
- `docs/` — case notes, mappings, partner-facing drafts (if needed)
- `traces/` — trace artifacts for the case
- `tests/` — unit checks / reproducibility guards

## Phase gate (slow-and-steady)

- Phase A/B/C happen in wiki + drafts.
- Phase D (data) opens only after partner approval and internal signoff.