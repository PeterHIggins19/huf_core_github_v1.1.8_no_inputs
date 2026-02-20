#!/usr/bin/env python3
"""Run Traffic Phase + Traffic Anomaly and print a long-tail comparison.

Designed to be script-first and Windows/Conda copy/paste friendly.

Usage (Windows PowerShell):
  .\.venv\Scripts\python scripts/run_long_tail_demo.py --status "Green Termination"

It will:
  1) run Traffic Phase -> out/traffic_phase_demo
  2) run Traffic Anomaly (exception-only) -> out/traffic_anomaly_demo
  3) print:
       - top regimes changed (top 10 by rho_global_post)
       - concentration metrics (items_to_cover_90pct)
       - discarded budget (if available)
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

# Local import (script is run from repo root)
from scripts.inspect_huf_artifacts import summarize, print_dashboard


def _find_huf_exe() -> List[str]:
    """Return argv prefix to run HUF.

    On Windows, prefer .venv\Scripts\huf.exe if this script is run via .venv\Scripts\python.
    On POSIX, prefer venv bin/huf.
    Fallback: python -m huf_core (if console script not found).
    """
    scripts_dir = Path(sys.executable).resolve().parent
    candidates = ["huf.exe", "huf", "huf.cmd", "huf-script.py"]
    for name in candidates:
        p = scripts_dir / name
        if p.exists():
            if p.suffix == ".py":
                return [sys.executable, str(p)]
            return [str(p)]
    # Fallback: try module execution
    return [sys.executable, "-m", "huf_core"]


def _run(cmd: List[str]) -> None:
    print(f"[run] {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def _csv_exists(path: Path) -> bool:
    return path.exists() and path.is_file()


def _compare_top_regimes(a: List[Tuple[str, float]], b: List[Tuple[str, float]]) -> Tuple[List[str], List[str], List[str]]:
    a_ids = [x[0] for x in a]
    b_ids = [x[0] for x in b]
    entered = [rid for rid in b_ids if rid not in a_ids]
    exited = [rid for rid in a_ids if rid not in b_ids]
    stayed = [rid for rid in b_ids if rid in a_ids]
    return entered, exited, stayed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--status", default="Green Termination", help="Traffic status for anomaly run.")
    ap.add_argument("--phase-csv", default="cases/traffic_phase/inputs/toronto_traffic_signals_phase_status.csv")
    ap.add_argument("--anomaly-csv", default="cases/traffic_anomaly/inputs/toronto_traffic_signals_phase_status.csv")
    ap.add_argument("--out-phase", default="out/traffic_phase_demo")
    ap.add_argument("--out-anomaly", default="out/traffic_anomaly_demo")
    ap.add_argument("--top", type=int, default=10, help="Top regimes to compare.")
    args = ap.parse_args()

    phase_csv = Path(args.phase_csv)
    anomaly_csv = Path(args.anomaly_csv)

    if not _csv_exists(phase_csv) or not _csv_exists(anomaly_csv):
        print("[error] Toronto CSV inputs not found.")
        print("Expected at least one of:")
        print(f"  - {phase_csv}")
        print(f"  - {anomaly_csv}")
        print()
        print("Fetch them with:")
        print(r"  .\.venv\Scripts\python scripts/fetch_data.py --toronto --yes")
        return 2

    out_phase = Path(args.out_phase)
    out_anom = Path(args.out_anomaly)
    out_phase.mkdir(parents=True, exist_ok=True)
    out_anom.mkdir(parents=True, exist_ok=True)

    huf = _find_huf_exe()

    # 1) Baseline
    _run(huf + ["traffic", "--csv", str(phase_csv), "--out", str(out_phase)])

    # 2) Exception-only
    _run(huf + ["traffic-anomaly", "--csv", str(anomaly_csv), "--out", str(out_anom), "--status", args.status])

    # 3) Summaries
    s_base = summarize(out_phase, top_regimes=args.top)
    s_anom = summarize(out_anom, top_regimes=args.top)

    print()
    print("=== BASELINE: Traffic Phase ===")
    print_dashboard(s_base)

    print()
    print("=== EXCEPTION: Traffic Anomaly ===")
    print_dashboard(s_anom)

    # 4) Comparison headline
    base_top = s_base.get("top_regimes", [])
    anom_top = s_anom.get("top_regimes", [])
    entered, exited, stayed = _compare_top_regimes(base_top, anom_top)

    base_items90 = s_base.get("items_to_cover_90pct", None)
    anom_items90 = s_anom.get("items_to_cover_90pct", None)

    print()
    print("=== LONG-TAIL HEADLINE ===")
    print(f"Top-{args.top} regimes changed: entered={len(entered)} exited={len(exited)} stayed={len(stayed)}")
    if entered:
        print("  Entered (exception-only top list): " + ", ".join(entered[:10]))
    if exited:
        print("  Exited (baseline-only top list): " + ", ".join(exited[:10]))

    if base_items90 is not None and anom_items90 is not None:
        if anom_items90 < base_items90:
            print(f"Concentration increased: items_to_cover_90pct {base_items90} -> {anom_items90}")
        elif anom_items90 > base_items90:
            print(f"Concentration decreased: items_to_cover_90pct {base_items90} -> {anom_items90}")
        else:
            print(f"Concentration unchanged: items_to_cover_90pct {base_items90} -> {anom_items90}")
    else:
        print("Concentration: (could not compute items_to_cover_90pct for one or both runs)")

    print()
    print("Next: open the CSVs in Excel, or run the inspector on any folder:")
    print(r"  .\.venv\Scripts\python scripts/inspect_huf_artifacts.py --out out/traffic_anomaly_demo")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
