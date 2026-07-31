# Independent reverse graph-to-block benchmark at degree 10

## 1. What this is, and why independence matters

The twelve published equation-(4.24) candidates span Q10. That is a forward
result: the formulas were transcribed, implemented, and projected. This
benchmark asks the same question from the other end — enumerate compact
quadratic-block contractions directly and see whether the quotient is reached
**without being told the answer**.

Independence is enforced, not promised.
`src/sdinv/reverse_block_decomposition.py` does not import
`published_degree10_invariants`, and
`tests/test_reverse_block_decomposition.py::test_reverse_engine_does_not_import_the_published_formulas`
parses the module's AST and fails if it ever does. The published result is used
only after a span has been recovered, for comparison.

## 2. Why a naive search is impossible, and what makes this one work

A degree-10 scalar is five quadratic blocks, each degree 2 in `F`: `M`
(2 slots), `N^(1050)` (6 slots), `N^(4125)` (6 slots). Five `N` blocks give 30
index slots, and a perfect matching of raw slots would be

    29!! ~ 6.2 x 10^15

which is not searchable.

The slots are not distinguishable. `composite_n1050` antisymmetrises axes
(0,1,2,3,4), so those five slots are interchangeable up to sign and only axis 5
is distinct. Each block therefore has **slot classes**:

| block | class A | class B |
|---|---|---|
| `M` | 2 slots | — |
| `N^(1050)` | 5 slots, antisymmetric | 1 slot |
| `N^(4125)` | 6 slots | — |

A contraction is then fully described by how many edges join each ordered pair
of `(block, class)` endpoints — a small integer enumeration with degree
constraints, rather than a matching over 30 labelled slots.

### Pruning, in the order applied

1. **Forbidden traces.** An edge joining two class-A slots of the *same* block
   contracts two indices inside an antisymmetric group and vanishes
   identically. Rejected before any arithmetic, so structural nulls never
   reach the evaluator.
2. **Degree feasibility.** Every block must saturate its slot count exactly.
3. **Connectivity.** A disconnected topology factorises into a product of
   lower-degree invariants, lives in the product subspace, and cannot carry a
   primitive direction.
4. **Canonicalisation.** Topologies related by relabelling like blocks describe
   the same scalar; the lexicographic minimum over that permutation group is
   the canonical key.

Index placement follows the rule the forward work paid for: **every contracted
edge carries exactly one raised end**, enforced by
`test_build_einsum_raises_exactly_one_end_of_every_edge`. An edge joining two
equally-placed slots contracts with `delta` instead of `eta` and is not a
Lorentz scalar — the exact defect that shipped in `P10_07`.

## 3. Enumeration, all 21 sectors

Block multisets are ordered **cheapest first** by total slot count. An earlier
ordering put the 30-slot all-`N` sector first and the survey stalled inside it;
the `M`-heavy sectors are 10 slots and complete instantly.

| sector | slots | canonical | selected | truncated | enum time |
|---|---:|---:|---:|---|---:|
| M+M+M+M+M | 10 | 1 | 1 | no | 0.0 s |
| M+M+M+M+N1050 | 14 | 4 | 4 | no | 0.0 s |
| M+M+M+M+N4125 | 14 | 1 | 1 | no | 0.0 s |
| M+M+M+N1050+N1050 | 18 | 46 | 40 | no | 0.3 s |
| M+M+M+N1050+N4125 | 18 | 19 | 19 | no | 0.0 s |
| M+M+M+N4125+N4125 | 18 | 5 | 5 | no | 0.0 s |
| M+M+N1050+N1050+N1050 | 22 | 289 | 40 | no | 5.2 s |
| M+M+N1050+N1050+N4125 | 22 | 208 | 40 | no | 0.8 s |
| M+M+N1050+N4125+N4125 | 22 | 55 | 40 | no | 0.1 s |
| M+M+N4125+N4125+N4125 | 22 | 8 | 8 | no | 0.0 s |
| M+N1050+N1050+N1050+N1050 | 26 | 1793 | 40 | **yes** | 85.8 s |
| M+N1050+N1050+N1050+N4125 | 26 | 1603 | 40 | no | 16.1 s |
| M+N1050+N1050+N4125+N4125 | 26 | 652 | 40 | no | 2.6 s |
| M+N1050+N4125+N4125+N4125 | 26 | 116 | 40 | no | 0.7 s |
| M+N4125+N4125+N4125+N4125 | 26 | 15 | 15 | no | 0.3 s |
| N1050 x5 | 30 | 3014 | 40 | **yes** | 97.6 s |
| N1050 x4 + N4125 | 30 | 4667 | 40 | **yes** | 66.4 s |
| N1050 x3 + N4125 x2 | 30 | 3057 | 40 | **yes** | 34.0 s |
| N1050 x2 + N4125 x3 | 30 | 834 | 40 | no | 8.6 s |
| N1050 + N4125 x4 | 30 | 120 | 40 | no | 2.2 s |
| N4125 x5 | 30 | 15 | 15 | no | 0.8 s |
| **total** | | **16 522** | **588** | 5 sectors | ~322 s |

**Five sectors are truncated** at the 30 000 raw-topology cap, so their
canonical counts are lower bounds and those sectors are **not exhausted**. This
is a bounded pilot, and the search space is not closed.

## 4. Cost model

Measured at prime 32749:

| quantity | value |
|---|---:|
| quadratic-block build, per sample | 4.4 s |
| one contraction, heaviest sector | ~150 ms |
| atlas construction, 14 columns x 22 samples | 34 s |
| evaluation, 588 candidates x 22 samples | ~130 s per sample |

Evaluation is **sample-outer**: each sample's three blocks are built once and
every candidate is swept against them. Candidate-outer would rebuild the blocks
for every (candidate, sample) pair — 4.4 s of setup for 150 ms of work, thirty
times the cost of the thing being measured. Caching all 22 samples' blocks
instead would hold ~350 MB, which this machine does not have.

**Projected cost of an exhaustive search.** Taking the untruncated canonical
counts as a lower bound of 16 522 candidates, at 22 samples and ~150 ms:

    16 522 x 22 x 0.15 s  ~  15 hours

on one worker, and that is a *lower* bound because five sectors are truncated.
Exhausting the declared space is a multi-day job at this throughput, not a
session-scale one.

## 5. Result

See `results/intrinsic_candidates/degree10_reverse_benchmark.json` for the
machine-readable record, including every recovered quotient vector and the
einsum specification of the candidate that produced it.

## 6. Scope

**Permitted**: statements about what the *bounded pilot* covered — 588 of at
least 16 522 canonical candidates, 40 per sector, one fit prime.

**Forbidden**: any claim that the degree-10 block search space has been
exhausted. It has not. Five sectors are truncated at enumeration and every
sector above 40 canonical candidates is sampled rather than swept.
