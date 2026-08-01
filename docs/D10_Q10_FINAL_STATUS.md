# D10 and Q10 --- final characteristic-zero status

Generated 2026-08-01T21:28:55+00:00 by `scripts/exact_D10_Q10_characteristic_zero.py`.

## Result

| space | lower bound | upper bound | exact over Q | status |
|---|---|---|---|---|
| A10 | 14 (modular) | 14 (structural) | **14** | PROVED |
| D10 | 11 (modular) | 11 (exact rational) | **11** | PROVED |
| Q10 | --- | --- | **3** | PROVED |

## Why the modular record was not enough

`rank_{F_p} <= rank_Q`. For a subspace that is *subtracted* this is the
wrong direction: `dim Q10 = dim A10 - dim D10`, so a D10 that is larger
over Q than mod p makes the obstruction smaller, and agreement across
primes cannot rule that out.

The gap never needed a modular argument. The flow targets carry exact
rational coordinates, so the same fixed-point closure runs over Q with
Fraction arithmetic; it reached its fixed point in 3 sweeps
and its rank was read off by exact rational elimination. That computes the
rank rather than bounding it, which is both bounds at once.

A10 needs no computation for its upper bound: the fourteen basis elements
are the coordinate system, so nothing spanned by them exceeds fourteen, and
the modular rank 14 supplies the matching lower bound.

## Three different numbers live at degree 10

Getting this wrong is easy and the first attempt did:

| object | dimension | quotient |
|---|---|---|
| span of all 37 degree-10 flow targets | 14 | 0 |
| new-forcing space (Tr(tau) excluded) | 5 | 9 |
| static stress span | 2 | 12 |
| **D10, the seed closure** | **11** | **3** |

Only the last is D10. The first has no activation condition and reaches
everything; the second removes Tr(tau) as a generator; the third is static
rather than dynamical.

## Cross-check against the modular record

| quantity | exact over Q | modular record | agree |
|---|---|---|---|
| rank of D10 | 11 | 11 | yes |
| free columns | [5, 6, 11] | [5, 6, 11] | yes |

Basis elements not reached by the flow:

- `I10_6` (column 5)
- `I10_7` (column 6)
- `I10_12` (column 11)

## Wording the manuscript may use

> dim_Q A10 = 14, dim_Q D10 = 11, dim_Q Q10 = 3

## Scope

> D_d is a SEED closure. The generator-extension problem dV/dlambda = f(T,S,lambda) is different and is not answered here.

This settles the dimension of the seed closure over Q. It does not answer
the generator-extension problem, and nothing here should be read as doing so.

