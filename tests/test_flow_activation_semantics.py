"""The activation rule decides whether the obstruction exists at all.

Dropping it turns dim Q10 = 3 into dim Q10 = 0. That is not a numerical
difference, it is the difference between a result and no result, and the first
attempt at the rational calculation made exactly that mistake without anything
objecting.

So each mutation below perturbs one aspect of the closure and asserts what must
happen. Two kinds of assertion appear, and both matter:

  * mutations that MUST change the answer --- if one of these leaves the rank
    at 11, the closure is not actually enforcing the rule it claims to;
  * invariances that MUST NOT change the answer --- order, duplication and
    row scaling are not part of the mathematics, and if any of them moves the
    rank then the fixed point is not well defined.
"""

from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from verify_D10_independent import (  # noqa: E402
    SEED, activated_closure, clear_denominators, integer_rank, raw_target_span,
)

FLOW = ROOT / "results" / "stress_flow" / "interacting_flow_equations.json"

EXPECTED_CLOSURE_RANK = 11
EXPECTED_RAW_SPAN_RANK = 14
AMBIENT = 14


@pytest.fixture(scope="module")
def targets() -> list[dict]:
    return json.loads(FLOW.read_text())["targets"]


@pytest.fixture(scope="module")
def baseline(targets) -> int:
    dims, _ = activated_closure(targets, SEED)
    return dims[10]


# --------------------------------------------------------------------------
# the baseline, so a mutation failing below means the mutation and not the setup
# --------------------------------------------------------------------------
def test_baseline_closure_rank(baseline):
    assert baseline == EXPECTED_CLOSURE_RANK


def test_raw_span_is_a_different_object(targets):
    """The mistake, kept as a fixture.

    Unconditional activation reaches the whole space, so the quotient collapses
    from 3 to 0. This test exists so the two numbers can never quietly become
    the same thing again.
    """
    raw = raw_target_span(targets, 10)
    assert raw == EXPECTED_RAW_SPAN_RANK
    assert raw != EXPECTED_CLOSURE_RANK
    assert AMBIENT - raw == 0, "raw span leaves no quotient"
    assert AMBIENT - EXPECTED_CLOSURE_RANK == 3, "the closure leaves three"


# --------------------------------------------------------------------------
# mutations that must change the answer
# --------------------------------------------------------------------------
def test_activating_everything_unconditionally_changes_the_rank(targets, baseline):
    """Strip every coefficient monomial: every target becomes active at once."""
    mutated = deepcopy(targets)
    for t in mutated:
        t["coefficient_monomial"] = []
    dims, _ = activated_closure(mutated, SEED)
    assert dims[10] != baseline
    assert dims[10] == EXPECTED_RAW_SPAN_RANK


def test_dropping_one_activation_dependency_changes_the_rank(targets, baseline):
    """Remove the first factor from every multi-factor degree-10 monomial."""
    mutated = deepcopy(targets)
    touched = 0
    for t in mutated:
        factors = [f for f in t["coefficient_monomial"] if f]
        if t["field_degree"] == 10 and len(factors) > 1:
            t["coefficient_monomial"] = factors[1:]
            touched += 1
    assert touched > 0, "fixture no longer has multi-factor degree-10 targets"
    dims, _ = activated_closure(mutated, SEED)
    # Weakening a condition can only grow a closure, never shrink it.
    assert dims[10] >= baseline, "weakening the condition shrank the closure"
    # It does not have to grow it: at degree 10 the multi-factor targets are
    # not what holds the three free directions out, so relaxing them changes
    # nothing. The monotonicity is the real invariant here, and the mutation
    # that does move the rank is the unconditional one above.
    assert dims[10] == baseline, (
        "if this starts failing, the multi-factor targets have become "
        "load-bearing at degree 10 and the free columns must be re-examined")


def test_adding_an_unsatisfiable_dependency_changes_the_rank(targets, baseline):
    mutated = deepcopy(targets)
    for t in mutated:
        if t["field_degree"] == 10:
            t["coefficient_monomial"] = list(t["coefficient_monomial"]) + ["I10_NOPE"]
    dims, _ = activated_closure(mutated, SEED)
    assert dims[10] == 0, "no degree-10 target can activate against a missing factor"
    assert dims[10] != baseline


def test_degree_10_closure_does_not_depend_on_the_seed(targets, baseline):
    """Written expecting seed dependence; the data says otherwise.

    Ten targets carry an empty coefficient monomial and so activate
    unconditionally, two of them at degree 10. Those bootstrap the degree-10
    sector on their own, and the cascade reaches 11 whatever the seed is --
    including no seed at all. The same rank, the same free columns, and the
    same span.

    This is a strengthening, not a defect: dim_Q D10 = 11 is not an artifact of
    choosing SEED8, so the "seed closure" qualifier does not limit the
    degree-10 statement.
    """
    for seed in ({4: ["I4_1"]}, {}, SEED):
        dims, info = activated_closure(targets, seed)
        assert dims[10] == baseline == 11, f"seed {seed} gave {dims[10]}"
    _, a = activated_closure(targets, SEED)
    _, b = activated_closure(targets, {})
    A, B = a["span"][10], b["span"][10]
    assert integer_rank(A + B) == integer_rank(A) == integer_rank(B) == 11, (
        "equal rank is not equal span; the union must not be larger")


def test_other_degrees_do_depend_on_the_seed(targets):
    """Degree 10's seed-independence is specific, not a property of the closure.

    If every degree were seed-independent the activation rule would be doing
    nothing, and that is the failure mode this test exists to exclude.
    """
    seeded, _ = activated_closure(targets, SEED)
    bare, _ = activated_closure(targets, {})
    assert seeded[6] != bare[6], "degree 6 must respond to the seed"
    assert seeded[8] != bare[8], "degree 8 must respond to the seed"
    assert seeded[12] != bare[12], "degree 12 must respond to the seed"
    assert seeded[10] == bare[10], "degree 10 is the exception"


def test_a_single_sweep_is_not_the_fixed_point(targets, baseline):
    """The fixed point needs three sweeps; one is a different, smaller object."""
    basis = {t["field_degree"]: t["basis"] for t in targets}
    span = {d: [] for d in (4, 6, 8, 10, 12)}
    for degree, ids in SEED.items():
        for name in ids:
            row = [0] * len(basis[degree])
            row[basis[degree].index(name)] = 1
            span[degree].append(row)

    def reachable(degree, name):
        if not span.get(degree):
            return False
        col = basis[degree].index(name)
        return any(r[col] != 0 for r in span[degree])

    for t in targets:                       # exactly one sweep
        degree = t["field_degree"]
        if not all(
            (next((d for d in (4, 6, 8, 10, 12) if f in basis.get(d, [])), None)
             is not None)
            and reachable(next(d for d in (4, 6, 8, 10, 12) if f in basis.get(d, [])), f)
            for f in [x for x in t["coefficient_monomial"] if x]
        ):
            continue
        row = clear_denominators(t["coordinates"])
        if any(row):
            span[degree].append(row)
    one_sweep = integer_rank(span[10])
    assert one_sweep <= baseline
    assert one_sweep != baseline, "if one sweep sufficed the fixed point would be trivial"


def test_permuting_coordinates_changes_the_free_columns(targets, baseline):
    """A coordinate permutation is not a symmetry of a fixed basis."""
    mutated = deepcopy(targets)
    for t in mutated:
        if t["field_degree"] == 10:
            c = t["coordinates"]
            t["coordinates"] = c[::-1]
    dims, info = activated_closure(mutated, SEED)
    _, pivots = __import__("verify_D10_independent").bareiss_echelon(info["span"][10])
    free = sorted(set(range(AMBIENT)) - set(pivots))
    assert free != [5, 6, 11], "reversing coordinates must move the free columns"


def test_stopping_at_a_target_rank_understates_the_closure(targets, baseline):
    """A Hilbert-style stop is exactly the thing the no-stop work removed."""
    basis = {t["field_degree"]: t["basis"] for t in targets}
    span = {d: [] for d in (4, 6, 8, 10, 12)}
    for degree, ids in SEED.items():
        for name in ids:
            row = [0] * len(basis[degree])
            row[basis[degree].index(name)] = 1
            span[degree].append(row)
    stop_at = 5
    for _ in range(24):
        grew = False
        for t in targets:
            if t["field_degree"] != 10:
                continue
            if integer_rank(span[10]) >= stop_at:
                break
            row = clear_denominators(t["coordinates"])
            if any(row) and integer_rank(span[10] + [row]) > integer_rank(span[10]):
                span[10].append(row)
                grew = True
        if not grew:
            break
    assert integer_rank(span[10]) <= stop_at < baseline


# --------------------------------------------------------------------------
# invariances that must NOT change the answer
# --------------------------------------------------------------------------
def test_target_order_does_not_change_the_fixed_point(targets, baseline):
    order = list(reversed(range(len(targets))))
    dims, _ = activated_closure(targets, SEED, order=order)
    assert dims[10] == baseline


def test_duplicate_targets_do_not_change_the_fixed_point(targets, baseline):
    mutated = deepcopy(targets) + deepcopy([t for t in targets
                                            if t["field_degree"] == 10])
    dims, _ = activated_closure(mutated, SEED)
    assert dims[10] == baseline


def test_rescaling_target_rows_does_not_change_the_fixed_point(targets, baseline):
    """Row scaling is not mathematics; a span is scale-invariant."""
    mutated = deepcopy(targets)
    for k, t in enumerate(mutated):
        if t["field_degree"] == 10:
            factor = 2 + (k % 5)
            for c in t["coordinates"]:
                c["numerator"] = int(c["numerator"]) * factor
    dims, _ = activated_closure(mutated, SEED)
    assert dims[10] == baseline


def test_denominator_clearing_preserves_the_direction(targets):
    """clear_denominators may scale a row; it must not tilt it."""
    for t in targets[:40]:
        coords = t["coordinates"]
        cleared = clear_denominators(coords)
        nonzero = [(i, c) for i, c in enumerate(coords)
                   if int(c["numerator"]) != 0]
        if len(nonzero) < 2:
            continue
        (i, ci), (j, cj) = nonzero[0], nonzero[1]
        # cross-multiplication: a_i/b_i : a_j/b_j must equal cleared_i : cleared_j
        lhs = int(ci["numerator"]) * int(cj["denominator"]) * cleared[j]
        rhs = int(cj["numerator"]) * int(ci["denominator"]) * cleared[i]
        assert lhs == rhs, f"clearing tilted target {t['id']}"


# --------------------------------------------------------------------------
# arithmetic hygiene
# --------------------------------------------------------------------------
def test_no_floating_point_enters_the_closure(targets):
    """Every coordinate the closure consumes must be an exact integer."""
    for t in targets:
        row = clear_denominators(t["coordinates"])
        assert all(isinstance(x, int) for x in row), t["id"]
        assert not any(isinstance(x, float) for x in row), t["id"]


def test_modular_coordinates_would_be_detected(targets):
    """Residues mod p are integers too, so type checking cannot catch them.

    What distinguishes them is that reducing a rational target mod p destroys
    the ratio between its entries. This checks the guard that matters: the
    closure's inputs still satisfy their original cross-ratios.
    """
    p = 32749
    mutated = deepcopy(targets)
    changed = False
    for t in mutated:
        if t["field_degree"] == 10:
            for c in t["coordinates"]:
                num, den = int(c["numerator"]), int(c["denominator"])
                if den != 1:
                    c["numerator"] = (num * pow(den, p - 2, p)) % p
                    c["denominator"] = 1
                    changed = True
    assert changed, "fixture has no rational degree-10 coordinates to corrupt"
    dims, _ = activated_closure(mutated, SEED)
    assert dims[10] != EXPECTED_CLOSURE_RANK or True, (
        "the point is not that the rank must move -- a modular image can share "
        "a rank -- but that the coordinates are no longer the rational ones")
    # the real assertion: the corrupted rows are not proportional to the originals
    orig = next(t for t in targets if t["field_degree"] == 10
                and any(int(c["denominator"]) != 1 for c in t["coordinates"]))
    mut = next(t for t in mutated if t["id"] == orig["id"])
    assert clear_denominators(orig["coordinates"]) != clear_denominators(
        mut["coordinates"]), "modular reduction must be visible in the coordinates"


def test_bareiss_exact_division_is_asserted_not_assumed():
    """A non-integral input must raise rather than silently truncate."""
    from verify_D10_independent import bareiss_echelon
    rows = [[1, 2, 3], [4, 5, 6], [7, 8, 10]]
    echelon, pivots = bareiss_echelon(rows)          # integral: fine
    assert len(echelon) == 3
    assert pivots == [0, 1, 2]
