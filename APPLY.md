# Patch: Fix MkDocs strict warnings from docs/index.md

This replaces `docs/index.md` with a version that:
- removes invalid `docs/...` link prefixes
- converts non-doc-file links (scripts, START_HERE_*.bat/.command/.sh) to external GitHub links
- adds HUF two-line header (as YAML comments)

Apply:
- paste `docs/index.md` over your repo `docs/index.md`

Then:
```powershell
.\.venv\Scripts\python -m mkdocs build --strict
```
