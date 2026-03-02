HUF-DOC: HUF.REL.DOCS.PAGE.DOCS_INVENTORY | HUF:1.1.8 | DOC:v0.1.0 | STATUS:release | LANE:release | RO:Peter Higgins
CODES: DOCS | ART: CM, AS, TR, EB | EVID:E1 | POSTURE:OP | WEIGHTS: OP=0.80 TOOL=0.20 PEER=0.00 | CAP: OP_MIN=0.51 TOOL_MAX=0.49 | CANON:docs/docs_inventory.md

# Docs inventory

This page is **generated** from the doc catalog:

- `notes/doc_catalog/docs_current.json`
- `notes/doc_catalog/docs_removed.json`

Do not edit this page by hand. Run:

```powershell
.\.venv\Scripts\python scripts/docs_hygiene.py
```

---

## Summary

- Current docs: **0**
- Removed docs tracked: **0**

---

## Current docs

| Group | Page | Path |
|---|---|---|

## Removed docs (tracked)

_None currently tracked._

---

## What changed?

If you want a visible changelog for stakeholders, keep `docs_removed.json` populated with entries like:

```json
[{"path":"old_page.md","removed_at":"2026-02-20","reason":"superseded","replaced_by":"new_page.md"}]
```
