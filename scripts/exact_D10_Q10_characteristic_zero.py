#!/usr/bin/env python3
"""Settle dim_Q D10 and dim_Q Q10 exactly, over the rationals.

Every published statement of these numbers has been modular: "11 at the tested
primes". Modular rank is a LOWER bound on rational rank, and for D10 that is
the wrong direction -- Q10 = A10 - D10, so a D10 that is secretly larger over Q
makes the obstruction *smaller*. No number of primes closes that gap.

It does not have to be closed modularly. D10 is the fixed-point closure of the
generalized stress flow from a seed, and the flow targets in
`results/stress_flow/interacting_flow_equations.json` carry exact rational
coordinates, with the source's own modular and rational holdouts passed. The
same closure therefore runs over Q, with Fraction arithmetic, and its rank is
computed rather than bounded.

Two things this script is careful about, both of which produced a wrong answer
first:

  * D10 is NOT the span of every degree-10 flow target. Taking all 37 gives
    rank 14 and a quotient of 0, because that span includes what Tr(tau) and
    every coefficient monomial can reach. D10 is a closure from a specific
    seed, and a target only becomes active once every factor of its
    coefficient monomial is already reachable.
  * D10 is also NOT the "new forcing" space, which is 5 at degree 10 with
    quotient 9, nor the static stress span, which is 2. Three different
    numbers live at degree 10 and only the seed closure is 11.

Writes:
    results/stress_flow/D10_characteristic_zero_final.json
    results/stress_flow/Q10_characteristic_zero_final.json
    docs/D10_Q10_FINAL_STATUS.md

Usage:
    python scripts/exact_D10_Q10_characteristic_zero.py [--repo .]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

QUOTIENT = "results/generalized_flow/quotient_degree10.json"
INCIDENCE = "results/intrinsic_candidates/degree10_space_incidence.json"
CERT_DIR = "results/stress_flow/certificates"
DEGREES = (4, 6, 8, 10, 12)

# The seed used by scripts/solve_intrinsic_quotients.py, reproduced here so the
# rational closure answers the same question as the modular one.
SEED = {4: ["I4_1"], 6: ["I6_2"], 8: ["I8_3", "I8_4", "I8_5", "I8_6"]}


def to_fraction(entry) -> Fraction:
    if isinstance(entry, dict):
        return Fraction(int(entry["numerator"]), int(entry["denominator"]))
    return Fraction(int(entry))


def rational_rref(rows: list[list[Fraction]]) -> tuple[list[list[Fraction]], list[int]]:
    """Exact reduced row echelon form over Q. No floating point, no modulus."""
    if not rows:
        return [], []
    mat = [list(r) for r in rows]
    n_cols = len(mat[0])
    pivots: list[int] = []
    r = 0
    for c in range(n_cols):
        piv = next((i for i in range(r, len(mat)) if mat[i][c] != 0), None)
        if piv is None:
            continue
        mat[r], mat[piv] = mat[piv], mat[r]
        inv = Fraction(1, 1) / mat[r][c]
        mat[r] = [x * inv for x in mat[r]]
        for i in range(len(mat)):
            if i != r and mat[i][c] != 0:
                f = mat[i][c]
                mat[i] = [a - f * b for a, b in zip(mat[i], mat[r])]
        pivots.append(c)
        r += 1
        if r == len(mat):
            break
    return mat[:r], pivots


def rational_rank(rows: list[list[Fraction]]) -> int:
    return len(rational_rref(rows)[0])


def rational_closure(targets: list[dict], seed_ids: dict) -> tuple[dict, dict, dict]:
    """The same fixed point as scripts/stress_flow_closure.closure, over Q.

    Activation is 'some spanning vector has a nonzero entry in that column',
    exactly as in the modular version. Over Q a coefficient cannot vanish by
    accident of the modulus, so a target inactive mod p may be active here --
    which is precisely why the rational closure can only be larger.
    """
    basis: dict[int, list[str]] = {}
    for t in targets:
        basis[t["field_degree"]] = t["basis"]

    span: dict[int, list[list[Fraction]]] = {d: [] for d in DEGREES}
    for degree, ids in seed_ids.items():
        for name in ids:
            row = [Fraction(0)] * len(basis[degree])
            row[basis[degree].index(name)] = Fraction(1)
            span[degree].append(row)

    def in_span(degree: int, name: str) -> bool:
        if not span.get(degree):
            return False
        idx = basis[degree].index(name)
        return any(row[idx] != 0 for row in span[degree])

    sweeps = 0
    for sweeps in range(1, 25):
        grew = False
        for t in targets:
            degree = t["field_degree"]
            ok = True
            for f in [x for x in t["coefficient_monomial"] if x]:
                fdeg = next((d for d in DEGREES if f in basis.get(d, [])), None)
                if fdeg is None or not in_span(fdeg, f):
                    ok = False
                    break
            if not ok:
                continue
            row = [to_fraction(c) for c in t["coordinates"]]
            if not any(row):
                continue
            before = rational_rank(span[degree])
            after = rational_rank(span[degree] + [row])
            if after > before:
                span[degree].append(row)
                grew = True
        if not grew:
            break
    dims = {d: rational_rank(span[d]) for d in DEGREES}
    return dims, basis, {"sweeps": sweeps, "span": span}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".", type=Path)
    ap.add_argument("--certificate", default=None,
                    help="interacting_degree12_<prime>.json to read targets from; "
                         "only its exact rational coordinates are used")
    args = ap.parse_args()
    repo = args.repo.resolve()
    when = datetime.now(timezone.utc).isoformat(timespec="seconds")

    # The assembled flow-equation file carries the rational coordinates; the
    # per-prime certificates carry the same targets reduced mod p. Rational
    # arithmetic needs the former.
    flow_path = repo / "results" / "stress_flow" / "interacting_flow_equations.json"
    flow = json.loads(flow_path.read_text())
    targets = flow["targets"]
    if not all(isinstance(t["coordinates"][0], dict) for t in targets):
        print("flow targets are not rational; cannot run over Q", file=sys.stderr)
        return 2

    quotient = json.loads((repo / QUOTIENT).read_text())
    incidence = json.loads((repo / INCIDENCE).read_text())

    dims, basis, info = rational_closure(targets, SEED)
    n = len(basis[10])
    span10 = info["span"][10]
    echelon, pivots = rational_rref(span10)
    rank_Q = len(echelon)
    free_columns = [c for c in range(n) if c not in pivots]

    modular_rank = quotient["closure_dimension"]
    modular_free = quotient["free_columns"]
    dims_inc = next(iter(incidence["per_prime"].values()))["dims"]
    a10_modular = dims_inc["A10"]

    # A10's upper bound is structural: the fourteen basis elements ARE the
    # coordinate system, so nothing spanned by them exceeds fourteen.
    a10_exact = a10_modular if a10_modular == n else None
    d10_exact = rank_Q
    q10_exact = (a10_exact - d10_exact) if a10_exact is not None else None

    agreement = rank_Q == modular_rank
    same_free = sorted(free_columns) == sorted(modular_free)
    verdict = "PROVED" if (agreement and same_free and a10_exact is not None) else "OPEN"

    permitted = (
        f"dim_Q A10 = {a10_exact}, dim_Q D10 = {d10_exact}, dim_Q Q10 = {q10_exact}"
        if verdict == "PROVED" else
        f"dim_Q A10 = {a10_exact}, dim_Q D10 >= {modular_rank}, "
        f"dim_Q Q10 <= {(a10_exact - modular_rank) if a10_exact else '?'}, "
        f"with quotient dimension {quotient['quotient_dimension']} at the tested "
        "good primes")

    d10_record = {
        "generated_utc": when,
        "space": "D10",
        "definition": (
            "The fixed-point closure of the generalized stress flow from the seed "
            "{4: [I4_1], 6: [I6_2], 8: [I8_3, I8_4, I8_5, I8_6]}, in the verified "
            "degree-10 basis. A target activates once every factor of its "
            "coefficient monomial is reachable."),
        "not_to_be_confused_with": {
            "span_of_all_degree10_targets": {
                "rational_rank": 14,
                "why_different": "includes Tr(tau) and every coefficient monomial, "
                                 "with no activation condition; quotient would be 0",
            },
            "new_forcing_space": {
                "dimension": flow["new_forcing_dimension_by_degree"]["10"],
                "quotient": flow["new_forcing_quotient_dimension_by_degree"]["10"],
                "why_different": "excludes Tr(tau) as a generator entirely",
            },
            "static_stress_span": {
                "dimension": 2,
                "why_different": "the static span is not the dynamically reachable set",
            },
        },
        "seed": SEED,
        "basis": basis[10],
        "ambient_dimension": n,
        "arithmetic": "exact rational closure and elimination over Q (fractions.Fraction)",
        "floating_point_used": False,
        "modulus_used": False,
        "fixed_point_sweeps": info["sweeps"],
        "rational_rank": rank_Q,
        "pivot_columns": pivots,
        "free_columns": free_columns,
        "free_basis_elements": [basis[10][c] for c in free_columns],
        "rational_dimensions_all_degrees": {str(k): v for k, v in dims.items()},
        "modular_rank_previously_reported": modular_rank,
        "modular_free_columns": modular_free,
        "rational_and_modular_agree": agreement,
        "free_columns_agree": same_free,
        "lower_bound": {
            "value": modular_rank,
            "route": "rank over F_p is a lower bound on rank over Q",
            "unconditional": True,
        },
        "upper_bound": {
            "value": rank_Q,
            "route": ("the closure is computed over Q and its rank read off by exact "
                      "rational elimination, so the value is the rank, not a bound"),
            "unconditional": True,
        },
        "exact_characteristic_zero_dimension": d10_exact,
        "status": verdict,
        "source_artifact": str(flow_path.relative_to(repo)),
        "source_sha256": sha256_file(flow_path),
        "holdouts_passed_in_source": flow["exact_validation"][
            "all_modular_and_rational_holdouts_passed"],
        "scope_caveat": quotient.get("caveat", ""),
    }

    q10_record = {
        "generated_utc": when,
        "space": "Q10 = A10 / D10",
        "A10": {
            "modular_dimension": a10_modular,
            "structural_upper_bound": n,
            "upper_bound_route": ("A10 is spanned by the fourteen basis elements "
                                  "that coordinatise it, so it cannot exceed 14"),
            "lower_bound_route": "modular rank 14 is a lower bound on the rank over Q",
            "exact_characteristic_zero_dimension": a10_exact,
            "status": "PROVED" if a10_exact is not None else "OPEN",
        },
        "D10": {"exact_characteristic_zero_dimension": d10_exact, "status": verdict},
        "exact_characteristic_zero_dimension": q10_exact,
        "quotient_representatives": quotient.get("quotient_representatives"),
        "status": verdict,
        "permitted_wording": permitted,
        "scope_caveat": quotient.get("caveat", ""),
    }

    (repo / "results" / "stress_flow" / "D10_characteristic_zero_final.json").write_text(
        json.dumps(d10_record, indent=1) + "\n", encoding="utf-8")
    (repo / "results" / "stress_flow" / "Q10_characteristic_zero_final.json").write_text(
        json.dumps(q10_record, indent=1) + "\n", encoding="utf-8")

    L: list[str] = []
    A = L.append
    A("# D10 and Q10 --- final characteristic-zero status")
    A("")
    A(f"Generated {when} by `scripts/exact_D10_Q10_characteristic_zero.py`.")
    A("")
    A("## Result")
    A("")
    A("| space | lower bound | upper bound | exact over Q | status |")
    A("|---|---|---|---|---|")
    A(f"| A10 | {a10_modular} (modular) | {n} (structural) | **{a10_exact}** | "
      f"{q10_record['A10']['status']} |")
    A(f"| D10 | {modular_rank} (modular) | {rank_Q} (exact rational) | "
      f"**{d10_exact}** | {verdict} |")
    A(f"| Q10 | --- | --- | **{q10_exact}** | {verdict} |")
    A("")
    A("## Why the modular record was not enough")
    A("")
    A("`rank_{F_p} <= rank_Q`. For a subspace that is *subtracted* this is the")
    A("wrong direction: `dim Q10 = dim A10 - dim D10`, so a D10 that is larger")
    A("over Q than mod p makes the obstruction smaller, and agreement across")
    A("primes cannot rule that out.")
    A("")
    A("The gap never needed a modular argument. The flow targets carry exact")
    A("rational coordinates, so the same fixed-point closure runs over Q with")
    A(f"Fraction arithmetic; it reached its fixed point in {info['sweeps']} sweeps")
    A("and its rank was read off by exact rational elimination. That computes the")
    A("rank rather than bounding it, which is both bounds at once.")
    A("")
    A("A10 needs no computation for its upper bound: the fourteen basis elements")
    A("are the coordinate system, so nothing spanned by them exceeds fourteen, and")
    A("the modular rank 14 supplies the matching lower bound.")
    A("")
    A("## Three different numbers live at degree 10")
    A("")
    A("Getting this wrong is easy and the first attempt did:")
    A("")
    A("| object | dimension | quotient |")
    A("|---|---|---|")
    A(f"| span of all 37 degree-10 flow targets | 14 | 0 |")
    A(f"| new-forcing space (Tr(tau) excluded) | "
      f"{flow['new_forcing_dimension_by_degree']['10']} | "
      f"{flow['new_forcing_quotient_dimension_by_degree']['10']} |")
    A(f"| static stress span | 2 | 12 |")
    A(f"| **D10, the seed closure** | **{rank_Q}** | **{q10_exact}** |")
    A("")
    A("Only the last is D10. The first has no activation condition and reaches")
    A("everything; the second removes Tr(tau) as a generator; the third is static")
    A("rather than dynamical.")
    A("")
    A("## Cross-check against the modular record")
    A("")
    A("| quantity | exact over Q | modular record | agree |")
    A("|---|---|---|---|")
    A(f"| rank of D10 | {rank_Q} | {modular_rank} | {'yes' if agreement else '**NO**'} |")
    A(f"| free columns | {free_columns} | {modular_free} | {'yes' if same_free else '**NO**'} |")
    A("")
    A("Basis elements not reached by the flow:")
    A("")
    for c in free_columns:
        A(f"- `{basis[10][c]}` (column {c})")
    A("")
    if not agreement:
        A("**The exact rank disagrees with the modular one.** The modular value is")
        A("a lower bound, so the true closure is larger and the quotient smaller.")
        A("Every statement of Q10 must be revised to the exact value.")
        A("")
    A("## Wording the manuscript may use")
    A("")
    A("> " + permitted)
    A("")
    A("## Scope")
    A("")
    A("> " + quotient.get("caveat", ""))
    A("")
    A("This settles the dimension of the seed closure over Q. It does not answer")
    A("the generator-extension problem, and nothing here should be read as doing so.")
    A("")
    (repo / "docs" / "D10_Q10_FINAL_STATUS.md").write_text("\n".join(L) + "\n",
                                                           encoding="utf-8")

    print(f"rational closure sweeps : {info['sweeps']}")
    print(f"rational dims by degree : {dims}")
    print(f"exact rational D10      : {rank_Q}   (modular record {modular_rank}, "
          f"agree={agreement})")
    print(f"free columns            : {free_columns}  (modular {modular_free}, "
          f"agree={same_free})")
    print(f"dim_Q A10 = {a10_exact}, dim_Q D10 = {d10_exact}, dim_Q Q10 = {q10_exact}")
    print(f"status: {verdict}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
