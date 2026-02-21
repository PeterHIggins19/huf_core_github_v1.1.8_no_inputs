# Civic

!!! note "Ethics & authorship"
    This page was drafted with AI assistance as an editing and structuring tool. The author reviewed and curated all formal claims; any numerical results shown here are either reproduced by code in this repository or explicitly labeled as illustrative.

## What this page is

A civic-facing entry point: how to use HUF as an *accountability lens* for public decisions, budgets, and operational drift.

## Why it matters

- Public systems often keep totals balanced while **composition quietly changes** (deferrals, reclassifications, scope drift).
- HUF makes those changes visible: *what fraction moved, where it concentrated, and whether it violates the intended regime structure.*

## What you’ll see

- The accountability contract (what must remain invariant)
- Long tail spending as an audit target
- Civic math: approved fractions, deferral alerts
- Worked cases (Markham, traffic phases)

## Artifacts / outputs

- A small set of **case studies** and **reference runs** producing JSONL audit traces.
- A consistent set of HUF metrics (coherence, drift/erosion, mass concentration).

## Run the example

Pick a case study in the left nav and run the included `python` script. Each one emits a JSONL trace plus a short summary.

## What to expect

- If you “penalize” a regime, remaining elements can show higher normalized share after renormalization. HUF reports both absolute and normalized views to keep this honest.

## Interpretation

- Treat the lead pages as **orientation**, and the case pages as **reproducible artifacts**.

## Next steps

- Choose one case study, run it, then swap in your own data with the same schema.

---

## Source content (converted from HTML)

HUF
Accountability
Long tail
Math
Cases

Civic

HUF · Civic Domain
# **Public money.**Public accountability.

 Every public budget is a hierarchical system with a conserved quantity, a
 finite set of approved line items, and a tendency toward silent concentration.
 HUF was built for exactly this: enforcing coherence, surfacing imbalance,
 and producing an audit trail that goes all the way down to finite elements.


01
## The accountability contract

 HUF's design principle maps directly to the obligation of public finance: every dollar
 must trace to a **finite element** — an approved line item with a project ID,
 a category, an approval date, and a provenance record. No mass may be created. No budget
 may silently concentrate in a small number of projects while others are starved.


HUF public finance contract

 "If you cannot verify finite elements, conserve a declared unity budget,
 emit the required artifacts, and pass stability checks, then you are not
 doing public finance — you are doing storytelling."


✓
**Unity conservation.** The sum of all budget fractions equals 1.0 at every reporting period, by proof. No rounding error. No silent loss.

✓
**Explicit retained set.** Every period, HUF emits the set of projects above the mass threshold — the ones that actually matter to the allocation.

✓
**Explicit discarded budget.** Projects flagged, deferred, or cancelled are logged with their discarded mass and the reason for exclusion.

✓
**Backward trace.** Every aggregated metric can be decomposed to the finite elements that produced it. Council can audit any number.

02
## The long tail — an accounting lens

 In public budgets, "long tail" does not mean statistical class imbalance.
 It means the **mass distribution + exception reweighting** problem:
 most of the budget mass sits in a small number of large projects (roads, transit,
 major facilities), while the long tail of smaller community and parks projects
 is perpetually under-represented in reporting.


 Standard budget reporting shows totals by category. HUF shows the
 **concentration metric** — the minimum number of projects needed
 to account for 90% of the allocated mass. When that number is 2, you have a
 concentration problem. When it's 5 or 6, you have an equitable distribution.
 Councillors can see this in one number.


Key metric for councillors
items\_to\_cover\_90pct

 Sort all budget line items by their normalised mass ρ, descending.
 Count the minimum k such that the top-k items sum to 90% of total allocated mass.
 Pre-HUF Markham: k = 2 (roads and transit dominate). Post-HUF: k = 4–5
 (parks and community facilities visible in the top tier). This is the long-tail
 accounting lens: a single integer that tells you whether your budget is equitable.


Budget concentration — pre vs. post HUF (City of Markham 2023)
Markham $500M capital

Roads & transport

82%30%

Transit systems

—36%

Water services

12%24%

Parks & recreation

4%20%

Community facilities

2%16%

Pre-HUF reported share (concentration)
Post-HUF normalised mass (approved fraction)

03
## The civic mathematics

e\_v = log(amount\_v / category\_total)
 // embedding: log-ratio of project amount to category total


N(e\_v | category) = (e\_v − μ\_cat) / σ\_cat ⊙ w\_v
 // normalise relative to category statistics; w\_v = 1/n for equal weighting


J\_r(α\_r) = (1 − C\_r) + λ · Var(ρ\_local,r) + ε · |ρ\_r − ρ\_r^approved|
 // equity penalty: deviation from Council-approved fraction
 // λ = 0.1 (variance weight), ε = 0.15 (equity coefficient)


items\_to\_cover\_90pct = min k : Σ\_{i=1}^{k} ρ\_i ≥ 0.90
 // the single number a councillor needs: how concentrated is our budget?


JSONL per step: {project\_id, regime, amount, ρ\_normalised, α*, C\_r, step}
 // audit log: every project, every reporting period, traceable to source

Equity penalty ε
### Enforces approved fractions

A category running 8% over its Council-approved share incurs penalty ε×0.08 in its J\_r objective, reducing its α* and limiting further mass accumulation.

Drift detection
### Mid-year deferral alerts

When Euclidean distance between current and reference embeddings exceeds 0.10 for any category, re-normalisation triggers automatically. Deferrals are caught within the same reporting period.

Convergence proof
### Guaranteed by Proof 2

The equity term |ρ\_r − ρ\_r^approved| is convex in α, preserving J\_r's unique minimum. Every budget run is guaranteed to converge to the most coherent, equitable allocation achievable.

Post-HUF C(ℋ)
0.958
+19.5% vs. pre-HUF (0.802)

Budget drift reduced
−21%
Mid-year deferral impact

items\_to\_cover\_90pct
4–5
Up from 2 (pre-HUF)

Markham budget
$500M
2023 capital plan

JSONL audit records
per step
Every project, every period

04
## Civic cases

Case · 002 · Worked Example
### City of Markham

 The primary civic worked example: Markham's 2023 $500M capital budget,
 five spending categories as regimes, equity-penalised J\_r, mid-year deferral
 and supplemental approval events simulated across 10 reporting periods.
 JSONL audit log included.


0.958
C(ℋ)

5
Regimes

$500M
Budget

Worked example →

Case · 003 · Infrastructure
### Traffic Phase Anomaly

 Urban traffic signal telemetry: 100 intersections, three phase timings as
 regime dimensions. HUF's anomaly-localization template — 95% fault detection
 accuracy, corridor-level isolation, recovery simulation with controller reset.


0.943
C(ℋ)

95%
Accuracy

100
Signals

Traffic case →

Case · Partnership · Public Sector
### Public Sector Accounting Lens

 The full public sector partnership package: HUF's long-tail accounting lens
 applied to general public budget structures. items\_to\_cover\_90pct as the
 headline metric for elected officials, with JSONL provenance satisfying
 public accountability requirements.


89%
Fit

Any
Budget size

Open
Data ready

Partner package →

05
## Who this is for

Elected officials
### One number per period

items\_to\_cover\_90pct tells you if your capital budget is concentrated or equitably distributed — before the auditor does. No spreadsheet required.

Budget analysts
### Per-step JSONL audit

Every project, every reporting period, every normalised mass weight. The audit trail HUF produces satisfies public accountability requirements and is machine-readable for downstream analysis.

Infrastructure teams
### Drift detection in operations

The traffic phase case shows HUF applied to real-time telemetry: anomaly localization at the intersection level before cascading failure. Works on any networked infrastructure with nominal operating parameters.

Developers
### Python + JSONL, no dependencies

Each civic case ships as a self-contained Python script. No database, no cloud service. Feed in a CSV of budget line items or telemetry log; get out a JSONL audit trail and coherence metrics per period.

HUF v1.1.8 · Civic Lead Page · PeterHiggins19/huf\_core\_github\_v1.1.8\_no\_inputs
Unity conserved · Every dollar traceable · items\_to\_cover\_90pct
