# Referee D — computational proof

Adversarial internal review.

---

## D1. Thirteen of fifteen rank-matrix cells are unverified

The paper discloses this, which is to its credit. But it then leans on the
15-cell agreement — "identical pivot structure across primes and seeds is
considerably harder to arrange by accident" — as the main evidence for
robustness. If thirteen of the cells came from a single external run in a
different working tree, their mutual agreement is close to guaranteed regardless
of correctness. The rhetorical weight and the evidential weight are mismatched.

**Severity: serious.**

## D2. The cells record no source-critical hash

The provenance note in the artifact says the cells "record no source-critical
hash", and provenance was closed empirically by comparing two overlapping cells.
That means you cannot tell what code produced the other thirteen. If that code
had the orientation defect of appendix B, would you know?

**Severity: serious.** This connects directly to the `p = 32707` finding.

## D3. Exceptional primes: the spanning-set argument's reach

You argue that `A10`, `P10`, `G10` and `B10` escape the exceptional-prime problem
by a spanning-set bound. That argument needs rational representatives. State
where each of those four gets them.

**Severity: serious.** Same objection as Referee A6, arrived at independently.

## D4. Rational reconstruction can succeed and be wrong

You lift 9 rows by CRT plus rational reconstruction and validate at one held-out
prime. A single held-out prime gives a one-in-`p` chance of a false pass per row,
which is small but not zero, and the failure mode is silent. Why one prime and
not two?

**Severity: moderate.**

## D5. Two determinant routines, one implementation lineage

You compute the certifying determinant "by two independent routines". How
independent? If both are your own code sharing a modular-arithmetic layer, a bug
in that layer defeats both.

**Severity: moderate.**

## D6. The Euler homogeneity check

Every row is checked against Euler's relation. Euler's relation is a consequence
of homogeneity, which your construction guarantees by fiat. What error would this
check actually catch that the construction does not already exclude?

**Severity: minor.**

## D7. Figures generated from macros, macros generated from artifacts — but who checks the macro generator?

The chain is artifact → `make_numbers.py` → `numbers.tex` → manuscript. A bug in
`make_numbers.py` propagates to every number in the paper, and the claim gates
read the same macros. What is the independent check on that link?

**Severity: moderate.**

## D8. `opt_einsum` and the environment

The certified runs used a fallback contraction ordering because an optional
dependency was absent, and it is not in `requirements.txt`. A reproducer who
installs it takes a different code path. You assert results are identical. Was
that tested, or assumed?

**Severity: moderate.**

## D9. Process provenance

The paper mentions an incident of two processes sharing a row cache. It does not
say how the current architecture *prevents* it as opposed to discouraging it.

**Severity: minor.**
