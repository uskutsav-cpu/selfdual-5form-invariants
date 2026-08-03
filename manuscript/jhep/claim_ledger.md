# Claim ledger — mentor-review draft

One row per major claim. `Type` uses the classification of table 13 in the
manuscript. `Artifact` names the file a reviewer should open to check the number;
`Script` names what produced it.

Commit: recorded in `build_manifest.json` alongside the SHA-256 of every
artifact. Certificate hashes are in
`results/mentor_draft/scientific_input_manifest.json`.

---

## Central claims

### C-01 · `dim_Q A10 = 14`
- **Wording:** "the full degree-ten invariant space has dimension 14"
- **Location:** abstract; §9 theorem 5 [`thm:reach`]; table 5 [`tab:degree10`]
- **Type:** exact finite-field certificate, carried to `Q` by the spanning-set argument
- **Artifact:** `results/stress_flow/Q10_characteristic_zero.json`
- **Script:** `scripts/d10_characteristic_zero.py`
- **Why it is exact over Q:** the atlas is spanned by 14 explicit
  integer-coefficient polynomials, so `dim_Q ≤ 14` independently of any prime;
  modular rank 14 forces equality. Stated in §6.
- **Status:** settled

### C-02 · `dim_Q D10 = 11`
- **Wording:** "the subspace reachable by the stress flow has dimension 11"
- **Location:** abstract; §9 theorem 5 [`thm:reach`]; appendix H
- **Type:** exact rational certificate
- **Artifact:** `results/stress_flow/D10_characteristic_zero.json`
- **Script:** `scripts/d10_characteristic_zero.py`
- **Instrument:** fixed point in `Fraction` arithmetic after CRT lift of 9
  non-integral rows across 5 primes, validated at held-out prime 32771; explicit
  non-vanishing 11×11 integer minor
- **Status:** settled. **Depends on C-06.**

### C-03 · `dim_Q Q10 = 3`
- **Wording:** "three independent degree-ten directions the flow does not reach"
- **Location:** abstract; §9 theorem 5 [`thm:reach`]
- **Type:** exact rational certificate
- **Artifact:** `results/stress_flow/Q10_characteristic_zero.json`
- **Status:** settled. **Depends on C-02 and C-06.**
- **Note:** an equality, not a bound. Running over `Q` removes the modular
  admission test that made the predecessor a lower bound.

### C-04 · `dim_Q(B10 ∩ P10) = 1`, with explicit generator
- **Wording:** "the published span meets the product sector in exactly one dimension"
- **Location:** abstract; §11 theorem 10 [`thm:bp`]; equation (11.1) [`eq:bpidentity`]
- **Type:** exact rational certificate
- **Artifact:** `results/degree10/B10_P10_intersection_exact.json`,
  `..._generator.json`
- **Script:** `scripts/b10_p10_characteristic_zero.py`
- **Instrument:** CRT across 7 primes, held-out prime 32783, identity re-verified
  at fresh prime 32869 on 6 fresh samples
- **Caveat:** the integer coefficients are normalisation-dependent; §11 says so.
- **Status:** settled

### C-05 · Generic functional rank ≥ 81
- **Wording:** "the analytic count is reproduced as a rigorous lower bound"
- **Location:** abstract; §8; appendix G
- **Type:** exact finite-field certificate → characteristic zero
- **Artifact:** `results/rank81/minor81_certificate.json`,
  `results/rank81/full_rank_matrix_publication_final.json`
- **Script:** `scripts/aggregate_rank_matrix.py`
- **The matching upper bound is analytic and is cited, not proved here**
  (arXiv:2509.14351).
- **Status:** lower bound settled; the value 81 is not claimed as ours

### C-06 · Free stress-tensor trace vanishes at quadratic order (G-10)
- **Wording:** "`Tr(τ)` first contributes at field degree four"
- **Location:** §10 theorem 7 [`thm:gten`]; appendix I
- **Type:** analytic theorem, with computational control
- **Artifact:** `results/stress_flow/G10_publication_certificate.json`,
  `G10_counterfactual.json`
- **Script:** `tests/test_G10_trace_activation.py`
- **Load-bearing:** yes — the counterfactual gives `Q10 = 0`
- **Status:** proved for a stress tensor of the standard `p`-form shape with
  arbitrary improvement coefficient. **Whether the flow's `τ` has that shape in
  the source's intended formulation is review item G-10.**

### C-07 · Bridge rank 126 with exact left inverse
- **Location:** §5 proposition 1 [`prop:bridge`]; appendix C
- **Type:** exact finite-field certificate
- **Script:** `spinor_trace_bridge/tests/`
- **Status:** settled

### C-08 · Tensor and spinor spans agree at `d = 4, 6, 8, 10`
- **Location:** §7; table 2 [`tab:degranks`]; figure 1 [`fig:degranks`]
- **Type:** exact finite-field, multi-prime, with held-out validation
- **Status:** settled for the families constructed

### C-09 · Tensor words indispensable at degree eight
- **Wording:** "within the tested candidate-family decomposition" — **the
  qualifier is mandatory and is enforced by a gate**
- **Location:** §7.2; figure 2 [`fig:ablation`]
- **Type:** ablation
- **Status:** settled as qualified; **not** a uniqueness theorem

### C-10 · Cardinality minimality
- **Location:** §9.4 proposition 6 [`prop:cardinality`]
- **Type:** analytic theorem
- **Status:** proved. **Explicitly not novel** — elementary linear algebra.

### C-11 · Orientation branch pinned by construction
- **Location:** §5.3; appendix B
- **Type:** analytic + regression
- **Status:** fixed. No published value changed.

---

## Open and delimited

| id | claim | status |
|---|---|---|
| O-01 | Removal minimality of the exhibited closing set | open outside the fixed graph basis |
| O-02 | Minimality under arbitrary `GL` change of basis | not attempted |
| O-03 | Generator extension: would a larger generator set reach more? | not addressed |
| O-04 | Complete degree-twelve tensor–spinor equivalence | not claimed; degree 12 is partial input only |
| O-05 | Full invariant-ring presentation / Hilbert series | not computed |
| O-06 | All-order flow theorem | not offered |
| O-07 | AMB-01/02 source ambiguity | avoided, not resolved — needs the source's authors |
| O-08 | 13 of 15 rank-matrix cells not independently recomputed | disclosed |
| O-09 | Physical meaning of the three missed directions | open |
| O-10 | Optional-dependency code path not certified both ways | disclosed |

---

## Claims requiring the mentor's attention

Ordered by how much rests on them.

1. **G-10 — which stress tensor.** C-06, and through it C-02 and C-03. The
   theorem is improvement-independent, which is reassuring, but whether the
   flow's `τ` is of the assumed shape is a question about the source's
   conventions. *This is the single most load-bearing unconfirmed input.*
2. **Interpretation of `D10`.** Is "reachable by the stress flow" the right name
   for what the closure computes?
3. **Credit for rank 81.** The draft claims the exact lower bound and the
   certificate, never the number. Is that apportionment right?
4. **Split versus Lorentzian.** The draft states the two real forms are *not*
   related by a real orthogonal frame transformation, correcting an earlier error
   in this project. Confirm.
5. **Orientation convention.** Is the branch we pin the one intended?
6. **Physical significance of `Q10`.** The draft declines to interpret. Too
   cautious, or right?
7. **Type IIB scope.** The draft makes no Type IIB claim at all. Correct?
8. **Novelty wording.** Every row of the novelty ledger is PROVISIONAL. None may
   be upgraded without a human who knows the field.
9. **Published-basis correction.** C-04 says the published span is not a product
   complement. The framing is deliberately non-critical; confirm it reads that
   way.
10. **Title.** *Exact degree-ten invariants of a self-dual five-form in ten
    dimensions.* Every word is checked against the novelty ledger.
