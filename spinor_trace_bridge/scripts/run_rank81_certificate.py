"""Stages 5-7: evaluate all 83 candidates exactly and certify the Jacobian rank.

For every (sample point, prime) this records a terminal status for every
scheduled candidate, the exact analytic Jacobian, degree-block and cumulative
ranks, pivot rows and columns, and the Euler homogeneity check.

Four statements are kept apart throughout and never merged:

  * float64 evidence            -- not produced here at all
  * exact modular rank          -- what this script computes
  * characteristic-zero bound   -- follows because the basis is INTEGRAL, so the
                                   Jacobian is the reduction of an integer matrix
                                   and rank can only drop under reduction
  * generic rank                -- a statement about a generic point, which no
                                   finite set of points establishes on its own

Writes incrementally and skips completed (prime, seed) pairs, so an interrupted
run resumes by re-issuing the same command.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "spinor_trace_bridge" / "src"))

from sdbridge import conventions as C                    # noqa: E402
from sdbridge.candidates import (                        # noqa: E402
    build_context, evaluate_all, load_schedule, schedule_summary,
)
from sdbridge.modular import rank as modrank, rref       # noqa: E402
import sdbridge.spinor_invariants as si                  # noqa: E402


def degree_blocks(schedule, J) -> dict:
    """Rank contributed by each degree, and cumulative rank up to each degree."""
    evaluated = [c for c in schedule if c.terminal_status == "evaluated"]
    p = None
    out = {}
    return evaluated, out


def analyse(schedule, J, p: int) -> dict:
    evaluated = [c for c in schedule if c.terminal_status == "evaluated"]
    degrees = sorted({c.degree for c in evaluated})
    per_degree, cumulative = {}, {}
    for d in degrees:
        idx = [i for i, c in enumerate(evaluated) if c.degree == d]
        per_degree[str(d)] = {
            "candidates": len(idx),
            "block_rank": int(modrank(J[idx], p)) if idx else 0,
        }
        upto = [i for i, c in enumerate(evaluated) if c.degree <= d]
        cumulative[str(d)] = int(modrank(J[upto], p)) if upto else 0
    R, pivots = rref(J, p)
    total = int(modrank(J, p))
    # which rows form an independent set, in schedule order
    pivot_rows, seen = [], np.zeros((0, J.shape[1]), dtype=np.int64)
    for i in range(J.shape[0]):
        trial = np.concatenate([seen, J[i:i + 1]], axis=0)
        if modrank(trial, p) > seen.shape[0]:
            seen = trial
            pivot_rows.append(i)
        if len(pivot_rows) == total:
            break
    return {
        "n_rows": int(J.shape[0]),
        "n_columns": int(J.shape[1]),
        "total_rank": total,
        "per_degree_block_rank": per_degree,
        "cumulative_rank_by_degree": cumulative,
        "pivot_columns": [int(c) for c in pivots],
        "pivot_rows": pivot_rows,
        "pivot_row_candidate_ids": [evaluated[i].candidate_id for i in pivot_rows],
        "row_normalisation_used": False,
        "note": ("No row normalisation is applied. Over F_p a row is zero or it "
                 "is not; normalising would be meaningless here and is the "
                 "mechanism that inflated the float64 rank."),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--archive", required=True)
    ap.add_argument("--fitting-primes", default="32749,32719,32717")
    ap.add_argument("--holdout-primes", default="32713,32707")
    ap.add_argument("--seeds", default="11,22,33")
    ap.add_argument("--flop-limit", type=float, default=5e10)
    ap.add_argument("--out", default=str(ROOT / "results" / "rank81" / "certificate.json"))
    args = ap.parse_args()

    si.MAX_CONTRACTION_FLOPS = args.flop_limit
    si._modular_contract.__defaults__ = (None, si.MAX_INTERMEDIATE_ELEMENTS,
                                         args.flop_limit)

    selection = Path(args.archive).expanduser().resolve() / \
        "run_4_12_tensor_words_s96" / "selected_graphs.json"
    fitting = [int(x) for x in args.fitting_primes.split(",")]
    holdout = [int(x) for x in args.holdout_primes.split(",")]
    seeds = [int(x) for x in args.seeds.split(",")]

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "schema": 1,
        "method": "exact analytic Jacobian; no finite differences, no tolerance",
        "flop_limit": args.flop_limit,
        "fitting_primes": fitting,
        "holdout_primes": holdout,
        "seeds": seeds,
        "statement_separation": {
            "float64_evidence": "not used",
            "exact_modular_rank": "computed here per (seed, prime)",
            "characteristic_zero": ("the coordinate basis is integral, so each "
                                    "Jacobian is the reduction of an integer "
                                    "matrix and rank_{F_p} <= rank_Q holds "
                                    "unconditionally"),
            "generic_rank": ("not established by finitely many points; the "
                             "matching upper bound 126 - 45 = 81 is analytic "
                             "and comes from the literature"),
        },
        "runs": [],
    }
    if out.exists():
        try:
            report = json.loads(out.read_text())
        except json.JSONDecodeError:
            pass
    done = {(r["prime"], r["seed"]) for r in report["runs"]}

    for p in fitting + holdout:
        for seed in seeds:
            if (p, seed) in done:
                print(f"[p={p} seed={seed}] already done", flush=True)
                continue
            t0 = time.time()
            schedule = load_schedule(selection)
            ctx = build_context(p, seed=seed)
            J, schedule = evaluate_all(schedule, ctx)
            summary = schedule_summary(schedule)
            stats = analyse(schedule, J, p)

            # Euler homogeneity, per candidate, on the same point
            euler = {"checked": 0, "passed": 0, "failed": []}
            evaluated = [c for c in schedule if c.terminal_status == "evaluated"]
            for i, c in enumerate(evaluated):
                lhs = int(ctx.coeffs % p @ J[i] % p)
                rhs = (c.degree * int(c.value)) % p
                euler["checked"] += 1
                if lhs == rhs:
                    euler["passed"] += 1
                else:
                    euler["failed"].append({"candidate": c.candidate_id,
                                            "lhs": lhs, "rhs": rhs})

            entry = {
                "prime": p, "seed": seed,
                "role": "fitting" if p in fitting else "holdout",
                "schedule_summary": summary,
                "jacobian": stats,
                "euler_homogeneity": euler,
                "zero_rows": [c.candidate_id for c in evaluated if c.zero_row],
                "zero_row_explanations": {c.candidate_id: c.zero_row_explanation
                                          for c in evaluated if c.zero_row},
                "terminal_records": [c.record() for c in schedule],
                "wall_seconds": round(time.time() - t0, 1),
            }
            report["runs"].append(entry)
            print(f"[p={p} seed={seed}] rank {stats['total_rank']} "
                  f"rows {stats['n_rows']} "
                  f"errors {summary['evaluation_errors']} "
                  f"euler {euler['passed']}/{euler['checked']} "
                  f"({entry['wall_seconds']}s)", flush=True)
            out.write_text(json.dumps(report, indent=1))

    ranks = sorted({r["jacobian"]["total_rank"] for r in report["runs"]})
    complete = all(r["schedule_summary"]["complete"] for r in report["runs"])
    euler_ok = all(not r["euler_homogeneity"]["failed"] for r in report["runs"])
    report["summary"] = {
        "distinct_total_ranks": ranks,
        "max_exact_rank": max(ranks) if ranks else 0,
        "all_runs_agree": len(ranks) == 1,
        "all_schedules_complete": complete,
        "all_euler_checks_pass": euler_ok,
        "n_runs": len(report["runs"]),
        "characteristic_zero_lower_bound": max(ranks) if ranks else 0,
        "characteristic_zero_justification": (
            "the integral basis makes each Jacobian an integer reduction, so the "
            "observed modular rank is an unconditional lower bound on rank over Q"),
    }
    out.write_text(json.dumps(report, indent=1))
    print("done ->", out, "ranks:", ranks, "complete:", complete,
          "euler:", euler_ok, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
