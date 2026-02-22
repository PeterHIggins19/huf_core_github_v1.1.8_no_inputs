HUF polish bundle (v4)
======================

Fixes
-----
- PowerShell 5.1 parsing issues (no backticks, no non-ASCII in the .ps1 file).
- Correctly repairs common mojibake (â€œ / Ã¢â‚¬Å“ forms) by CP1252->UTF8 reversal.
- Normalizes punctuation to ASCII to prevent recurrence.

Included
--------
- scripts/fix_readme_mojibake.ps1
- .gitattributes
- .gitignore.additions.txt
- README_TOP_SUGGESTION.md

Steps
-----
1) Unzip into repo root (overwrite existing files).
2) Run:
   powershell -ExecutionPolicy Bypass -File scripts\fix_readme_mojibake.ps1

3) Verify:
   rg "â|Ã|Â" README.md

4) Commit + push:
   git add README.md .gitattributes
   git commit -m "Fix README encoding + reduce Linguist HTML noise"
   git push

Generated: 2026-02-22T05:31:35
