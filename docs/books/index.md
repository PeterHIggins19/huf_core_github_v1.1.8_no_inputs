HUF-DOC: HUF.REL.BOOK.INDEX.BOOKS | HUF:1.1.8 | DOC:v0.2.0 | STATUS:release | LANE:release | RO:Peter Higgins
CODES: BOOK, INDEX | ART: CM, AS, TR, EB | EVID:E1 | POSTURE:OP | WEIGHTS: OP=0.80 TOOL=0.20 PEER=0.00 | CAP: OP_MIN=0.51 TOOL_MAX=0.49 | CANON:docs/books/index.md

# HUF Books

This section is the **stable, public library** of HUF long-form documents.

- **Release lane:** Markdown-first, link-stable, suitable for citation.
- **Draft lane:** clearly marked; content may change.
- **Source artifacts:** DOCX working files live under `notes/current_documents/` (not in MkDocs nav).

---

## Current sources (authoritative working copies)

These links point to the authoritative working copies under `notes/current_documents/staged/`.

| Book | Current source |
|---|---|
| HUF Handbook | https://github.com/PeterHiggins19/huf_core/blob/main/notes/current_documents/staged/HUF.LEGACY.BOOK.MANUSCRIPT.HUF_HANDBOOK_V1_2_0/HUF_Handbook_v1.2.0.docx |
| HUF Reference | https://github.com/PeterHiggins19/huf_core/blob/main/notes/current_documents/staged/HUF.DRAFT.BOOK.MANUSCRIPT.HUF_COMPLETE_REFERENCE_FEB2026/HUF_Complete_Reference_Feb2026.docx |

## Quick pick (what to read first)

| If you want… | Read |
|---|---|
| A technical map of “what HUF is” without overclaiming | **[HUF Field Guide](../field_guide.md)** |
| To run HUF and interpret outputs | **[HUF Handbook (current)](../handbook.md)** |
| A definitions-first reference you can cite internally | **[HUF Reference (current)](../huf_reference.md)** |
| Disclosure + conservative claims posture | **[Ethics & disclosure](../ethics.md)** |
| The motivating essay (interpretive) | **[The Trap of Coherence](../trap_of_coherence.md)** |

---

## Books by difficulty

### Level 1 — Orientation (start here)
- **[HUF Field Guide](../field_guide.md)**  
  Purpose: a clean conceptual map (formal core vs interpretive extensions).  
  Output: you should be able to explain regimes, mass accounting, and the CM/AS/TR/EB artifacts.

- **[Ethics & disclosure](../ethics.md)**  
  Purpose: AI-assisted drafting disclosure, scope boundaries, reproducibility posture.

### Level 2 — Operator manual (run the system)
- **[HUF Handbook (current)](../handbook.md)**  
  Purpose: step-by-step “run it / read artifacts / troubleshoot”.  
  Audience: operators, analysts, engineers.

### Level 3 — Reference (definitions + nomenclature)
- **[HUF Reference (current)](../huf_reference.md)**  
  Purpose: stable definitions, symbols, and conservative claims you can point to.

### Level 4 — Advanced mathematics (draft, expanding)
- **[Advanced Mathematics Handbook (draft)](advanced_mathematics/)**  
  Purpose: deeper formalism and extensions.  
  Status: **draft** (expect edits; claims must remain labeled and conservative).

---

## Books by purpose

### Onboarding and shared vocabulary
- Field Guide
- Ethics & disclosure
- Reference

### Getting real work done (operators)
- Handbook
- Running examples (see **[Running examples](../running_examples.md)**)

### Interpretation and motivation (clearly labeled)
- **[The Trap of Coherence](../trap_of_coherence.md)**  
- Optional mirror version (for historical continuity): **[Trap of Coherence (wiki mirror)](../wiki_trap_of_coherence.md)**

---

## Notes for contributors

- If you add a new book: link it here, add it to MkDocs nav, and apply the **two-line HUF header**.
- Keep “draft vs release” explicit.
- Do not host raw HTML in `docs/` (keep partner HTML under `notes/partner_html/`).

