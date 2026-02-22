HUF polish bundle
=================

Included
--------
- scripts/fix_readme_mojibake.ps1      (fix UTF-8 mojibake in README.md)
- .gitattributes                       (exclude partner HTML from Linguist language stats)
- .gitignore.additions.txt             (lines to paste into your .gitignore)
- README_TOP_SUGGESTION.md             (suggested new README header with PROOF line)

How to use
----------
1) Unzip into your repo root (it adds scripts/ and the other files).
2) Fix README encoding:
   powershell -ExecutionPolicy Bypass -File scripts\fix_readme_mojibake.ps1

3) Apply .gitattributes:
   - If you already have .gitattributes, merge the content.
   - Otherwise copy in the provided .gitattributes.

4) Add the .gitignore additions:
   - Paste the contents of .gitignore.additions.txt into your existing .gitignore.

5) (Optional) Update README title + move PROOF line up:
   - Use README_TOP_SUGGESTION.md as your new top section.

Generated: 2026-02-22T05:11:56
