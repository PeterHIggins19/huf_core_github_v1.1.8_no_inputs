HUF-DOC: HUF.REL.ORG.POLICY.DOC_GOVERNANCE | HUF:1.1.8 | DOC:v0.2.0 | STATUS:draft | LANE:release | RO:Peter Higgins
CODES: ORG, GOVERNANCE | ART: CM, AS, TR, EB | EVID:E1 | POSTURE:OP | WEIGHTS: OP=0.80 TOOL=0.20 PEER=0.00 | CAP: OP_MIN=0.51 TOOL_MAX=0.49 | CANON:notes/_org/doc_governance.md

# HUF Document Governance
*Repo management standard (draft) — 2026-03-01*

This file defines the minimum rules that prevent:
- naming collisions
- silent overwrites
- unclear canonicity ("which version is real?")

HUF principle applied to documentation:
> **Nothing disappears silently.**  
If weights and gates are not declared, the system cannot be audited.

---

## 1) Doc ID rules (required)

Every document MUST have a stable Doc ID that never changes.

Format:
`HUF.<LANE>.<DOMAIN>.<TYPE>.<SLUG>`

- LANE: `DRAFT | REL | LEGACY`
- DOMAIN: `ORG | LRN | BOOK | CASE | PARTNER | WIKI | SOFTWARE`
- TYPE: `POLICY | INDEX | MODULE | MANUSCRIPT | PRIMER | LETTER | EXHIBIT | NOTE | TEMPLATE | TRACE | PACKAGE | SCRIPT | DATA | CODE`
- SLUG: uppercase + underscores

Doc versions:
- `HUF:X.Y.Z` — framework version assumed
- `DOC:vX.Y.Z` — document revision

---

## 2) Two-line header rule (required)

Every document MUST begin with these two lines (or first-page block for DOCX/PDF).

Line 1:
`HUF-DOC: <DOC_ID> | HUF:<HUF_VERSION> | DOC:<DOC_VERSION> | STATUS:<status> | LANE:<lane> | RO:<responsible_operator>`

Line 2:
`CODES: <tags> | ART: CM, AS, TR, EB | EVID:E0-E4 | POSTURE: DEF/OP/INT/THM | WEIGHTS: OP=.. TOOL=.. PEER=.. | CAP: OP_MIN=0.51 TOOL_MAX=0.49 | CANON:<canonical_path>`

If a document lacks the header, it is treated as INBOX (not canonical).

---

## 3) Lanes (media flow)

- **INBOX:** `notes/current_documents/inbox/YYYY-MM/` (raw intake)
- **STAGED:** `notes/current_documents/staged/<DOC_ID>/` (ID + header + manifest entry)
- **RELEASE:** canonical stable paths under `docs/`, `cases/`, or `notes/_org`
- **LEGACY:** retained trail; marked deprecated with `superseded_by`

---

## 4) Status definitions

- `draft` — moving; not safe to circulate
- `reviewed` — stable structure (48h no structural change) + header + manifest entry
- `release` — safe to circulate; posture aligned; canonical path locked; human-only release gate passed
- `deprecated` — superseded; retained for audit trail

---

## 5) Artifact abbreviations (locked)

- `CM` — Coherence Map
- `AS` — Active Set
- `TR` — Trace Report
- `EB` — Error Budget

---

## 6) Evidence levels (E0–E4)

- `E0` Narrative only
- `E1` Artifact evidence
- `E2` Reproducible run (code + inputs -> outputs)
- `E3` Empirical evaluation (real dataset + method)
- `E4` Formal proof (assumptions + proof)

---

## 7) Operator control contract (HUF-51/49) — required

Safety posture: **the tool must never control the operator.**

Declared weights MUST satisfy:
- `OP >= 0.51`
- `TOOL <= 0.49`
- `OP + TOOL + PEER = 1.0`

Recommended presets:
- Beginner: `OP=0.80 TOOL=0.20 PEER=0.00`
- Team: `OP=0.65 TOOL=0.20 PEER=0.15`
- Mature experimental: `OP=0.51 TOOL=0.49 PEER=0.00` (explicit opt-in)

Weights apply to draft readiness only.
Release/publish/merge/send remains human-only.

---

## 8) Supersedes rule (no silent replacement)

If a document replaces another, it MUST declare:
- `supersedes: [old_doc_id]`
and the old doc MUST be marked:
- `deprecated` + `superseded_by`

Policy: nothing disappears silently.
