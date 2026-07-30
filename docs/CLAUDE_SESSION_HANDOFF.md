# Session handoff

**Branch** `research/maximal-chiral-four-form-program`. Nothing pushed.
**Current commit**: see `git log -1`.

## Running process

`scripts/project_published_degree12.py --primes 32749 32717`
Log: `/private/tmp/.../scratchpad/p12proj2.log`
Healthy at last check: 93% CPU, 134 MB RSS. ~8+ min/prime; later degree-12
graphs evaluate more slowly than the first twelve columns suggested.

## Formulas complete

| id | formula | brackets | status |
|---|---|---|---|
| P10_01 | tr M^5 | — | implemented, Q10 -> [0,0,0] |
| P10_02 | (MM)M M N^(4125) | — | implemented, Q10 -> [0,0,0] |
| P10_03 | M M M (N^(1050) N^(1050)) | black only | implemented, homogeneity OK |
| P10_06 | (MM) M N^(1050) N^(4125) | black only | implemented, homogeneity OK |
| P10_07 | N^(1050) (MM) (N^(1050) N^(1050)) | black only | implemented, homogeneity OK |
| P12_01/02/03 | eq (4.25) | — | implemented; Q12 projection RUNNING |

## Formulas blocked

| id | reason |
|---|---|
| P10_04, P10_09 | **RED brackets** `(mu ... rho]lambda)`; need the staged bracket program encoded. A test asserts these stay unimplemented until then. |
| P10_05, P10_08 | black brackets on the M factors themselves, e.g. `(MM)_{[nu1}^{[mu1} M_{nu2]}^{mu2]}`; needs BracketOp application to the M product |
| P10_10, P10_11, P10_12 | nested black structures; larger index bookkeeping |

## Ranks

- M-only Q10 rank: **0** (six primes)
- P10 Q10 rank from P10_01, P10_02: **0 / 3**
- P10_03, P10_06, P10_07 projections: **not yet run**
- P12 Q12 rank: **pending**

## Next exact command

    .venv/bin/python scripts/project_published_degree10.py

then encode bracket programs for P10_05 / P10_08 (M-factor antisymmetrisation)
using `sdinv.index_symmetry_ops.BracketProgram`.

## Unresolved

1. Red-bracket candidates P10_04/P10_09 need staged programs.
2. Source arithmetic: paper says order 12 has 64 while totalling 83;
   1+2+6+12+62 = 83 matches the repository. Unresolved, logged.
3. PO-03: paper conjectures non-linear relations; repo established Jacobian
   dependence. Different statements.

## Safety notes

- Bare multi-operand `np.einsum` on modular operands overflows silently; the
  P10_02 incident (9605 -> 4674) is a permanent regression test.
- Homogeneity at several `c` is the detector that actually catches wrapping.
