# Independent mathematical audit — completed continuation

Frozen target: `2b7663bbf5a06d1340973434f195a84ae2773e8f`. All assigned graph-only mathematical checks below passed in the fresh phase02 environment. This does not change the failed phase01 source-transcription finding or certify that disputed literature mapping.

| Check | Completed observation |
|---|---|
| Stored 81×81 minors | Independent integer Bareiss residues: 20345, 30761, 1653, 2167. |
| Fresh independent 81×81 minors | Bareiss on independently recomputed rows: 50021: 35642, 32749: 22345. |
| Fresh forward-dual oracle | 81 values and 81 directional derivatives agree at each of two fresh points, primes 50021 and 32749. |
| Independent reverse rows | All 162 selected full 126-entry rows agree with production and independent forward dual; four additional I12_61/I12_62 rows agree with independent forward dual. |
| Conventions | Independent star²=+1, dimension 126, integral direction hash, all 81 ordered formulas/edge placements/topologies pass. |
| Automorphism signs | All 136 automorphisms across 81 graphs enumerated; zero negative induced signs. |
| Relabeling / odd-slot signs | 81 numerical graph relabelings, 81 numerical odd slot swaps, and 823 structural adjacent-vertex swaps/inverses pass. |
| Value-only derivative interpolation | Exact finite-field interpolation checks one representative each at degrees 4, 6, 8, 10, 12. |

## Degree-twelve homogeneous polynomial space

Each matrix has 72 rows: ten explicit lower-product polynomials and 62 connected graph polynomials. Gradients at distinct points within one prime are concatenated horizontally; different primes are never mixed.

| Prime | Fresh points | Matrix | Rank | Independent integer-minor residue |
|---:|---:|---|---:|---:|
| 50021 | 2 | 72×252 | 72 | 43334 |
| 32749 | 2 | 72×252 | 72 | 12699 |

The nonzero stacked-gradient minors independently prove linear independence of the 72 homogeneous polynomials over characteristic zero. This lower bound is separate from functional rank 81. It does not assert algebraic independence of 72 degree-twelve polynomials, a complete invariant-ring presentation, or the literature upper bound itself.

## Reproduction and limits

`METHOD.md` gives derivations, algorithms, arithmetic bounds and independence qualifications. `SCRIPT_PROVENANCE.json` discloses the authorized reuse of independently authored script source; all numerical results, environments and intermediates are fresh. Command records in `../commands/math_*/` contain exact arguments, working directories, runtimes, exits and stdout/stderr hashes.

`MATH_SUMMARY.json` contains exact counts and seeds. `degree12_polynomial_gradient_certificate.json` preserves full 72×252 matrices, fresh coordinates, all point gradients, pivot columns, complete integer determinants and residues. `reverse_gradient_results.json` and `fresh_dual_comparison.json` preserve derivative comparisons. `permutation_sign_results.json`, `automorphism_sign_results.json`, and `interpolation_derivative_results.json` preserve sign and interpolation evidence.

The independent forward and reverse programs share this audit's custom forward contraction kernel. Both use NumPy/BLAS primitives, also used by production, with independently checked exact integer bounds below 2^53. No production evaluator, Hodge builder, tree planner, coordinate projector, rank sieve or verifier is imported by these independent programs. The edge records remain the specified frozen inputs; they were validated, not independently rediscovered. No 72-point value matrix is claimed: independently validated stacked gradients replaced that more expensive plan.

The root's separate pure-Python orbit-action implementation was reviewed read-only for its sign conventions and lifting argument. Its 45 integral infinitesimal generators and nonzero modular orbit minor support generic orbit dimension 45. The global upper bound 126−45=81 uses tensor-contraction invariance, not sampled tangent annihilation alone. This branch did not duplicate that computation.
