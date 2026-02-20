"""Plot HUF artifact CSVs (coherence + concentration).

This script is intentionally lightweight and cross-platform.

Inputs (under --out):
  - artifact_1_coherence_map.csv
  - artifact_2_active_set.csv

Outputs (under <out>/plots by default):
  - coherence_by_regime.png
  - concentration_curve.png

Usage examples:

  # Windows PowerShell
  #   & .\.venv\Scripts\python.exe scripts/plot_huf_artifacts.py --out out\vector_db_demo

  # macOS/Linux
  #   ./.venv/bin/python scripts/plot_huf_artifacts.py --out out/vector_db_demo

If matplotlib isn't installed:
  python -m pip install matplotlib
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def _f(x) -> float:
    try:
        return float(str(x).strip())
    except Exception:
        return 0.0


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def _pick_first(keys: list[str], row0: dict[str, str]) -> str | None:
    for k in keys:
        if k in row0:
            return k
    return None


def plot(out_dir: Path, save_dir: Path, top_k: int = 20) -> None:
    import matplotlib

    # Use a non-interactive backend by default so this works on headless CI.
    matplotlib.use("Agg", force=True)
    import matplotlib.pyplot as plt

    coh_p = out_dir / "artifact_1_coherence_map.csv"
    act_p = out_dir / "artifact_2_active_set.csv"

    if not coh_p.exists():
        raise FileNotFoundError(f"Missing: {coh_p}")
    if not act_p.exists():
        raise FileNotFoundError(f"Missing: {act_p}")

    coh = _read_csv(coh_p)
    act = _read_csv(act_p)

    if not coh:
        raise RuntimeError(f"Empty file: {coh_p}")

    rho_col = _pick_first(["rho_global_post", "rho_post"], coh[0])
    reg_col = _pick_first(["regime_id", "namespace", "regime"], coh[0])

    if not rho_col or not reg_col:
        raise RuntimeError(
            "Could not find expected columns in coherence map. "
            f"Saw columns: {list(coh[0].keys())}"
        )

    # ---- coherence bar (top-K) ----
    coh_sorted = sorted(coh, key=lambda r: _f(r.get(rho_col)), reverse=True)
    coh_top = coh_sorted[:top_k]
    labels = [r.get(reg_col, "") for r in coh_top]
    values = [_f(r.get(rho_col)) for r in coh_top]

    plt.figure(figsize=(10, 5))
    plt.bar(range(len(values)), values)
    plt.xticks(range(len(values)), labels, rotation=45, ha="right")
    plt.ylabel(rho_col)
    plt.title(f"Coherence by regime (top {min(top_k, len(values))})")
    plt.tight_layout()
    (save_dir / "coherence_by_regime.png").parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_dir / "coherence_by_regime.png", dpi=160)
    plt.close()

    # ---- concentration curve (active set) ----
    if not act:
        raise RuntimeError(f"Empty file: {act_p}")

    # Prefer rho columns if present; otherwise fall back to 'value'
    w_col = _pick_first(["rho_global_post", "rho_post", "value"], act[0])
    if not w_col:
        raise RuntimeError(
            "Could not find a weight column in active set. "
            f"Saw columns: {list(act[0].keys())}"
        )

    weights = sorted((_f(r.get(w_col)) for r in act), reverse=True)
    total = sum(weights) or 1.0
    cum = []
    s = 0.0
    for w in weights:
        s += w / total
        cum.append(s)

    xs = list(range(1, len(cum) + 1))

    # items to cover 90%
    k90 = next((i for i, v in enumerate(cum, start=1) if v >= 0.9), len(cum))

    plt.figure(figsize=(10, 5))
    plt.plot(xs, cum, marker="o", linewidth=1.5)
    plt.axhline(0.9, linestyle="--")
    plt.axvline(k90, linestyle="--")
    plt.xlabel("Top-N items (sorted)")
    plt.ylabel("Cumulative mass")
    plt.ylim(0, 1.02)
    plt.title(f"Concentration curve (90% at {k90} items)")
    plt.tight_layout()
    plt.savefig(save_dir / "concentration_curve.png", dpi=160)
    plt.close()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, help="Output folder containing artifact_*.csv")
    ap.add_argument(
        "--save-dir",
        default=None,
        help="Where to write plots (default: <out>/plots)",
    )
    ap.add_argument("--top-k", type=int, default=20, help="Top-K regimes to plot")
    args = ap.parse_args()

    out_dir = Path(args.out)
    save_dir = Path(args.save_dir) if args.save_dir else (out_dir / "plots")

    plot(out_dir=out_dir, save_dir=save_dir, top_k=args.top_k)

    print(f"[OK] Wrote plots to: {save_dir}")
    print(f"      - {save_dir / 'coherence_by_regime.png'}")
    print(f"      - {save_dir / 'concentration_curve.png'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
