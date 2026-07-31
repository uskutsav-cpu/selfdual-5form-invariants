# The published degree-10 candidates in the atlas and in Q10

## 1. Stage-1 result — five candidates, six primes

Artifact `results/intrinsic_candidates/published_degree10_map.json`.

| prime | dim Q10 | P10_01 | P10_02 | P10_03 | P10_06 | P10_07 | Q10 rank |
|---|---:|---|---|---|---|---|---:|
| 32749 | 3 | `[0,0,0]` | `[0,0,0]` | `[0,0,0]` | `[0,0,0]` | `[0,0,0]` | **0** |
| 32719 | 3 | `[0,0,0]` | `[0,0,0]` | `[0,0,0]` | `[0,0,0]` | `[0,0,0]` | **0** |
| 32693 | 3 | `[0,0,0]` | `[0,0,0]` | `[0,0,0]` | `[0,0,0]` | `[0,0,0]` | **0** |
| 32771 | 3 | `[0,0,0]` | `[0,0,0]` | `[0,0,0]` | `[0,0,0]` | `[0,0,0]` | **0** |
| 32713 | 3 | `[0,0,0]` | `[0,0,0]` | `[0,0,0]` | `[0,0,0]` | `[0,0,0]` | **0** |
| 32717 | 3 | `[0,0,0]` | `[0,0,0]` | `[0,0,0]` | `[0,0,0]` | `[0,0,0]` | **0** |

`consistent: true`. Every entry has `status = "solved"` — each candidate lies
in the atlas span and its coordinates were obtained exactly. **The result is
not vacuous**: a candidate that merely failed to solve would also contribute
rank 0, for an entirely uninformative reason, and the `status` field is what
separates the two cases.

Cumulative Q10 rank after each addition: P10_01 → 0; P10_02 → 0; P10_03 → 0;
P10_06 → 0; P10_07 → 0.

## 2. Why the P10_07 entry is the important one

In the run immediately before this, `P10_07` did **not** read `solved`. It read
`not_in_atlas_span`, on all six primes.

That was correct behaviour by the projection, not a failure of it. The
evaluator was not computing a Lorentz scalar — it raised all six axes on both
inner `N^(1050)` factors, so three of its edges contracted with `delta` instead
of `eta` — and a non-scalar cannot lie in the span of genuine invariants. The
machinery refused it rather than returning a plausible wrong vector.

Full diagnosis in `PUBLISHED_DEGREE10_INDEX_AUDIT.md` §3 and ledger entry
`C-P10-BUG-01`. The distinction that matters for reading the table above:

> `status: "solved"` with a zero vector means *the candidate was computed and
> lies inside D10*. `status: "not_in_atlas_span"` means *nothing was
> established about the candidate at all*.

A rank of 0 assembled from `not_in_atlas_span` rows would have been worthless.
All thirty entries above are `solved`.

## 3. What this does and does not say

**Permitted**: "the five implemented equation-(4.24) candidates lie inside the
computed reachable closure D10 and have zero image in Q10 under the stated
formal flow definition, at six primes."

**Forbidden**, each an available misreading:

1. **Not** that Q10 has no compact tensor representation. Q10 has dimension 3;
   these candidates simply do not reach it.
2. **Not** that the candidates are redundant or trivial. They are nonzero
   elements of the degree-10 invariant ring that happen to lie in D10.
3. **Not** that the remaining seven behave the same way. That is a separate
   measurement, in progress.
4. **Not** anything about degree 12.

## 4. Pattern across degrees — recorded, not concluded

Every compact published structure tested so far, at either degree, has zero
image in its quotient:

| structure | degree | quotient | image |
|---|---:|---|---|
| complete M-only family | 10 | Q10 (dim 3) | rank 0 |
| P10_01, 02, 03, 06, 07 | 10 | Q10 (dim 3) | rank 0 |
| P12_01, P12_02, P12_03 | 12 | Q12 (dim 4) | rank 0 |

This is a suggestive pattern and it is **not** a theorem. It is consistent with
at least two very different explanations, and the data here does not separate
them:

- the published candidates genuinely span only D10 and D12, so a compact
  representative of the quotient must be sought outside the published lists; or
- the formal flow definition used to build D is broader than the physical one,
  making D larger than it should be and the quotient correspondingly harder to
  reach.

Distinguishing these is proof obligation PO-03 and is not addressed here.
