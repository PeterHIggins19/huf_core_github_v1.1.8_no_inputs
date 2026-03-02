HUF-DOC: HUF.REL.DOCS.PAGE.REPO_HYGIENE | HUF:1.1.8 | DOC:v0.1.0 | STATUS:release | LANE:release | RO:Peter Higgins
CODES: DOCS | ART: CM, AS, TR, EB | EVID:E1 | POSTURE:OP | WEIGHTS: OP=0.80 TOOL=0.20 PEER=0.00 | CAP: OP_MIN=0.51 TOOL_MAX=0.49 | CANON:docs/repo_hygiene.md

# Repo hygiene (clean commits)

If you publish `site/` (MkDocs output) or `out/` (run artifacts) into git, GitHub will treat the repo like a static site
and the language bar becomes “mostly HTML”. This can reduce credibility for technical skimmers.

This repo is set up to **build** `site/` in GitHub Actions and publish it to Pages — you should not commit `site/`.

---

## Quick cleanup (recommended)

1) Ensure `.gitignore` includes:

- `site/`
- `out/`
- `*.egg-info/`
- `.venv/`

2) Remove generated folders from git tracking (keeps local files on disk):

```powershell
git rm -r --cached site out huf_core.egg-info
git commit -m "Repo hygiene: stop tracking generated outputs"
git push
```

If you don’t have `huf_core.egg-info` tracked, remove it from the command.

---

## Helper script (dry-run by default)

This repo includes a helper that detects tracked generated files and prints the exact commands:

```powershell
.\.venv\Scripts\python scripts/repo_cleanup.py
```

To apply automatically:

```powershell
.\.venv\Scripts\python scripts/repo_cleanup.py --apply
```

---

## Why this matters

- Cleaner diffs
- Fewer merge conflicts
- Correct GitHub language stats (shows Python, not HTML)
- Faster PR review (no “built site” noise)
