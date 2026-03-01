HUF-DOC: HUF.REL.ORG.NOTE.AI_USE_STANDARD | HUF:1.1.8 | DOC:v0.2.0 | STATUS:draft | LANE:release | RO:Peter Higgins
CODES: ORG, AI_DISCLOSURE, SAFETY | ART: TR, EB | EVID:E0 | POSTURE:OP | WEIGHTS: OP=0.80 TOOL=0.20 PEER=0.00 | CAP: OP_MIN=0.51 TOOL_MAX=0.49 | CANON:notes/_org/ai_use_standard.md

# HUF AI Use Standard (one-page insert)
AI tools may assist drafting/editing/critique. The operator reviews/curates final content.

## Human-in-command
AI output is advisory. No release occurs without explicit human approval.

## Declared weights (required)
Weights must be declared and sum to 1.0:
- OP (Responsible Operator)
- TOOL (AI/tools)
- PEER (humans)

Hard cap:
- OP >= 0.51
- TOOL <= 0.49

Beginner recommendation:
- OP=0.80 TOOL=0.20

## What weights control
Weights apply to draft readiness only.
Release/publish/merge/send is human-only.

## Minimal disclosure line
AI-assisted drafting/editing may be used for clarity; the operator reviewed/curated final content. Formal claims are conservative and supported by reproducible artifacts where stated.
