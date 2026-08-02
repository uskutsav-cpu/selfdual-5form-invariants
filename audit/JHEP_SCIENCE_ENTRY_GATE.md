# JHEP Stage 1 --- science entry gate

Generated 2026-08-02T01:32:11+00:00 at `0206f4e2cb28` by `scripts/emit_jhep_science_gate.py`.

## Verdict: **PASS**

| gate | subject | status | checks |
|---|---|---|---|
| 1.1 | Exact Clifford and real-form structure | **PASS** | 16/16 |
| 1.2 | Exact tensor-spinor bridge and its inverse | **PASS** | 22/22 |
| 1.3 | Candidate accounting and the rank-81 certificate | **PASS** | 154/154 |
| 1.4 | Degree-resolved tensor-spinor span equivalence | **PASS** | 55/55 |
| 1.5 | Degree-ten application | **PASS** | 10/10 |
| 1.6 | Degree-twelve scope decision | **NOT APPLICABLE --- EXCLUDED FROM THIS MANUSCRIPT'S CLAIM SCOPE** | 0/0 |

A gate is `PASS` only when every predicate over its artifacts holds.
`PARTIAL` means every predicate holds but the specified evidence matrix
is not yet filled. `FAIL` means a predicate is false.

## 1.1 Exact Clifford and real-form structure

**Status: PASS**

*Requirement.* Clifford metric extracted from anticommutators; split oscillator realisation; Hodge square per signature; the four real forms kept distinct; frame map exact.

*Evidence.*

- `spinor_trace_bridge/results/bridge_validation.json`
- `spinor_trace_bridge/docs/REAL_FORM_DICTIONARY.md`
- `spinor_trace_bridge/docs/HODGE_STAR_CONVENTIONS.md`

All 16 checks hold.

> The oscillator frame's real form is split (5,5), not Euclidean SO(10): a null frame has isotropic vectors and Euclidean signature has none. There *^2 = +1 on five-forms exactly as in Lorentzian (1,9), so real self-dual five-forms exist in both.

> (5,5) and (1,9) are INEQUIVALENT real forms. They are not related by a real orthogonal frame transformation and the manuscript must not say they are. Both metrics have discriminant -1 up to squares, so they are congruent over C and over F_p, and the bridge constructs that congruence explicitly.

## 1.2 Exact tensor-spinor bridge and its inverse

**Status: PASS**

*Requirement.* Phi : Lambda^5_+ V -> Sym^2_{gamma-tr} S_+ with domain 126, codomain 126, forward rank 126, zero kernel on the selected channel, exact round trip, linear scaling, and equivariance.

*Evidence.*

- `spinor_trace_bridge/results/bridge_validation.json`
- `spinor_trace_bridge/docs/BRIDGE_DERIVATION.md`

All 22 checks hold.

> The kernel and image statements are SPAN equalities, not dimension coincidences: the certificate compares row spaces, not just ranks.

> Reflections generate the full orthogonal group by Cartan-Dieudonne, so checking two- and four-reflection elements certifies equivariance on the group, not on a sample of it.

## 1.3 Candidate accounting and the rank-81 certificate

**Status: PASS**

*Requirement.* 83 planned, 83 evaluated, 0 errors, 0 interrupted, 0 silently skipped, 0 zero rows, Euler homogeneity 83/83; exact modular Jacobian; explicit 81x81 minor with nonzero determinant from two independent routines; integer-lift argument; matrix over three samples, three fitting primes, two holdout primes.

*Evidence.*

- `results/rank81/certificate_matrix.json`
- `results/rank81/cells/cell_p{prime}_s{seed}.json (one per cell)`
- `results/rank81/minor81_certificate.json`
- `docs/RANK81_CHARACTERISTIC_ZERO_PROOF.md`

All 154 checks hold.

> Sample x prime matrix: 3/3 seeds [11, 22, 33], 3/3 fitting primes [32717, 32719, 32749], 2/2 holdout primes [32693, 32713], 15/15 cells. Complete.

> Each cell is an immutable per-(prime, seed) artifact written atomically under a lock; the certificate is assembled by a read-only aggregator that fails on a missing, duplicated, incomplete or inconsistently ordered cell rather than producing a partial certificate that reads as a whole one.

> What the computation gives is the LOWER half only. The coordinate basis is integral, so each Jacobian is the reduction of an integer matrix and rank_{F_p} <= rank_Q holds unconditionally; hence rank_Q >= 81. The matching upper bound 126 - 45 = 81 is analytic, from the generic stabiliser dimension, and is not supplied by any computation here.

> Rank 81 among 83 functions means at least two functional dependencies. The manuscript must never say '83 algebraically independent invariants'.

## 1.4 Degree-resolved tensor-spinor span equivalence

**Status: PASS**

*Requirement.* At each certified degree: tensor rank, spinor rank, union rank, span equality in both directions, a fitted change of basis, and holdout validation on samples not used in the fit.

*Evidence.*

- `verification/spinor_trace_comparison.json`
- `verification/COMMON_SAMPLE_REGISTRY.json`
- `verification/degree8_span_equality.json`

All 55 checks hold.

> p=32749 d=8: port-graph-only spinor rank 6 against tensor rank 7; containment is strict and this is a property of that candidate family, not of the bridge. Degree 8 is settled by verification/degree8_span_equality.json with the full family.

> Equal dimension is not equal span, and the certificate never uses it as one: containment is checked in both directions and a change of basis is fitted on one sample set and validated on a disjoint one.

> Degree 12: NO spinor-side enumeration exists, so no degree-12 span equivalence is claimed. Degree 12 enters only through the tensor-side atlas and through the degree-12 block of the 83-candidate Jacobian.

## 1.5 Degree-ten application

**Status: PASS**

*Requirement.* dim A10 = 14, dim D10 = 11, dim Q10 = 3, P10 contained in D10, reproduced at more than one prime.

*Evidence.*

- `results/intrinsic_candidates/degree10_space_incidence.json`

All 10 checks hold.

> This is an APPLICATION of the invariant framework in this manuscript, not its headline. The obstruction itself is allocated to the Letter; see docs/PUBLICATION_CLAIM_ALLOCATION.md.

## 1.6 Degree-twelve scope decision

**Status: NOT APPLICABLE --- EXCLUDED FROM THIS MANUSCRIPT'S CLAIM SCOPE**

*Requirement.* Degree 12 may enter the title, abstract or central claims only with a complete atlas, a verified product/primitive split, an exact rank certificate, a trace/spinor comparison, holdout validation, and no silently omitted candidate sector.

*Evidence.*

- `results/10d_order12.json`

All 0 checks hold.

> Degree 12 is excluded from this manuscript's claim scope. There is a degree-12 tensor atlas but no spinor-side degree-12 enumeration, so no comparison, no holdout validation and no span equivalence exist to state.

> What the manuscript MAY say: the degree-12 block of the 83-candidate Jacobian, which is certified as part of the rank calculation; clearly labelled partial higher-degree evidence; and future work.

> What it may NOT say: degree-12 tensor-spinor equivalence; a complete degree-12 spinor atlas; a degree-12 basis map; or complete equivalence through degree 12.

> Building a degree-12 spinor enumeration is out of scope for this manuscript. No theorem in it requires one.

