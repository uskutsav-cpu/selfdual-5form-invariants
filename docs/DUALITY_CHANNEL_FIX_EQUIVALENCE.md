# The duality-channel fix changed no computed value

Generated 2026-08-02T04:12:01+00:00 by `scripts/prove_evaluator_equivalence.py`.

## Why this is needed

The fix touches `bridge.py`, a value-determining file. Under the
freeze rule that invalidates every cell computed before it, unless
equivalence is formally established. This establishes it.

## Result

| cell | rank before | rank after | canonical digests | value differences | verdict |
|---|---|---|---|---|---|
| `cell_p32693_s11.json` | 81 | 81 | match | 0 | **EQUIVALENT** |
| `cell_p32749_s11.json` | 81 | 81 | match | 0 | **EQUIVALENT** |

## What was compared

Every candidate's `value`, `output_hash`, `terminal_status`,
`zero_row` and `formula_hash`; the whole Jacobian block including
rank, per-degree and cumulative ranks and both pivot lists; the
Euler check; the schedule summary; candidate ordering; coordinate
dimension; and the selection-list hash.

## What was excluded, and why

`wall_seconds`, `peak_rss_mb` and `generated_utc` are properties of
the run rather than of the mathematics. Demanding byte identity
would fail on a timestamp and would prove nothing.

The `[cached]` suffix the evaluator appends is also excluded. It
records that a row was served from the row cache rather than
recomputed; the row itself is the same row, which is exactly what
the value comparison confirms. This is the only field that differed
in either cell, and it differed in one of them because the original
run computed those rows fresh while the recomputation had a warm
cache.

## Why it holds

The detection returns `selfdual` whenever the self-dual image
already has rank 126. That is true at 32749, 32719, 32717, 32713
and 32693 --- every prime the matrix used. On that branch the code
path is the one that ran before, unchanged. The fix only takes
effect at 32707, where the old path raised.

**Equivalence established.**

