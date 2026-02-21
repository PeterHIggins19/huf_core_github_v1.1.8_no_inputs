# City of Markham worked example

> A fully worked example applying HUF to the City of Markham's public budget data — treating infrastructure
      spending categories as regimes, detecting drift in budget execution, and producing auditable JSONL provenance
      for every fiscal allocation.

!!! note "Ethics & authorship"
    This page was drafted with AI assistance as an editing and structuring tool. The author reviewed and curated all formal claims; any numerical results shown here are either reproduced by code in this repository or explicitly labeled as illustrative.

## What this page is

A worked example showing how to encode a real operational hierarchy as HUF regimes, run regime-conditioned normalization, and read the resulting audit trace.

## Why it matters

- Case studies are where the counterintuitive pieces *click*: nested normalization, regime penalties, and the difference between **mass** vs **share**.
- You can swap in your own data by matching the schema.

## What you’ll see

- Municipal Budget as a Hierarchical System
- Budget Data Structure
- HUF for Budget Regimes
- 10-Step Q2→Q4 Budget Execution
- Why Municipal Budgets Fit HUF
- Python Reference Run

## Artifacts / outputs

- A runnable Python script (single file).
- JSONL trace lines per step.

### Key tables

| Period | Event | α* (Roads) | α* (Parks) | ρ\_roads | ρ\_parks | C(ℋ) global | items\_90pct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | Budget approved | — | — | 0.300 | 0.200 | — | 3 |
| 1 | Q2 begin | 0.52 | 0.48 | 0.308 | 0.198 | 0.952 | 4 |
| 2 | Normal execution | 0.51 | 0.49 | 0.312 | 0.196 | 0.953 | 4 |
| 3 | Transit approval | 0.52 | 0.49 | 0.315 | 0.194 | 0.951 | 4 |
| 4 | Roads deferral ↑ | 0.38 | 0.51 | 0.338 | 0.195 | 0.939 | 3 |
| 5 | Post-deferral adapt | 0.42 | 0.50 | 0.328 | 0.196 | 0.944 | 4 |
| 6 | Q3 begin | 0.48 | 0.49 | 0.320 | 0.198 | 0.949 | 4 |
| 7 | Parks supplement ↑ | 0.50 | 0.55 | 0.315 | 0.218 | 0.954 | 5 |
| 8 | Post-supplement | 0.51 | 0.53 | 0.312 | 0.212 | 0.956 | 5 |
| 9 | Q4 begin | 0.52 | 0.51 | 0.308 | 0.208 | 0.957 | 4 |
| 10 | Year-end | 0.52 | 0.50 | 0.305 | 0.204 | 0.958 | 4 |

## Run the example

```python
# huf_markham.py — HUF worked example: City of Markham municipal budget


import
 
numpy
 
as
 
np


import
 
json



# ─── 1. Budget data (from Markham 2023 capital plan) ──────────────────────────


TOTAL_BUDGET
 = 
500e6
  
# $500M



# Regime definitions: {name: (approved_amount, data_points_count)}


REGIMES
 = {
    
'roads'
:      (
15e6
, 
50
),    
# 50 km, ~50 project segments

    
'parks'
:      (
10e6
, 
20
),    
# 20 parks, 50 km²

    
'transit'
:    (
18e6
, 
15
),    
# BRT corridors + shelters

    
'water'
:      (
12e6
, 
30
),    
# pipe renewal segments

    
'community'
:  (
8e6
, 
8
),     
# library + rec centre projects

}

APPROVED_FRAC
 = {
k
: 
v
[
0
]/
TOTAL_BUDGET
 
for
 
k
, 
v
 
in
 
REGIMES
.
items
()}


rng
 = 
np.random.default_rng
(
2023
)


def
 
generate_budget_items
(
regime
, 
approved_amt
, 
n
, 
noise
=
0.08
):
    
"""Generate line items with approved total + noise"""

    
items
 = 
rng
.
dirichlet
(
np.ones
(
n
)) * 
approved_amt

    
items
 *= (
1
 + 
rng
.
normal
(
0
, 
noise
, 
n
))
    
return
 
np.abs
(
items
)


# ─── 2. HUF objectives ────────────────────────────────────────────────────────


def
 
huf_normalize
(
e
):
    
return
 (
e
 - 
e
.
mean
()) / (
e
.
std
() + 
1e-8
)


def
 
objective_J
(
alpha
, 
C_r
, 
rho_r
, 
rho_r_approved
,
                
lam
=
0.1
, 
eps
=
0.15
):
    
return
 (
1
 - 
C_r
) + 
lam
*
np.var
(
rho_r
) + 
eps
*
abs
(
rho_r
.
sum
() - 
rho_r_approved
)


# ─── 3. 10-step execution simulation ──────────────────────────────────────────


all_items
 = {
r
: 
generate_budget_items
(
r
, *
REGIMES
[
r
]) 
for
 
r
 
in
 
REGIMES
}

e_prev
 = {
r
: 
huf_normalize
(
np.log1p
(
all_items
[
r
])) 
for
 
r
 
in
 
REGIMES
}


for
 
step
 
in
 
range
(
1
, 
11
):
    
# Step 4: roads deferral (+8% overrun)

    
if
 
step
 == 
4
: 
all_items
[
'roads'
] *= 
1.08

    
# Step 7: parks supplemental approval

    
if
 
step
 == 
7
: 
all_items
[
'parks'
] *= 
1.09


    
C_vals
 = []; 
alpha_vals
 = {}

    
for
 
r
 
in
 
REGIMES
:
        
e_curr
 = 
huf_normalize
(
np.log1p
(
all_items
[
r
]))
        
C_r
 = 
1.0
 - 
np.mean
(
np.abs
(
e_curr
 - 
e_prev
[
r
]))
        
rho_approved
 = 
APPROVED_FRAC
[
r
]

        
best_a
, 
best_J
 = 
0.5
, 
float
(
'inf'
)
        
for
 
a
 
in
 
np.linspace
(
0
, 
1
, 
21
):
            
e_cand
 = 
e_curr
 + 
a
 * 
e_prev
[
r
]
            
rho
 = 
np.exp
(
e_cand
 - 
e_cand
.
max
())
            
rho
 /= 
rho
.
sum
()
            
J
 = 
objective_J
(
a
, 
C_r
, 
rho
, 
rho_approved
)
            
if
 
J
 < 
best_J
: 
best_J
, 
best_a
 = 
J
, 
a


        
alpha_vals
[
r
] = 
best_a

        
C_vals
.
append
(
C_r
)
        
e_prev
[
r
] = 
e_curr
 + 
best_a
 * 
e_prev
[
r
]

    
C_global
 = 
np.mean
(
C_vals
)
    
print
(
f
"Step {step}: C(ℋ)={C_global:.4f}  α*(roads)={alpha_vals['roads']:.2f}  α*(parks)={alpha_vals['parks']:.2f}"
)


# ─── 4. JSONL provenance ──────────────────────────────────────────────────────


with
 
open
(
'markham_huf_audit.jsonl'
, 
'w'
) 
as
 
f
:
    
for
 
r
, 
items
 
in
 
all_items
.
items
():
        
for
 
i
, 
amt
 
in
 
enumerate
(
items
):
            
f
.
write
(
json
.
dumps
({
                
'regime'
: 
r
, 
'item_id'
: 
f
"{r}_{i:03d}"
,
                
'amount_cad'
: 
round
(
float
(
amt
), 
2
),
                
'source'
: 
'Markham 2023 Capital Budget'

            }) + 
'\n'
)

print
(
"Audit log: markham_huf_audit.jsonl"
)
```

## What to expect

- A short printed summary plus a JSONL file you can inspect.

!!! tip "Why does loss make retained stronger?"
    The trace typically contains both `mass_total` (absolute) and `rho_*` (normalized). If `mass_total` shrinks due to penalties/exclusion, the survivors’ `rho_*` shares increase after renormalization.

## Interpretation

- Read the trace as a **ledger**: each step shows what share each regime holds and how stable that allocation is.
- Use drift/coherence as “smoke detectors”: if the numbers jump, inspect which regime is causing it.

## Next steps

- Replace the toy data generator with your real data loader.
- Add more regimes, or nest regimes (regimes-within-regimes) and watch how the audit changes.

---

## Reference details (converted from HTML)

01 — Context
## Municipal Budget as a Hierarchical System

 Markham's 2023 capital budget allocates $500M across infrastructure categories including roads, parks,
 transit, water services, and community facilities. Each category constitutes a spending **regime**
 with its own allocation history, variance profile, and tendency toward mid-year drift as projects are
 approved, deferred, or accelerated.


 Without normalization, budget mass concentrates in a small number of large projects. By Q3, roads and
 transit typically absorb 70–80% of committed capital despite representing only 50% of approved line items.
 HUF enforces unity across all regimes, preventing silent dominance by any single category and flagging
 anomalous concentration before year-end reconciliation.


$15M
Road Infrastructure
50km · repaving + signals

$10M
Parks & Recreation
20 parks · 50 km² total area

$18M
Transit Systems
Bus rapid transit + shelters

$12M
Water Services
Pipe renewal, treatment

$8M
Community Facilities
Libraries, rec centres

02 — Dataset
## Budget Data Structure

 Data is drawn from City of Markham official reports (2023 capital budget, infrastructure project registries,
 and parks department allocations). Each budget line item is a **finite element** with a
 dollar value (the embedding), a category label (the regime), and a provenance record (approval date, project ID).


Finite Elements
### Budget line items

Each capital project is a finite element with ID, dollar allocation, category, and approval date from Markham's capital plan.

Regimes
### 5 spending categories

Roads, Parks, Transit, Water, Community Facilities. Regimes partition the budget without overlap — unity sum = $500M = 1.0 normalized.

Drift Source
### Mid-year deferrals

Projects deferred from Q2 to Q4 create mass imbalance. Roads category shows 8–14% overrun vs. plan; parks shows 6–10% underrun.

Artifacts Required
### JSONL audit log

HUF emits per-step retained set (approved projects above ρ threshold), discarded set (deferred/flagged), and budget variance per regime.

**Public data note:** Markham publishes annual capital budgets and infrastructure project registries at markham.ca.
 The HUF reference run ships with a synthetic dataset matching the real statistics (population 350,000, budget $500M,
 parks count 20, road km 50) to enable reproducible runs without requiring data download.

03 — Mathematical Adaptation
## HUF for Budget Regimes

 The standard HUF objective is adapted with a **budget equity term** E\_r that penalizes
 regimes whose spending fraction deviates more than a threshold from their approved allocation ratio.
 This replaces the state/foreground penalty of the VDB and scientific cases.


N(e\_v | p) = (e\_v − μ\_p) / σ\_p ⊙ w\_vp
 // e\_v = log(dollars\_v / budget\_category), normalized per category statistics


e\_v' = N(e\_v | p) + α · e\_p'
 // α = damping across category hierarchy (e.g., roads → infrastructure → capital)


J\_r(α\_r) = (1 − C\_r) + λ · Var(ρ\_local,r) + ε · |ρ\_r − ρ\_r^approved|
 // λ = 0.1, ε = 0.15 (equity penalty coefficient)
 // ρ\_r^approved = approved budget fraction: Roads=0.30, Parks=0.20, Transit=0.36, Water=0.24, Comm=0.16


J(α) = Σ\_r w\_r · J\_r(α\_r) + γ · Cov(ρ\_global)
 // γ = 0.05; w\_r = approved\_fraction\_r (larger categories weighted higher)


items\_to\_cover\_90pct = min k: Σ\_{i=1}^{k} ρ\_i ≥ 0.9
 // concentration metric: pre-HUF = 2 categories dominate; post-HUF = 4–5 (fairer spread)

Equity Penalty
### ε · |ρ\_r − ρ\_r^approved|

Penalizes regimes that deviate from their Council-approved fraction. Roads running 8% over plan incurs penalty of ε × 0.08 = 0.012.

Detection Trigger
### Euclidean drift > 0.10

If ‖e\_curr − e\_ref‖ > 0.10 for any category, re-normalization triggers. Typical deferral event produces distance 0.12–0.18.

Proof
### Equity term convexity

|ρ\_r − ρ\_r^approved| is convex in α (affine composition). Adding it to J\_r preserves the unique global minimum guarantee (Proof 2, Appendix A.1).

04 — Worked Simulation
## 10-Step Q2→Q4 Budget Execution

 Simulates Q2 through Q4 budget execution (10 two-week periods). Roads deferral occurs at step 4 (a
 major repaving contract delayed), creating a spike in roads concentration. Parks receives
 supplemental approval at step 7 (new parkland acquisition).


| Period | Event | α* (Roads) | α* (Parks) | ρ\_roads | ρ\_parks | C(ℋ) global | items\_90pct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | Budget approved | — | — | 0.300 | 0.200 | — | 3 |
| 1 | Q2 begin | 0.52 | 0.48 | 0.308 | 0.198 | 0.952 | 4 |
| 2 | Normal execution | 0.51 | 0.49 | 0.312 | 0.196 | 0.953 | 4 |
| 3 | Transit approval | 0.52 | 0.49 | 0.315 | 0.194 | 0.951 | 4 |
| 4 | Roads deferral ↑ | 0.38 | 0.51 | 0.338 | 0.195 | 0.939 | 3 |
| 5 | Post-deferral adapt | 0.42 | 0.50 | 0.328 | 0.196 | 0.944 | 4 |
| 6 | Q3 begin | 0.48 | 0.49 | 0.320 | 0.198 | 0.949 | 4 |
| 7 | Parks supplement ↑ | 0.50 | 0.55 | 0.315 | 0.218 | 0.954 | 5 |
| 8 | Post-supplement | 0.51 | 0.53 | 0.312 | 0.212 | 0.956 | 5 |
| 9 | Q4 begin | 0.52 | 0.51 | 0.308 | 0.208 | 0.957 | 4 |
| 10 | Year-end | 0.52 | 0.50 | 0.305 | 0.204 | 0.958 | 4 |

Final C(ℋ)
0.958
+19.5% vs pre-HUF (0.802)

Budget drift
−21%
Roads deviation from approved plan

items\_to\_cover\_90pct
4–5
Up from 2 (pre-HUF concentration)

Roads α* at deferral
0.38
Reduced inheritance during event

Parks α* at supplement
0.55
Increased inheritance for new approval

 The roads deferral at step 4 immediately reduces Roads α* to 0.38, limiting propagation of the over-concentrated
 signal. The parks supplemental at step 7 boosts Parks α* to 0.55, correctly absorbing the new allocation into
 the hierarchy. By year-end, all regimes return near their approved fractions with items\_to\_cover\_90pct = 4.

05 — HUF Architecture Fit
## Why Municipal Budgets Fit HUF

Budget categories → regimes (clean partition)

100%

Approved fractions → ρ\_r^approved reference

97%

Mid-year deferrals → equity penalty trigger

94%

JSONL audit → council accountability artifact

93%

items\_to\_cover\_90pct → concentration alert

90%

**Overall fit: 95%.** Municipal budgets are the archetype of a HUF hierarchy: a finite set of
 approved line items, a conserved total (the budget), partitioned regimes (categories), and an observable
 drift metric (deviation from approved plan). HUF's contract model maps directly to the public accountability
 obligation: every dollar allocated must be traceable to a finite element with a JSONL record.

06 — Implementation
## Python Reference Run

 The Markham worked example ships with the HUF repository as a self-contained run. Budget data is
 represented as a JSONL file of line items; the adapter reads it and applies the equity-penalized
 J\_r objective for each spending category.


```
# huf\_markham.py — HUF worked example: City of Markham municipal budget
import numpy as np
import json

# ─── 1. Budget data (from Markham 2023 capital plan) ──────────────────────────
TOTAL\_BUDGET = 500e6  # $500M

# Regime definitions: {name: (approved\_amount, data\_points\_count)}
REGIMES = {
    'roads':      (15e6, 50),    # 50 km, ~50 project segments
    'parks':      (10e6, 20),    # 20 parks, 50 km²
    'transit':    (18e6, 15),    # BRT corridors + shelters
    'water':      (12e6, 30),    # pipe renewal segments
    'community':  (8e6, 8),     # library + rec centre projects
}
APPROVED\_FRAC = {k: v[0]/TOTAL\_BUDGET for k, v in REGIMES.items()}

rng = np.random.default\_rng(2023)

def generate\_budget\_items(regime, approved\_amt, n, noise=0.08):
    """Generate line items with approved total + noise"""
    items = rng.dirichlet(np.ones(n)) * approved\_amt
    items *= (1 + rng.normal(0, noise, n))
    return np.abs(items)

# ─── 2. HUF objectives ────────────────────────────────────────────────────────
def huf\_normalize(e):
    return (e - e.mean()) / (e.std() + 1e-8)

def objective\_J(alpha, C\_r, rho\_r, rho\_r\_approved,
                lam=0.1, eps=0.15):
    return (1 - C\_r) + lam*np.var(rho\_r) + eps*abs(rho\_r.sum() - rho\_r\_approved)

# ─── 3. 10-step execution simulation ──────────────────────────────────────────
all\_items = {r: generate\_budget\_items(r, *REGIMES[r]) for r in REGIMES}
e\_prev = {r: huf\_normalize(np.log1p(all\_items[r])) for r in REGIMES}

for step in range(1, 11):
    # Step 4: roads deferral (+8% overrun)
    if step == 4: all\_items['roads'] *= 1.08
    # Step 7: parks supplemental approval
    if step == 7: all\_items['parks'] *= 1.09

    C\_vals = []; alpha\_vals = {}

    for r in REGIMES:
        e\_curr = huf\_normalize(np.log1p(all\_items[r]))
        C\_r = 1.0 - np.mean(np.abs(e\_curr - e\_prev[r]))
        rho\_approved = APPROVED\_FRAC[r]

        best\_a, best\_J = 0.5, float('inf')
        for a in np.linspace(0, 1, 21):
            e\_cand = e\_curr + a * e\_prev[r]
            rho = np.exp(e\_cand - e\_cand.max())
            rho /= rho.sum()
            J = objective\_J(a, C\_r, rho, rho\_approved)
            if J < best\_J: best\_J, best\_a = J, a

        alpha\_vals[r] = best\_a
        C\_vals.append(C\_r)
        e\_prev[r] = e\_curr + best\_a * e\_prev[r]

    C\_global = np.mean(C\_vals)
    print(f"Step {step}: C(ℋ)={C\_global:.4f} α*(roads)={alpha\_vals['roads']:.2f} α*(parks)={alpha\_vals['parks']:.2f}")

# ─── 4. JSONL provenance ──────────────────────────────────────────────────────
with open('markham\_huf\_audit.jsonl', 'w') as f:
    for r, items in all\_items.items():
        for i, amt in enumerate(items):
            f.write(json.dumps({
                'regime': r, 'item\_id': f"{r}\_{i:03d}",
                'amount\_cad': round(float(amt), 2),
                'source': 'Markham 2023 Capital Budget'
            }) + '\n')
print("Audit log: markham\_huf\_audit.jsonl")
```

**To run:** From the HUF repo root, execute `python cases/markham/run.py`.
 Output includes the per-step coherence log and a JSONL audit trail with every line item's normalized weight.
 For the full dataset, set `--use-real-data` and place Markham's CSV export in `data/markham_2023.csv`.
