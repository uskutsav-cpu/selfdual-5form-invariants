# Internal response to referees A–D

Every objection is answered below with one of: **fixed** (the draft changed),
**limitation** (an explicit limitation was added), **already addressed** (with a
pointer), or **rejected** (with a reason). No objection is left unanswered, and
none was dismissed for being inconvenient.

Two of the sharpest objections — A6 and D3, raised independently — turned out to
identify a real gap in exposition. They are treated first.

---

## The exposition gap: A6 and D3 (spanning-set argument needs rational representatives)

**Objection.** The spanning-set argument (`dim_Q ≤ k` for a space spanned by `k`
explicit elements) requires the spanning elements to be defined over `Q`. If the
atlas elements exist only as modular coordinate vectors, the argument does not
apply, and three headline dimensions would revert to modular lower bounds.

**Investigated, not assumed.** An invariant in this project is specified by a
contraction graph, stored as an integer incidence pattern, and evaluated by
contracting copies of `F` with `eta` and `epsilon` — both integer-entried. Each
candidate is therefore a polynomial with **integer** coefficients in the 126
coordinates, fixed before any prime is chosen; the prime enters only at
evaluation. The spanning families for `A10`, `G10` and `P10` are integer families
in this sense, and the argument applies. `B10` is covered twice over, since its
structures are also lifted to `Q` outright.

**Status: fixed.** Section 6 now states this explicitly instead of leaving it
implicit. The objection did not change a result, but the paper was relying on a
step it had not spelled out, and a referee would have been right to stop there.

---

## Referee A — invariant theory

| # | objection | response |
|---|---|---|
| A1 | "Generic" rank certified at specific points | **Already addressed, now sharper.** A point exhibiting rank 81 bounds the generic rank from below; that is the only direction claimed. Appendix G states it explicitly. |
| A2 | Functional vs algebraic independence | **Already addressed.** Section 8.4 and appendix G both disclaim algebraic independence in terms. A gate fails the build if the disclaimer disappears. |
| A3 | Is `D10` a subspace? | **Fixed.** Section 9 now states that the induced map is linear on each graded piece and that `D10` is by construction a span, so the quotient is defined. |
| A4 | "Basis" where "spanning set" is honest | **Limitation added** (§14, item 10). The word is used loosely and the paper now says so. |
| A5 | Proposition 9.4 might read as a contribution | **Already addressed.** The disclaimer follows immediately after the proof, not only in an audit file. |
| A6 | Spanning-set argument needs rational representatives | **Fixed.** See above. |
| A7 | No Hilbert series cross-check | **Limitation added** (§14, item 11). We did not compute one; its absence is now stated rather than left for the reader to notice. |

## Referee B — spinors and real forms

| # | objection | response |
|---|---|---|
| B1 | Orientation selection is circular as a verification | **Accepted and fixed.** This was the strongest objection in the report. Section 5.3 now separates the selection criterion (rank 126) from the independent check (that `star F = +F` holds on the image), which is a property of the output rather than the criterion that produced it. |
| B2 | Signature dependence of `star^2` | **Fixed** by stating it in appendix A where the convention is set, given the project's history of confusing a Euclidean projector for an anti-self-dual one. |
| B3 | Reality of `Sym^2 S_+` differs between real forms | **Partially addressed.** The symmetry of `C Γ^(5)` is checked in the implementation rather than assumed (appendix C). We agree the exposition could separate the complexified and real statements further, and flag it for the mentor. |
| B4 | Equivariance check has low discriminating power if `χ ≡ 1` | **Accepted, not fully resolved.** Solving for `χ` catches errors that fail to commute with the group action; it would not catch one that does. Recorded for the mentor rather than papered over. |
| B5 | Does the `1/5!` cancel in the *integer* identity? | **Accepted and fixed.** It does not. Section 11 now states that the coefficients are normalisation-dependent, names the normalisation, and separates the normalisation-independent content (one-dimensionality, and which structures the generator is supported on). This was a real imprecision. |
| B6 | Abstract could be read as "invertible" | **Fixed.** The abstract now says injective, with image the gamma-traceless subspace, and explicitly a left and not a two-sided inverse. |

## Referee C — non-linear chiral field theory

| # | objection | response |
|---|---|---|
| C1 | Whose stress tensor is the theorem about? | **Accepted; escalated rather than resolved.** A new remark in section 10 states plainly that whether the flow's `τ` has the shape the theorem assumes is a question about the source's conventions, that we could not settle it from the published text, and that it is review item **G-10**. The improvement-independence makes survival likely, and the draft says "likely is not the standard the rest of this paper is held to." |
| C2 | The flow is referenced, not written down | **Fixed.** Section 9 now gives the flow schematically as equation (9.1) and states exactly what the argument consumes from it — the trace monomials and their starting degrees — both listed in appendix H. |
| C3 | "Does not reach three directions" invites a stronger reading | **Already addressed in §14, reinforced.** The generator-extension limitation is item 1; section 13 opens by restating that the result is about a construction. |
| C4 | The six-dimensional comparison is asserted | **Accepted.** Section 13 attributes the comparison to the cited works rather than asserting it independently. We did not verify their results and do not claim to. |
| C5 | Type IIB section raised then dropped | **Fixed.** The paragraph now opens by declaring itself motivation that establishes nothing, instead of arriving at that only in its final sentence. |
| C6 | Missing physical reading of the trace/reach connection | **Rejected for this draft.** It would be the most interesting sentence in the paper and we cannot currently support it. Speculation dressed as interpretation is worse than silence. Flagged as an open question. |
| C7 | Free vs deformed trace | **Fixed.** A new remark in section 10 states that the grading needs only where `Tr(τ)` begins, that the leading term of the deformed trace is the free trace, and that we make no claim the deformed trace vanishes — it generally does not, which is what makes the flow non-trivial. |

## Referee D — computational proof

| # | objection | response |
|---|---|---|
| D1 | Rhetorical weight of 15-cell agreement exceeds its evidential weight | **Accepted and fixed.** Section 8.3 was rewritten. It now says the agreement is corroboration and not independent confirmation, and redirects the weight onto the two recomputed cells and the single explicit minor, which does not depend on the matrix at all. |
| D2 | Cells record no source-critical hash | **Already disclosed, now connected.** The provenance limitation is stated in §8.4 and §14. We agree it connects to the orientation defect; the two recomputed cells postdate the fix, and the minor can be rechecked independently. |
| D3 | Spanning-set argument's reach | **Fixed.** See above. |
| D4 | One held-out prime leaves a `1/p` failure probability | **Limitation added** (§14, item 12), stated with the failure mode named as silent. |
| D5 | Two determinant routines share a modular layer | **Limitation added** (§14, item 13). The objection is correct and the mitigation is partial. |
| D6 | What would the Euler check catch? | **Rejected as a defect, accepted as a question.** Homogeneity is guaranteed by construction only if the differentiation is correct; the Euler check tests the differentiation, which is exactly the step it is meant to police. Appendix K states this. |
| D7 | Single point of failure in macro generation | **Limitation added** (§14, item 14), including the partial mitigation that gates parse artifact fields independently rather than comparing macros to each other. |
| D8 | Optional-dependency code path untested | **Limitation added** (§14, item 15), stated as an expectation rather than a verified claim. |
| D9 | How is cache sharing prevented, not discouraged? | **Partially addressed.** Section 6 describes immutable per-cell artifacts and read-only aggregation. We agree the architectural guarantee could be stated more strongly. |

---

## Summary

- **Fixed in the draft:** A3, A6, B1, B2, B5, B6, C2, C5, C7, D1, D3.
- **Limitations added:** A4, A7, D4, D5, D7, D8.
- **Escalated to the mentor:** C1 (as G-10), B3, B4.
- **Rejected with reasons:** C6, D6.
- **Already addressed, pointer given:** A1, A2, A5, C3, C4, D2, D9.

Net effect on results: **none**. No dimension, rank or identity changed. What
changed is that three steps the paper was leaning on without stating — the
rationality of the spanning families, the non-circular orientation check, and
the normalisation-dependence of the integer identity — are now stated, and six
new limitations are declared.
