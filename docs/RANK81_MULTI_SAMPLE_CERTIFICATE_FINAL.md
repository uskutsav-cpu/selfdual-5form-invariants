# Rank-81 multi-sample certificate --- final

Generated 2026-08-02T01:24:43+00:00 by `scripts/emit_rank81_multi_sample_certificate.py`.

Execution `rank81-matrix-5f46a2cbbe93-flop1e11`, frozen at commit `5f46a2cbbe93`, contraction budget 1e+11.

## Every cell

| prime | role | seed | rank | rows | cols | Euler | errors | zero rows | seconds | peak MB |
|---|---|---|---|---|---|---|---|---|---|---|
| 32717 | fitting | 11 | **81** | 83 | 126 | 83/83 | 0 | 0 | 619.5 | 571.0 |
| 32717 | fitting | 22 | **81** | 83 | 126 | 83/83 | 0 | 0 | 3360.9 | 456.1 |
| 32717 | fitting | 33 | **81** | 83 | 126 | 83/83 | 0 | 0 | 1442.7 | 518.8 |
| 32719 | fitting | 11 | **81** | 83 | 126 | 83/83 | 0 | 0 | 1076.3 | 607.9 |
| 32719 | fitting | 22 | **81** | 83 | 126 | 83/83 | 0 | 0 | 809.3 | 594.3 |
| 32719 | fitting | 33 | **81** | 83 | 126 | 83/83 | 0 | 0 | 561.6 | 587.3 |
| 32749 | fitting | 11 | **81** | 83 | 126 | 83/83 | 0 | 0 | 4.0 | 233.3 |
| 32749 | fitting | 22 | **81** | 83 | 126 | 83/83 | 0 | 0 | 268.7 | 508.9 |
| 32749 | fitting | 33 | **81** | 83 | 126 | 83/83 | 0 | 0 | 586.3 | 591.1 |
| 32693 | holdout | 11 | **81** | 83 | 126 | 83/83 | 0 | 0 | 694.0 | 573.9 |
| 32693 | holdout | 22 | **81** | 83 | 126 | 83/83 | 0 | 0 | 535.0 | 719.9 |
| 32693 | holdout | 33 | **81** | 83 | 126 | 83/83 | 0 | 0 | 553.7 | 699.3 |
| 32713 | holdout | 11 | **81** | 83 | 126 | 83/83 | 0 | 0 | 1169.0 | 583.3 |
| 32713 | holdout | 22 | **81** | 83 | 126 | 83/83 | 0 | 0 | 2176.2 | 472.2 |
| 32713 | holdout | 33 | **81** | 83 | 126 | 83/83 | 0 | 0 | 1674.6 | 492.6 |

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
| 32693 | 81 |
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
| holdout | [32693, 32713] | 6 | [81] |

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

- total cell runtime 15532 s (4.31 h)
- maximum peak RSS across cells 719.9 MB
- one cell at a time, on one machine

## Hashes

- assembled matrix scientific content `5180e03d38e62ff1184ff4d525bcc17b`
- frozen source tree `09abe782ecb5eb606b4d67ecdf4c07e8`
- dependency lock `095e3141babb343e9ce8ab05b4cd4e20`

| cell | content sha256 |
|---|---|
| p=32693 s=11 | `41b8fdba0a1ff9b9246099c93e57b62b` |
| p=32693 s=22 | `ffbf8492aeb7e4bd98a966e61b982bf2` |
| p=32693 s=33 | `fa888abea2d57b9b26971e95f9106a85` |
| p=32713 s=11 | `bb831ef8c882fa00eff8596128666d61` |
| p=32713 s=22 | `b05cfb2e22c7529303021d2199a2ea4f` |
| p=32713 s=33 | `549457c9f0014f18694e037cd86f328c` |
| p=32717 s=11 | `931309a51b112e25d833844bdf3b86a2` |
| p=32717 s=22 | `2f6fedd7c48f3b3d8971de74509c17a5` |
| p=32717 s=33 | `eb714ea57d24c7fe8f778fc726d2d461` |
| p=32719 s=11 | `a67a801b15a865d2c0eeacd018f3eb0b` |
| p=32719 s=22 | `926236c55c767a8d07b3d187580b3eb3` |
| p=32719 s=33 | `f4ba174e5e3b6be53610d293454db160` |
| p=32749 s=11 | `ccd04a02b738edbeaff5b429be9a673f` |
| p=32749 s=22 | `d59cceeefcad15b0dd6ed357428bdaf0` |
| p=32749 s=33 | `464dfac08d5403eb01ba60c13313168b` |

