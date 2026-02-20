#!/usr/bin/env python
"""
print_huf_summary.py

Paste-safe way to inspect HUF outputs on Windows.
Reads:
  artifact_1_coherence_map.csv
  artifact_2_active_set.csv

Usage (PowerShell):
  .\.venv\Scripts\python scripts\print_huf_summary.py --out out\planck70
  .\.venv\Scripts\python scripts\print_huf_summary.py --out out\vector_db_demo

Optional:
  --top-regimes 10
  --top-items 10
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List, Any

def read_csv(path: Path) -> List[Dict[str, Any]]:
    # utf-8-sig handles BOM if present
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def fnum(x: Any, default: float = 0.0) -> float:
    try:
        return float(str(x).strip())
    except Exception:
        return default

def find_first(cols: List[str], row: Dict[str, Any]) -> str | None:
    for c in cols:
        if c in row:
            return c
    return None

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, help="Output directory containing artifact_*.csv")
    ap.add_argument("--top-regimes", type=int, default=10)
    ap.add_argument("--top-items", type=int, default=10)
    args = ap.parse_args()

    out = Path(args.out)
    coh_p = out / "artifact_1_coherence_map.csv"
    act_p = out / "artifact_2_active_set.csv"

    if not coh_p.exists():
        raise SystemExit(f"[err] Missing: {coh_p}")
    if not act_p.exists():
        raise SystemExit(f"[err] Missing: {act_p}")

    coh = read_csv(coh_p)
    act = read_csv(act_p)

    if not coh:
        print("[warn] coherence_map is empty")
    else:
        rho_col = find_first(["rho_global_post", "rho_post", "rho_global"], coh[0])
        reg_col = find_first(["regime_id", "namespace", "collection", "source", "tenant"], coh[0])
        disc_col = find_first(["discarded_mass", "discarded_global", "rho_discarded"], coh[0])

        if rho_col and reg_col:
            coh.sort(key=lambda r: fnum(r.get(rho_col)), reverse=True)
            print("\nTop regimes by rho_global_post:")
            for i, r in enumerate(coh[: args.top_regimes], 1):
                if disc_col:
                    disc = fnum(r.get(disc_col))
                    print(f"  {i:2d}. {r.get(reg_col,'')}  rho_post={fnum(r.get(rho_col)):.6f}  discarded={disc:.6g}")
                else:
                    print(f"  {i:2d}. {r.get(reg_col,'')}  rho_post={fnum(r.get(rho_col)):.6f}")
        else:
            print("\n[warn] Could not locate regime/rho columns in artifact_1_coherence_map.csv")

    # Active set
    if not act:
        print("\n[warn] active_set is empty")
        return 0

    rank_col = find_first(["rank", "global_rank"], act[0])
    if rank_col:
        def rank_key(r):
            try:
                return int(float(r.get(rank_col) or 10**18))
            except Exception:
                return 10**18
        act.sort(key=rank_key)

    cols = ["rank","regime_id","item_id","value","rho_global_post","rho_local_post"]
    existing = [c for c in cols if c in act[0]]
    if not existing:
        existing = list(act[0].keys())[:8]

    print(f"\nTop {min(args.top_items, len(act))} retained items:")
    print("  " + " | ".join(existing))
    print("  " + "-+-".join("-"*len(c) for c in existing))
    for r in act[: args.top_items]:
        print("  " + " | ".join(str(r.get(c,"")) for c in existing))

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
