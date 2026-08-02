# The pre-fix matrix is superseded, not wrong

## Status

    SUPERSEDED AS FINAL PUBLICATION CERTIFICATES
    because the evaluator provenance changed

Explicitly **not**: invalid mathematical calculations. The values were correct
and the evidence for that is direct — three cells recomputed under the merged
evaluator match the pre-fix cells with zero value differences
(`results/orientation_merge/two_cell_value_comparison.json`).

## What changed and why it matters

`signature.py` now pins the frame orientation canonically. At every prime the
old matrix used, the pinned frame is bit-identical to the old one, so nothing
those cells computed was affected. But a publication certificate should come
from one execution under one evaluator, not from a mixture of pre-fix and
post-fix provenance — and the old execution cannot include 32707 at all,
because the old evaluator could not build a left inverse there.

So the matrix is being recomputed in full rather than patched.

## What is superseded

15 cells, execution `rank81-matrix-5f46a2cbbe93-flop1e11`, all rank 81,
fitting 32749/32719/32717 and holdout 32713/32693. Nothing is deleted: the
cells are preserved on disk and in git history at `8719579^`.

## What remains informative

- Every pre-fix rank is 81 and every post-fix rank so far is 81. That is
  corroboration across two evaluator provenances, which is worth more than one.
- The three 32707 failures under the old evaluator are what found the unpinned
  branch. They are evidence, and they are kept.
- The pivot-stability result — 81 stable rows and 81 stable columns across
  every cell — was first observed in the pre-fix matrix and is being re-derived
  post-fix.

## What replaces it

One post-fix execution: 15 required publication cells over fitting
32749/32719/32717 and holdout **32713/32707**, plus 3 extra validation cells at
32693. 32693 is an addition, never a substitute for 32707.
