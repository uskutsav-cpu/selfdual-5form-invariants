"""Exact modular Jacobian of the ARCHIVE's own selected candidate set.

The archive computed a float64 finite-difference Jacobian of 83 selected
candidates and reported rank 81 after row normalisation.  This script
differentiates the *same* candidates analytically and exactly over F_p.

Scope, stated up front because it matters: of the 83 candidates, 70 are port
graphs and 13 are "structured" tensor-word candidates whose definitions live in
the archive's `tensor_form.py`.  Only the port graphs are re-implemented here.
The tensor words are NOT silently dropped -- they are counted and reported, and
the resulting rank is reported as the rank of the port-graph subset, never as
the rank of the full 83.

Usage:
    python spinor_trace_bridge/scripts/run_archive_jacobian_exact.py --archive PATH
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "spinor_trace_bridge" / "src"))

from sdbridge import conventions as C                       # noqa: E402
from sdbridge.integral import integral_basis_mod, integral_gamma_traceless_basis  # noqa: E402
from sdbridge.jacobian import graph_jacobian_row, random_spinor_point  # noqa: E402
from sdbridge.modular import rank as modrank                # noqa: E402
from sdbridge.spinor_invariants import (                    # noqa: E402
    ContractionTooLarge, PortGraph, sigma_stacks,
)


def load_archive_candidates(path: Path):
    """Split the archive's selection into port graphs and structured candidates."""
    raw = json.loads(path.read_text())
    graphs, structured = [], []
    for d in raw:
        if d.get("kind") == "structured":
            structured.append({"name": d["name"], "degree": int(d["degree"])})
            continue
        edges = tuple(tuple(sorted((tuple(a), tuple(b)))) for a, b in d["edges"])
        graphs.append((int(d["degree"]),
                       PortGraph(n_nodes=int(d["n_I"]), edges=edges)))  # type: ignore[arg-type]
    return graphs, structured


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--archive", required=True)
    ap.add_argument("--primes", default="32749,32719")
    ap.add_argument("--seeds", default="11,22,33")
    ap.add_argument("--flop-limit", type=float, default=None,
                    help="override the per-contraction flop budget")
    ap.add_argument("--out", default=str(ROOT / "verification" / "spinor_archive_jacobian_exact.json"))
    args = ap.parse_args()

    if args.flop_limit:
        import sdbridge.spinor_invariants as si
        si.MAX_CONTRACTION_FLOPS = args.flop_limit
        # the default argument was bound at import time, so rebind it too
        si._modular_contract.__defaults__ = (
            None, si.MAX_INTERMEDIATE_ELEMENTS, args.flop_limit)
    archive = Path(args.archive).expanduser().resolve()
    cand_path = archive / "run_4_12_tensor_words_s96" / "selected_graphs.json"
    graphs, structured = load_archive_candidates(cand_path)
    by_degree = collections.Counter(d for d, _ in graphs)
    print(f"{len(graphs)} port graphs {dict(sorted(by_degree.items()))}, "
          f"{len(structured)} structured candidates (not re-implemented)", flush=True)

    integral_basis = integral_gamma_traceless_basis()
    report = {
        "schema": 1,
        "candidate_source": str(cand_path.name),
        "n_candidates_total": len(graphs) + len(structured),
        "n_port_graphs_used": len(graphs),
        "n_structured_not_reimplemented": len(structured),
        "structured_names": [s["name"] for s in structured],
        "port_graphs_by_degree": {str(k): v for k, v in sorted(by_degree.items())},
        "method": "analytic amputated derivative, exact over F_p, integral basis",
        "flop_limit": args.flop_limit,
        "why_the_bound_is_rigorous": (
            "The gamma-traceless basis is integral and the point is an integer "
            "combination of it, so the Jacobian is the reduction of a genuine "
            "integer matrix. rank_{F_p}(J mod p) <= rank_Q(J) then holds "
            "unconditionally: reduction can only drop rank."),
        "analytic_upper_bound": 81,
        "analytic_upper_bound_source": "126 - dim so(10) = 126 - 45; literature",
        "runs": [],
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    for p in [int(x) for x in args.primes.split(",")]:
        basis = np.array([[int(x) % p for x in row] for row in integral_basis],
                         dtype=np.int64)
        basis_matrices = np.array([
            _sym(basis[r], p) for r in range(basis.shape[0])])
        stacks = sigma_stacks(p)
        for seed in [int(x) for x in args.seeds.split(",")]:
            S = random_spinor_point(p, seed)
            rows, skipped, zero = [], [], 0
            t0 = time.time()
            for deg, g in graphs:
                try:
                    row = graph_jacobian_row(g, S, basis_matrices, p, stacks)
                except ContractionTooLarge as exc:
                    skipped.append({"degree": deg, "reason": str(exc)})
                    continue
                if not np.any(row % p):
                    zero += 1
                rows.append(row)
            J = np.array(rows, dtype=np.int64) if rows else np.zeros((0, 126), np.int64)
            r = int(modrank(J, p)) if J.size else 0
            entry = {
                "prime": p, "point_seed": seed,
                "rows_evaluated": int(J.shape[0]),
                "rows_skipped_too_expensive": len(skipped),
                "skipped_detail": skipped,
                "identically_zero_rows": zero,
                "exact_modular_rank_of_port_graph_subset": r,
                "wall_seconds": round(time.time() - t0, 1),
            }
            report["runs"].append(entry)
            print(f"[p={p} seed={seed}] rows={entry['rows_evaluated']} "
                  f"skipped={entry['rows_skipped_too_expensive']} "
                  f"EXACT RANK={r} ({entry['wall_seconds']}s)", flush=True)
            out.write_text(json.dumps(report, indent=1))

    ranks = sorted({r["exact_modular_rank_of_port_graph_subset"] for r in report["runs"]})
    report["summary"] = {
        "distinct_ranks": ranks,
        "all_runs_agree": len(ranks) == 1,
        "interpretation": (
            f"The port-graph subset of the archive's selection attains exact "
            f"modular rank {ranks[0] if len(ranks) == 1 else ranks}. Because the "
            f"matrix is an integer reduction this is a rigorous lower bound on "
            f"the characteristic-zero rank. It is the rank of the port-graph "
            f"subset only; the {len(structured)} structured tensor-word "
            f"candidates were not re-implemented and may contribute further "
            f"directions."),
    }
    out.write_text(json.dumps(report, indent=1))
    print("done ->", out, ranks, flush=True)
    return 0


def _sym(v, p):
    from sdbridge.clifford import symmetric_pairs
    M = np.zeros((C.SPINOR_DIM, C.SPINOR_DIM), dtype=np.int64)
    for val, (i, j) in zip(v, symmetric_pairs()):
        M[i, j] = int(val) % p
        M[j, i] = int(val) % p
    return M


if __name__ == "__main__":
    raise SystemExit(main())
