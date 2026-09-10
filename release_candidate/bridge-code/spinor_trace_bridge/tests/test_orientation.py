"""The frame orientation must be pinned, not left to the square-root branch.

Three rank-matrix cells failed at p = 32707 with "image has dimension 0, not
126". The prime is not exceptional: the congruence that builds the null frame is
fixed only up to a square-root branch, that branch reverses the frame's
orientation, and the orientation reverses the sign of the Hodge star -- which
swaps which eigenspace the gamma map annihilates.

Flipping the branch breaks a working prime in exactly the same way, which is what
established that the cause is the choice and not the prime.
"""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sdbridge import conventions as C          # noqa: E402
from sdbridge.bridge import BridgeMap          # noqa: E402
from sdbridge.modular import matmul, rank      # noqa: E402
from sdbridge.signature import (                # noqa: E402
    TransitionFrame, _raw_L, orientation_normalised_L,
)

PRIMES = [32749, 32719, 32717, 32713, 32707, 32693]


@pytest.mark.parametrize("p", PRIMES)
def test_self_dual_space_survives_at_every_prime(p):
    """The convention the package states must hold at every prime, 32707 included."""
    b = BridgeMap(p)
    surviving = rank(matmul(b.selfdual_basis, b.forward_matrix, p), p)
    killed = rank(matmul(b.antiselfdual_basis, b.forward_matrix, p), p)
    assert surviving == C.N_SELFDUAL_COMPONENTS, (
        f"p={p}: the forward map does not inject the self-dual space "
        f"(rank {surviving}); the frame orientation is not normalised")
    assert killed == 0, (
        f"p={p}: the forward map does not annihilate the anti-self-dual space "
        f"(rank {killed})")


@pytest.mark.parametrize("p", PRIMES)
def test_left_inverse_exists_at_every_prime(p):
    sel, _ = BridgeMap(p).left_inverse
    assert len(sel) == C.N_SELFDUAL_COMPONENTS


@pytest.mark.parametrize("p", [32707, 32749])
def test_the_other_branch_breaks_it(p):
    """The diagnosis, as a test: the wrong branch swaps the eigenspaces.

    Without this, a future refactor could drop the normalisation and the suite
    would still pass at five of six primes.
    """
    good = orientation_normalised_L(p)
    other = _raw_L(p, flip=True) if (good == _raw_L(p, flip=False)).all() \
        else _raw_L(p, flip=False)
    b = BridgeMap(p, _frame_override=TransitionFrame(p=p, _L_override=other))
    surviving = rank(matmul(b.selfdual_basis, b.forward_matrix, p), p)
    assert surviving == 0, (
        f"p={p}: the opposite square-root branch was expected to annihilate the "
        f"self-dual space, but it has rank {surviving}. If this changes, the "
        f"orientation argument in signature.py needs revisiting")
