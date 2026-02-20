#!/usr/bin/env python3
"""Inspect HUF artifacts for a quick, copy/paste-friendly console summary.

Usage (Windows PowerShell):
  .\.venv\Scripts\python scripts\inspect_huf_artifacts.py --out out\traffic_phase

Recommended on Windows: use forward slashes in paths:
  .\.venv\Scripts\python scripts/inspect_huf_artifacts.py --out out/traffic_phase

What it prints (minimum dashboard):
  - top 10 regimes by rho_global_post
  - items_to_cover_90pct (from active set)
  - discarded budget (from artifact_4_error_budget.json, if present)

It also tolerates UTF-8 BOM in CSV/JSON (common on Windows).
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple


COH = "artifact_1_coherence_map.csv"
ACTIVE = "artifact_2_active_set.csv"
ERR = "artifact_4_error_budget.json"
STAMP = "run_stamp.json"


def _find(base: Path, name: str) -> Optional[Path]:
    p = base / name
    if p.exists():
        return p
    p2 = base / "artifacts" / name
    if p2.exists():
        return p2
    return None


def _read_csv(path: Path) -> List[Dict[str, str]]:
    # utf-8-sig tolerates BOM
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def _f(row: Dict[str, str], key: str, default: float = 0.0) -> float:
    try:
        return float(row.get(key, "") or default)
    except Exception:
        return default


def summarize(out_dir: Path, top_regimes: int = 10) -> Dict[str, object]:
    out_dir = out_dir.expanduser().resolve()
    res: Dict[str, object] = {"out_dir": str(out_dir)}

    coh_path = _find(out_dir, COH)
    act_path = _find(out_dir, ACTIVE)
    err_path = _find(out_dir, ERR)
    stamp_path = _find(out_dir, STAMP)

    if stamp_path:
        try:
            stamp = json.loads(stamp_path.read_text(encoding="utf-8-sig"))
            res["run_id"] = stamp.get("run_id")
            res["dataset_id"] = stamp.get("dataset_id")
        except Exception:
            pass

    discarded = None
    if err_path:
        try:
            eb = json.loads(err_path.read_text(encoding="utf-8-sig"))
            discarded = (
                eb.get("discarded_budget_global")
                or eb.get("discarded_global")
                or eb.get("discarded_frac")
            )
        except Exception:
            discarded = None
    res["discarded_budget_global"] = discarded

    top_regime_rows: List[Tuple[str, float]] = []
    if coh_path:
        coh = _read_csv(coh_path)
        coh_sorted = sorted(coh, key=lambda r: _f(r, "rho_global_post"), reverse=True)
        for r in coh_sorted[:top_regimes]:
            rid = r.get("regime_id") or r.get("regime") or ""
            top_regime_rows.append((rid, _f(r, "rho_global_post")))
        res["top_regimes"] = top_regime_rows
    else:
        res["top_regimes"] = []

    items_to_cover_90 = None
    if act_path:
        act = _read_csv(act_path)
        act_sorted = sorted(act, key=lambda r: _f(r, "rho_global_post"), reverse=True)
        cum = 0.0
        for i, r in enumerate(act_sorted, start=1):
            cum += _f(r, "rho_global_post")
            if cum >= 0.90:
                items_to_cover_90 = i
                break
    res["items_to_cover_90pct"] = items_to_cover_90

    return res


def print_dashboard(summary: Dict[str, object], title: str = "") -> None:
    if title:
        print(title)
    out_dir = summary.get("out_dir", "")
    run_id = summary.get("run_id", "")
    dataset_id = summary.get("dataset_id", "")
    discarded = summary.get("discarded_budget_global", None)
    items90 = summary.get("items_to_cover_90pct", None)
    top_regimes = summary.get("top_regimes", [])

    print(f"[out] {out_dir}")
    if run_id or dataset_id:
        print(f"[run_stamp] run_id={run_id} dataset_id={dataset_id}")

    if discarded is not None:
        try:
            print(f"[error_budget] discarded_budget_global={float(discarded):.6f}")
        except Exception:
            print(f"[error_budget] discarded_budget_global={discarded}")

    if items90 is not None:
        print(f"[tail] items_to_cover_90pct={items90}")

    print()
    print("Top regimes by rho_global_post:")
    if not top_regimes:
        print("  (missing artifact_1_coherence_map.csv)")
    else:
        for i, (rid, rho) in enumerate(top_regimes, start=1):
            print(f" {i:>2}. {rid}  rho_post={rho:.6f}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, type=Path, help="Output folder containing HUF artifacts.")
    ap.add_argument("--top-regimes", type=int, default=10)
    args = ap.parse_args()

    out_dir = args.out
    if not out_dir.exists():
        print(f"[error] output folder not found: {out_dir}")
        return 2

    s = summarize(out_dir, top_regimes=args.top_regimes)
    print_dashboard(s)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
