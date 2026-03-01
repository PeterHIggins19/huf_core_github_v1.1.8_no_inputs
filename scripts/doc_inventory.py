\
#!/usr/bin/env python
"""
HUF doc inventory scanner (manual tool)

Scans for the HUF two-line header:

Line 1:
  HUF-DOC: <DOC_ID> | HUF:<HUF_VERSION> | DOC:<DOC_VERSION> | STATUS:<status> | LANE:<lane> | RO:<name>

Line 2:
  CODES: ... | ART: CM, AS, TR, EB | EVID:E0-E4 | POSTURE: DEF/OP/INT/THM |
  WEIGHTS: OP=.. TOOL=.. PEER=.. | CAP: OP_MIN=.. TOOL_MAX=.. | CANON:<path>

Writes notes/_org/doc_manifest.json

This is intended to be run manually until structure stabilizes.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from docx import Document  # type: ignore
except Exception:
    Document = None  # type: ignore

SKIP_DIRS = {
    ".git", ".venv", "venv", "site", "out", "node_modules", "__pycache__",
    ".pytest_cache", ".mypy_cache", ".ruff_cache", ".idea", ".vscode",
}

TEXT_EXTS = {
    ".md", ".txt", ".py", ".js", ".jsx", ".ts", ".tsx", ".sh", ".ps1",
    ".yml", ".yaml",
}
DOCX_EXTS = {".docx"}

H1_PAT = re.compile(r"^\s*(?:#\s*)?(?://\s*)?(?:/\*\s*)?(?:\*\s*)?HUF-DOC:\s*(.+?)\s*$")
H2_PAT = re.compile(r"^\s*(?:#\s*)?(?://\s*)?(?:\*\s*)?CODES:\s*(.+?)\s*$")
PIPE_SPLIT = re.compile(r"\s*\|\s*")

def _parse_kv_segments(line: str) -> Dict[str, str]:
    parts = [p.strip() for p in PIPE_SPLIT.split(line.strip()) if p.strip()]
    out: Dict[str, str] = {}
    if not parts:
        return out
    out["_first"] = parts[0]
    for seg in parts[1:]:
        if ":" in seg:
            k, v = seg.split(":", 1)
            out[k.strip().lower()] = v.strip()
        else:
            out[seg.strip().lower()] = ""
    return out

def _parse_codes_line(line: str) -> Dict[str, Any]:
    parts = [p.strip() for p in PIPE_SPLIT.split(line.strip()) if p.strip()]
    codes_raw = parts[0]
    out: Dict[str, Any] = {"codes": [c.strip() for c in codes_raw.split(",") if c.strip()]}
    for seg in parts[1:]:
        up = seg.upper()
        if up.startswith("ART"):
            _, v = seg.split(":", 1)
            out["artifacts"] = [a.strip() for a in v.split(",") if a.strip()]
        elif up.startswith("EVID"):
            _, v = seg.split(":", 1)
            out["evidence"] = v.strip()
        elif up.startswith("POSTURE"):
            _, v = seg.split(":", 1)
            out["posture"] = v.strip()
        elif up.startswith("WEIGHTS"):
            _, v = seg.split(":", 1)
            w = {}
            for tok in re.split(r"[,\s]+", v.strip()):
                if "=" in tok:
                    k, val = tok.split("=", 1)
                    try:
                        w[k.strip().lower()] = float(val.strip())
                    except Exception:
                        pass
            out["weights"] = {"op": w.get("op"), "tool": w.get("tool"), "peer": w.get("peer")}
        elif up.startswith("CAP"):
            _, v = seg.split(":", 1)
            c = {}
            for tok in re.split(r"[,\s]+", v.strip()):
                if "=" in tok:
                    k, val = tok.split("=", 1)
                    try:
                        c[k.strip().lower()] = float(val.strip())
                    except Exception:
                        pass
            out["caps"] = {"op_min": c.get("op_min"), "tool_max": c.get("tool_max")}
        elif up.startswith("CANON"):
            _, v = seg.split(":", 1)
            out["canonical_path"] = v.strip()
    return out

def _scan_text_file(path: Path) -> Optional[Dict[str, Any]]:
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return None
    h1_i = None
    h1_val = None
    for i, line in enumerate(lines[:120]):
        m = H1_PAT.match(line)
        if m:
            h1_i = i
            h1_val = m.group(1).strip()
            break
    if h1_i is None or h1_val is None:
        return None

    codes_val = None
    for j in range(h1_i + 1, min(h1_i + 60, len(lines))):
        m2 = H2_PAT.match(lines[j])
        if m2:
            codes_val = m2.group(1).strip()
            break
    if codes_val is None:
        return None

    h1 = _parse_kv_segments(h1_val)
    doc_id = h1.get("_first", "").strip()
    if not doc_id:
        return None
    codes = _parse_codes_line(codes_val)

    return {
        "doc_id": doc_id,
        "title": path.stem.replace("_", " "),
        "status": h1.get("status") or None,
        "lane": (h1.get("lane") or None),
        "huf_version": h1.get("huf") or None,
        "doc_version": h1.get("doc") or None,
        "responsible_operator": h1.get("ro") or None,
        "canonical_path": codes.get("canonical_path") or path.as_posix(),
        "codes": codes.get("codes", []),
        "artifacts": codes.get("artifacts", []),
        "evidence": codes.get("evidence") or None,
        "posture": codes.get("posture") or None,
        "weights": codes.get("weights") or None,
        "caps": codes.get("caps") or None,
        "source_file": path.as_posix(),
        "source_type": "text",
    }

def _scan_docx_file(path: Path) -> Optional[Dict[str, Any]]:
    if Document is None:
        return None
    try:
        d = Document(str(path))
        paras = [p.text.strip() for p in d.paragraphs[:40] if p.text and p.text.strip()]
    except Exception:
        return None
    line1 = None
    line2 = None
    for p in paras:
        if "HUF-DOC:" in p and not line1:
            line1 = p.split("HUF-DOC:", 1)[1].strip()
        if p.startswith("CODES:") and not line2:
            line2 = p.split("CODES:", 1)[1].strip()
        if line1 and line2:
            break
    if not line1 or not line2:
        return None

    h1 = _parse_kv_segments(line1)
    doc_id = h1.get("_first", "").strip()
    if not doc_id:
        return None
    codes = _parse_codes_line(line2)

    return {
        "doc_id": doc_id,
        "title": path.stem.replace("_", " "),
        "status": h1.get("status") or None,
        "lane": (h1.get("lane") or None),
        "huf_version": h1.get("huf") or None,
        "doc_version": h1.get("doc") or None,
        "responsible_operator": h1.get("ro") or None,
        "canonical_path": codes.get("canonical_path") or path.as_posix(),
        "codes": codes.get("codes", []),
        "artifacts": codes.get("artifacts", []),
        "evidence": codes.get("evidence") or None,
        "posture": codes.get("posture") or None,
        "weights": codes.get("weights") or None,
        "caps": codes.get("caps") or None,
        "source_file": path.as_posix(),
        "source_type": "docx",
    }

def _iter_files(root: Path) -> List[Path]:
    out: List[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        d = Path(dirpath)
        dirnames[:] = [n for n in dirnames if n not in SKIP_DIRS and not n.startswith(".")]
        for fn in filenames:
            p = d / fn
            ext = p.suffix.lower()
            if ext in TEXT_EXTS or ext in DOCX_EXTS:
                out.append(p)
    return out

def _backup(path: Path) -> Optional[Path]:
    if not path.exists():
        return None
    ts = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    b = path.with_suffix(path.suffix + f".bak_{ts}")
    b.write_bytes(path.read_bytes())
    return b

def _load_json(path: Path) -> Optional[Dict[str, Any]]:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None

def _build_manifest(entries: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_id: Dict[str, Dict[str, Any]] = {}
    collisions: Dict[str, List[str]] = {}
    for e in entries:
        doc_id = e["doc_id"]
        if doc_id not in by_id:
            by_id[doc_id] = e
            continue
        collisions.setdefault(doc_id, []).append(e.get("source_file", ""))
        cur = by_id[doc_id]
        if e.get("source_file") == e.get("canonical_path"):
            by_id[doc_id] = e
        elif cur.get("source_file") != cur.get("canonical_path") and e.get("source_type") == "text":
            by_id[doc_id] = e

    return {
        "version": "1.0",
        "generated": _dt.date.today().isoformat(),
        "documents": sorted(by_id.values(), key=lambda x: x["doc_id"]),
        "collisions": collisions,
    }

def _merge(old: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
    old_docs = {d["doc_id"]: d for d in old.get("documents", []) if "doc_id" in d}
    merged_docs = []
    for d in new.get("documents", []):
        doc_id = d["doc_id"]
        od = old_docs.get(doc_id, {})
        merged = dict(od)
        merged.update({k: v for k, v in d.items() if v is not None and v != []})
        merged_docs.append(merged)
    out = dict(new)
    out["documents"] = sorted(merged_docs, key=lambda x: x["doc_id"])
    return out

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="Repo root to scan")
    ap.add_argument("--manifest", default="notes/_org/doc_manifest.json", help="Manifest file to write")
    ap.add_argument("--print", action="store_true", help="Print manifest JSON")
    ap.add_argument("--write", action="store_true", help="Write manifest JSON (backs up existing)")
    ap.add_argument("--merge", action="store_true", help="Merge with existing manifest (preserve extra fields)")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    manifest_path = (root / args.manifest).resolve()

    entries: List[Dict[str, Any]] = []
    for p in _iter_files(root):
        ext = p.suffix.lower()
        e = _scan_text_file(p) if ext in TEXT_EXTS else _scan_docx_file(p)
        if e:
            if e.get("lane"):
                e["lane"] = str(e["lane"]).upper()
            entries.append(e)

    new_manifest = _build_manifest(entries)

    if args.merge:
        old = _load_json(manifest_path)
        if old:
            new_manifest = _merge(old, new_manifest)

    if args.print or not args.write:
        print(json.dumps(new_manifest, indent=2, ensure_ascii=False))

    if args.write:
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        _backup(manifest_path)
        manifest_path.write_text(json.dumps(new_manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
