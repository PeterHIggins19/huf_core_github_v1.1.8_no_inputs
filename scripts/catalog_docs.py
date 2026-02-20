\
r"""scripts/catalog_docs.py

Docs hygiene tool (MkDocs + Material), designed for Windows-friendly workflows.

Why this exists:
- Keeps `mkdocs build --strict` bulletproof by making nav / docs drift visible.
- Prevents accidental loss of pages during overlay merges.
- Maintains a “removed docs” tombstone list, and auto-recovers if a doc reappears.

What it writes (persisted):
- notes/doc_catalog/docs_current.json      (all Markdown files currently under docs/)
- notes/doc_catalog/docs_removed.json      (tombstones: pages that used to exist but are now missing)
- notes/doc_catalog/nav_files.json         (Markdown files referenced by mkdocs.yml nav)
- notes/doc_catalog/orphans.json           (docs present but not in nav; excludes '_' snippet files)
- notes/doc_catalog/missing_in_docs.json   (docs referenced by nav but missing on disk)

Rule:
- If a doc is in docs_removed.json but reappears under docs/, it is removed from docs_removed.json.

Run (PowerShell, repo venv):
  .\.venv\Scripts\python scripts/catalog_docs.py

Optional:
  .\.venv\Scripts\python scripts/catalog_docs.py --print-suggested-nav
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Set

import yaml


def sha256_text(path: Path) -> str:
    txt = path.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
    return hashlib.sha256(txt.encode("utf-8")).hexdigest()


def first_h1(path: Path) -> str:
    try:
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("# "):
                return line[2:].strip()
    except Exception:
        pass
    return ""


def scan_docs(docs_dir: Path) -> Dict[str, Dict[str, Any]]:
    items: Dict[str, Dict[str, Any]] = {}
    for p in sorted(docs_dir.rglob("*.md")):
        if not p.is_file():
            continue
        rel = p.relative_to(docs_dir).as_posix()
        items[rel] = {
            "path": rel,
            "title": first_h1(p),
            "sha256": sha256_text(p),
        }
    return items


def _extract_nav_yaml_text(mkdocs_text: str) -> str:
    """
    Extract just the `nav:` block from mkdocs.yml.

    This avoids PyYAML failures on Material's python tags like:
      emoji_index: !!python/name:material.extensions...

    We only need nav, and nav is plain YAML.
    """
    lines = mkdocs_text.splitlines()
    nav_start = None
    for i, line in enumerate(lines):
        if re.match(r"^nav:\s*$", line):
            nav_start = i
            break
    if nav_start is None:
        return "nav: []\n"

    # nav continues until next top-level key at column 0 (e.g., "theme:", "plugins:", etc.)
    nav_lines = [lines[nav_start]]
    for j in range(nav_start + 1, len(lines)):
        line = lines[j]
        if re.match(r"^[A-Za-z0-9_][A-Za-z0-9_\-]*\s*:\s*$", line) and not line.startswith(" "):
            break
        nav_lines.append(line)
    return "\n".join(nav_lines) + "\n"


def _walk_nav(node: Any, out: Set[str]) -> None:
    if node is None:
        return
    if isinstance(node, str):
        if "://" in node:
            return
        out.add(node.replace("\\", "/").lstrip("./"))
        return
    if isinstance(node, list):
        for x in node:
            _walk_nav(x, out)
        return
    if isinstance(node, dict):
        for _, v in node.items():
            _walk_nav(v, out)
        return


def parse_nav_files(mkdocs_yml: Path) -> Set[str]:
    mk_text = mkdocs_yml.read_text(encoding="utf-8")
    nav_yaml_text = _extract_nav_yaml_text(mk_text)
    data = yaml.safe_load(nav_yaml_text) or {}
    nav = data.get("nav", [])
    out: Set[str] = set()
    _walk_nav(nav, out)
    return {p for p in out if p.endswith(".md")}


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--print-suggested-nav", action="store_true")
    args = ap.parse_args()

    root = Path(__file__).resolve().parents[1]
    docs_dir = root / "docs"
    mkdocs_yml = root / "mkdocs.yml"
    catalog_dir = root / "notes" / "doc_catalog"
    catalog_dir.mkdir(parents=True, exist_ok=True)

    current = scan_docs(docs_dir)
    current_set = set(current.keys())

    nav_set = set(parse_nav_files(mkdocs_yml))

    def is_ignored(rel: str) -> bool:
        return Path(rel).name.startswith("_")

    orphans = sorted([p for p in current_set - nav_set if not is_ignored(p)])
    missing_in_docs = sorted([p for p in nav_set - current_set])

    prev_current = load_json(catalog_dir / "docs_current.json", {})
    prev_removed = set(load_json(catalog_dir / "docs_removed.json", []))

    # track newly removed
    for p in prev_current.keys():
        if p not in current_set:
            prev_removed.add(p)
    # auto-recover if reappears
    for p in list(prev_removed):
        if p in current_set:
            prev_removed.remove(p)

    save_json(catalog_dir / "docs_current.json", current)
    save_json(catalog_dir / "docs_removed.json", sorted(prev_removed))
    save_json(catalog_dir / "nav_files.json", sorted(nav_set))
    save_json(catalog_dir / "orphans.json", orphans)
    save_json(catalog_dir / "missing_in_docs.json", missing_in_docs)

    print(f"[root] {root}")
    print(f"[docs] {len(current_set)} markdown files under docs/")
    print(f"[nav ] {len(nav_set)} markdown files referenced by mkdocs.yml nav")
    print(f"[orphans] {len(orphans)} docs present but not in nav (excluding '_' snippets)")
    print(f"[missing] {len(missing_in_docs)} docs referenced by nav but missing on disk")
    print(f"[removed] {len(prev_removed)} docs tracked as removed")

    if orphans:
        print("\nOrphans (present in docs/, not in nav):")
        for p in orphans[:50]:
            print(f"  - {p}")
        if len(orphans) > 50:
            print("  ...")

    if missing_in_docs:
        print("\nMissing-in-docs (in nav, missing from docs/):")
        for p in missing_in_docs:
            print(f"  - {p}")

    if args.print_suggested_nav and orphans:
        print("\nSuggested nav leaf lines (paste where appropriate):")
        for p in orphans:
            title = current.get(p, {}).get("title") or Path(p).stem.replace("_", " ").title()
            print(f"      - {title}: {p}")

    return 2 if missing_in_docs else 0


if __name__ == "__main__":
    raise SystemExit(main())
