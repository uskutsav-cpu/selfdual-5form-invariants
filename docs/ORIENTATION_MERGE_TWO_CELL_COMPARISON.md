# Did the canonical orientation fix change any value?

**No.** Three cells recomputed under the merged evaluator, compared field by
field against copies taken before the merge: **zero** differences in any
candidate value, output hash, terminal status, zero-row flag or formula hash,
and identical Jacobian blocks, Euler checks, schedule summaries, candidate
ordering and coordinate dimension.

| cell | rank before | rank after | value differences | verdict |
|---|---|---|---|---|
| `cell_p32749_s11` | 81 | 81 | 0 | EQUIVALENT |
| `cell_p32749_s22` | 81 | 81 | 0 | EQUIVALENT |
| `cell_p32749_s33` | 81 | 81 | 0 | EQUIVALENT |

## Why it holds

`orientation_normalised_L` tries the plain square-root branch first and keeps
it when the self-dual space survives. At 32749, 32719, 32717, 32713 and 32693
it does survive, so the frame `L` is bit-identical to the pre-fix frame and
every downstream value follows unchanged.

Only 32707 and 32771 — where the plain branch fails — receive a different
frame, and there the pre-fix code produced no cell at all.

## What differed, and why it is not a value

Two route annotations. One row cache was rebuilt by the merge, so those rows
were recomputed rather than served from cache; and one derivative row reached
its value through the dense-I contraction plan in one run and from cache in the
other. `output_hash` matches in every case, which is what says the row is the
same row.

The first cell took 634 s and the next two took 15 s each, for exactly this
reason — a rebuilt cache, not a changed result.

## Consequence, stated carefully

The pre-fix cell **values were mathematically correct**. They are superseded as
final publication certificates because the evaluator provenance changed, not
because the arithmetic was wrong. That distinction is the whole content of
`audit/PRE_CANONICAL_ORIENTATION_MATRIX_SUPERSEDED.md`, and this comparison is
the evidence for it.

A three-cell match is not a substitute for recomputing the matrix, and the
matrix is being recomputed in full — 15 required publication cells plus 3 extra
validation cells — under one authoritative post-fix execution.
