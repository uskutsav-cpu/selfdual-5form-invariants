"""The duality channel is pinned by construction, and does NOT depend on p mod 8.

This file used to assert the opposite, and the history is worth keeping because
the wrong version was reasonable on the evidence available.

Three rank-81 holdout cells at p=32707 failed with "image has dimension 0, not
126". 32707 is 3 mod 8; so is 32771, which failed the same way; none of the
working primes were. On two examples that looks like a congruence condition,
and the file that stood here encoded it as one, excluded both primes, and
required the failure to stay loud.

The real cause is elsewhere. The frame congruence is solved via a modular
square root, which has two values differing by an orientation reversal;
orientation flips the Hodge star, which exchanges the eigenspace the gamma map
annihilates. `signature.orientation_normalised_L` now picks the branch under
which the self-dual space survives.

With that pinned, **32633 --- which is 1 mod 8 --- needs the same reversed
branch as 32707 and 32771**. A prime outside the suspected class requires the
identical correction, so the residue class was never the mechanism. Every class
works, no prime is excluded, and 32707 is back in the holdout set.

What these tests pin now:

  * every prime lands on the self-dual channel, across all four usable classes;
  * the branch a prime needs is not a function of p mod 8, evidenced by 32633;
  * a DELIBERATELY reversed frame still raises loudly, because the protection
    against silently mixing conventions is still wanted --- it just no longer
    fires during ordinary construction;
  * the matrix driver uses 32707, and would fail if it were dropped again.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from sdbridge import conventions as C
from sdbridge import signature as sig
from sdbridge.bridge import BridgeMap
from sdbridge.modular import matmul, rank

N_SELFDUAL = C.N_SELFDUAL_COMPONENTS

# All four usable residue classes mod 8.
ALL_PRIMES = [32633, 32647, 32653, 32687, 32693, 32707, 32713, 32717, 32719,
              32749, 32771]

# The primes that need the reversed square-root branch. Note the classes:
# 1, 3 and 3. This list is the refutation of the mod-8 rule.
NEED_REVERSED_BRANCH = [32633, 32707, 32771]

DRIVER = (Path(__file__).resolve().parents[1] / "scripts"
          / "run_rank81_matrix.sh")


def channel(p: int) -> str:
    b = BridgeMap(p)
    sd = rank(matmul(b.selfdual_basis, b.forward_matrix, p), p)
    asd = rank(matmul(b.antiselfdual_basis, b.forward_matrix, p), p)
    if sd == N_SELFDUAL and asd == 0:
        return "selfdual"
    if asd == N_SELFDUAL and sd == 0:
        return "antiselfdual"
    return f"neither(sd={sd},asd={asd})"


@pytest.mark.parametrize("p", ALL_PRIMES)
def test_every_prime_is_on_the_selfdual_channel(p):
    """No prime is exceptional once the orientation is pinned."""
    assert channel(p) == "selfdual"


@pytest.mark.parametrize("p", ALL_PRIMES)
def test_left_inverse_exists_at_every_prime(p):
    sel, _ = BridgeMap(p).left_inverse
    assert len(sel) == N_SELFDUAL


def test_the_branch_needed_is_not_a_function_of_p_mod_8():
    """The refutation, as a test rather than as a comment.

    If the branch requirement tracked the residue class, every prime needing
    the reversed branch would share one class. 32633 is 1 mod 8 and 32707 is
    3 mod 8, and both need it.
    """
    classes = {p % 8 for p in NEED_REVERSED_BRANCH}
    assert len(classes) > 1, (
        f"all reversed-branch primes are in class {classes}; if that ever "
        "becomes true again the mod-8 hypothesis deserves another look")
    assert 32633 % 8 == 1 and 32707 % 8 == 3


@pytest.mark.parametrize("p", NEED_REVERSED_BRANCH)
def test_reversed_branch_primes_still_end_up_selfdual(p):
    """These are the primes the old code could not handle. They are ordinary now."""
    assert channel(p) == "selfdual"
    sel, _ = BridgeMap(p).left_inverse
    assert len(sel) == N_SELFDUAL


@pytest.mark.parametrize("p", [32707, 32771, 32633])
def test_the_unpinned_branch_would_have_inverted(p):
    """The bug, preserved as a fixture.

    Taking the branch production does NOT choose puts these primes on the
    anti-self-dual channel. That is what used to happen, and it is why the
    left inverse reported an image of dimension zero.
    """
    wrong = sig._raw_L(p, not _production_used_flip(p))
    b = BridgeMap(p, _frame_override=sig.TransitionFrame(p=p, _L_override=wrong))
    sd = rank(matmul(b.selfdual_basis, b.forward_matrix, p), p)
    assert sd == 0, f"p={p}: the other branch should annihilate the self-dual space"


def _production_used_flip(p: int) -> bool:
    import numpy as np
    L = np.asarray(BridgeMap(p).frame.L) % p
    return not np.array_equal(L, np.asarray(sig._raw_L(p, False)) % p)


@pytest.mark.parametrize("p", [32707, 32771])
def test_failure_is_loud_not_a_silent_fallback(p):
    """Still required, just no longer reachable by ordinary construction.

    A bridge that quietly switched channel would let two cells be evaluated
    against different conventions. Ordinary construction can no longer land on
    a reversed frame, but if one is forced, it must raise rather than adapt.
    """
    wrong = sig._raw_L(p, not _production_used_flip(p))
    b = BridgeMap(p, _frame_override=sig.TransitionFrame(p=p, _L_override=wrong))
    with pytest.raises(RuntimeError, match="image has dimension 0"):
        _ = b.left_inverse


def test_matrix_driver_uses_32707():
    """The exclusion is reversed, and the driver must reflect it.

    32707 was dropped while the wrong diagnosis stood. It is a holdout prime
    again, and 32693 --- which briefly replaced it --- is an extra.
    """
    text = DRIVER.read_text()
    primes: list[int] = []
    for line in text.splitlines():
        m = re.match(r'\s*(FITTING|HOLDOUT|EXTRA)="([0-9 ]+)"', line)
        if m:
            primes.extend(int(x) for x in m.group(2).split())
    assert primes, "could not parse primes out of the driver script"
    assert 32707 in primes, "32707 must not be excluded again"
    assert 32693 in primes, "32693 is retained as an extra validation prime"


def test_driver_does_not_encode_a_residue_rule():
    """No prime-exclusion law may reappear in the driver."""
    text = DRIVER.read_text().lower()
    for banned in ("% 8", "mod 8 exclusion", "must be non-congruent"):
        assert banned not in text, f"driver encodes a residue rule: {banned!r}"


def test_no_source_file_branches_on_p_mod_8():
    src = (Path(__file__).resolve().parents[1] / "src" / "sdbridge")
    for f in src.glob("*.py"):
        body = f.read_text()
        assert "% 8" not in body, f"{f.name} branches on a residue class"
