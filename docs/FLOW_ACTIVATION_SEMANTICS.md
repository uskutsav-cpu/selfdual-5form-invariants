# Flow activation semantics

The activation rule is the difference between an obstruction and no
obstruction. Stated once here, mathematically, so that neither the manuscript
nor a future reader has to infer it from code.

## The three spaces

Confusing any two of these changes the answer.

| object | definition | dimension at degree 10 |
|---|---|---|
| raw target span | the linear span of every generated degree-10 flow target vector, with no condition on when a target applies | 14 |
| activated flow closure `D10` | the smallest fixed point containing the seed under the activation rule below | 11 |
| complete invariant space `A10` | the full space of degree-10 scalar invariants | 14 |

The raw span coincides numerically with `A10` and is not the same object; it is
the span of a particular generating family that happens to exhaust the space.
Using it where `D10` belongs gives `dim Q10 = 0` instead of `3`.

This is not hypothetical. The first attempt at the rational calculation did
exactly that and returned a confident, self-consistent zero.

## The activation rule

Each flow target is indexed by a triple: a trace generator, a field degree, and
a **coefficient monomial**. Write a target as `(G, d, C)`, contributing a
coordinate vector `P[G, d, C]` in the degree-`d` basis.

Let `S_d` be the set of degree-`d` directions reached so far. A direction `a` is
*reachable* at degree `d` when some vector already in `S_d` has a nonzero
`a`-coordinate — not when the unit vector `e_a` itself lies in the span, which
would be strictly stronger and would understate the closure.

> **Activation.** The target `(G, d, C)` contributes `P[G, d, C]` if and only if
> **every factor** of the coefficient monomial `C` is reachable at its own
> degree.

A monomial with no factors is vacuously satisfied, so such a target is
unconditionally active. There are ten of these, two at degree 10.

Adding an active target can enlarge a span, which can satisfy a monomial that
was previously unsatisfied, which can activate further targets. The construction
therefore iterates:

```
S ← seed
repeat
    for each target (G, d, C):
        if every factor of C is reachable:
            if P[G, d, C] is independent of S_d:
                S_d ← S_d + P[G, d, C]
until no S_d grows
```

The fixed point is the smallest stress-closed family containing the seed. It is
reached in three sweeps.

## Properties, all measured

| property | holds | why it matters |
|---|---|---|
| independent of target visiting order | yes, three shuffled orderings | a fixed point that depended on order would not be well defined |
| independent of duplicate targets | yes | duplication is not mathematics |
| independent of row scaling | yes | a span is scale-invariant |
| **independent of the seed, at degree 10** | **yes** | the ten unconditional targets bootstrap the sector alone; the same rank, the same free columns, the same span |
| dependent on the seed at degrees 6, 8, 12 | yes | so the rule is not vacuous |
| one sweep is not the fixed point | correct, one sweep is smaller | the iteration is load-bearing |
| unconditional activation changes the answer | 11 → 14 | this is the failure that occurred |
| an unsatisfiable factor blocks everything | 11 → 0 | the condition really is enforced |

## Why degree 10 is seed-independent

Two degree-10 targets carry an empty coefficient monomial, so they contribute
whatever the seed is. Their images make degree-10 directions reachable, which
satisfies the single-factor degree-10 monomials, which contribute further
vectors, and so on until the cascade closes at 11. Nothing in that chain
consults the seed.

Degrees 6, 8 and 12 have no such self-sustaining core and do depend on what they
are given.

**Consequence for wording.** `dim_Q D10 = 11` needs no seed qualifier. The
"seed closure" language in the earlier record is accurate but, at degree 10,
describes a dependence that is not there.

## What is still scoped

The closure answers: what does the flow reach, from a starting family, under
this activation rule. It does **not** answer the generator-extension problem
`dV/dλ = f(T, S, λ)`, which permits generator coefficients this construction
does not range over. That question is open and is not touched by anything here.

## Regression tests

`tests/test_flow_activation_semantics.py`, 17 tests. Each perturbs one aspect
and asserts either that the answer must move or that it must not. The
rank-14 mistake is kept as a fixture so it cannot return silently.
