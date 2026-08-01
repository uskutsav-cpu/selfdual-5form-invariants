# The exact rational proof of dim_Q D10 = 11 and dim_Q Q10 = 3

Generated 2026-08-01T22:03:05+00:00.

## Statement

    dim_Q A10 = 14    dim_Q D10 = 11    dim_Q Q10 = 3

Over the rationals, not at good primes.

## Three spaces that are easy to confuse

| object | definition | dimension |
|---|---|---|
| raw target span | the span of all degree-10 flow target vectors, with no activation condition | 14 |
| activated flow closure, D10 | the smallest fixed point containing the seed under the activation rule | 11 |
| complete invariant space, A10 | all degree-10 scalar invariants | 14 |

Using the first where the second belongs gives a quotient of
0 instead of 3. That is not a subtle discrepancy; it is the
difference between an obstruction and no obstruction, and it is why the
activation rule is stated below as mathematics rather than left to the
implementation.

## The activation rule

Each flow target is indexed by a generator, a field degree, and a
coefficient monomial. A target contributes to the closure **only once
every factor of its coefficient monomial is a direction already**
**reachable**. Adding an active target can enlarge the span, which can
activate further targets, so the construction iterates to a fixed point.
The fixed point is the smallest stress-closed family containing the seed.

Seed: `{4: ['I4_1'], 6: ['I6_2'], 8: ['I8_3', 'I8_4', 'I8_5', 'I8_6']}`.
Fixed point reached in 3 sweeps.

## Independent verification

| | production | independent verifier |
|---|---|---|
| arithmetic | `Fraction` | integers, denominators cleared per row |
| algorithm | Gauss-Jordan RREF | fraction-free Bareiss |
| closure code | `exact_D10_Q10_characteristic_zero.py` | re-implemented |
| shared rank routine | --- | none |
| rank | 11 | 11 |
| free columns | [5, 6, 11] | [5, 6, 11] |

Sweep-order independence: 3 shuffled
orderings, ranks [11, 11, 11].

## Lower bound certificate

An explicit 11x11 minor of the integer
spanning matrix, with

    det = 12126533474468034240675840

computed by fraction-free Bareiss and again by cofactor expansion; the two
agree (True). A nonzero minor of that size forces
`dim_Q D10 >= 11`.

Columns: ['I10_1', 'I10_2', 'I10_3', 'I10_4', 'I10_5', 'I10_8', 'I10_9', 'I10_10', 'I10_11', 'I4_1*I6_1', 'I4_1*I6_2']

## Upper bound certificate

3 exact integer covectors annihilate every spanning
vector of D10:

1. +1·I10_6
2. +1·I10_7
3. +1·I10_12

Verified against every spanning vector: True.
Three independent linear conditions on a 14-dimensional space place D10
inside a subspace of dimension 11, so
`dim_Q D10 <= 11`.

Both bounds meet at 11.

## The quotient

Representatives: ['I10_6', 'I10_7', 'I10_12']

| check | result |
|---|---|
| each lies outside D10 | True |
| independent modulo D10 | True |
| together they span A10 with D10 | True |
| rank gain when added to D10 | 3 |
| every one is needed | True |
| they are exactly the free columns | True |

Drop-one tests:

| dropped | rank of D10 + remaining | still spans |
|---|---|---|
| I10_6 | 13 | False |
| I10_7 | 13 | False |
| I10_12 | 13 | False |

## Scope

> D_d is a SEED closure. The generator-extension problem dV/dlambda = f(T,S,lambda) is different and is not answered here.

This is the dimension of the seed closure over Q. The
generator-extension problem is a different question and is not answered.

