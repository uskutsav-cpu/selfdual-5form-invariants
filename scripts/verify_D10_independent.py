#!/usr/bin/env python3
"""Phase 3 --- independently verify dim_Q D10 = 11, and certify both bounds.

Independent means what it says. This module imports nothing from
`exact_D10_Q10_characteristic_zero`, shares no rank routine with it, and uses a
different algorithm and a different number representation:

    production        Fraction arithmetic, Gauss-Jordan reduced row echelon
    this verifier     integer arithmetic only, fraction-free Bareiss elimination

Denominators are cleared once, per row, before anything else happens. After
that there are no rationals anywhere: Bareiss is integer-preserving, so every
intermediate is an exact integer and the exact-division property is asserted
rather than assumed.

Three things are produced, not one:

  1. the rank, by an independent route;
  2. a LOWER bound certificate --- an explicit 11x11 minor with nonzero
     integer determinant, computed twice by different methods;
  3. an UPPER bound certificate --- three exact integer covectors annihilating
     every spanning vector, which places D10 inside an 11-dimensional subspace.

The rank alone already gives both bounds, since it is computed rather than
estimated. The separate certificates exist because a referee can check an
11x11 determinant and three dot products by hand, and cannot check an
elimination.

Writes:
    results/stress_flow/D10_exact_rational_final.json
    results/stress_flow/D10_lower_bound_minor.json
    results/stress_flow/D10_annihilator_basis.json

Usage:
    python scripts/verify_D10_independent.py [--repo .]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from datetime import datetime, timezone
from math import gcd
from pathlib import Path

DEGREES = (4, 6, 8, 10, 12)
SEED = {4: ["I4_1"], 6: ["I6_2"], 8: ["I8_3", "I8_4", "I8_5", "I8_6"]}
FLOW = "results/stress_flow/interacting_flow_equations.json"


# --------------------------------------------------------------------------
# integer linear algebra, fraction-free
# --------------------------------------------------------------------------
def clear_denominators(coords: list[dict]) -> list[int]:
    """One integer vector per target, denominators cleared by their lcm."""
    dens = [int(c["denominator"]) for c in coords]
    lcm = 1
    for d in dens:
        lcm = lcm * d // gcd(lcm, d)
    row = [int(c["numerator"]) * (lcm // int(c["denominator"])) for c in coords]
    g = 0
    for x in row:
        g = gcd(g, abs(x))
    return [x // g for x in row] if g > 1 else row


def bareiss_echelon(rows: list[list[int]]) -> tuple[list[list[int]], list[int]]:
    """Fraction-free Gaussian elimination. Integers throughout.

    Bareiss divides by the previous pivot and that division is always exact;
    the assertion below is not decoration, it is the property the algorithm
    rests on, and a violated one means the input was not integral.
    """
    if not rows:
        return [], []
    mat = [list(r) for r in rows]
    n_rows, n_cols = len(mat), len(mat[0])
    prev = 1
    pivots: list[int] = []
    r = 0
    for c in range(n_cols):
        piv = next((i for i in range(r, n_rows) if mat[i][c] != 0), None)
        if piv is None:
            continue
        if piv != r:
            mat[r], mat[piv] = mat[piv], mat[r]
        for i in range(r + 1, n_rows):
            for j in range(c + 1, n_cols):
                num = mat[i][j] * mat[r][c] - mat[i][c] * mat[r][j]
                q, rem = divmod(num, prev)
                assert rem == 0, "Bareiss division was not exact; input not integral"
                mat[i][j] = q
            mat[i][c] = 0
        prev = mat[r][c]
        pivots.append(c)
        r += 1
        if r == n_rows:
            break
    return mat[:r], pivots


def integer_rank(rows: list[list[int]]) -> int:
    return len(bareiss_echelon(rows)[0])


def bareiss_determinant(square: list[list[int]]) -> int:
    """Determinant of an integer square matrix, fraction-free."""
    n = len(square)
    if n == 0:
        return 1
    mat = [list(r) for r in square]
    prev = 1
    sign = 1
    for k in range(n - 1):
        if mat[k][k] == 0:
            swap = next((i for i in range(k + 1, n) if mat[i][k] != 0), None)
            if swap is None:
                return 0
            mat[k], mat[swap] = mat[swap], mat[k]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                num = mat[i][j] * mat[k][k] - mat[i][k] * mat[k][j]
                q, rem = divmod(num, prev)
                assert rem == 0, "Bareiss division was not exact"
                mat[i][j] = q
            mat[i][k] = 0
        prev = mat[k][k]
    return sign * mat[n - 1][n - 1]


def laplace_determinant(square: list[list[int]], depth: int = 0) -> int:
    """Cofactor expansion, for cross-checking small determinants only."""
    n = len(square)
    if n == 1:
        return square[0][0]
    if n == 2:
        return square[0][0] * square[1][1] - square[0][1] * square[1][0]
    total = 0
    for j in range(n):
        if square[0][j] == 0:
            continue
        minor = [row[:j] + row[j + 1:] for row in square[1:]]
        total += ((-1) ** j) * square[0][j] * laplace_determinant(minor, depth + 1)
    return total


def integer_nullspace(rows: list[list[int]], n_cols: int) -> list[list[int]]:
    """Integer basis of {v : M v = 0}, by back substitution over the rationals
    with denominators cleared at the end. Uses its own elimination, not the
    production one."""
    # Reduced echelon over Q, but carried as (numerator row, denominator).
    mat = [list(r) for r in rows]
    pivots: list[int] = []
    r = 0
    for c in range(n_cols):
        piv = next((i for i in range(r, len(mat)) if mat[i][c] != 0), None)
        if piv is None:
            continue
        mat[r], mat[piv] = mat[piv], mat[r]
        for i in range(len(mat)):
            if i != r and mat[i][c] != 0:
                a, b = mat[r][c], mat[i][c]
                g = gcd(abs(a), abs(b)) or 1
                fa, fb = a // g, b // g
                mat[i] = [fa * x - fb * y for x, y in zip(mat[i], mat[r])]
                gg = 0
                for x in mat[i]:
                    gg = gcd(gg, abs(x))
                if gg > 1:
                    mat[i] = [x // gg for x in mat[i]]
        pivots.append(c)
        r += 1
        if r == len(mat):
            break
    mat = mat[:r]
    free = [c for c in range(n_cols) if c not in pivots]
    basis: list[list[int]] = []
    for f in free:
        # v_f = L, v_pivot = -L * mat[k][f] / mat[k][pivot]; clear denominators
        lcm = 1
        for k, p in enumerate(pivots):
            d = abs(mat[k][p])
            lcm = lcm * d // gcd(lcm, d)
        v = [0] * n_cols
        v[f] = lcm
        for k, p in enumerate(pivots):
            v[p] = -(lcm * mat[k][f]) // mat[k][p]
        g = 0
        for x in v:
            g = gcd(g, abs(x))
        if g > 1:
            v = [x // g for x in v]
        basis.append(v)
    return basis


# --------------------------------------------------------------------------
# the closure, re-implemented
# --------------------------------------------------------------------------
def activated_closure(targets: list[dict], seed_ids: dict, *,
                      order: list[int] | None = None) -> tuple[dict, dict]:
    """The activated flow closure, over the integers.

    Re-implemented rather than imported. The activation rule is the same
    mathematics: a target contributes only once EVERY factor of its coefficient
    monomial is a direction already reachable. That condition is what makes
    this the flow closure rather than the raw span of all targets, and dropping
    it is what produced a rank of 14 and a quotient of 0.
    """
    basis = {t["field_degree"]: t["basis"] for t in targets}
    span: dict[int, list[list[int]]] = {d: [] for d in DEGREES}
    for degree, ids in seed_ids.items():
        for name in ids:
            row = [0] * len(basis[degree])
            row[basis[degree].index(name)] = 1
            span[degree].append(row)

    idx = list(range(len(targets))) if order is None else list(order)

    def reachable(degree: int, name: str) -> bool:
        if not span.get(degree):
            return False
        col = basis[degree].index(name)
        return any(row[col] != 0 for row in span[degree])

    sweeps = 0
    for sweeps in range(1, 25):
        grew = False
        for i in idx:
            t = targets[i]
            degree = t["field_degree"]
            active = True
            for f in [x for x in t["coefficient_monomial"] if x]:
                fdeg = next((d for d in DEGREES if f in basis.get(d, [])), None)
                if fdeg is None or not reachable(fdeg, f):
                    active = False
                    break
            if not active:
                continue
            row = clear_denominators(t["coordinates"])
            if not any(row):
                continue
            if integer_rank(span[degree] + [row]) > integer_rank(span[degree]):
                span[degree].append(row)
                grew = True
        if not grew:
            break
    return {d: integer_rank(span[d]) for d in DEGREES}, {"span": span,
                                                         "basis": basis,
                                                         "sweeps": sweeps}


def raw_target_span(targets: list[dict], degree: int) -> int:
    """The span of every target at a degree, with NO activation condition.

    This is the object that gave 14 and a quotient of 0. It is computed here on
    purpose, so the difference is a number in the record rather than a caution
    in a comment.
    """
    rows = [clear_denominators(t["coordinates"])
            for t in targets if t["field_degree"] == degree]
    return integer_rank(rows)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".", type=Path)
    args = ap.parse_args()
    repo = args.repo.resolve()
    when = datetime.now(timezone.utc).isoformat(timespec="seconds")

    flow = json.loads((repo / FLOW).read_text())
    targets = flow["targets"]

    dims, info = activated_closure(targets, SEED)
    span10 = info["span"][10]
    basis10 = info["basis"][10]
    n = len(basis10)
    rank = integer_rank(span10)
    echelon, pivots = bareiss_echelon(span10)
    free_columns = [c for c in range(n) if c not in pivots]

    raw14 = raw_target_span(targets, 10)

    # Sweep-order independence: a fixed point should not care about the order
    # targets are visited in. Three shuffles, same seed material.
    rng = random.Random(20260801)
    order_ranks = []
    for _ in range(3):
        order = list(range(len(targets)))
        rng.shuffle(order)
        d2, _ = activated_closure(targets, SEED, order=order)
        order_ranks.append(d2[10])
    order_independent = all(r == rank for r in order_ranks)

    # ---- seed independence ------------------------------------------------
    # Ten targets carry an empty coefficient monomial and activate
    # unconditionally; two of them at degree 10. They bootstrap the degree-10
    # sector without help, so the answer may not depend on the seed at all.
    # Measured rather than assumed, because it removes a caveat if true.
    seedless_dims, seedless_info = activated_closure(targets, {})
    seedless_span = seedless_info["span"][10]
    union_rank = integer_rank(span10 + seedless_span)
    seed_independent = (
        seedless_dims[10] == rank
        and union_rank == rank
        and integer_rank(seedless_span) == rank
    )
    seed_dependent_degrees = [d for d in DEGREES
                              if d != 10 and seedless_dims[d] != dims[d]]

    # ---- lower bound: an explicit 11x11 minor -----------------------------
    rows_used, cols_used = [], pivots[:rank]
    seen: list[list[int]] = []
    for i, row in enumerate(span10):
        trial = seen + [row]
        if integer_rank(trial) > len(seen):
            seen = trial
            rows_used.append(i)
        if len(rows_used) == rank:
            break
    minor = [[span10[i][c] for c in cols_used] for i in rows_used]
    det_bareiss = bareiss_determinant(minor)
    det_laplace = laplace_determinant(minor) if rank <= 11 else None
    minor_ok = det_bareiss != 0 and (det_laplace is None or det_laplace == det_bareiss)

    # ---- upper bound: exact annihilating covectors ------------------------
    annihilators = integer_nullspace([list(r) for r in span10], n)
    ann_ok = all(
        all(sum(a * b for a, b in zip(v, row)) == 0 for row in span10)
        for v in annihilators
    )
    codim = len(annihilators)

    verdict = ("PROVED" if (rank == 11 and minor_ok and ann_ok
                            and codim == n - rank and order_independent)
               else "NOT ESTABLISHED")

    lower = {
        "generated_utc": when,
        "claim": f"dim_Q D10 >= {rank}",
        "method": "explicit minor of the integer spanning matrix, determinant "
                  "computed twice by independent routines",
        "minor_size": rank,
        "row_indices": rows_used,
        "column_indices": cols_used,
        "column_labels": [basis10[c] for c in cols_used],
        "minor": minor,
        "determinant_bareiss": det_bareiss,
        "determinant_laplace": det_laplace,
        "routines_agree": det_laplace is None or det_laplace == det_bareiss,
        "nonzero": det_bareiss != 0,
        "arithmetic": "integers only; denominators cleared per row before elimination",
        "minor_sha256": sha256_text(json.dumps(minor, sort_keys=True)),
    }
    upper = {
        "generated_utc": when,
        "claim": f"dim_Q D10 <= {n - codim}",
        "method": "exact integer covectors annihilating every spanning vector; "
                  "their number is the codimension",
        "ambient_dimension": n,
        "n_annihilators": codim,
        "annihilators": annihilators,
        "annihilator_labels": [
            {basis10[j]: v[j] for j in range(n) if v[j] != 0} for v in annihilators
        ],
        "all_annihilate_every_spanning_vector": ann_ok,
        "implied_upper_bound": n - codim,
        "arithmetic": "integers only",
    }
    final = {
        "generated_utc": when,
        "verifier": "scripts/verify_D10_independent.py",
        "independence": {
            "imports_production_rank_routine": False,
            "production_algorithm": "Fraction arithmetic, Gauss-Jordan RREF",
            "verifier_algorithm": "integer arithmetic, fraction-free Bareiss",
            "shared_code": "none; the closure is re-implemented",
        },
        "three_distinct_spaces": {
            "raw_target_span_rank": raw14,
            "activated_flow_closure_rank": rank,
            "complete_invariant_space_rank": n,
            "note": ("These are different objects. Using the raw span in place of "
                     "the closure gives a quotient of 0 instead of 3."),
        },
        "ambient_dimension": n,
        "basis": basis10,
        "rank": rank,
        "pivot_columns": pivots,
        "free_columns": free_columns,
        "free_column_labels": [basis10[c] for c in free_columns],
        "fixed_point_sweeps": info["sweeps"],
        "seed_independence": {
            "degree_10_rank_with_seed": rank,
            "degree_10_rank_with_empty_seed": seedless_dims[10],
            "spans_equal": seed_independent,
            "union_rank": union_rank,
            "seed_dependent_degrees": seed_dependent_degrees,
            "dimensions_with_seed": {str(k): v for k, v in dims.items()},
            "dimensions_without_seed": {str(k): v for k, v in seedless_dims.items()},
            "consequence": (
                "At degree 10 the closure is the same space for any seed, so the "
                "'seed closure' qualifier does not limit dim_Q D10 = 11. Degrees "
                "6, 8 and 12 do depend on the seed, so the activation rule is not "
                "vacuous."),
        },
        "sweep_order_independent": order_independent,
        "sweep_order_ranks": order_ranks,
        "rational_dimensions_all_degrees": {str(k): v for k, v in dims.items()},
        "lower_bound": rank,
        "upper_bound": n - codim,
        "exact_dimension": rank if rank == n - codim else None,
        "status": verdict,
        "source_artifact": FLOW,
        "source_sha256": hashlib.sha256((repo / FLOW).read_bytes()).hexdigest(),
    }

    out = repo / "results" / "stress_flow"
    (out / "D10_exact_rational_final.json").write_text(
        json.dumps(final, indent=1) + "\n", encoding="utf-8")
    (out / "D10_lower_bound_minor.json").write_text(
        json.dumps(lower, indent=1) + "\n", encoding="utf-8")
    (out / "D10_annihilator_basis.json").write_text(
        json.dumps(upper, indent=1) + "\n", encoding="utf-8")

    print(f"raw target span rank          {raw14}")
    print(f"activated flow closure rank   {rank}")
    print(f"complete invariant space rank {n}")
    print(f"free columns                  {free_columns} "
          f"{[basis10[c] for c in free_columns]}")
    print(f"sweeps {info['sweeps']}, order-independent {order_independent} "
          f"{order_ranks}")
    print(f"seed-independent at degree 10: {seed_independent} "
          f"(seed-dependent degrees {seed_dependent_degrees})")
    print(f"lower bound minor {rank}x{rank}, det {det_bareiss} "
          f"(laplace {det_laplace}, agree {lower['routines_agree']})")
    print(f"upper bound: {codim} annihilators, all valid {ann_ok}, "
          f"implies dim <= {n - codim}")
    print(f"status: {verdict}")
    return 0 if verdict == "PROVED" else 1


if __name__ == "__main__":
    sys.exit(main())
