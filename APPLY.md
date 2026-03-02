# Paste-over patch: docs clean + mkdocs nav + HUF headers

This patch:
- Adds HUF two-line headers to all docs pages missing them (keeps existing headers)
- Fixes Field Guide anchor mismatch (double hyphen -> single)
- Updates mkdocs.yml nav so Learning + Books (and everything else) appears on the site
- Includes scripts/doc_inventory.py (placeholder DOC_ID ignored)

Apply:
1) Paste all contents of this zip into repo root (merge/overwrite).
2) Run:
   .\.venv\Scripts\python -m mkdocs build --strict

If you want to regenerate the manifest after:
   .\.venv\Scripts\python scripts\doc_inventory.py --root . --write --merge
