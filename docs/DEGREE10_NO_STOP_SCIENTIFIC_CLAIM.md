# The degree-10 no-stop run: what it could prove, and whether this paper needs it

Written before deciding whether to run it, so that the decision is about the
claim rather than about the compute budget.

## What the run is

Every archived spinor scan stopped at a Hilbert target — a rank supplied from
outside the computation. A search that halts when it reaches a number someone
told it to reach demonstrates nothing about the ansatz it was searching. The
`--no-hilbert-stop` variant removes that rule, so the run ends in a state that
carries information:

| terminal state | meaning |
|---|---|
| `candidate_exhaustion` | the declared ansatz was searched out |
| `hilbert_target` | stopped at an externally supplied rank; uninformative |
| `stagnation` | no rank gain within the configured patience |
| `incomplete` | no terminal state reached |

Recorded status, from `verification/spinor_degree10_no_stop.json`:

| degree | final rank | target | unique graphs tried | stopped by |
|---:|---:|---:|---:|---|
| 4 | 1 | 1 | 2 | `candidate_exhaustion` |
| 6 | 2 | 2 | 5 | `candidate_exhaustion` |
| 8 | 7 | 7 | 32 | `candidate_exhaustion` |
| 10 | 12 (partial) | 14 | 64 (first batch) | **killed** |

Degrees 4, 6 and 8 are searched out. Degree 10 is not.

## What a completed degree-10 run could prove

Exactly one thing:

> Within the declared finite port-graph grammar at degree 10, no further
> candidate increases the rank beyond the recorded value.

That is a statement about **a grammar**, not about the invariant ring. It would
be `EXHAUSTIVE WITHIN THE DEFINED FINITE GRAMMAR`, never
`EXHAUSTIVE BY MATHEMATICAL PROOF`, because the grammar's own completeness —
that every degree-10 spinor invariant is expressible in it — is not established
and is not something a search can establish about itself.

## What it cannot prove

- completeness of the invariant ring at degree 10;
- that the spinor construction is the only one possible;
- minimality of any basis;
- anything about degree 12.

## Does this manuscript need it?

**No.** The degree-10 claim this paper makes is span equality between two
independently constructed families, and its proof does not route through
exhaustion of either grammar.

The argument:

1. The tensor side reaches rank 14 at degree 10, which is `dim A10`.
2. `dim_Q A10 = 14` is structural: A10 is spanned by the fourteen basis
   elements that coordinatise it, so it cannot be larger, and the modular rank
   14 shows it is not smaller. See `docs/DEGREE10_SPACES_FINAL_STATUS.md`.
3. The spinor family also reaches rank 14 on the common sample, with
   containment checked in both directions and validated on holdout samples the
   change of basis was not fitted on.
4. Both spans therefore equal A10 itself.

Step 4 is what makes the no-stop run unnecessary. Any additional degree-10
spinor candidate the grammar might still contain is, whatever else it is, a
degree-10 invariant — so it lies in A10, which is already spanned. It cannot
enlarge the spinor span, so it cannot break the equality. Exhaustion would tell
us something about the grammar; it would not change the span.

Note where this argument does **not** apply. It works at degree 10 because the
tensor side saturates the full atlas there. It would not licence the same move
at a degree where the tensor enumeration is itself incomplete.

## Decision

**Status: `NOT REQUIRED FOR THE MANUSCRIPT CLAIMS`.**

The production run is not launched. Two reasons, and the second is the one that
matters:

1. The machine is committed to the rank-certificate matrix, and the standing
   instruction is not to start additional expensive computation. The earlier
   attempt was killed after one batch of 64 graphs.
2. Even completed, it would license a claim this manuscript does not make. Its
   absence costs nothing here.

## What the manuscript may and may not say

May say:

- degrees 4, 6 and 8 reached `candidate_exhaustion` with the Hilbert stopping
  rule disabled;
- at degree 10 the two families span the same space, by the argument above;
- the degree-10 grammar was not searched out, and this is stated rather than
  omitted.

May **not** say:

- that the degree-10 spinor grammar is exhausted;
- that the enumeration is complete in any sense at degree 10;
- that the spinor family is minimal, unique or canonical;
- anything that reads as completeness of the invariant ring.

## If someone later wants to run it

The job files are prepared under `cluster/`. Nothing in this paper depends on
the outcome, so it is a strengthening exercise rather than a blocker, and it
should be reported as `EXHAUSTIVE WITHIN THE DEFINED FINITE GRAMMAR` if it
terminates — not as exhaustion in any stronger sense.
