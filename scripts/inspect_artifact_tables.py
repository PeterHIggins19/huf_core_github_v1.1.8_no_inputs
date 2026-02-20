"""scripts/inspect_artifact_tables.py

Windows-safe console preview for common HUF artifacts (no pandas required).

Usage:
  .\.venv\Scripts\python scripts/inspect_artifact_tables.py --out out/planck70 --top 10
  .\.venv\Scripts\python scripts/inspect_artifact_tables.py --out out/vector_db_demo --top 10

What it prints:
- Top regimes by rho_global_post (artifact_1_coherence_map.csv)
- Top retained items (artifact_2_active_set.csv)
- Discarded budget (artifact_4_error_budget.json), if present
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any, Dict, List, Optional


def _read_csv(path: Path) -> List[Dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def _to_float(x: Any, default: float = 0.0) -> float:
    try:
        if x is None:
            return default
        s = str(x).strip()
        if not s:
            return default
        return float(s)
    except Exception:
        return default


def _col(rows: List[Dict[str, Any]], name: str) -> bool:
    return bool(rows) and (name in rows[0])


def _pick_first(rows: List[Dict[str, Any]], names: List[str]) -> Optional[str]:
    for n in names:
        if _col(rows, n):
            return n
    return None


def print_top_regimes(coh_path: Path, top: int) -> None:
    rows = _read_csv(coh_path)
    rho_col = _pick_first(rows, ["rho_global_post", "rho_post", "rho"])
    rid_col = _pick_first(rows, ["regime_id", "regime", "namespace", "collection", "source", "tenant"])
    if not rho_col or not rid_col:
        print(f"[warn] {coh_path.name}: missing expected columns (need regime_id + rho_global_post)")
        return

    rows.sort(key=lambda r: _to_float(r.get(rho_col)), reverse=True)
    print("\nTop regimes by rho_global_post:")
    for i, r in enumerate(rows[:top], start=1):
        rid = r.get(rid_col, "")
        rho = _to_float(r.get(rho_col))
        print(f"  {i:2d}. {rid}  rho_post={rho:.6f}")


def print_top_items(active_path: Path, top: int) -> None:
    rows = _read_csv(active_path)
    rho_g = _pick_first(rows, ["rho_global_post", "rho_post", "rho"])
    rho_l = _pick_first(rows, ["rho_local_post", "rho_local"])
    rank = _pick_first(rows, ["rank", "global_rank", "rnk"])
    rid  = _pick_first(rows, ["regime_id", "regime", "namespace", "collection", "source", "tenant"])
    iid  = _pick_first(rows, ["item_id", "id", "doc_id", "chunk_id"])
    val  = _pick_first(rows, ["value", "score", "mass", "w"])

    if not rho_g:
        print(f"[warn] {active_path.name}: missing rho_global_post column")
        return

    # Prefer explicit rank if present; else sort by rho_global_post desc
    if rank:
        rows.sort(key=lambda r: int(float(r.get(rank, 1e9) or 1e9)))
    else:
        rows.sort(key=lambda r: _to_float(r.get(rho_g)), reverse=True)

    print("\nTop retained items:")
    headers = ["rank", "regime_id", "item_id", "value", "rho_global_post", "rho_local_post"]
    print("  " + " | ".join(headers))
    print("  " + "-|-".join(["-" * len(h) for h in headers]))

    for r in rows[:top]:
        def g(c: Optional[str]) -> str:
            return str(r.get(c, "")) if c else ""
        rg = _to_float(r.get(rho_g))
        rl = _to_float(r.get(rho_l)) if rho_l else 0.0
        line = [
            g(rank),
            g(rid),
            g(iid),
            g(val),
            f"{rg:.6f}" if rho_g else "",
            f"{rl:.6f}" if rho_l else "",
        ]
        print("  " + " | ".join(line))


def print_discarded_budget(err_path: Path) -> None:
    try:
        data = json.loads(err_path.read_text(encoding="utf-8"))
    except Exception:
        print(f"[warn] could not read {err_path.name}")
        return

    keys = [
        "discarded_budget_global",
        "discarded_global",
        "discarded_budget",
        "discarded_mass",
        "discarded",
    ]
    for k in keys:
        if k in data:
            try:
                v = float(data[k])
                print(f"\nDiscarded budget: {v:.6f}  ({k})")
                return
            except Exception:
                print(f"\nDiscarded budget: {data[k]}  ({k})")
                return
    print("\nDiscarded budget: (key not found — open artifact_4_error_budget.json to inspect)")


def main() -> int:
    ap = argparse.ArgumentParser(description="Print a quick console preview of HUF artifacts (no pandas).")
    ap.add_argument("--out", required=True, type=Path, help="Run output folder containing artifact_*.{csv,json}")
    ap.add_argument("--top", type=int, default=10, help="How many rows to print for regimes/items")
    args = ap.parse_args()

    out_dir = args.out
    print(f"[out] {out_dir.resolve()}")

    coh = out_dir / "artifact_1_coherence_map.csv"
    act = out_dir / "artifact_2_active_set.csv"
    err = out_dir / "artifact_4_error_budget.json"

    if coh.exists():
        print_top_regimes(coh, top=args.top)
    else:
        print(f"[miss] {coh.name}")

    if act.exists():
        print_top_items(act, top=args.top)
    else:
        print(f"[miss] {act.name}")

    if err.exists():
        print_discarded_budget(err)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
