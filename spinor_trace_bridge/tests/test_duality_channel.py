"""The bridge must not assume which Hodge channel it carries.

The frame congruence between the split (5,5) oscillator metric and the
Lorentzian (1,9) metric is solved mod p, and that solution is not unique.
Distinct solutions can differ by an orientation reversal, which flips the sign
of the Hodge star and exchanges its eigenspaces.

At p = 32707 the solver returns an orientation-reversing congruence. Before the
fix, the left inverse assumed the self-dual channel and raised "image has
dimension 0, not 126" there. Four of five primes worked, which is why the
validation suite -- which exercises two of them -- never noticed.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from sdbridge.bridge import BridgeMap          # noqa: E402
from sdbridge import conventions as C          # noqa: E402
from sdbridge.modular import matmul, rank      # noqa: E402

MATRIX_PRIMES = (32749, 32719, 32717, 32713, 32693)
REVERSED_PRIME = 32707


@pytest.mark.parametrize("p", MATRIX_PRIMES)
def test_matrix_primes_are_orientation_preserving(p):
    """Every prime the certificate matrix used carries the self-dual channel.

    If this ever fails, the matrix cells were computed against a different
    convention than the one the manuscript describes.
    """
    b = BridgeMap(p)
    assert b.duality_channel == "selfdual"
    assert b.orientation_reversed is False


def test_32707_is_orientation_reversed():
    """The prime that exposed the assumption, kept as a fixture."""
    b = BridgeMap(REVERSED_PRIME)
    assert b.duality_channel == "antiselfdual"
    assert b.orientation_reversed is True


@pytest.mark.parametrize("p", MATRIX_PRIMES + (REVERSED_PRIME,))
def test_exactly_one_channel_is_faithful(p):
    """One Hodge eigenspace maps isomorphically, the other dies. Never both,
    never neither -- that is what makes the bridge a bridge."""
    b = BridgeMap(p)
    sd = rank(matmul(b.selfdual_basis, b.forward_matrix, p), p)
    asd = rank(matmul(b.antiselfdual_basis, b.forward_matrix, p), p)
    assert sorted((sd, asd)) == [0, C.N_SELFDUAL_COMPONENTS], (
        f"p={p}: self-dual image {sd}, anti-self-dual image {asd}")


@pytest.mark.parametrize("p", MATRIX_PRIMES + (REVERSED_PRIME,))
def test_left_inverse_exists_at_every_prime(p):
    """Including the reversed one. This is what the fix bought."""
    b = BridgeMap(p)
    sel, M = b.left_inverse
    assert len(sel) == C.N_SELFDUAL_COMPONENTS
    assert M.shape[0] == C.N_SELFDUAL_COMPONENTS


def test_the_channel_is_detected_not_assumed():
    """A guard against the fix being quietly reverted.

    `faithful_basis` must follow `duality_channel`. If someone hard-codes the
    self-dual basis again, 32707 breaks and this catches it before the holdout
    cells do.
    """
    good = BridgeMap(MATRIX_PRIMES[0])
    bad = BridgeMap(REVERSED_PRIME)
    assert good.faithful_basis is good.selfdual_basis
    assert bad.faithful_basis is bad.antiselfdual_basis


def test_no_prime_class_claim_is_encoded():
    """32707 is 3 mod 8, and that is an observation about one prime.

    A single failing prime does not establish a congruence class. Nothing in
    the code may branch on p mod 8, because the mechanism is an orientation
    branch in a congruence solve and no argument has been given tying it to a
    residue class. The channel is detected per prime instead.
    """
    src = (Path(__file__).resolve().parents[1] / "src" / "sdbridge"
           / "bridge.py").read_text()
    assert "% 8" not in src and "mod 8" not in src.replace("mod 8;", ""), (
        "bridge.py must not branch on a residue class it has not justified")
