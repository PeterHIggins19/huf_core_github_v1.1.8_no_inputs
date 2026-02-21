# Nav required

`nav_required.json` defines nav entries that should *always* be present in the sidebar.

Use it with:

- `scripts/ensure_nav_entries.py`

This avoids MkDocs warnings like:

- “pages exist in docs/ but are not included in nav”

…and prevents accidental nav regression when overlays overwrite mkdocs.yml.
