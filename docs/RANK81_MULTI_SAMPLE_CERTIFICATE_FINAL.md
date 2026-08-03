# Rank-81 multi-sample certificate --- final

Generated 2026-08-03T00:23:03+00:00 by `scripts/emit_rank81_multi_sample_certificate.py`.

Execution `rank81-canonical-orientation-1b5a6ba9d175-flop1e11`, frozen at commit `1b5a6ba9d175`, contraction budget 1e+11.

## Every cell

| prime | role | seed | rank | rows | cols | Euler | errors | zero rows | seconds | peak MB |
|---|---|---|---|---|---|---|---|---|---|---|
| 32717 | fitting | 11 | **81** | 83 | 126 | 83/83 | 0 | 0 | 16.6 | 235.5 |
| 32717 | fitting | 22 | **81** | 83 | 126 | 83/83 | 0 | 0 | 16.2 | 228.8 |
| 32717 | fitting | 33 | **81** | 83 | 126 | 83/83 | 0 | 0 | 15.9 | 236.9 |
| 32719 | fitting | 11 | **81** | 83 | 126 | 83/83 | 0 | 0 | 18.6 | 231.7 |
| 32719 | fitting | 22 | **81** | 83 | 126 | 83/83 | 0 | 0 | 17.9 | 236.5 |
| 32719 | fitting | 33 | **81** | 83 | 126 | 83/83 | 0 | 0 | 18.0 | 237.3 |
| 32749 | fitting | 11 | **81** | 83 | 126 | 83/83 | 0 | 0 | 633.6 | 532.0 |
| 32749 | fitting | 22 | **81** | 83 | 126 | 83/83 | 0 | 0 | 15.2 | 243.4 |
| 32749 | fitting | 33 | **81** | 83 | 126 | 83/83 | 0 | 0 | 15.4 | 236.4 |
| 32707 | holdout | 11 | **81** | 83 | 126 | 83/83 | 0 | 0 | 1299.9 | 741.3 |
| 32707 | holdout | 22 | **81** | 83 | 126 | 83/83 | 0 | 0 | 1534.5 | 686.6 |
| 32707 | holdout | 33 | **81** | 83 | 126 | 83/83 | 0 | 0 | 2123.2 | 650.8 |
| 32713 | holdout | 11 | **81** | 83 | 126 | 83/83 | 0 | 0 | 16.3 | 238.3 |
| 32713 | holdout | 22 | **81** | 83 | 126 | 83/83 | 0 | 0 | 14.8 | 231.1 |
| 32713 | holdout | 33 | **81** | 83 | 126 | 83/83 | 0 | 0 | 17.0 | 237.6 |

15 cells: 9 fitting, 6 holdout. Distinct ranks [81].

## Degree blocks

| degree | block rank across cells | cumulative rank across cells |
|---|---|---|
| 4 | 1 | 1 |
| 6 | 2 | 3 |
| 8 | 6 | 9 |
| 10 | 12 | 21 |
| 12 | 62 | 81 |

A single value in a column means every cell agreed.

## Pivot stability

- stable pivot rows, present in all 15 cells: 81
- unstable pivot rows, present in some but not all: 0 
- stable pivot columns: 81
- unstable pivot columns: 0 

The same rows and the same columns carry the rank at every sample point
and every prime. That is stronger than the ranks merely agreeing: it
means one fixed minor witnesses the rank throughout.

## Sample and prime dependence

| prime | ranks over its seeds |
|---|---|
| 32707 | 81 |
| 32713 | 81 |
| 32717 | 81 |
| 32719 | 81 |
| 32749 | 81 |

| seed | ranks over its primes |
|---|---|
| 11 | 81 |
| 22 | 81 |
| 33 | 81 |

## Fitting against holdout

| set | primes | cells | ranks |
|---|---|---|---|
| fitting | [32717, 32719, 32749] | 9 | [81] |
| holdout | [32707, 32713] | 6 | [81] |

The holdout primes were not used in selecting the minor or in any fit.

## The explicit minor

- size 81
- selection prime 32749, sample seed 11
- determinant routines ['modular LU with pivoting', 'fraction-free Bareiss, carried out mod p']
- p=32749: det 20755, routines agree True, nonzero True

## What this certifies, and what it does not

Certified: at each of these 15 points the exact modular Jacobian of the 83
selected functions has rank 81, with all 83 candidates evaluated, no
evaluation errors, no zero rows, and Euler homogeneity holding for every
row. Because the coordinate basis is integral, each Jacobian is the
reduction of an integer matrix, so `rank_{F_p} <= rank_Q` and therefore
`rank_Q >= 81` unconditionally.

Not certified here: the matching upper bound. `126 - 45 = 81` is analytic,
comes from the generic-orbit dimension in the literature, and no
computation in this package supplies it. Nor does any finite set of points
establish a statement about a generic point.

Rank 81 among 83 functions means at least two functional dependencies exist
in the selected family. The manuscript never says 83 independent invariants.

## Cost

- total cell runtime 5773 s (1.60 h)
- maximum peak RSS across cells 741.3 MB
- one cell at a time, on one machine

## Hashes

- assembled matrix scientific content `5ed06febdcd16c8ddc0c4758da6f0ced`
- frozen source tree `2e4ff404e15600315b9936015e3fab34`
- dependency lock `095e3141babb343e9ce8ab05b4cd4e20`

| cell | content sha256 |
|---|---|
| p=32707 s=11 | `04dd51047adba4e174265e8f240b94a3` |
| p=32707 s=22 | `1bdd7839de7ebb7b3106136ba84d75c3` |
| p=32707 s=33 | `383d35d04436f53f5b3371c8b1407ec9` |
| p=32713 s=11 | `de402617a6590ae05afdd057cb6954af` |
| p=32713 s=22 | `31c7bb7834c811946d1512d9f4438d3f` |
| p=32713 s=33 | `ecd9d50e79cd0f4953e95713e9f02f64` |
| p=32717 s=11 | `029a00585d60f9af137b92150cda664c` |
| p=32717 s=22 | `a4572d144ce5f6ff5dc56b241e9843a2` |
| p=32717 s=33 | `241459e57b407a58cb822c849121489e` |
| p=32719 s=11 | `000ca853ac843299c0b68f963b7a174d` |
| p=32719 s=22 | `97950b18c19525d6930c8fd34e4624cc` |
| p=32719 s=33 | `f8a76857c6bbc4227648104c09339d37` |
| p=32749 s=11 | `0fc6baa4c0df2e34ee89744ca93bdfcb` |
| p=32749 s=22 | `2e17fb8950495fc409880672990a1a8c` |
| p=32749 s=33 | `2552d94c8195a03afc890832eac58366` |

