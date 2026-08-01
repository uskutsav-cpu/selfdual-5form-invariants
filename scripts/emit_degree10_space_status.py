#!/usr/bin/env python3
"""Stage 7.1 and 7.4 --- what is exact over Q at degree 10, and what is not.

Four of the five degree-10 subspaces need no computation to pin down over Q,
and one of them does. Saying so precisely matters more than making them all
look equally settled, because the manuscript's wording has to follow the
weakest of them.

  A10, G10, P10   spans of DISTINCT STANDARD BASIS VECTORS in atlas
                  coordinates. A set of k distinct unit vectors has rank k over
                  any field, so their dimensions are structural: 14, 12, 2.
                  No prime is involved and none can be exceptional.

  D10             the seed closure, settled over Q separately by
                  scripts/exact_D10_Q10_characteristic_zero.py.

  B10             the span of the published equation-(4.24) candidates, each
                  recovered by solving a linear system against a design matrix
                  MOD P. There is no rational solve, so dim_Q B10 is bounded,
                  not known: >= 12 from the modular rank, <= 14 from A10.

The intersection B10 ∩ P10 inherits that: its modular value is 1, and over Q
only bounds follow.

Writes:
    results/stress_flow/degree10_spaces_final.json
    docs/DEGREE10_SPACES_FINAL_STATUS.md

Usage:
    python scripts/emit_degree10_space_status.py [--repo .]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

INCIDENCE = "results/intrinsic_candidates/degree10_space_incidence.json"
D10_FINAL = "results/stress_flow/D10_characteristic_zero_final.json"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".", type=Path)
    args = ap.parse_args()
    repo = args.repo.resolve()
    when = datetime.now(timezone.utc).isoformat(timespec="seconds")

    inc = json.loads((repo / INCIDENCE).read_text())
    d10 = json.loads((repo / D10_FINAL).read_text())
    per_prime = inc["per_prime"]
    primes = sorted(per_prime)
    dims = {p: per_prime[p]["dims"] for p in primes}

    # Consistency across primes is a precondition for saying anything at all.
    consistent = all(dims[p] == dims[primes[0]] for p in primes)
    base = dims[primes[0]]

    caps = {p: per_prime[p]["incidence"].get("P10|B10", {}).get("intersection")
            for p in primes}
    cap_consistent = len(set(caps.values())) == 1
    cap_value = caps[primes[0]]

    spaces = {
        "A10": {
            "description": "the full degree-10 atlas",
            "construction": "all 14 standard basis vectors in atlas coordinates",
            "modular_dimension": base["A10"],
            "exact_over_Q": 14,
            "route": ("structural: 14 distinct unit vectors have rank 14 over any "
                      "field, so no prime can be exceptional"),
            "status": "PROVED",
        },
        "G10": {
            "description": "the span of the twelve graph generators I10_1..I10_12",
            "construction": "12 distinct standard basis vectors",
            "modular_dimension": base["G10"],
            "exact_over_Q": 12,
            "route": "structural, as for A10",
            "status": "PROVED",
        },
        "P10": {
            "description": "the lower-product subspace I4_1*I6_1, I4_1*I6_2",
            "construction": "2 distinct standard basis vectors",
            "modular_dimension": base["P10"],
            "exact_over_Q": 2,
            "route": "structural, as for A10",
            "status": "PROVED",
        },
        "D10": {
            "description": "the seed closure of the generalized stress flow",
            "construction": "fixed-point closure over Q from the recorded seed",
            "modular_dimension": base["D10"],
            "exact_over_Q": d10["exact_characteristic_zero_dimension"],
            "route": ("exact rational closure and elimination; see "
                      "docs/D10_Q10_FINAL_STATUS.md"),
            "status": d10["status"],
        },
        "B10": {
            "description": "the span of the published equation-(4.24) candidates",
            "construction": ("each candidate recovered by an exact linear solve "
                             "against a design matrix MOD P; there is no rational "
                             "solve, so the coefficients themselves are only known "
                             "modularly"),
            "modular_dimension": base["B10"],
            "exact_over_Q": None,
            "lower_bound_over_Q": base["B10"],
            "lower_bound_route": "rank_{F_p} <= rank_Q",
            "upper_bound_over_Q": 14,
            "upper_bound_route": "B10 is a subspace of A10, which is 14-dimensional",
            "route": None,
            "status": "CERTIFIED AT THE TESTED PRIMES; NOT PROVED OVER Q",
            "what_would_close_it": (
                "a rational solve for the published candidates against the design "
                "matrix, which needs a rational evaluator for the atlas elements; "
                "the present evaluators are modular"),
        },
    }

    intersection = {
        "quantity": "dim(B10 ∩ P10)",
        "identity": "dim(B ∩ P) = dim B + dim P - dim(B + P)",
        "modular_value": cap_value,
        "consistent_across_primes": cap_consistent,
        "primes": [int(p) for p in primes],
        "exact_over_Q": None,
        "status": "CERTIFIED AT THE TESTED PRIMES; NOT PROVED OVER Q",
        "why": ("the identity needs all three dimensions over Q, and dim_Q B10 is "
                "itself only bounded, so the intersection inherits the gap"),
        "bounds_over_Q": {
            "dim_Q P10": 2,
            "dim_Q B10": f">= {base['B10']}, <= 14",
            "dim_Q (B10 + P10)": "<= 14",
            "conclusion": ("no exact value follows; the modular value 1 is what is "
                           "certified, at the tested primes"),
        },
    }

    record = {
        "generated_utc": when,
        "primes": [int(p) for p in primes],
        "dimensions_consistent_across_primes": consistent,
        "spaces": spaces,
        "intersection_B10_P10": intersection,
        "source_artifacts": {
            INCIDENCE: sha256_file(repo / INCIDENCE),
            D10_FINAL: sha256_file(repo / D10_FINAL),
        },
        "manuscript_consequence": (
            "A10, G10, P10 and D10 may be stated as exact characteristic-zero "
            "dimensions. B10 and B10 ∩ P10 must carry 'at the tested primes' "
            "wherever they appear."),
    }

    out = repo / "results" / "stress_flow" / "degree10_spaces_final.json"
    out.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")

    L: list[str] = []
    A = L.append
    A("# Degree-10 subspaces --- final status")
    A("")
    A(f"Generated {when} by `scripts/emit_degree10_space_status.py`.")
    A("")
    A("## Summary")
    A("")
    A("| space | modular | exact over Q | status |")
    A("|---|---|---|---|")
    for name, s in spaces.items():
        exact = s["exact_over_Q"]
        A(f"| {name} | {s['modular_dimension']} | "
          f"{exact if exact is not None else '**not established**'} | {s['status']} |")
    A(f"| B10 ∩ P10 | {cap_value} | **not established** | "
      f"{intersection['status']} |")
    A("")
    A("## Why three of these need no computation")
    A("")
    A("A10, G10 and P10 are spans of *distinct standard basis vectors* in atlas")
    A("coordinates --- all fourteen, the twelve graph generators, and the two lower")
    A("products respectively. A set of k distinct unit vectors has rank k over any")
    A("field. Their dimensions are therefore structural: no prime enters, and no")
    A("prime can be exceptional. Reporting them with a modular caveat would have")
    A("been a caveat about nothing.")
    A("")
    A("## Why B10 is different")
    A("")
    A("B10 is the span of the published equation-(4.24) candidates, and each")
    A("candidate's coordinate vector is *recovered* by solving a linear system")
    A("against a design matrix mod p. The coefficients are modular objects. There")
    A("is no rational solve, because the atlas evaluators are modular, so:")
    A("")
    A(f"- `dim_Q B10 >= {base['B10']}`, since rank over F_p bounds rank over Q from below")
    A("- `dim_Q B10 <= 14`, since B10 is a subspace of A10")
    A("")
    A("and nothing between them is established. Closing it needs a rational")
    A("evaluator for the atlas elements, which does not exist in this package.")
    A("")
    A("## The intersection")
    A("")
    A("`dim(B ∩ P) = dim B + dim P - dim(B + P)` needs all three dimensions over Q.")
    A(f"`dim_Q P10 = 2` exactly, but `dim_Q B10` is only bounded, so the")
    A(f"intersection inherits the gap. Its modular value is {cap_value}, consistent")
    A(f"across {len(primes)} primes, and that is what may be stated.")
    A("")
    A("## Consequence for the manuscript")
    A("")
    A("> " + record["manuscript_consequence"])
    A("")
    (repo / "docs" / "DEGREE10_SPACES_FINAL_STATUS.md").write_text(
        "\n".join(L) + "\n", encoding="utf-8")

    for name, s in spaces.items():
        print(f"{name:5s} modular {s['modular_dimension']:3d}  "
              f"exact {str(s['exact_over_Q']):>5s}  {s['status']}")
    print(f"B10∩P10 modular {cap_value}  exact None  {intersection['status']}")
    if not consistent:
        print("WARNING: dimensions differ between primes")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
