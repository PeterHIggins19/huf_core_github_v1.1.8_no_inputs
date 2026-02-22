Partner HTML Link Patch (v2)
============================

Why v2
------
PowerShell hashtables are case-insensitive by default, so keys that differ only by case
(e.g., PeterHiggins19 vs PeterHIggins19) trigger a "duplicate key" parser error.
v2 uses an ordered list of replacement pairs instead.

Purpose
-------
Updates partner-facing HTML (and any accompanying markdown/text in the same folder)
so all links/footers point to the canonical repo/site:

  Repo: https://github.com/PeterHiggins19/huf_core
  Docs: https://peterhiggins19.github.io/huf_core/

What it does
------------
- Creates a timestamped backup folder next to notes\partner_html
- Rewrites old repo/site strings to the new canonical ones
- Fixes the common typo "PeterHIggins19" -> "PeterHiggins19"
- Updates git+ install URLs and "cd ..." instructions

How to run (PowerShell)
-----------------------
From the repo root:

  powershell -ExecutionPolicy Bypass -File scripts\patch_partner_html_links.ps1

Optional: also patch notes\legacy_md:

  powershell -ExecutionPolicy Bypass -File scripts\patch_partner_html_links.ps1 -IncludeLegacyNotes

Verify
------
  rg "huf_core_github_v1\.1\.8_no_inputs|PeterHIggins19|peterhiggins19\.github\.io/huf_core_github_v1\.1\.8_no_inputs" -n notes\partner_html

Commit
------
  git add notes\partner_html
  git commit -m "Update partner HTML links to canonical huf_core repo/site"
  git push

Generated: 2026-02-22T04:10:14
