#!/usr/bin/env python3
"""Inspect HUF artifacts for a quick, copy/paste-friendly console summary.

Designed for the Vector DB demo, but it also works with other HUF outputs.

Usage (Windows PowerShell):
  .\.venv\Scripts\python scripts/inspect_vector_db_artifacts.py --out out/vector_db_demo

It looks for these files in the output folder (or in out/artifacts/ if present):
  - artifact_1_coherence_map.csv
  - artifact_2_active_set.csv
  - artifact_4_error_budget.json
  - run_stamp.json (optional)
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Dict, List, Tuple


COH = "artifact_1_coherence_map.csv"
ACTIVE = "artifact_2_active_set.csv"
ERR = "artifact_4_error_budget.json"
STAMP = "run_stamp.json"


def _find(base: Path, name: str) -> Path | None:
    p = base / name
    if p.exists():
        return p
    p2 = base / "artifacts" / name
    if p2.exists():
        return p2
    return None


def _read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def _f(row: Dict[str, str], key: str, default: float = 0.0) -> float:
    try:
        return float(row.get(key, "") or default)
    except Exception:
        return default


def _summarize(out_dir: Path, top_regimes: int, top_items: int) -> int:
    coh_path = _find(out_dir, COH)
    act_path = _find(out_dir, ACTIVE)
    err_path = _find(out_dir, ERR)
    stamp_path = _find(out_dir, STAMP)

    print(f"[out] {out_dir}")

    if stamp_path:
        try:
            stamp = json.loads(stamp_path.read_text(encoding="utf-8"))
            rid = stamp.get("run_id") or ""
            ds = stamp.get("dataset_id") or ""
            print(f"[run_stamp] run_id={rid} dataset_id={ds}")
        except Exception:
            pass

    discarded = None
    if err_path:
        try:
            eb = json.loads(err_path.read_text(encoding="utf-8"))
            discarded = (
                eb.get("discarded_budget_global")
                or eb.get("discarded_global")
                or eb.get("discarded_frac")
            )
        except Exception:
            discarded = None

    if coh_path:
        coh = _read_csv(coh_path)
        # Common columns across cases:
        #   regime_id, rho_global_post, rho_discarded_pre
        coh_sorted = sorted(coh, key=lambda r: _f(r, "rho_global_post"), reverse=True)
        total_post = sum(_f(r, "rho_global_post") for r in coh_sorted)
        total_discard_pre = sum(_f(r, "rho_discarded_pre") for r in coh_sorted)
        print()
        print(f"[coherence] rows={len(coh)}  sum(rho_global_post)={total_post:.6f}")
        if discarded is not None:
            try:
                print(f"[error_budget] discarded_budget_global={float(discarded):.6f}")
            except Exception:
                pass
        elif total_discard_pre > 0:
            print(f"[discard] sum(rho_discarded_pre)={total_discard_pre:.6f}")

        print()
        print(f"Top regimes by rho_global_post (n={min(top_regimes, len(coh_sorted))}):")
        for i, r in enumerate(coh_sorted[:top_regimes], start=1):
            rid = r.get("regime_id") or r.get("regime") or ""
            rg = _f(r, "rho_global_post")
            rd = _f(r, "rho_discarded_pre")
            if rd > 0:
                print(f" {i:>2}. {rid}  rho_post={rg:.6f}  discarded_pre={rd:.6f}")
            else:
                print(f" {i:>2}. {rid}  rho_post={rg:.6f}")
    else:
        print(f"[warn] missing {COH}")

    if act_path:
        act = _read_csv(act_path)
        # Common columns: rank, regime_id, item_id, rho_global_post, rho_local_post
        # Some cases use 'element_id' instead of item_id.
        def item_key(r: Dict[str, str]) -> Tuple[float, float]:
            return (_f(r, "rho_global_post"), _f(r, "rho_local_post"))

        act_sorted = sorted(act, key=item_key, reverse=True)
        print()
        print(f"[active_set] rows={len(act)}")

        # “How many items cover 90% of the retained budget?”
        cum = 0.0
        k90 = None
        for i, r in enumerate(act_sorted, start=1):
            cum += _f(r, "rho_global_post")
            if k90 is None and cum >= 0.90:
                k90 = i
                break
        if k90 is not None:
            print(f"[tail] items_to_cover_90pct={k90}")

        print()
        print(f"Top items (n={min(top_items, len(act_sorted))}):")
        for i, r in enumerate(act_sorted[:top_items], start=1):
            rid = r.get("regime_id") or r.get("regime") or ""
            iid = r.get("item_id") or r.get("element_id") or r.get("item") or ""
            rg = _f(r, "rho_global_post")
            rl = _f(r, "rho_local_post")
            if rl > 0:
                print(f" {i:>2}. {rid} :: {iid}  rho_global={rg:.6f}  rho_local={rl:.6f}")
            else:
                print(f" {i:>2}. {rid} :: {iid}  rho_global={rg:.6f}")
    else:
        print(f"[warn] missing {ACTIVE}")

    print()
    print("Tip: open the CSVs in Excel, or load them in a notebook for deeper slicing.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, type=Path, help="Output folder containing HUF artifacts.")
    ap.add_argument("--top-regimes", type=int, default=10)
    ap.add_argument("--top-items", type=int, default=20)
    args = ap.parse_args()

    out_dir = args.out.expanduser().resolve()
    if not out_dir.exists():
        print(f"[error] output folder not found: {out_dir}")
        return 2
    return _summarize(out_dir, args.top_regimes, args.top_items)


if __name__ == "__main__":
    raise SystemExit(main())
