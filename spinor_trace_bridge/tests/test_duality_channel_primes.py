"""The duality channel the bridge preserves depends on p mod 8.

See docs/EXCEPTIONAL_PRIMES_DUALITY_CHANNEL.md. Three rank-81 holdout cells at
p=32707 failed with "image has dimension 0, not 126"; the cause is that for
p = 3 (mod 8) the forward map annihilates the subspace the code calls self-dual
and is injective on the anti-self-dual one.

These tests pin three things:

  * the channel assignment itself, so a change to the Clifford or null-frame
    construction cannot move it without failing here;
  * that the failure stays LOUD -- inverse() must raise rather than fall back
    to whichever channel happens to have rank 126, because a silent fallback
    would let one certificate mix two conventions;
  * that every prime the rank-81 matrix actually uses is on the intended side.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from sdbridge.bridge import BridgeMap
from sdbridge.modular import matmul, rank

N_SELFDUAL = 126

GOOD = [32713, 32749, 32717, 32719, 32693]   # 1, 5, 7 mod 8
FLIPPED = [32707, 32771]                      # 3 mod 8

DRIVER = (Path(__file__).resolve().parents[1] / "scripts"
          / "run_rank81_matrix.sh")


@pytest.mark.parametrize("p", GOOD)
def test_intended_channel_is_preserved(p):
    """For p != 3 (mod 8) the forward map is injective on the self-dual space."""
    assert p % 8 != 3, "fixture error: this prime is in the flipped class"
    b = BridgeMap(p)
    assert rank(matmul(b.selfdual_basis, b.forward_matrix, p), p) == N_SELFDUAL
    assert rank(matmul(b.antiselfdual_basis, b.forward_matrix, p), p) == 0


@pytest.mark.parametrize("p", FLIPPED)
def test_channel_inverts_at_three_mod_eight(p):
    """For p = 3 (mod 8) the two channels are exchanged."""
    assert p % 8 == 3, "fixture error: this prime is not in the flipped class"
    b = BridgeMap(p)
    assert rank(matmul(b.selfdual_basis, b.forward_matrix, p), p) == 0
    assert rank(matmul(b.antiselfdual_basis, b.forward_matrix, p), p) == N_SELFDUAL


def test_p_mod_4_does_not_separate_the_cases():
    """32719 and 32707 are both 3 mod 4 and behave differently.

    Guards against anyone 'simplifying' the rule to p mod 4, which would admit
    32707 and reintroduce the failure.
    """
    assert 32719 % 4 == 32707 % 4 == 3
    assert 32719 % 8 != 32707 % 8
    b_ok, b_bad = BridgeMap(32719), BridgeMap(32707)
    assert rank(matmul(b_ok.selfdual_basis, b_ok.forward_matrix, 32719), 32719) == N_SELFDUAL
    assert rank(matmul(b_bad.selfdual_basis, b_bad.forward_matrix, 32707), 32707) == 0


@pytest.mark.parametrize("p", FLIPPED)
def test_failure_is_loud_not_a_silent_fallback(p):
    """inverse() must raise. A fallback would silently mix conventions."""
    b = BridgeMap(p)
    with pytest.raises(RuntimeError, match=r"image has dimension 0, not 126"):
        _ = b.left_inverse


def test_matrix_driver_uses_no_flipped_prime():
    """Every prime in the rank-81 driver must be on the intended channel."""
    text = DRIVER.read_text()
    primes = []
    for line in text.splitlines():
        m = re.match(r'\s*(FITTING|HOLDOUT)="([0-9 ]+)"', line)
        if m:
            primes.extend(int(x) for x in m.group(2).split())
    assert primes, "could not parse primes out of the driver script"
    flipped = [p for p in primes if p % 8 == 3]
    assert not flipped, (
        f"driver uses primes congruent to 3 mod 8: {flipped}. Their cells "
        "cannot complete; see docs/EXCEPTIONAL_PRIMES_DUALITY_CHANNEL.md"
    )
