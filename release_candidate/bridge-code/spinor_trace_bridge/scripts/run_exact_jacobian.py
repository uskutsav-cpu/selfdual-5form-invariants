"""Exact modular Jacobian rank of the spinor invariants, at several points and primes.

This is the replacement for the archive's single float64 finite-difference
sample.  It has no step size and no rank tolerance.

Usage:
    python spinor_trace_bridge/scripts/run_exact_jacobian.py
        [--primes 32749,32719] [--seeds 11,22,33,44,55] [--degrees 4,6,8,10,12]
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "spinor_trace_bridge" / "src"))

from sdbridge.jacobian import accumulate_jacobian_rank   # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--primes", default="32749,32719")
    ap.add_argument("--seeds", default="11,22,33,44,55")
    ap.add_argument("--degrees", default="4,6,8,10,12")
    ap.add_argument("--patience", type=int, default=35)
    ap.add_argument("--max-graphs", type=int, default=200)
    ap.add_argument("--out", default=str(ROOT / "verification" / "spinor_exact_jacobian.json"))
    args = ap.parse_args()

    primes = [int(x) for x in args.primes.split(",")]
    seeds = [int(x) for x in args.seeds.split(",")]
    degrees = [int(x) for x in args.degrees.split(",")]
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    report = {"schema": 1,
              "method": "analytic derivative by amputation, exact over F_p",
              "validated_by": "Euler identity sum_r c_r dI/dc_r = deg * I, exact",
              "runs": []}
    if out.exists():
        try:
            report = json.loads(out.read_text())
        except json.JSONDecodeError:
            pass
    done = {(r["prime"], r["point_seed"]) for r in report["runs"]}

    for p in primes:
        for s in seeds:
            if (p, s) in done:
                print(f"[p={p} seed={s}] already done", flush=True)
                continue
            t0 = time.time()

            def progress(row, _p=p, _s=s):
                print(f"  [p={_p} seed={_s}] degree {row['degree']}: "
                      f"rank {row['rank_before']} -> {row['rank_after']} "
                      f"({row['rows_kept']} kept of {row['graphs_drawn']} drawn, "
                      f"{row['stopped_on']})", flush=True)

            res = accumulate_jacobian_rank(
                degrees, p, seed=s, patience=args.patience,
                max_graphs_per_degree=args.max_graphs, progress=progress)
            res["wall_seconds"] = round(time.time() - t0, 1)
            report["runs"].append(res)
            print(f"[p={p} seed={s}] EXACT MODULAR RANK = {res['exact_modular_rank']} "
                  f"({res['wall_seconds']}s, {res['stopping_reason']})", flush=True)
            out.write_text(json.dumps(report, indent=1, sort_keys=True))

    ranks = sorted({r["exact_modular_rank"] for r in report["runs"]})
    report["summary"] = {
        "distinct_ranks_observed": ranks,
        "all_runs_agree": len(ranks) == 1,
        "n_runs": len(report["runs"]),
    }
    out.write_text(json.dumps(report, indent=1, sort_keys=True))
    print("done ->", out, "ranks:", ranks, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
