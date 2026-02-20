\
"""scripts/cleanup_docs_snippets.py

Moves internal snippet markdown files out of docs/ so MkDocs doesn't report
"pages exist but are not included in nav".

Current behavior:
- moves docs/_snippet_windows_no_heredoc.md -> notes/orphaned_docs/_snippet_windows_no_heredoc.md

Run (repo venv):
  .\.venv\Scripts\python scripts/cleanup_docs_snippets.py
"""

from __future__ import annotations

from pathlib import Path
import shutil


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    docs = root / "docs"
    notes = root / "notes" / "orphaned_docs"
    notes.mkdir(parents=True, exist_ok=True)

    src = docs / "_snippet_windows_no_heredoc.md"
    if src.exists():
        dst = notes / src.name
        shutil.move(str(src), str(dst))
        print(f"[move] {src} -> {dst}")
    else:
        print("[ok] no snippet file to move")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
