# The canonical orientation-fixed bridge

## Root cause

The frame `L` relating the split (5,5) oscillator metric to the Lorentzian
(1,9) metric is obtained by solving `L^T eta_null L = eta_lorentzian` mod p.
That solve calls a modular square root, and a square root mod p has **two**
values, `r` and `p - r`. Both give a valid congruence. They differ by an
orientation reversal.

Orientation reverses the sign of the volume form, hence of the Hodge star,
hence exchanges the star's `+1` and `-1` eigenspaces. So the branch decides
which Hodge eigenspace the gamma map annihilates — and it was never pinned.

Left unpinned the bridge is the self-dual projector at some primes and the
anti-self-dual projector at others, silently, with no error until a later step
reports an image of dimension zero.

## The fix

`signature.orientation_normalised_L(p)` tries both branches in a fixed order
and keeps the one under which the self-dual space survives. Deterministic, and
a property of the construction rather than a per-prime exception.

## Independent verification

`scripts/verify_orientation_canonical_independent.py` never calls the
production selector. It takes the final frame, checks the congruence itself
with its own determinant routine, reconstructs **both** branches
independently, and confirms that exactly one of them is self-dual-surviving
and that production chose it.

Eleven primes, all four usable residue classes mod 8:

| prime | p mod 8 | branch chosen | channel | left inverse | congruence |
|---|---|---|---|---|---|
| 32633 | 1 | **flipped** | selfdual | yes | holds |
| 32647 | 7 | plain | selfdual | yes | holds |
| 32653 | 5 | plain | selfdual | yes | holds |
| 32687 | 7 | plain | selfdual | yes | holds |
| 32693 | 5 | plain | selfdual | yes | holds |
| 32707 | 3 | **flipped** | selfdual | yes | holds |
| 32713 | 1 | plain | selfdual | yes | holds |
| 32717 | 5 | plain | selfdual | yes | holds |
| 32719 | 7 | plain | selfdual | yes | holds |
| 32749 | 5 | plain | selfdual | yes | holds |
| 32771 | 3 | **flipped** | selfdual | yes | holds |

Zero problems. Every class lands on the self-dual channel.

## The mod-8 hypothesis is refuted, not merely unproven

An earlier hypothesis held that primes congruent to `3 mod 8` are exceptional
and must be excluded. The evidence for it was two primes, 32707 and 32771,
both of which happened to be in that class.

**32633 is 1 mod 8 and also requires the flipped branch.** A prime outside the
suspected class needs exactly the same correction, so the branch requirement is
not a function of the residue class. The pattern was a coincidence of the two
examples available when it was proposed.

Two separate conclusions follow, and both matter:

1. no prime needs excluding — every class works once the orientation is pinned;
2. `3 mod 8` was never the mechanism, so no code may branch on it, and the
   regression suite forbids that.

## What the bridge now guarantees

At every tested prime, by construction rather than by luck:

    ker Phi         = the anti-self-dual 126
    im Phi|selfdual = the gamma-traceless 126
    left inverse    exists, and composes to the self-dual projector

The convention the package states is now the convention it has.
