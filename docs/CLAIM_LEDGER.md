# Claim ledger

Every scientific assertion this repository is permitted to make, with its
evidence class, its allowed manuscript wording, and the stronger wording that
is **forbidden**.

Baseline commit: `3ed32805b38ce34216b34888f6539e3538e90fb9`
Branch: `research/maximal-chiral-four-form-program`
Last updated: Phase 0 (baseline audit)

## Evidence classes

| class | meaning |
|---|---|
| `EXACT-THM` | proved by hand, no computer step |
| `EXACT-CA-THM` | proved, with a finite computer-checked certificate |
| `FINITE-ORDER` | exact but only up to a stated degree cutoff |
| `MOD-CERT` | modular (finite-field) certificate; characteristic-zero inference needs stated hypotheses |
| `RAT-RECON` | rational reconstruction, CRT-bounded, holdout-validated |
| `NUM-EV` | high-precision numerical evidence only |
| `CONJ` | conjecture |
| `HEUR` | heuristic |
| `BLOCKED` | external blocker |

**Global caveat applying to every `MOD-CERT` row.** A rank computed mod p is a
lower bound for the characteristic-zero rank, and equals it unless p divides a
relevant minor. We use ≥4 primes and observe identical ranks; that makes an
exceptional-prime coincidence unlikely but does **not** prove it. No row below
may be upgraded to `EXACT-THM` on the strength of prime agreement alone.

---

## C-ATLAS-01 — homogeneous invariant dimensions through degree 12

- **Wording**: "The spaces of homogeneous Lorentz invariants of a self-dual
  five-form in D=10 have dimensions 1, 2, 7, 14, 72 at degrees 4, 6, 8, 10, 12."
- **Assumptions**: generic self-dual five-form; the graph-contraction candidate
  set is complete at each degree; exact canonicalisation.
- **Range**: degrees 4–12.
- **Class**: `MOD-CERT` + `FINITE-ORDER`
- **Sources**: `results/10d_order12.json`, `src/sdinv/graphs.py`
- **Verification**: 15 primes, 4 samples/prime, identical ranks.
- **Independent verification**: **NOT DONE** (clean-room, Phase 10).
- **Permitted**: "exact ranks over several finite fields, identical at every
  prime tested."
- **Forbidden**: "proved dimensions"; "the invariant ring has these dimensions"
  (ring vs. space of homogeneous polynomials is not established here).
- **Caveats**: completeness of the candidate set relies on the multigraph
  argument, which is sound, plus exact canonicalisation for n ≤ 6 and pynauty
  above; see C-ATLAS-05.

## C-ATLAS-02 — degree-12 decomposition

- **Wording**: "At degree 12 there are 10 lower-degree product directions and
  62 connected primitive directions, total value-space rank 72."
- **Class**: `MOD-CERT` + `FINITE-ORDER`
- **Independent verification**: **NOT DONE**
- **Forbidden**: calling the 62 a basis of primitives of the invariant *ring*.

## C-ATLAS-03 — cumulative generic functional rank 81

- **Wording**: "The cumulative generic Jacobian rank through degree 12 is 81."
- **Assumptions**: genericity of the sample point; Jacobian rank at a generic
  point equals the functional rank.
- **Class**: `MOD-CERT`
- **Permitted**: "the cumulative Jacobian rank saturates the expected count 81
  = 126 − 45 at degree 12."
- **Forbidden**: "we have found all 81 invariants"; "the atlas is complete."
  Saturating a rank is not exhibiting a generating set.
- **Caveats**: 126 − 45 = 81 is a dimension count for a generic orbit, not a
  proof that these 81 generate the invariant ring.

## C-ATLAS-04 — I12_61 and I12_62 do not raise the rank

- **Wording**: "Ordered candidates I12_61 and I12_62 do not increase the
  cumulative Jacobian rank."
- **Class**: `MOD-CERT`
- **Forbidden**: **"these are polynomial syzygies."** A Jacobian dependence is
  not a polynomial identity. Calling them syzygies requires constructing and
  verifying an actual polynomial relation (Phase 3).
- **Caveats**: open proof obligation PO-03.

## C-ATLAS-05 — candidate-set completeness above degree 6

- **Wording**: "Candidate multigraphs are deduplicated by exact canonical form
  for n ≤ 6 and by pynauty above."
- **Class**: `EXACT-CA-THM` (given pynauty correctness)
- **Caveats**: an earlier Weisfeiler–Leman fallback was shown to collide on
  regular multigraphs (49 classes → 39 keys at order 6) and would silently
  *drop* candidates. Confirm pynauty is actually in the active path at every
  degree used; PO-01.

## C-SEXTIC-01/02/03 — intrinsic sextic basis

- **Wording**: "J6 = Tr(M³) = (32/3)·I6_1; K6 = −(1/1125)·I6_1 + (3/125)·I6_2;
  the change of basis has determinant 32/125 and quotient coordinate
  q6(c1,c2) = (125/3)·c2."
- **Class**: `RAT-RECON` + `EXACT-CA-THM`
- **Sources**: `results/stress_flow/change_of_basis/sextic_intrinsic.json`
- **Verification**: primes 32749/32719/32693, 4 samples each; an independently
  implemented dense N^(1050) cubic contraction agrees exactly on every sample.
- **Independent verification**: partial — the dense contraction is a genuine
  second implementation *within* this repository, not clean-room.
- **Permitted**: "exact change of basis, verified against an independent dense
  tensor contraction."
- **Forbidden**: claiming K6 is the published spinor invariant Σ₂. The source
  proves (Σ₁,Σ₂) is a sextic basis but does **not** publish the change of basis;
  our identification is inferred. See PO-04.

## C-STATIC-01 — static free-stress span

- **Wording**: "The static free-stress span has dimensions 1, 1, 2, 2, 4 at
  degrees 4, 6, 8, 10, 12."
- **Class**: `MOD-CERT` + `FINITE-ORDER`
- **Forbidden**: presenting this as the set a flow can reach. See C-CLOSURE-02.

## C-TRM6-01 — Tr(M⁶) coordinates are NOT certified

- **Wording**: "The degree-12 free-stress span is 4-dimensional. Tr(M⁶) is
  retained as a stress-adapted basis element; its coordinates in the 72-element
  graph basis are not certified."
- **Class**: rank is `MOD-CERT`; coordinates are `BLOCKED`
- **Evidence**: 15 primes, CRT modulus ≈ 5.2e67; **29 of 72 columns** exceed
  the uniqueness bound.
- **Permitted**: "the rank is certified; no certified rational coordinate
  vector exists at the current prime budget."
- **Forbidden**: quoting any rational coordinate vector for Tr(M⁶), including
  the entries under `rational_lift_audit.successfully_reconstructed_columns`
  (CRT terminating is not CRT being correct).
- **Caveats**: PO-05; Phase 2 must either find an analytic reduction or prove
  the theorems basis-independently.

## C-FLOW-01 — new-forcing dimensions

- **Wording**: "The new-forcing span of the interacting stress flow has
  dimensions 1, 1, 3, 5, 21 against full 1, 2, 7, 14, 72, leaving obstruction
  dimensions 0, 1, 4, 9, 51."
- **Assumptions**: analytic polynomial interactions; scalar trace generators;
  `Tr(tau)` excluded from forcing because it is the homogeneity operator.
- **Class**: `RAT-RECON` + `FINITE-ORDER`
- **Sources**: `results/stress_flow/interacting_flow_equations.json`
- **Verification**: fit primes 32749/32719/32693/32771/32713; independent
  holdout 32717; `all_modular_and_rational_holdouts_passed: true`.
- **Independent verification**: **NOT DONE**
- **Caveats**: a *single* holdout prime. The objective asks for two; PO-06.

## C-FLOW-02 — the K6 transport equation

- **Wording**: "The degree-six component of the flow obeys
  dq6/dλ = 10·(6−2)·a(λ)·q6 = 40·a(λ)·q6, where a is the coefficient of the
  Tr(τ) generator."
- **Assumptions**: the degree-6 sector closes (no higher-degree feedback);
  the generator set is complete at degree 6.
- **Range**: degree 6; **all orders in λ as a formal series**.
- **Class**: `EXACT-CA-THM`
- **Supporting facts now verified**: the generator enumeration is complete —
  18 expected multisets, 18 present, additivity of leading degrees holds for
  every generator (verified Phase 0). Only `tr_tau`, `tr_tau2`, `tr_tau3` have
  leading degree ≤ 6, and all three produce rows.
- **Permitted**: "an exact linear homogeneous transport equation, valid to all
  orders in λ as a formal power series at field degree six."
- **Forbidden**: "valid to all orders" without the words *formal* and *at
  degree six*. Convergence in λ is not established.

## C-FLOW-03 — K6 is transported, never created

- **Wording**: "q6(λ) = q6(0)·exp(40∫a). Hence q6(0)=0 ⟹ q6≡0, and q6(0)≠0 ⟹
  q6≠0 for all λ."
- **Class**: `EXACT-CA-THM` (immediate from C-FLOW-02)
- **Permitted**: "K6 is transported, never created."
- **Forbidden**: **"K6 must vanish in every pure stress flow"** — false for a
  seeded flow. Also forbidden: calling this a universal obstruction, or
  inferring it from the static span alone.
- **Caveats**: this is an off-shell, field-redefinition-fixed statement.
  Whether it survives field redefinitions and use of equations of motion is
  PO-07 and is **not** established.

## C-CLOSURE-01 — free-seed iterative closure

- **Wording**: "The iterative closure from the free seed has dimensions
  1, 1, 3, 11, 67."
- **Class**: `MOD-CERT` + `FINITE-ORDER`
- **Sources**: `results/stress_flow/closure_and_minimality.json`
- **Caveats**: computed under *seed* enlargement, which is not the same as
  adding a flow generator; see C-MIN-03.

## C-CLOSURE-02 — closure strictly exceeds the static span

- **Wording**: "The reachable set (1,1,3,11,67) strictly exceeds the static
  span (1,1,2,2,4) at degrees 8, 10 and 12."
- **Class**: `MOD-CERT`
- **Permitted**: "a no-go argument built on the static span alone is invalid."
- **Forbidden**: any claim that the static complement is a dynamical
  obstruction.

## C-MIN-01 — minimal completion through degree 8

- **Wording**: "Through degree 8 the completion requires exactly five
  directions — K6, I8_3, I8_4, I8_5, I8_6 — each non-redundant under removal."
- **Class**: `MOD-CERT` + `FINITE-ORDER`
- **Forbidden**: claiming minimality under *arbitrary* basis change; only
  removal-minimality within the fixed basis is shown. PO-08.

## C-MIN-02 — residual deficit

- **Wording**: "After that completion, degrees 10 and 12 retain deficits of 3
  and 4."
- **Class**: `MOD-CERT` + `FINITE-ORDER`
- **Status**: **the open target of Phase 1.**

## C-MIN-03 — seeding vs. generators

- **Wording**: "The closure analysis enlarges the seed, not the generator set."
- **Class**: `EXACT-THM` (definitional)
- **Forbidden**: presenting seeding results as `f(T,S,λ)` generator results.

## C-GEN-01 — generator enumeration complete

- **Wording**: "The 18 trace generators are exactly the multisets of Tr(τ^k)
  whose leading field degrees sum to at most 12."
- **Class**: `EXACT-CA-THM` (verified Phase 0: 18 expected = 18 present,
  none missing, none extra, additivity holds for all)
- **Caveats**: relies on `leading_field_degree` being correct per generator,
  which is itself computed; PO-02.

## C-REPRO-01 — test suite

- **Wording**: "96 tests pass at commit 3ed3280."
- **Class**: `EXACT-CA-THM` (software fact)
- **Status**: Phase 0 fresh-clone reproduction — see
  `docs/baseline_reproduction_maximal_program.md`.

---

## Claims that must be WEAKENED or are FORBIDDEN outright

| # | forbidden statement | why |
|---|---|---|
| F-1 | "K6 must vanish in every pure stress flow" | false for a seeded flow (C-FLOW-03) |
| F-2 | "I12_61/I12_62 are syzygies" | Jacobian dependence ≠ polynomial identity (C-ATLAS-04) |
| F-3 | any rational coordinate vector for Tr(M⁶) | uncertified (C-TRM6-01) |
| F-4 | "we have all 81 invariants" | rank saturation ≠ generating set (C-ATLAS-03) |
| F-5 | "all-orders theorem" from degree-12 data | no induction established |
| F-6 | "relevant to Type IIB" as a result | not a result; Phase 8 gate |
| F-7 | "independently reproduced" | no clean-room implementation yet (Phase 10) |
| F-8 | "K6 is the published spinor invariant Σ₂" | change of basis not in the source |
| F-9 | "the static complement is an obstruction" | contradicted by C-CLOSURE-02 |
| F-10 | "new nonlinear theory" | no theory constructed yet (Phase 6) |
