"""Stage 9: degree-8 span equality on common samples, with the structured families.

The port-graph stream alone reaches rank 6 of 7 at degree 8.  This script adds
the two families that were missing --- tensor words and the selected Omega/Theta
contractions --- and tests whether the spinor side then spans the same
seven-dimensional space as the tensor side.

Three ranks are reported separately and must not be conflated:

    trace rank    the tensor-side registry at degree 8
    spinor rank   the spinor-side candidates at degree 8
    union rank    both stacked

Span equality is `union == trace == spinor`.  Equal ranks with a larger union
would mean two different 7-spaces, which is exactly the failure a dimension-only
comparison hides.  The change-of-basis map is fitted on the fitting samples and
then validated on holdout samples that took no part in the fit.
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

from sdbridge.bridge import BridgeMap                       # noqa: E402
from sdbridge.clifford import NullFrameClifford             # noqa: E402
from sdbridge.comparison import trace_evaluation_matrix     # noqa: E402
from sdbridge.modular import (                              # noqa: E402
    matmul, rank as modrank, row_space_contains, rref, spans_equal,
)
from sdbridge.samples import build_registry, registry_hash, verify_selfduality  # noqa: E402
from sdbridge.spinor_invariants import (                    # noqa: E402
    evaluate_graph_batch, random_port_graph, sigma_stacks,
)
from sdbridge.structured_degree8 import SELECTED, StructuredDegree8  # noqa: E402
from sdbridge.tensor_words import TensorWordEvaluator, necklaces     # noqa: E402
from sdbridge.traceside import load_registry                # noqa: E402


DEGREE = 8


def spinor_degree8_rows(bridge, samples, n_port_graphs: int, seed: int):
    """Every spinor-side degree-8 source, labelled by family.

    Products of lower-degree spinor invariants are included explicitly: the
    degree-8 space contains I4^2, and omitting it would understate the span for a
    reason that has nothing to do with the candidate families.
    """
    p = bridge.p
    cl = NullFrameClifford(p=p)
    tw = TensorWordEvaluator(p=p)
    sd8 = StructuredDegree8(p=p)
    stacks = sigma_stacks(p)

    S_batch, F_null = [], []
    for s in samples:
        F = s.as_array()
        S_batch.append(cl.coords_to_symmetric(bridge.forward(F)))
        F_null.append(bridge.frame.five_form_to_null(bridge.traceside_dense(F)))
    S_batch = np.array(S_batch)

    rows, labels = [], []

    # 1. tensor words of length 4
    for w in necklaces(4):
        vals = [tw.word_value(w, *tw.blocks(Fn)) for Fn in F_null]
        rows.append(np.array(vals, dtype=np.int64) % p)
        labels.append(f"tensor_word/{w}")

    # 2. the four selected Omega/Theta contractions
    for name in SELECTED:
        vals = [sd8.values(S)[name] for S in S_batch]
        rows.append(np.array(vals, dtype=np.int64) % p)
        labels.append(f"structured/{name}")

    # 3. degree-8 port graphs, sampled
    rng = np.random.default_rng(seed)
    kept = 0
    seen = set()
    for _ in range(n_port_graphs * 8):
        if kept >= n_port_graphs:
            break
        g = random_port_graph(rng, DEGREE // 2)
        if g is None:
            continue
        key = tuple(sorted(g.edges))
        if key in seen:
            continue
        seen.add(key)
        try:
            row = evaluate_graph_batch(g, S_batch, p, stacks).astype(np.int64)
        except Exception:                      # noqa: BLE001
            continue
        if not np.any(row % p):
            continue
        rows.append(row % p)
        labels.append(f"port_graph/{kept}")
        kept += 1

    # 4. the product of the degree-4 invariant with itself
    g4 = None
    r4 = np.zeros(len(samples), dtype=np.int64)
    rng4 = np.random.default_rng(seed + 1)
    for _ in range(200):
        g = random_port_graph(rng4, 2)
        if g is None:
            continue
        row = evaluate_graph_batch(g, S_batch, p, stacks).astype(np.int64)
        if np.any(row % p):
            g4, r4 = g, row % p
            break
    if g4 is not None:
        rows.append((r4 * r4) % p)
        labels.append("product/I4_squared")

    return np.array(rows, dtype=np.int64) % p, labels


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fitting-primes", default="32749,32719")
    ap.add_argument("--holdout-primes", default="32717,32713")
    ap.add_argument("--port-graphs", type=int, default=14)
    ap.add_argument("--seed", type=int, default=20260801)
    ap.add_argument("--out", default=str(ROOT / "verification" / "degree8_span_equality.json"))
    args = ap.parse_args()

    fitting = [int(x) for x in args.fitting_primes.split(",")]
    holdout = [int(x) for x in args.holdout_primes.split(",")]
    registry = load_registry()

    report = {
        "schema": 1,
        "degree": DEGREE,
        "arithmetic": "exact over F_p on both sides; no floating point",
        "fitting_primes": fitting,
        "holdout_primes": holdout,
        "primes": {},
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    for p in fitting + holdout:
        t0 = time.time()
        b = BridgeMap(p=p)
        samples = build_registry(b)
        sd = verify_selfduality(b, samples)
        fit_idx = [i for i, s in enumerate(samples)
                   if s.family in ("generic", "sparse", "structured")]
        hold_idx = [i for i, s in enumerate(samples) if s.family == "holdout"]

        T = trace_evaluation_matrix(b, samples, registry, DEGREE)
        Sp, labels = spinor_degree8_rows(b, samples, args.port_graphs, args.seed)
        U = np.concatenate([T, Sp], axis=0)

        # which families are needed: drop each family and re-rank
        family_contribution = {}
        fams = sorted({l.split("/")[0] for l in labels})
        for fam in fams:
            keep = [i for i, l in enumerate(labels) if not l.startswith(fam + "/")]
            family_contribution[fam] = {
                "rank_without_this_family": int(modrank(Sp[keep], p)) if keep else 0,
            }

        entry = {
            "role": "fitting" if p in fitting else "holdout",
            "n_samples": len(samples),
            "registry_sha256": registry_hash(samples),
            "all_samples_selfdual": sd["all_selfdual"],
            "trace_rank": int(modrank(T, p)),
            "spinor_rank": int(modrank(Sp, p)),
            "union_rank": int(modrank(U, p)),
            "spinor_row_labels": labels,
            "n_spinor_rows": int(Sp.shape[0]),
            "trace_in_spinor": bool(row_space_contains(Sp, T, p)),
            "spinor_in_trace": bool(row_space_contains(T, Sp, p)),
            "spans_equal": bool(spans_equal(T, Sp, p)),
            "family_contribution": family_contribution,
            "wall_seconds": round(time.time() - t0, 1),
        }
        entry["span_equality_holds"] = (
            entry["trace_rank"] == entry["spinor_rank"] == entry["union_rank"] == 7
            and entry["spans_equal"])

        # change of basis on fitting columns, validated on holdout columns
        Tf, Sf = T[:, fit_idx], Sp[:, fit_idx]
        Th, Sh = T[:, hold_idx], Sp[:, hold_idx]
        if row_space_contains(Sf, Tf, p):
            R, piv = rref(Sf, p)
            from sdbridge.clifford import _inverse_mod
            basis = R[:len(piv)]
            coeff = matmul(Tf[:, piv], _inverse_mod(basis[:, piv], p), p)
            Tform = matmul(basis[:, piv], _inverse_mod(Sf[:, piv], p), p)
            predicted = matmul(coeff, matmul(Tform, Sh, p), p)
            entry["change_of_basis"] = {"shape": list(coeff.shape),
                                        "fitted_on": "generic + sparse + structured",
                                        "validated_on": "holdout only"}
            entry["holdout_validated"] = bool(np.array_equal(predicted % p, Th % p))
        else:
            entry["change_of_basis"] = None
            entry["holdout_validated"] = False

        report["primes"][str(p)] = entry
        print(f"[p={p}] trace {entry['trace_rank']} spinor {entry['spinor_rank']} "
              f"union {entry['union_rank']} equal={entry['spans_equal']} "
              f"holdout={entry['holdout_validated']} ({entry['wall_seconds']}s)",
              flush=True)
        out.write_text(json.dumps(report, indent=1))

    ok = [e for e in report["primes"].values() if e["span_equality_holds"]]
    report["summary"] = {
        "primes_tested": len(report["primes"]),
        "primes_with_span_equality": len(ok),
        "required": "trace = spinor = union = 7 with two-way containment",
        "passes_stage9": len(ok) == len(report["primes"]) and len(report["primes"]) >= 4,
    }
    out.write_text(json.dumps(report, indent=1))
    print("done ->", out, json.dumps(report["summary"]), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
