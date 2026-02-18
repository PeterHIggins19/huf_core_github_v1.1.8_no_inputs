# Higgins Unity Framework (HUF) Handbook

**Edition:** v1.1.8 (docs refresh)  
**Updated:** 2026-02-17  

This handbook is the *conceptual and contractual* description of HUF: what the Unity-Budgeted Hierarchy (UBH) is, how HUF emits auditable artifacts, and how to interpret stability sweeps.

**Real-data demos included in this repo:**
- **Markham (2018 budget)** — real Excel input fetched from the City of Markham open data site.
- **Toronto (traffic signals timing)** — real CSV derived from the City of Toronto open data “Traffic signals timing” ZIP.
- **Planck (70 GHz all-sky map)** — real FITS map *not shipped in the repo* (too large). You fetch it from PLA or IRSA (guided in `scripts/fetch_data.py --planck-guide`).

**Synthetic data:** only small “toy” examples (used for quick sanity checks) are synthetic. The headline demos above are real data.

---

## Origins (why this exists)

HUF grew out of a very practical question: how to **solve diffraction and dispersion** problems in loudspeakers well enough that the “why” became impossible to ignore.  
The working path was:

1. solve the physical problem (dispersion / diffraction) *empirically*
2. notice an “energy budget” invariant when moving from **2π to 4π radiation equalization**
3. formalize the invariant as an **isotropic budget / unity constraint**
4. generalize it into a contract for hierarchies → the **Unity‑Budgeted Hierarchy (UBH)**
5. treat every run as a reproducible artifact emitter → HUF

That’s the reason the framework is written like a lab protocol: it is designed to let people verify “is this real?” before debating “is this beautiful?”.


---

Higgins Unity Framework (HUF)
Handbook

A contract-first method for unity‑budgeted hierarchies,
auditable reduction, and stable anomaly localization

Handbook Edition • Version 1.0
February 2026

Peter Higgins

# Front matter

This handbook replaces the earlier ‘meeting spec’ lineage. It is written to be implementable, teachable, and hard to misread. The tone is intentionally contract‑driven: if you cannot verify finite elements, conserve a declared unity budget, emit the required artifacts, and pass stability checks, then you are not doing HUF — you are doing storytelling.

The handbook contains two comprehensive, real-data case studies (Planck 70 GHz and City of Markham public data) and a third operational case study (traffic signal telemetry) as an anomaly‑localization template.

## How to use this handbook

- If you need the method: read Part I and implement the contract (required artifacts + stability packet).

- If you need proof: read Part II and reproduce the reference runs (Planck and Markham).

- If you need to teach or deploy: read Part III (implementation patterns, templates, and training exercises).

# Table of contents

In Word: Right‑click the TOC → Update Field → Update entire table.

# Part I — HUF Core (Normative)

## 1. Definition in one page (the core, stripped)

HUF defines a system as a unity‑budgeted hierarchy with auditable finite elements.

1. Finite elements: verifiable units that contribute to a conserved budget.

1. Regimes: named groupings of finite elements (nestable) used for interpretability.

1. Unity budget: a declared conserved quantity (mass/weight or energy/power) with total sum exactly 1.0.

1. Locked cycle: Normalize → Propagate → Aggregate → Exclude → Renormalize.

1. Contract: a run is invalid unless it emits the required artifacts and passes declared stability checks.

## 2. Motivation (the shortest honest version)

Every serious system ends up doing some form of reduction: compressing models, pruning portfolios, prioritizing interventions, or summarizing telemetry. The failure mode is consistent: reduction happens, but the justification is ad hoc. HUF exists to make reduction auditable.

HUF does not promise ‘truth.’ It promises four things you can test: (1) unity conservation, (2) explicit retained set, (3) explicit discarded budget, and (4) backward trace to finite elements. That’s the entire game.

## 3. Primitives and invariants

3.1 Finite element

A finite element is the smallest unit you agree to audit. It must have: a unique identifier, a repeatable method of computing its contribution, and stored provenance.

Minimum finite-element record:

- id: stable string key (do not recycle IDs across runs)

- inputs: pointers to measured data, logs, or upstream artifacts

- contribution: a non-negative scalar (or paired positive/negative extension) used by the unity budget

- provenance: hash or stamp sufficient to reproduce the number

3.2 Regime

A regime is a partition (or nested partition) used to contextualize budget. A regime answers: ‘where did the budget go?’ Regimes must not double-count contributions. If an element belongs to multiple regimes, you must explicitly split its budget.

3.3 Unity budget

Unity is the only invariant HUF treats as sacred: after normalization, the sum of contributions equals 1.0 globally. Local unity (within a regime) may be enforced for a local view, but the global unity must always be satisfied.

## 4. Budget semantics (choose once; don’t cheat)

HUF is ruthless about budget semantics. Declare one of the following and never mix them mid-run:

- Mass/weight budget: ρᵢ ≥ 0 and Σρᵢ = 1. Examples: expenditure shares, portfolio weights, probability mass.

- Energy/power budget: ρᵢ = eᵢ / Σe with eᵢ = |xᵢ|² or another Parseval-consistent energy under a declared orthogonal basis.

If your domain has cancellation (signed contributions), do not fake it by allowing negative ρ. Use a paired-budget extension (track positive and negative magnitudes separately) or an explicitly signed framework with stability proofs.

## 5. The locked cycle and what each step is allowed to do

Figure 1. The locked HUF cycle. You may extend steps, but you may not reorder them without breaking audit expectations.

Normalize

Normalize converts raw contributions into a unity budget. For mass budgets: ρᵢ = wᵢ / Σw. For energy budgets: ρᵢ = |xᵢ|² / Σ|x|². Normalization must be deterministic and logged.

Propagate

Propagation moves budget between representations (e.g., from fine pixels to coarse blocks, from categories to wards, from events to root causes). Propagation is admissible only if it is conservative and traceable.

- Conservation check: |Σρ_out − Σρ_in| ≤ ε (declare ε).

- Traceability check: every output element stores a map back to input elements with weights.

- No hidden state: propagation must be a pure function of inputs + declared parameters (seeded if stochastic).

Aggregate

Aggregation merges elements to reduce complexity while preserving the budget. Examples: cluster similar items, sum within a regime, downsample by known hierarchical structure.

Exclude

Exclusion removes elements below a threshold τ or keeps the smallest set reaching a retained budget target. Exclusion must emit a discard ledger (what was removed and how much budget it carried).

Renormalize and validate

Renormalize after exclusion (and after any operation that may introduce floating-point drift). Then validate the contract: unity checks, trace completeness, artifact emission, and stability packet results.

## 6. The contract (required artifacts)

Contract: a HUF run is invalid unless it emits all artifacts

## 7. Artifact schemas (minimum workable forms)

HUF does not mandate file formats, but it does mandate fields. Minimal schemas:

Schema A — Active set

Schema B — Backward trace (per retained element)

Schema C — Error/Budget report

## 8. Stability packet (required anti-brittleness tests)

Minimum stability packet

## 9. Deployment hazards (the things critics correctly attack)

- Semantics drift: changing what unity means mid-run (e.g., mixing weight and energy).

- Black-box propagation: learned or heuristic mapping with no trace and no conservation validation.

- Double counting: elements belonging to overlapping regimes without explicit splitting.

- Unstable thresholds: large near-τ mass and low overlap across sweeps.

- Overfitting the narrative: tuning τ until your preferred story appears.

HUF’s job is to make these failures visible. If your run fails, that is not ‘HUF failing’; that is the system refusing to be compressed honestly.

# Part II — Comprehensive Reference Runs (Real Data)

## 10. Case Study A — Planck LFI 70 GHz (HEALPix, nside=1024)

This case demonstrates energy‑budget HUF on a large scientific dataset. Input file: LFI_SkyMap_070_1024_R3.00_full.fits. We use the Stokes I column (I_STOKES). The finite elements are pixels; the energy contribution is I².

### 10.1 Data model

- Raw finite elements: nside=1024 pixels (12×1024² = 12,582,912 elements).

- Aggregation: NESTED parent blocks at nside=64 (12×64² = 49,152 coarse elements), each covering 256 child pixels.

- Regimes: 12 HEALPix base faces (each face = 4,096 coarse blocks).

- Budget: energy share ρᵢ = eᵢ / Σe, with eᵢ = Σchild I² (for coarse blocks).

### 10.2 Run configuration

Aggregation: nside 1024 → 64 (ratio 16; 256 children per parent).

Retain target: 0.97 of total energy.

Outcome: K = 18,198 retained coarse blocks out of 49,152. Threshold τ = 1.66e-06.

Energy retained = 0.9700; discarded = 0.0300.

Pixel‑basis RMSE under keep‑or‑zero reconstruction = 7.6942e-05 (same units as I_STOKES).

### 10.3 Coherence map

Figure 2. Planck 70 GHz — global retained vs discarded energy share.

Figure 3. Planck 70 GHz — per‑face unity bars (faces as regimes).

Figure 4. Planck 70 GHz — active‑set growth curve (sorted by ρ).

Table 10‑A. Per‑face energy shares (global ρ)

Table 10‑B. Top retained coarse blocks (traceable sample)

### 10.4 Traceability (how to audit a retained block)

Because the map uses HEALPix NESTED ordering, each nside=64 parent block corresponds to a contiguous range of 256 nside=1024 child pixels. For a retained parent with index p, the child range is [256p, 256p+255]. This makes backward traces compact and exact.

Example: a compact backward trace for an aggregated HEALPix block

### 10.5 Stability packet (retain‑target sweep)

Table 10‑C. Sweep points (target → K, τ)

Table 10‑D. Active‑set overlap (Jaccard) between sweep points

Table 10‑E. Regime ranking stability (faces) across sweep points

### 10.6 What this run teaches (and what it does not)

- HUF can reduce 49,152 coarse blocks to ~18k while retaining 97% pixel-basis energy, with exact accounting.

- Per-regime views (faces) remain stable across threshold sweeps: the ‘where’ of energy is robust.

- The discard fraction is a quantitative error bound under the declared reconstruction.

- This is not cosmological inference. HUF is an auditable reduction layer; domain science still happens above it.

## 11. Case Study B — City of Markham (2018 budget + civic layers)

This case demonstrates mass/weight HUF on municipal public data. The conserved quantity is money. Primary budget workbook: 2018-Budget-Allocation-of-Revenue-and-Expenditure-by-Fund.xlsx (values in $000). We focus on expenditures (the allocation of outgoing funds), then show a propagation example onto wards using census population as a proxy.

### 11.1 Data inventory (what we used)

- 2018-Budget-Allocation-of-Revenue-and-Expenditure-by-Fund.xlsx — fund-level revenues/expenditures by category.

- 2018-Operating-Budget-by-Account.xlsx — operating revenue/expense categories and year comparisons.

- 2016-Tax-Rates.xlsx and 2018-Tax-Rates.xlsx — rate context (not used as budget, used for narrative checks).

- GIS layers: WARD.geojson, Parks.geojson, Fire_Stations.geojson, City_Facilities.geojson (used for a propagation demo).

- Census DA layer (Age/Sex) for Markham — used only to compute ward population shares (proxy).

### 11.2 Budget declaration and finite elements

Global budget: total 2018 expenditures across all funds = 456,171 ($000). Unity budget is ‘share of total expenditures’.

Finite element for the primary run: (Fund × ExpenditureCategory). Regimes: Funds. This gives a clean ‘where does the city spend money’ decomposition.

### 11.3 Primary run results (Fund×Category)

Retain target: 0.97. Outcome: K = 23 retained elements out of 67. Threshold τ = 0.004. Retained = 0.9710; discarded = 0.0290.

Figure 5. Markham 2018 expenditures — global retained vs discarded budget share.

Figure 6. Markham 2018 expenditures — per-fund unity bars (funds as regimes).

Figure 7. Markham 2018 expenditures — active-set growth curve (Fund×Category).

Table 11‑A. Fund regimes: totals and global shares

Table 11‑B. Largest spending contributors (Fund×Category)

### 11.4 Stability packet

Table 11‑C. Sweep points (target → K, τ)

Table 11‑D. Active-set overlap (Jaccard) across sweep points

### 11.5 Backward trace example (auditing a spending line)

In this run, the backward trace is trivial but non‑negotiable: each retained element points back to a specific worksheet row/column (Fund, Category, cell location) plus workbook hash. If you can’t point to the cell, you can’t claim the number.

Example: backward trace record for a budget line

### 11.6 Propagation demo — Operating Fund to wards (proxy allocation)

This section demonstrates propagation constraints on civic geography. We do NOT claim this is the real ward budget — the city budget is not ward‑allocated in this dataset. We demonstrate a conservative, auditable proxy mapping.

Propagation map: allocate Operating Fund expenditures to wards proportional to 2016 census population share. This is admissible as a mapping only if it is declared as a proxy, conservative (sums match), and traceable.

Figure 8. Markham wards — population shares (proxy weights for propagation).

Figure 9. Operating Fund propagated to wards — per-regime unity bars (retained vs discarded at target 0.97).

Table 11‑E. Ward proxy table: population, facilities counts, and Operating Fund allocation ($M)

Why include facilities counts? Not as causal claims — as audit context. They provide additional regimes for future propagation (e.g., allocate a parks-maintenance budget proportional to park count or area). Any such mapping must be declared and tested for stability.

### 11.7 What dominates and what to do next

The Fund×Category decomposition typically reveals (a) how concentrated spending is, (b) whether one fund dominates the budget narrative, and (c) which categories are ‘structural’ versus ‘tail.’ This run is a starting point.

- Next expansion: link operating categories to performance measures (if definitions match).

- Next expansion: add revenues as a parallel budget and compare structural mismatch (revenue concentration vs expenditure concentration).

- Next expansion: incorporate capital project lists and apply HUF to project portfolios (true finite elements with trace to project IDs).

## 12. Case Study C — Traffic signal telemetry (anomaly localization template)

This case shows how HUF behaves on operational event streams. The goal is not ‘compress for beauty’ — it is: what dominates anomalies, and where should you look first?

### 12.1 Finite element and budget definition (recommended)

Recommended finite element for anomaly work:
Finite element = TCS × PHASE × PHASE_STATUS_TEXT (optionally × PHASE_CALL_TEXT)
Budget = event share or severity‑weighted share (declare weights)
Output = which intersections/phases dominate drops/terminations/clearance with full trace to raw rows.

In this run we define a simple severity budget: Dropped calls weight 3, Termination statuses weight 2, everything else weight 1, then restrict the anomaly view to rows with severity > 1.

### 12.2 Compressed phase activity distribution (what dominates anomalies)

Figure 10. Traffic telemetry — anomaly severity budget by intersection (top contributors).

Figure 11. Traffic telemetry — anomaly severity budget by phase.

Figure 12. Traffic telemetry — anomaly severity budget by status.

Table 12‑A. Top intersections by anomaly severity budget share

Table 12‑B. Phases dominating the anomaly budget

Table 12‑C. Status distribution within anomaly budget

### 12.3 Traceability and actionability

A practical HUF anomaly run ends with a short, actionable list: top intersections, top phases, and the raw event rows supporting them. Backward traces should include timestamp ranges and source row IDs so an engineer can replay the evidence.

- If one intersection dominates: inspect controller configuration and detector health first.

- If one phase dominates across many intersections: inspect phase timing policy or coordination logic.

- If one status dominates: inspect the semantic definition (what exactly triggers ‘Termination’ in your system).

# Part III — Implementation, extension, and training

## 13. Reference implementation patterns

A handbook is useless if it can’t be implemented. This section defines the minimal architecture that prevents HUF from collapsing back into prose.

- Core data model: Element(id, rho, regime_path, trace).

- Adapters: domain-specific loaders and propagators that output the same element schema.

- I/O: artifact writers (CSV/JSON) that always include run stamps and file hashes.

- Tests: each reference run must have an automated test that checks unity, artifact emission, and stability packet generation.

Listing 13‑A. Reference core (excerpt, huf_core/core.py)

(Full source is intended for the accompanying repository/package; this excerpt is included for handbook completeness.)

## 14. How HUF prunes itself (expansion → contraction as a method)

The development history that produced this handbook is not a shameful detour — it is the method. You expand to explore, then you contract to ship. HUF applies to itself:

1. Expansion phase: explore candidate operations, artifacts, and narratives to discover what actually matters in practice.

1. Contraction phase: declare the contract, delete optionality from the core, and move everything else into extensions.

1. Stability phase: treat the framework definition as a system under HUF — track which sections survive pruning across reviewer critiques.

A useful internal exercise: assign a unity budget to sections of your draft (by reader time, by risk, or by implementation cost), then run HUF to see which sections dominate confusion or contribute little. That is ‘HUF on HUF.’

## 15. Training exercises (from toy to real)

Exercises are designed to build the habit of declaring budgets, regimes, and traces before you compute.

1. Take any spreadsheet with line items. Define finite elements and a mass budget. Produce the four artifacts.

1. Repeat with two regime partitions (by department vs by fund). Compare regime stability across thresholds.

1. Take an event log. Define anomaly budget weights. Produce a top‑N actionable list with backward traces to row IDs.

1. Design a propagation map (e.g., cost → ward) and prove conservation + traceability in one paragraph.

1. Perform a stability sweep and write the two-sentence interpretation of the stability packet.

# Appendix A — Data samples (print-friendly excerpts)

A1. Planck sample (first 5 coarse blocks; energies are in I² units)

A2. Markham sample (top 10 Fund×Category elements)

A3. Traffic sample (first 12 telemetry rows; severity weights shown)

# Appendix B — Artifact checklists (what a reviewer will ask for)

- Unity checks: global Σρ=1.0 after every normalization and renormalization step (log the tolerance).

- Discard ledger: list of excluded elements with their ρ; discarded sum must match 1−retained.

- Trace completeness: every retained element has a backward trace to finite elements (no null traces).

- Stability packet: sweep points, overlap metrics, regime rank stability, near‑τ band.

- Repro stamp: file hashes, code version, run_id, parameters (τ/target, seeds).

# Appendix C — Glossary (minimal)

Glossary

# Appendix D — Reproducibility stamps (recommended minimum)

Run stamp
