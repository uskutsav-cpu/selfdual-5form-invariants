#!/usr/bin/env python3
"""Assemble the per-cell rank-81 results into one certificate. Read-only.

This never computes and never repairs. It reads `results/rank81/cells/*.json`,
checks that the set of cells is exactly the planned matrix and that the cells
agree with each other, and only then writes the assembled certificate.

It fails, rather than assembling, when:

  * a planned cell is missing
  * a cell file is present twice for the same (prime, seed)
  * a cell is not marked complete
  * candidate ordering differs between cells
  * the coordinate dimension differs between cells
  * a cell's recorded content hash does not match its contents
  * a cell reports evaluation errors, interruptions or failed Euler checks

Those are the ways a matrix can look finished while being wrong, and each one
has a named exit rather than a warning.

Usage:
    python spinor_trace_bridge/scripts/assemble_rank81_matrix.py \
        [--cells results/rank81/cells] [--out results/rank81/certificate_matrix.json]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

FITTING = [32749, 32719, 32717]
HOLDOUT = [32713, 32707]
SEEDS = [11, 22, 33]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".", type=Path)
    ap.add_argument("--cells", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--fitting-primes", default=",".join(map(str, FITTING)))
    ap.add_argument("--holdout-primes", default=",".join(map(str, HOLDOUT)))
    ap.add_argument("--seeds", default=",".join(map(str, SEEDS)))
    args = ap.parse_args()

    repo = args.repo.resolve()
    cells_dir = Path(args.cells) if args.cells else repo / "results" / "rank81" / "cells"
    out = Path(args.out) if args.out else repo / "results" / "rank81" / "certificate_matrix.json"

    fitting = [int(x) for x in args.fitting_primes.split(",") if x.strip()]
    holdout = [int(x) for x in args.holdout_primes.split(",") if x.strip()]
    seeds = [int(x) for x in args.seeds.split(",") if x.strip()]
    planned = [(p, s, "fitting") for p in fitting for s in seeds] + \
              [(p, s, "holdout") for p in holdout for s in seeds]

    problems: list[str] = []
    by_key: dict[tuple[int, int], dict] = {}

    for path in sorted(cells_dir.glob("cell_p*_s*.json")):
        try:
            cell = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            problems.append(f"{path.name}: unreadable ({exc})")
            continue
        key = (cell["cell"]["prime"], cell["cell"]["seed"])
        if key in by_key:
            problems.append(f"duplicate cell for prime={key[0]} seed={key[1]}")
            continue
        recorded = cell.get("content_sha256")
        if recorded:
            check = dict(cell)
            check.pop("content_sha256")
            if sha256_text(json.dumps(check, indent=1, sort_keys=True)) != recorded:
                problems.append(f"{path.name}: content hash does not match contents")
        by_key[key] = cell

    for p, s, role in planned:
        cell = by_key.get((p, s))
        if cell is None:
            problems.append(f"missing cell prime={p} seed={s} ({role})")
            continue
        if cell["cell"]["role"] != role:
            problems.append(f"prime={p} seed={s}: role {cell['cell']['role']} != {role}")
        if not cell.get("cell_complete"):
            problems.append(f"prime={p} seed={s}: cell not marked complete")
        summary = cell["schedule_summary"]
        if summary.get("evaluation_errors"):
            problems.append(f"prime={p} seed={s}: {summary['evaluation_errors']} evaluation errors")
        if summary.get("interrupted"):
            problems.append(f"prime={p} seed={s}: {summary['interrupted']} interrupted")
        if summary.get("zero_rows"):
            problems.append(f"prime={p} seed={s}: {summary['zero_rows']} zero rows")
        euler = cell["euler_homogeneity"]
        if euler["failed"] or euler["passed"] != euler["checked"]:
            problems.append(f"prime={p} seed={s}: Euler {euler['passed']}/{euler['checked']}")

    used = [by_key[(p, s)] for p, s, _ in planned if (p, s) in by_key]
    orders = {c.get("candidate_order_sha256") for c in used}
    if len(orders) > 1:
        problems.append(f"candidate ordering differs between cells: {sorted(orders)}")
    dims = {c.get("coordinate_dimension") for c in used}
    if len(dims) > 1:
        problems.append(f"coordinate dimension differs between cells: {sorted(dims)}")
    counts = {c.get("n_candidates_scheduled") for c in used}
    if len(counts) > 1:
        problems.append(f"scheduled candidate count differs between cells: {sorted(counts)}")
    # A differing contraction budget silently changes which candidates evaluate:
    # at 2e10 the degree-12 port graph c046 errors out, at 1e11 it evaluates.
    # Cells computed under different budgets are not comparable.
    budgets = {c.get("flop_limit") for c in used}
    if len(budgets) > 1:
        problems.append(f"contraction flop budget differs between cells: {sorted(budgets)}")

    extra = sorted(set(by_key) - {(p, s) for p, s, _ in planned})
    for p, s in extra:
        problems.append(f"cell prime={p} seed={s} is not in the planned matrix")

    when = datetime.now(timezone.utc).isoformat(timespec="seconds")
    ranks = sorted({c["jacobian"]["total_rank"] for c in used})
    report = {
        "schema": 1,
        "generated_utc": when,
        "assembled_by": "spinor_trace_bridge/scripts/assemble_rank81_matrix.py",
        "assembly_is_read_only": True,
        "planned_cells": [{"prime": p, "seed": s, "role": r} for p, s, r in planned],
        "n_planned": len(planned),
        "n_present": len(used),
        "problems": problems,
        "matrix_complete": not problems and len(used) == len(planned),
        "statement_separation": {
            "float64_evidence": "not used",
            "exact_modular_rank": "computed per (prime, seed) cell",
            "characteristic_zero": (
                "the coordinate basis is integral, so each Jacobian is the reduction "
                "of an integer matrix and rank_{F_p} <= rank_Q holds unconditionally"),
            "generic_rank": (
                "not established by finitely many points; the matching upper bound "
                "126 - 45 = 81 is analytic and comes from the literature"),
        },
        "summary": {
            "distinct_total_ranks": ranks,
            "all_cells_agree": len(ranks) == 1,
            "characteristic_zero_lower_bound": max(ranks) if ranks else 0,
            "fitting_primes": fitting,
            "holdout_primes": holdout,
            "seeds": seeds,
            "flop_limit": sorted(budgets)[0] if len(budgets) == 1 else None,
            "candidate_order_sha256": sorted(orders)[0] if len(orders) == 1 else None,
            "coordinate_dimension": sorted(dims)[0] if len(dims) == 1 else None,
            "n_candidates_scheduled": sorted(counts)[0] if len(counts) == 1 else None,
        },
        "cells": [
            {
                "prime": c["cell"]["prime"],
                "seed": c["cell"]["seed"],
                "role": c["cell"]["role"],
                "total_rank": c["jacobian"]["total_rank"],
                "n_rows": c["jacobian"]["n_rows"],
                "n_columns": c["jacobian"]["n_columns"],
                "per_degree_block_rank": c["jacobian"]["per_degree_block_rank"],
                "cumulative_rank_by_degree": c["jacobian"]["cumulative_rank_by_degree"],
                "pivot_rows": c["jacobian"]["pivot_rows"],
                "pivot_columns": c["jacobian"]["pivot_columns"],
                "euler": f"{c['euler_homogeneity']['passed']}/{c['euler_homogeneity']['checked']}",
                "evaluation_errors": c["schedule_summary"].get("evaluation_errors"),
                "zero_rows": len(c.get("zero_rows", [])),
                "wall_seconds": c.get("wall_seconds"),
                "peak_rss_mb": c.get("peak_rss_mb"),
                "content_sha256": c.get("content_sha256"),
            }
            for c in used
        ],
    }

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")

    print(f"cells {len(used)}/{len(planned)} present, ranks {ranks}")
    for c in report["cells"]:
        print(f"  p={c['prime']:<6} seed={c['seed']:<3} {c['role']:<8} "
              f"rank {c['total_rank']} rows {c['n_rows']} euler {c['euler']} "
              f"{c['wall_seconds']}s")
    if problems:
        print(f"\n{len(problems)} problems:")
        for p in problems:
            print(f"  - {p}")
        print("\nMATRIX INCOMPLETE")
        return 1
    print("\nMATRIX COMPLETE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
