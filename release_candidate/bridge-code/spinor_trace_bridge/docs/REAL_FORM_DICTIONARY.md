# Real-form dictionary

This document exists because a previous session recorded a blocker that does not
exist, and the correction changes what the paper is allowed to claim.

## The claim that was wrong

The earlier record stated:

> the spinor code builds gammas from a null oscillator basis whose natural real
> form is Euclidean SO(10); a real self-dual 5-form exists in (1,9) but not in
> (10,0), where `*^2 = -1`.

The second half of that sentence is correct as a statement about Euclidean
signature. The first half — the identification of the oscillator frame's real
form as Euclidean — is false.

## What the oscillator frame actually is

The spinor implementation realises the ten vector gammas as five wedge operators
`e_i ^ (-)` and five contraction operators `iota_{e^i}` on `Lambda^* W`, `W = F^5`.
Their anticommutators are fixed by the exterior algebra alone:

    {e_i ^, e_j ^} = 0,   {iota_i, iota_j} = 0,   {e_i ^, iota_j} = delta_ij

so with `Gamma^mu` = (wedge_0..wedge_4, iota_0..iota_4) and the convention
`{Gamma^mu, Gamma^nu} = 2 eta^{mu nu}`,

    eta = (1/2) [[0, I_5], [I_5, 0]].

`tests/test_bridge.py::test_null_frame_signature_is_split` computes all one
hundred anticommutators of the archive's own operators and diagonalises the
result: five eigenvalues `+1/2` and five eigenvalues `-1/2`.

    real signature of the oscillator frame = (5,5)   -- SPLIT, not Euclidean.

This is not an accident of the archive's coding style. A null (isotropic) frame
of the kind an oscillator realisation produces *cannot* be Euclidean: Euclidean
signature has no nonzero isotropic vectors at all, whereas every `e_i` here
satisfies `eta(e_i, e_i) = 0`. The oscillator realisation is only available
because the form is split (or complex).

## Consequence for self-duality

For a metric of signature `(s,t)` on `R^n`, the Hodge star on `p`-forms obeys

    ** = (-1)^{p(n-p)} * sign(det eta).

At `n = 10`, `p = 5` the first factor is `(-1)^25 = -1`, so

| signature | `sign(det eta)` | `**` on 5-forms | real self-dual 5-forms |
|---|---:|---:|---|
| Euclidean `(10,0)` | `+1` | `-1` | **none** |
| Lorentzian `(1,9)` | `-1` | `+1` | 126-dimensional |
| Split `(5,5)`      | `-1` | `+1` | 126-dimensional |

Split and Lorentzian agree. The obstruction that was recorded as blocking the
whole comparison applies to a signature neither implementation uses.

## What genuinely does not transfer

Sylvester's law of inertia is still in force. `(5,5)` and `(1,9)` are
*inequivalent* real forms of `so(10,C)`: no real matrix conjugates one to the
other, because a real congruence cannot change a signature. Passing between them
multiplies four directions by `i`. So:

| level | status |
|---|---|
| over `C` | the two frames are congruent; one explicit complex matrix relates them |
| over `F_p` | congruent, and the transition matrix is exact — see below |
| over `R` | **not** congruent; the transition is necessarily complex |

## Why `F_p` sidesteps the real-form question entirely

Over a finite field there is no notion of signature. A nondegenerate quadratic
form in a fixed dimension over `F_p` is classified by its discriminant modulo
squares, and nothing else. Here

    det diag(-1,+1,...,+1) = -1
    det (1/2)[[0,I],[I,0]] = -2^{-10} = (-1) * (2^{-5})^2

so the two discriminants differ by a square and the forms are congruent. Both
implementations already work at the same two primes (`32749`, `32719`), so the
bridge inherits an exact transition matrix and never has to choose a real form.

`signature.py::congruence` builds that matrix by an explicit algorithm
(congruence-diagonalise, canonicalise each diagonal to `diag(1,...,1,disc)` using
`diag(a,b) ~ diag(1,ab)`, then match). `TransitionFrame.verify()` checks
`L^T eta_null L = eta_lorentzian` exactly, at both primes.

## What this licenses, and what it does not

**Licensed.** Comparison of invariant *dimensions* between the two
implementations, without any complexification hedge. Both `Spin(5,5)` and
`Spin(1,9)` are real forms of `Spin(10,C)`, hence Zariski-dense in it, so for a
real module `V_R` with `V_R (x) C = V_C` the invariant rings satisfy
`R[V_R]^{G_R} (x) C = C[V_C]^{G_C}` in every degree. Graded dimensions agree
exactly. This is why the degree-4/6/8/10 counts may be compared directly.

**Licensed.** Component-level comparison *over `F_p`*, because the transition
matrix exists there and is exact. This is what `WS-I` actually uses.

**Not licensed.** Component-level comparison of *real* tensors between a
Lorentzian and a split realisation without transporting through the complex
transition. A real self-dual five-form of `(1,9)` is not a real self-dual
five-form of `(5,5)`; it becomes one only after the complex change of frame, and
is then generally complex in the other frame.

**Not licensed.** Any statement that the two implementations agree "in the same
signature". They do not. They agree over a common field in which the frame
change is available.

## Majorana–Weyl, for the record

Ten dimensions admits Majorana–Weyl spinors in signatures with `s - t = 0 mod 8`,
which covers both `(1,9)` and `(5,5)`. In each the chiral spinor is a real
16-dimensional module and

    Sym^2(16) = 10 (+) 126,

the `126` being the gamma-traceless part and, as a module, the self-dual
five-form. This is the representation-theoretic reason the bridge is an
isomorphism onto its image rather than merely an injection, and the bridge tests
confirm the `126` splitting exactly at both primes rather than importing it.

## References

- M. Cederwall, J. Hutomo, S. M. Kuzenko, K. Lechner, D. P. Sorokin,
  *Some remarks on invariants*, J. Phys. A **59** (2026) 065203,
  doi:10.1088/1751-8121/ae3bb8; arXiv:2509.14350v2.
- J. Hutomo, K. Lechner, D. P. Sorokin, *On non-linear chiral 4-form theories in
  D=10*, arXiv:2509.14351v2 (revised 6 Jan 2026).

Both are recorded with hashes in `docs/PRIMARY_SOURCE_INGEST.md`.

## Status

Resolved computationally and recorded here. The signature identification and the
`F_p` congruence are machine-checked at two primes. The representation-theoretic
statement about invariant rings of real forms is standard but is flagged for
coauthor confirmation in `MENTOR_REVIEW_ITEMS.md` (item G-3).
