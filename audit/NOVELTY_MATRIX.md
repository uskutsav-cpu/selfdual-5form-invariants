# Novelty matrix

**Every row is marked PROVISIONAL — REQUIRES COAUTHOR CONFIRMATION.** Nothing
here may be described as new in the manuscript until a coauthor with knowledge of
the field signs off. What this file records is the evidence available now, and
the safest wording that evidence supports.

Literature consulted directly (not from summaries or search snippets):

- Cederwall, Hutomo, Kuzenko, Lechner, Sorokin, *Some remarks on invariants*,
  J. Phys. A **59** (2026) 065203, doi:10.1088/1751-8121/ae3bb8;
  arXiv:2509.14350v2 (revised 29 Jan 2026). Consulted 2026-07-30/31.
- Hutomo, Lechner, Sorokin, *On non-linear chiral 4-form theories in D=10*,
  arXiv:2509.14351v2 (revised 6 Jan 2026); no journal reference listed as of
  2026-07-31. Consulted 2026-07-31.

| # | claimed contribution | closest prior result | overlap | difference | safe wording | status |
|---|---|---|---|---|---|---|
| 1 | Degree-ten atlas is 14-dimensional, certified | Twelve explicit degree-ten structures given in arXiv:2509.14350 eq. (4.24); not claimed to be a basis, relations not determined | The twelve structures are a subset of our span | We determine the dimension, exhibit a basis, and certify it at two primes | "we determine the degree-ten graded dimension and give a certified basis" | PROVISIONAL |
| 2 | Published span is 12-dimensional and its relations are exact | Not stated in the source | none known | The source gives expressions, not a rank | "the published structures span a twelve-dimensional subspace" | PROVISIONAL |
| 3 | Published span is **not** a product complement (its non-product content is 11) | Not addressed in the source | none known | This is a negative structural result; we found it by direct computation after nearly asserting the opposite | "the published span contains one product direction" | PROVISIONAL |
| 4 | $A_{10} = G_{10}\oplus P_{10}$ | Not stated | none known | — | "the graph generators are a complement to the products" | PROVISIONAL |
| 5 | $\dim Q_{10} = 3$ with explicit representatives | The stress-flow construction appears in arXiv:2509.14351; the size of what it misses at degree ten is not computed there | The flow itself is theirs | We compute the reachable subspace and the quotient | "we compute the subspace reachable by the stress flow and exhibit the quotient" | PROVISIONAL |
| 6 | Formula-independent reverse recovery of $Q_{10}$ | No analogue known | none known | Methodological | "a bounded search independent of the published formulas recovers the same quotient span" | PROVISIONAL |
| 7 | Exact basis maps among graph, published and compact bases | Not present | none known | — | "explicit change-of-basis matrices, validated on holdout samples" | PROVISIONAL |
| 8 | Split-signature identification of the oscillator frame | Standard representation theory; the specific identification for this implementation is ours | The mathematics is textbook | The correction of a recorded error is what is new *here*, and it is not a research novelty | **Do not claim as novel.** State as a convention clarification | PROVISIONAL |
| 9 | Explicit convention-controlled spinor/tensor bridge, exact over $\mathbb{F}_p$ | The gamma-matrix map is standard; a machine-checked implementation with certified kernel and image is not in the literature we consulted | The formula is standard | The certificates, the exactness and the equivariance solve-for-character are ours | "we implement and certify the map"; **not** "we derive the map" | PROVISIONAL |
| 10 | Exact modular Jacobian replacing float64 finite differences | The count 81 is analytic and is in arXiv:2509.14351 | The number is theirs | The exact, tolerance-free computation is ours, over the complete 83-candidate selection, with an explicit 81x81 minor; it is a lower bound only | "the analytic count is reproduced as a rigorous lower bound by an exact computation" | PROVISIONAL |
| 11 | Cardinality bound `|S| >= dim Q` making minimality basis-independent | Elementary linear algebra; the rank-nullity style argument is textbook | The mathematics is entirely standard | Nothing. It is included because it discharges half of PO-08, not because it is new | **Do not claim as novel.** State as a proposition with proof and no priority language | PROVISIONAL |

## Explicitly NOT claimed as novel

- The number 81. It is analytic and it is in the literature.
- The Hilbert-series dimensions.
- The stress-flow construction.
- The gamma-matrix map itself.
- The cardinality bound of section 6.4. It is standard linear algebra, stated
  because it converts a basis-dependent assertion into a basis-free one.
- Majorana–Weyl existence in signatures with $s-t\equiv 0 \bmod 8$.

## Search coverage and its limits

A broader sweep has since been carried out and is recorded in
`RELATED_WORK_COMPLETE.md`, which audits six papers directly at their arXiv or
publisher landing pages and states for each whether it pre-empts any claim here.
`RELATED_WORK_SEARCH.md` records the earlier, narrower pass.

Every row nonetheless stays **PROVISIONAL**, and the reason has changed. It is no
longer that the search is outstanding. It is that a literature search establishes
absence of evidence, not evidence of absence: a coauthor who knows the field can
recognise a result the search would not surface — an unpublished note, a
different formulation of the same statement, a paper in an adjacent literature.
Upgrading a row is therefore a judgement, and it is a human one.

No row may be upgraded on the strength of this file alone.
