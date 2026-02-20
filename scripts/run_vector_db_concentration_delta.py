#!/usr/bin/env python
r"""
run_vector_db_concentration_delta.py

Run the vector-db demo twice (tau A vs tau B), then print a single-line
concentration delta based on the active set.

Definition:
  items_to_cover_90pct = the smallest k such that the top-k items by rho_global_post
  account for >= 90% of total retained mass (sum of rho_global_post).

Usage (PowerShell):
  .\.venv\Scripts\python scripts\run_vector_db_concentration_delta.py `
    --in cases/vector_db/inputs/retrieval.jsonl `
    --out out/vector_db_delta `
    --tau-a 0.02 `
    --tau-b 0.08 `
    --regime-field namespace

If you already ran the demo and just want to compare two output folders:
  .\.venv\Scripts\python scripts\run_vector_db_concentration_delta.py `
    --out-a out/vector_db_demo_tauA `
    --out-b out/vector_db_demo_tauB
"""
from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

def read_csv(path: Path) -> List[Dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def fnum(x: Any, default: float = 0.0) -> float:
    try:
        return float(str(x).strip())
    except Exception:
        return default

def safe_tag(x: str) -> str:
    # make a folder-friendly tag from a float like 0.02 -> 0p02
    x = str(x).strip()
    x = x.replace(".", "p")
    x = re.sub(r"[^0-9A-Za-z_\-p]+", "_", x)
    return x

def items_to_cover_90pct(out_dir: Path) -> int:
    act_p = out_dir / "artifact_2_active_set.csv"
    if not act_p.exists():
        raise SystemExit(f"[err] Missing: {act_p}")

    rows = read_csv(act_p)
    if not rows:
        return 0

    rho_col = "rho_global_post" if "rho_global_post" in rows[0] else ("rho_post" if "rho_post" in rows[0] else None)
    if not rho_col:
        raise SystemExit(f"[err] Could not find rho column in {act_p.name}")

    rhos = [fnum(r.get(rho_col)) for r in rows]
    total = sum(rhos)
    if total <= 0:
        return 0

    # sort descending
    rhos.sort(reverse=True)
    target = 0.9 * total
    cum = 0.0
    k = 0
    for v in rhos:
        cum += v
        k += 1
        if cum >= target:
            return k
    return k

def run_demo(py: str, in_path: Path, out_dir: Path, tau: float, regime_field: str) -> None:
    demo = Path("examples") / "run_vector_db_demo.py"
    if not demo.exists():
        raise SystemExit(f"[err] Cannot find {demo}. Run this from repo root.")
    out_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        py, str(demo),
        "--in", str(in_path),
        "--out", str(out_dir),
        "--tau-global", str(tau),
        "--regime-field", regime_field,
    ]
    print("[run] " + " ".join(cmd))
    subprocess.check_call(cmd)

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="in_path", default=None, help="JSONL retrieval export input")
    ap.add_argument("--out", dest="out_base", default=None, help="Base output folder (will create subfolders for tau A/B)")
    ap.add_argument("--tau-a", type=float, default=None)
    ap.add_argument("--tau-b", type=float, default=None)
    ap.add_argument("--regime-field", default="namespace")

    ap.add_argument("--out-a", default=None, help="Already-produced output folder A")
    ap.add_argument("--out-b", default=None, help="Already-produced output folder B")
    args = ap.parse_args()

    # Compare existing folders mode
    if args.out_a and args.out_b:
        out_a = Path(args.out_a)
        out_b = Path(args.out_b)
    else:
        # Run demo twice mode
        if args.in_path is None or args.out_base is None or args.tau_a is None or args.tau_b is None:
            ap.error("Either provide --out-a/--out-b, OR provide --in, --out, --tau-a, --tau-b")

        in_path = Path(args.in_path)
        if not in_path.exists():
            raise SystemExit(f"[err] Missing input: {in_path}")

        out_base = Path(args.out_base)
        out_a = out_base / f"tau_{safe_tag(args.tau_a)}"
        out_b = out_base / f"tau_{safe_tag(args.tau_b)}"

        py = sys.executable
        run_demo(py, in_path, out_a, args.tau_a, args.regime_field)
        run_demo(py, in_path, out_b, args.tau_b, args.regime_field)

    x = items_to_cover_90pct(out_a)
    y = items_to_cover_90pct(out_b)

    if y < x:
        print(f"Concentration increased: items_to_cover_90pct {x} -> {y}")
    elif y > x:
        print(f"Concentration decreased: items_to_cover_90pct {x} -> {y}")
    else:
        print(f"Concentration unchanged: items_to_cover_90pct {x} -> {y}")

    print(f"[details] A={out_a}")
    print(f"[details] B={out_b}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
