HUF-DOC: HUF.REL.LRN.MODULE.02_FORMAL_CORE | HUF:1.1.8 | DOC:v0.1.0 | STATUS:draft | LANE:release | RO:Peter Higgins
CODES: LRN, 02_FORMAL_CORE | ART: CM, AS, TR, EB | EVID:E0 | POSTURE:OP | WEIGHTS: OP=0.80 TOOL=0.20 PEER=0.00 | CAP: OP_MIN=0.51 TOOL_MAX=0.49 | CANON:docs/learning/02_formal_core/index.md

# Formal core (conservative)

What this page is:
A minimal “formal core” that is safe to state publicly: normalized weights, regimes as sub-objects, and sum-preserving mappings.

Why it matters:
It separates what’s formally defined from interpretive extensions (analogies, cross-domain comparisons).

What you’ll see:
- Objects, regimes, morphisms (minimal)
- Invariance statement (sum preservation)
- What is *not* claimed here

## Minimal formal core

A convenient formalization is:

- An **object** is a pair `(V, ρ)` where:
  - `V` is a finite-dimensional real vector space
  - `ρ` assigns nonnegative weights to a basis, with `Σ ρ = 1`

- A **regime** is a sub-collection `R ⊆ V` that is normalized locally:
  - `Σ_{r in R} ρ(r) = 1`

- A **morphism** is a map that preserves the relevant sums under transformation.

This is the “sum-preserving” backbone used by the implementation.

## Invariance (what HUF preserves)

At minimum, HUF preserves:

- **global normalization** (the total distribution sums to 1)
- **local normalization** inside regimes (when computed)

## What we are NOT claiming here

This module does **not** claim that:
- HUF is equivalent to sheaf theory / cohomology, topology, Langlands, etc.
- cross-domain “applications” are established results

Those can exist as **interpretive motivation** elsewhere, but they’re not treated as formal results in this learning track.

## Run the example

Any run gives you the invariance story in artifacts:
- AS shows normalized shares
- EB shows discarded mass explicitly

Next steps:
- Go to **03 Artifacts** to learn how to read the outputs like a reviewer.
