# Novelty ledger for the mentor draft

**Every row is PROVISIONAL and requires mentor confirmation.** Nothing in the
manuscript is described as new on the strength of this file alone.

The reason is not that the search is incomplete. A broader sweep was carried
out and is recorded in `MENTOR_DRAFT_REFERENCE_MATRIX.md`. The reason is that a
literature search establishes absence of evidence, not evidence of absence: a
mentor who knows the field can recognise a result the search would not surface
— an unpublished note, a different formulation of the same statement, a paper in
an adjacent literature. Upgrading a row is a judgement, and it is a human one.

## Claimed contributions

| # | contribution | closest prior work | what is genuinely different | wording used in the draft | status |
|---|---|---|---|---|---|
| 1 | `dim_Q A10 = 14`, certified | Twelve explicit degree-ten structures in arXiv:2509.14350 eq. (4.24), not claimed there as a basis | The source gives expressions; we give the dimension and a certified basis | "we determine the degree-ten graded dimension" | PROVISIONAL |
| 2 | `dim_Q B10 = 12` and its exact relations | Not stated in the source | The source gives expressions, not a rank | "the published structures span a twelve-dimensional subspace" | PROVISIONAL |
| 3 | `dim_Q(B10 ∩ P10) = 1` with an explicit integer generator | Not addressed anywhere we found | A negative structural result: the published span is not a product complement | "the published span contains one product direction" | PROVISIONAL |
| 4 | `A10 = G10 ⊕ P10` | Not stated | — | "the graph generators are a complement to the products" | PROVISIONAL |
| 5 | `dim_Q D10 = 11` and `dim_Q Q10 = 3` | The stress flow is from arXiv:2509.14351; what it misses at degree ten is not computed there | We compute the reachable subspace exactly over Q and exhibit the quotient | "we compute the subspace reachable by the stress flow and exhibit the quotient" | PROVISIONAL |
| 6 | Exact rational certification by CRT lifting with held-out-prime validation | The technique is standard computer algebra | Applying it to close the modular gap on these two spaces | "we establish both exactly over the rationals" — **not** "we introduce a method" | PROVISIONAL |
| 7 | Certified spinor/tensor bridge, exact over F_p | The gamma-matrix map is standard | The certificates, the exactness, the solved-for equivariance character | "we implement and certify the map" — **not** "we derive the map" | PROVISIONAL |
| 8 | Exact modular Jacobian replacing floating-point rank | The count 81 is analytic and is in arXiv:2509.14351 | The tolerance-free computation over the full 83-candidate family with an explicit 81×81 minor; a **lower bound** only | "the analytic count is reproduced as a rigorous lower bound" | PROVISIONAL |
| 9 | Analytic G-10 derivation, improvement-independent, with counterfactual | The tracelessness of the free stress tensor is standard | The improvement-independence and the demonstration that it is load-bearing | State as an input we derive, not as a discovery | PROVISIONAL |
| 10 | Orientation-branch defect and its fix | No analogue known | A convention-pinning defect specific to finite-field implementations | Report as a defect found and fixed, not as a research result | PROVISIONAL |
| 11 | Degree-eight tensor-word indispensability | Not addressed in the sources | Ablation within our own candidate families | "within the tested candidate-family decomposition" — never universal | PROVISIONAL |

## Explicitly NOT claimed as novel

- **The number 81.** It is analytic and it is in the literature. We claim the
  exact lower bound and the certificate, not the value.
- **The enumerate–evaluate–relate workflow.** It is the method of
  Elamaran–Ferko–Scarlett, arXiv:2512.23750, and the draft says so in the
  introduction and again in the methodology section.
- **The stress-flow construction.** It is from arXiv:2509.14351.
- **The gamma-matrix map itself.**
- **The cardinality bound** of proposition 9.4. Elementary linear algebra,
  stated because it converts a basis-dependent assertion into a basis-free one.
- **Hilbert-series dimensions.**
- **Majorana–Weyl existence** in signatures with `s − t ≡ 0 mod 8`.
- **Tracelessness of the free stress tensor** as a fact. What we add is that the
  vanishing is independent of the improvement coefficient, and the
  counterfactual showing the grading depends on it.

## Title check

The working title is *Exact degree-ten invariants of a self-dual five-form in
ten dimensions*. Every word is supported:

- "Exact" — the three headline dimensions are established over Q, not modulo p.
- "degree-ten" — the scope is exactly degree ten; degree twelve is excluded.
- "invariants" — not "invariant ring", which we do not present.

Forbidden formulations checked for and absent, enforced by a gate in
`manuscript/jhep/scripts/check_draft.py`: "complete invariant ring", "all-order
classification", "unique basis", "canonical basis", "complete through degree 12".

## The wording most likely to need a mentor's correction

Row 8. "Reproduced as a rigorous lower bound" is careful, but a reader skimming
could take the paper to be claiming 81. The draft states the split in the
abstract, in section 8.4 and in appendix G. A mentor should confirm the credit
is apportioned as they would apportion it — this is review item **G-5**.
