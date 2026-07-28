"""10D self-dual (chiral) 5-form F^+_{mu1..mu5}.

Target: 81 functionally independent invariants (Hutomo-Lechner-Sorokin,
arXiv:2509.14351, from a Hilbert series). Explicit generators are NOT known
in the literature -- only partial results at orders 4 and 8. That is the
gap this repo is aimed at.

Do NOT trust output from this script unless scripts/run_6d.py passes first.
"""

import sys, os, time, json, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import numpy as np
from sdinv.modp import P, ALT_P, RankSieve
from sdinv.forms import (selfdual_projector, to_dense, random_form,
                         basis_tuples, check_star_squared)
from sdinv.graphs import enumerate_graphs, graph_label
from sdinv.contract import build_basis_flat, jacobian_row, value

D, PDEG = 10, 5
TARGET = 81


def preflight(mod=P):
    c = check_star_squared(D, PDEG, True, mod)
    assert c == 1, f"star^2 = {c}, expected +1; self-duality is ill-posed"
    Pr = selfdual_projector(D, PDEG, True, mod)
    assert np.array_equal((Pr @ Pr) % mod, Pr % mod), "projector not idempotent"
    s = RankSieve(Pr.shape[1], mod)
    for r in Pr:
        s.add(r)
    assert s.rank == 126, f"self-dual subspace has rank {s.rank}, expected 126"
    return Pr


def run(orders, mod=P, seed=20260727, out=None):
    Pr = preflight(mod)
    rng = np.random.default_rng(seed)
    Fd = to_dense((Pr @ random_form(D, PDEG, rng, mod)) % mod, D, PDEG, mod)

    # quadratic invariant must vanish identically: F ^ F = 0 for odd-degree
    # forms, and self-duality gives F ^ *F = F ^ F, hence F.F = 0.
    g2 = enumerate_graphs(2, PDEG, max_mult=PDEG)
    assert value(g2[0], Fd, D, PDEG, True, mod) == 0, \
        "F.F did not vanish -- self-dual projection is wrong"

    basis = build_basis_flat(D, PDEG, Pr, mod)
    sieve = RankSieve(basis.shape[0], mod)
    log = {"prime": mod, "orders": {}, "generators": []}

    for n in orders:
        t0, before = time.time(), sieve.rank
        graphs = enumerate_graphs(n, PDEG, max_mult=PDEG - 1)
        for M in graphs:
            if sieve.add(jacobian_row(M, Fd, basis, D, PDEG, True, mod)):
                log["generators"].append({"order": n, "graph": graph_label(M)})
                print(f"    NEW  {graph_label(M)}")
        log["orders"][n] = {"graphs": len(graphs),
                            "new": sieve.rank - before,
                            "rank": sieve.rank,
                            "seconds": round(time.time() - t0, 1)}
        print(f"  order {n}: {len(graphs)} graphs -> +{sieve.rank - before} "
              f"new (rank {sieve.rank}/{TARGET}) "
              f"[{log['orders'][n]['seconds']}s]")

    if out:
        json.dump(log, open(out, "w"), indent=2)
    return sieve.rank, log


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--orders", type=int, nargs="+", default=[4, 6])
    ap.add_argument("--out", default="results/10d.json")
    a = ap.parse_args()
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    print(f"10D self-dual 5-form: 126 components, target {TARGET}")
    rank, _ = run(a.orders, P, out=a.out)
    print(f"\nrank so far: {rank} / {TARGET}")
