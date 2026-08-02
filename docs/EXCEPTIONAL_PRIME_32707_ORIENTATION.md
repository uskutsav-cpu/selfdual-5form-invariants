# p = 32707: the holdout prime did its job

Three cells failed, identically and seed-independently, with

    RuntimeError: image has dimension 0, not 126; cannot build a left inverse

This is not a budget artifact and not a bad input. 32707 is prime. What it is
is a latent defect in the bridge construction, surfaced by the only mechanism
in the package capable of surfacing it.

## What was measured

| prime | rank Φ(self-dual) | rank Φ(anti-self-dual) |
|---|---|---|
| 32749 | 126 | 0 |
| 32719 | 126 | 0 |
| 32717 | 126 | 0 |
| 32713 | 126 | 0 |
| **32707** | **0** | **126** |

Exactly swapped. Not degraded, not partially degenerate — swapped.

## Which side it comes from

The tensor side is identical at every prime tested:

| prime | `*²` | rank of `(1+*)/2` | self-dual basis rank |
|---|---|---|---|
| 32749 | +1 | 126 | 126 |
| 32713 | +1 | 126 | 126 |
| 32707 | +1 | 126 | 126 |

That is expected: the Hodge matrix is a fixed integer matrix, so `*² = +1`
holds over **Z** and therefore modulo every prime. The Hodge eigenspace
decomposition cannot be prime-dependent.

The spinor side can be, and is. The frame congruence relating the split (5,5)
oscillator metric to the Lorentzian (1,9) metric is obtained by **solving a
congruence mod p**, and that solution is not unique. Distinct solutions can
differ by an orientation reversal. Reversing orientation flips the sign of the
Hodge star, which exchanges its `+1` and `−1` eigenspaces — precisely the
swap observed.

At 32707 the solver returned an orientation-reversing congruence.

## What is and is not broken

**Not broken.** The bridge is still an isomorphism from a 126-dimensional
Hodge eigenspace onto the gamma-traceless 126. At 32707 it is a perfectly good
map; the left-inverse construction fails only because it looks for the image of
the *self-dual* space specifically.

**Broken.** The convention alignment between the two sides is not
orientation-fixed. The statement

> ker Φ = the anti-self-dual 126, im Φ|_{self-dual} = the gamma-traceless 126

is a claim this project makes, and it held at four of five primes because the
congruence solver happened to return the orientation-preserving branch. That is
luck, not construction.

## Why the validation suite could not catch it

`spinor_trace_bridge/results/bridge_validation.json` exercises exactly two
primes, 32719 and 32749. Both are orientation-preserving. The suite verifies
the kernel and image statements thoroughly and would have passed forever
without noticing that they are branch-dependent.

The holdout primes exist so that something not used in any fit gets a vote.
This is what that is for, and it is the first thing in the package to find a
defect the tests were structurally unable to see.

## The fix

Determine the branch and use the matching projector, rather than assuming
self-dual. Detecting it is one rank computation: whichever of `Φ(SD)` and
`Φ(ASD)` is nonzero identifies the orientation, and the construction can either
compose with an orientation flip or select the other eigenspace.

The fix is provably a no-op wherever `Φ(SD)` already has rank 126, which is
every cell completed so far.

## Consequence for the manuscript

Until the construction pins orientation, the kernel and image statements must
either be fixed in the code or stated with the orientation convention made
explicit and verified per prime. They must not be presented as automatic.

The rank-81 results are unaffected. Rank is a property of the Jacobian of the
invariant functions, and an orientation flip relabels which eigenspace is
called self-dual without changing any invariant's value.
