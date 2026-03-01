# doc_inventory.py (manual manifest regeneration)
This script scans the repo for the **two-line HUF header** and regenerates:

- `notes/_org/doc_manifest.json`

It is designed to be run manually (not CI) while the corpus is still moving.

## What it scans
Text files: `.md .py .js .jsx .ts .tsx .txt .sh .ps1 .yml .yaml`
DOCX files: `.docx` (reads first paragraphs) — optional but supported.

## What it extracts
From line 1:
- doc_id, huf_version, doc_version, status, lane, RO

From line 2:
- codes, artifacts, evidence, posture, weights, caps, canonical_path

## Usage (PowerShell)
```powershell
.\.venv\Scripts\python scripts\doc_inventory.py --root . --write
```

Preview only:
```powershell
.\.venv\Scripts\python scripts\doc_inventory.py --root . --print
```

If you want the script to **merge** with existing manifest rather than overwrite, add `--merge`.
(Default is overwrite-with-backup.)

## Safety
- Creates a timestamped backup of any existing manifest before writing.
- Skips generated folders by default (site/, out/, .venv/, .git/, node_modules/, etc.)

Created: 2026-03-01
