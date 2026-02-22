HUF polish bundle (v3)
======================

This v3 bundle fixes two issues:
1) PowerShell 5.1 parsing problems caused by non-ASCII characters in .ps1 files.
2) The '--' replacement bug (char vs string overload).

Included
--------
- scripts/fix_readme_mojibake.ps1  (ASCII-only; safe on Windows PowerShell 5.1)
- .gitattributes                   (exclude partner HTML from Linguist language stats)
- .gitignore.additions.txt         (lines to paste into your .gitignore)
- README_TOP_SUGGESTION.md         (new README header: no "Snapshot", PROOF moved up)

How to apply
------------
1) Unzip into your repo root (overwrite existing files).
2) Run:
   powershell -ExecutionPolicy Bypass -File scripts\fix_readme_mojibake.ps1

3) Verify:
   rg "â|Ã|Â" README.md

4) Commit + push:
   git add README.md .gitattributes
   git commit -m "Fix README encoding + adjust Linguist stats"
   git push

Generated: 2026-02-22T05:23:19
