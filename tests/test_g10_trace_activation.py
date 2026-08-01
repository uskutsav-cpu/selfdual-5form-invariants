"""G-10: Tr(tau) begins at degree four, and the closure depends on it.

The proof is in ``docs/G10_FREE_STRESS_TENSOR_TRACE_PROOF.md``. These tests
guard the two things a proof on disk cannot guard by itself:

  * that the shipped flow artifact still agrees with the analytic formula
    Tr(tau)[V_d] = 10*(d-2)*V_d, coefficient by coefficient, and still has no
    degree-2 target;
  * that if a quadratic trace contribution WERE present, the closure would
    notice. A rule nothing can violate is not being enforced.

The second is the counterfactual required by Phase 3.6. It is the same shape
as the mistake that once produced rank 14 and quotient 0: a wrong activation
semantics that nothing objected to.
"""

from __future__ import annotations

import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from verify_D10_independent import (  # noqa: E402
    SEED, activated_closure, integer_rank, raw_target_span,
)

FLOW = ROOT / "results" / "stress_flow" / "interacting_flow_equations.json"
G10_JSON = ROOT / "results" / "stress_flow" / "g10_trace_verification.json"

EXPECTED_CLOSURE_RANK = 11
EXPECTED_RAW_SPAN_RANK = 14
AMBIENT_A10 = 14
EXPECTED_Q10 = 3


@pytest.fixture(scope="module")
def targets() -> list[dict]:
    return json.loads(FLOW.read_text())["targets"]


# --------------------------------------------------------------------------
# the analytic formula, checked against the shipped artifact
# --------------------------------------------------------------------------
def test_tr_tau_coefficient_is_the_euler_factor(targets):
    """Every tr_tau coefficient equals 10*(d-2), from Tr(tau)[V_d]=10(d-2)V_d."""
    checked = 0
    for t in targets:
        if t["generator"] != "tr_tau":
            continue
        d = t["field_degree"]
        expected = 10 * (d - 2)
        nonzero = [c for c in t["coordinates"] if int(c["numerator"]) != 0]
        assert len(nonzero) == 1, (
            f"{t['id']}: a tr_tau target should hit exactly one basis direction"
        )
        c = nonzero[0]
        assert int(c["denominator"]) == 1, f"{t['id']}: unexpected denominator"
        assert int(c["numerator"]) == expected, (
            f"{t['id']}: coefficient {c['numerator']} != 10*(d-2) = {expected}"
        )
        checked += 1
    assert checked > 0, "no tr_tau targets found -- artifact shape changed"


def test_tr_tau_has_no_quadratic_target(targets):
    """The whole content of G-10: nothing in the tr_tau family at degree 2."""
    degrees = {t["field_degree"] for t in targets if t["generator"] == "tr_tau"}
    assert 2 not in degrees, (
        "a degree-2 tr_tau target exists; G-10 is violated and dim Q10 is not 3"
    )
    assert min(degrees) == 4, f"tr_tau starts at degree {min(degrees)}, expected 4"


def test_euler_factor_vanishes_exactly_at_degree_two():
    """10*(d-2) is zero at d=2 and nonzero at d=4. Both halves matter."""
    assert 10 * (2 - 2) == 0
    assert 10 * (4 - 2) != 0


# --------------------------------------------------------------------------
# baseline
# --------------------------------------------------------------------------
@pytest.fixture(scope="module")
def baseline(targets):
    dims, info = activated_closure(targets, SEED)
    return dims, info


def test_baseline_closure_is_eleven_and_quotient_is_three(baseline):
    dims, _ = baseline
    assert dims[10] == EXPECTED_CLOSURE_RANK
    assert AMBIENT_A10 - dims[10] == EXPECTED_Q10


def test_raw_span_is_fourteen_and_is_not_the_closure(targets):
    """The permanent negative fixture: raw span 14 is NOT D10."""
    assert raw_target_span(targets, 10) == EXPECTED_RAW_SPAN_RANK
    assert raw_target_span(targets, 10) != EXPECTED_CLOSURE_RANK


# --------------------------------------------------------------------------
# Phase 3.6 -- the counterfactual
# --------------------------------------------------------------------------
def _with_quadratic_trace(targets: list[dict]) -> list[dict]:
    """Fabricate the degree-2 trace contribution that G-10 rules out.

    If Tr(tau) began at degree two, the degree-4 tr_tau target would no longer
    need a degree-4 direction to already be reachable -- a quadratic trace is
    unconditional, so its coefficient monomial is empty and it activates
    immediately. That is the mutation: strip the activation dependency from the
    tr_tau family, exactly as a nonvanishing 10*(2-2) would have done.
    """
    out = deepcopy(targets)
    for t in out:
        if t["generator"] == "tr_tau":
            t["coefficient_monomial"] = []
    return out


def test_counterfactual_quadratic_trace_changes_the_closure(targets, baseline):
    """If Tr(tau) had a quadratic part, the answer would move. It must."""
    base_dims, _ = baseline
    mutated_dims, _ = activated_closure(_with_quadratic_trace(targets), SEED)

    assert mutated_dims[10] != base_dims[10], (
        "inserting a quadratic trace contribution left dim D10 at "
        f"{base_dims[10]}. The closure is not enforcing the activation rule, "
        "so G-10 is not load-bearing and the quotient is not trustworthy."
    )
    # Record the direction of the effect: more is reachable, so the quotient
    # shrinks. This is the collapse G-10 prevents.
    assert mutated_dims[10] > base_dims[10]
    mutated_q10 = AMBIENT_A10 - mutated_dims[10]
    assert mutated_q10 < EXPECTED_Q10


def test_counterfactual_effect_is_reported_not_just_asserted(targets, baseline):
    """The mutation's effect on dim D10 and dim Q10 is a recorded number."""
    base_dims, _ = baseline
    mutated_dims, _ = activated_closure(_with_quadratic_trace(targets), SEED)
    effect = {
        "dim_D10_baseline": base_dims[10],
        "dim_D10_with_quadratic_trace": mutated_dims[10],
        "dim_Q10_baseline": AMBIENT_A10 - base_dims[10],
        "dim_Q10_with_quadratic_trace": AMBIENT_A10 - mutated_dims[10],
    }
    assert effect["dim_Q10_baseline"] == EXPECTED_Q10
    assert effect["dim_D10_with_quadratic_trace"] >= effect["dim_D10_baseline"] + 1
    print("G-10 counterfactual effect:", json.dumps(effect, sort_keys=True))


# --------------------------------------------------------------------------
# the independent verifier must actually run and actually pass
# --------------------------------------------------------------------------
def test_independent_verifier_runs_clean():
    """Phase 3.4: rerun it here rather than trusting a stored JSON."""
    proc = subprocess.run(
        [sys.executable, "scripts/verify_g10_trace_independent.py"],
        cwd=ROOT, capture_output=True, text=True, timeout=300,
    )
    assert proc.returncode == 0, f"verifier failed:\n{proc.stdout}\n{proc.stderr}"

    data = json.loads(G10_JSON.read_text())
    s = data["summary"]
    assert s["all_traces_vanish"] is True
    assert s["n_failures"] == 0
    assert s["samples_tested"] >= 100
    assert s["trace_starting_degree_of_Tr_tau"] == 4
    assert data["imports_production_code"] is False


def test_real_self_duality_only_where_star_squared_is_plus_one():
    """Lorentzian and split admit real self-dual 5-forms; Euclidean does not."""
    data = json.loads(G10_JSON.read_text())
    sq = data["star_squared"]
    for key, value in sq.items():
        if key.startswith("euclidean"):
            assert value == -1, f"{key}: expected **=-1 in Euclidean signature"
        else:
            assert value == 1, f"{key}: expected **=+1"
