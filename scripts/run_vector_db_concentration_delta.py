\
r"""scripts/run_vector_db_concentration_delta.py

Run the Vector DB coherence demo twice (tau A vs tau B) and print a one-line
delta:

  Concentration increased: items_to_cover_90pct X -> Y

Why this exists:
- Gives you a “proof line” that’s repeatable in an email / issue / PR comment.
- Lets you sanity-check whether tightening tau concentrates the kept set.

Windows / PowerShell (repo venv):

  .\.venv\Scripts\python scripts/run_vector_db_concentration_delta.py `
    --in cases/vector_db/inputs/retrieval.jsonl `
    --out out/vector_db_delta `
    --tau-a 0.005 `
    --tau-b 0.02 `
    --regime-field namespace
"""

from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List


def _read_csv(path: Path) -> List[Dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def _to_float(x: Any, default: float = 0.0) -> float:
    try:
        return float(str(x).strip())
    except Exception:
        return default


def _safe_tag(x: float) -> str:
    # folder-friendly tag: 0.02 -> 0p02
    s = f"{x:.6g}".replace(".", "p")
    s = re.sub(r"[^0-9A-Za-z_\-p]+", "_", s)
    return s


def _items_to_cover_90pct(out_dir: Path) -> int:
    act_p = out_dir / "artifact_2_active_set.csv"
    rows = _read_csv(act_p)
    if not rows:
        return 0

    rho_col = "rho_global_post" if "rho_global_post" in rows[0] else ("rho_post" if "rho_post" in rows[0] else None)
    if not rho_col:
        raise SystemExit(f"[err] Could not find rho column in {act_p}")

    rhos = sorted((_to_float(r.get(rho_col)) for r in rows), reverse=True)
    total = sum(rhos)
    if total <= 0:
        return 0

    target = 0.90 * total
    cum = 0.0
    for i, v in enumerate(rhos, start=1):
        cum += v
        if cum >= target:
            return i
    return len(rhos)


def _run_demo(py: str, in_path: Path, out_dir: Path, tau: float, regime_field: str) -> None:
    demo = Path("examples") / "run_vector_db_demo.py"
    if not demo.exists():
        raise SystemExit(f"[err] Cannot find {demo}. Run from repo root.")

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
    ap = argparse.ArgumentParser(description="Run vector-db demo twice and print concentration delta.")
    ap.add_argument("--in", dest="in_path", required=True, type=Path, help="JSONL retrieval export (id+score).")
    ap.add_argument("--out", required=True, type=Path, help="Output root (creates tau subfolders).")
    ap.add_argument("--tau-a", required=True, type=float, help="Baseline tau A.")
    ap.add_argument("--tau-b", required=True, type=float, help="Comparison tau B.")
    ap.add_argument("--regime-field", default="namespace", help="Grouping field (namespace/collection/source/tenant).")
    args = ap.parse_args()

    out_a = args.out / f"tau_{_safe_tag(args.tau_a)}"
    out_b = args.out / f"tau_{_safe_tag(args.tau_b)}"

    py = sys.executable
    _run_demo(py, args.in_path, out_a, args.tau_a, args.regime_field)
    _run_demo(py, args.in_path, out_b, args.tau_b, args.regime_field)

    x = _items_to_cover_90pct(out_a)
    y = _items_to_cover_90pct(out_b)

    if y < x:
        msg = "Concentration increased"
    elif y > x:
        msg = "Concentration decreased"
    else:
        msg = "Concentration unchanged"

    print(f"{msg}: items_to_cover_90pct {x} -> {y}")
    print(f"[details] A={out_a}")
    print(f"[details] B={out_b}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
