# Referee B — spinors and real forms

## B1. "The oscillator frame is Euclidean, so there are no real self-dual five-forms."

**Refuted, with a computation.** The frame's real signature is `(5,5)` — split —
obtained by diagonalising the metric built from all one hundred anticommutators
of the archive's own operators. In split signature `*^2 = +1` on five-forms
exactly as in Lorentzian, so real self-dual five-forms exist. A null frame cannot
be Euclidean at all: Euclidean signature has no nonzero isotropic vectors.

This objection was, for a time, the project's own recorded position. It was
wrong.

## B2. "Then Lorentzian and split are related by a real frame transformation."

**No, and the paper does not say so.** `(5,5)` and `(1,9)` are inequivalent real
forms; no real orthogonal transformation connects them. What is true is that both
metrics have discriminant `-1` up to squares, so over `C` and over `F_p` they are
congruent, and the bridge constructs that congruence explicitly. Every
component-level comparison is therefore stated at the modular level and no
stronger.

## B3. "The Hodge sign, chirality and charge-conjugation conventions are unpinned."

They were, in one respect, and the referee is right to press. The null-frame
congruence is determined only up to a square-root branch, and that branch
reverses the frame's orientation — which reverses the sign of the star, which
swaps which eigenspace the gamma map annihilates.

Left unpinned, the construction was the self-dual projector at five of six primes
and the anti-self-dual projector at the sixth, silently, with no error until a
later step reported an image of dimension zero. That is exactly what happened at
`p = 32707`.

**Fixed**: the orientation is now normalised by construction. Three regression
tests, including one that asserts the *opposite* branch breaks it — without which
a refactor could drop the normalisation and the suite would still pass at five of
six primes.

## B4. "Equivariance at sampled group elements is not equivariance."

Conceded and stated. It is verified exactly under `GL(5)` with character
`det(A)`, and under products of Clifford reflections, which by Cartan–Dieudonné
generate the full orthogonal group. That samples finitely many elements; it is
not a symbolic identity. Coauthor item G-4 asks whether a Schur argument should
replace it.

## B5. "Is the inverse a genuine inverse?"

It is a **left** inverse on the self-dual subspace, and the paper says left
inverse. `inverse . forward` reproduces the self-dual projector exactly; the
kernel is the anti-self-dual `126` and the image the gamma-traceless `126`, each
by two-way span equality rather than dimension counting.

## Verdict

B3 was a real defect, found by this review's own line of attack, and is fixed.
B1 is refuted. The rest are correctly scoped.
