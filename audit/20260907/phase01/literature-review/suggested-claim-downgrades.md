# Suggested claim downgrades — separate from frozen source

Frozen commit: `2b7663bbf5a06d1340973434f195a84ae2773e8f`. Date: 2026-09-07. No manuscript or code edits made. These are wording recommendations and proof-obligation assessments, not new scientific claims.

**STOP status.** After this partial review, the coordinator reported a definite mismatch between the frozen degree-ten J10–J12 antisymmetrizers and independently transcribed primary PDF/TeX. Exact details belong to the separate source-review report. Numerical agreement among implementations of the same incorrectly transcribed formula cannot establish agreement with the publication. The graph-only certificate has a separate dependency path.

1. **Define “basis” and “completion” narrowly.** Target title and lines18–20 should say “maximal generically independent family of81 explicit invariant polynomials” or “a certificate for generic functional independence of81 graph contractions.” An abstract reader should not have to reach lines88–90 to learn that global orbit separation, rational-field generation, polynomial generation and a full ring presentation are not proved. A recommended sentence is: “The nonzero minor establishes algebraic independence of this explicit family; together with the cited generic quotient dimension, this proves its maximality.”

2. **Make the computational hypothesis explicit in the proof sentence.** Lines84–85 should refer to “a verified evaluation of the Jacobian minor,” not simply “a saved determinant.” The argument requires that the rows are derivatives of the declared graph polynomials. The saved-matrix mode verifies matrix arithmetic and internal metadata; it does not independently establish that link. The recompute mode uses the production evaluator again. Those distinctions are already mostly present later in the target and should remain visible at the proof.

3. **Separate algebraic independence from differential rank.** At lines85–87, suggested wording: “The81 polynomials are algebraically independent in characteristic zero, and their differentials are independent on the nonvanishing locus of the minor.” Algebraic independence is not a pointwise property restricted to a Zariski-open set.

4. **State the quotient input precisely.** Lines27–28 and87–89 rely on the cited generic quotient dimension. Cite the exact source location and explain that the relevant assumption is generic orbit dimension45 (equivalently zero-dimensional generic stabilizer at Lie-algebra level). Do not let the bare subtraction126−45 appear to establish the required genericity. If this audit has not independently verified that input, explicitly call it an inherited theorem/input.

5. **Clarify the local-coordinate claim.** Lines88–89 should specify a regular local quotient or transverse slice. Full-rank invariant differentials and quotient dimension provide local coordinates in that sense. They do not prove that all invariant functions are globally rational functions of the selected81 or that the map is globally injective.

6. **Keep degree-twelve polynomial evidence inherited until independently checked.** Lines57–58 and96–98 should call the62 graph classes and rank72 an inherited homogeneous-space result. Product counts enumerate ten monomials; their independence and spanning role require their own rank evidence and Hilbert upper bound. The81-row functional certificate does not certify the other two degree-twelve homogeneous directions.

7. **Resolve the source arithmetic discrepancy by explicit citation, not silent correction.** Cite Cederwall et al. Eq.(4.2) for the degree-twelve coefficient/exponent. Its §4.1.4 prose has the inconsistent64 count, as recorded in the literature report. The frozen62 value agrees with Eq.(4.2); the discrepancy is not evidence that the frozen number is false. Do not claim an author-approved correction.

8. **Describe the octic map as a reconstructed rational map with finite-sample validation.** Lines105–108 use “exact” near a map whose polynomial identities have not been proved symbolically. Suggested wording: “The machine-readable reconstructed rational matrix includes the product correction explicitly; its finite-field fitting and holdout tests are recorded.” The entries are exact rational numbers, while the asserted identity between polynomials is conditional. Preserve lines117–118.

9. **Separate octic fresh evaluations from degree-ten inherited reconstruction.** At lines116–118, recommended wording: “The octic map is tested on fresh modular values. The degree-ten map is reconstructed from inherited per-prime coordinates and checked against an inherited held-out prime. Neither finite-sample procedure alone proves the polynomial identities over the rationals.” This directly matches `scripts/map_literature_basis.py:80–159`.

10. **Downgrade published-formula identification after the reported source mismatch.** Lines110–115 may describe the exact rank/incidence of the frozen implemented formulas or reconstructed matrices, clearly labeled as such. They should not imply the same incidence for the publication's formulas until the J10–J12 transcription issue is resolved and new calculations are authorized. Existing source-reading qualifications and AMB labels do not cure a definite transcription mismatch.

11. **Treat regression/Lorentz tests as validation, not the mathematical invariance proof.** Lines142–146 describe appropriate checks. The full group's invariance follows from tensor contraction and Hodge compatibility, whereas finitely many tested rotations/boosts only corroborate the implementation. Name prime/seed scope, and do not call the production-evaluator recompute a wholly independent implementation.

12. **Report validation outcomes with exact scope.** Count successful independent computations separately from inspected existing artifacts, skips, unexecuted checks and blocked work. This reviewer supplied source inspection and a claim ledger, not fresh numerical validation. The coordinator has its own execution evidence; it should be integrated only under its exact names and limits.

## Materially stronger claims in other frozen manuscripts

The primary target is `paper/manuscript.tex`; the following are limited spot-checks, not a complete review of those older documents.

- `manuscript/main.tex:372–393` describes rationally reconstructing modular sample-coordinate rows, then claims an unconditional rational polynomial-space fixed-point equality. Exact closure of a rational reconstructed coordinate matrix is not, by itself, a proof that every coordinate row is the correct identity for the underlying polynomial target. This exceeds the new graph manuscript's finite-sample caveat. Recommended status: exact matrix result, conditional polynomial-space conclusion unless a symbolic identity or independently proved coefficient bound closes the lifting obligation.

- `manuscript/main.tex:602–643` uses two-way containment on common evaluation samples to assert invariant-span equality. Equal evaluation spans with holdouts are evidence for polynomial-span equality, but require an additional theorem/certificate to promote sampled zero residuals to identities. A genuinely injective evaluation certificate for the entire claimed finite-dimensional space could close that gap, but was not established in this partial review.

- `manuscript/main.tex:210` says there are “exactly two functional relations.” Differential rank83→81 shows two excess functional directions locally under the generic-rank assumptions; it does not present two defining polynomial syzygies, prove they generate the relation ideal, or identify a complete intersection. Preserve the distinction made by the new target at lines57–59.

- `manuscript/main.tex:807–811` correctly says the generic count is inherited and the computations give the lower half of the argument. This is compatible with the new paper's central distinction and should be retained.

- `submission_candidate/main.tex` repeats several of the same paragraphs. Spot searches also located stronger claims in PRD/JHEP/PRL variants, but their full dependencies were not audited before STOP. Their presence must not be treated as independent corroboration.

No spot-check above, by itself, demonstrates a false graph rank or false numerical value. These are claim-strength and missing-proof findings. The separate J10–J12 source transcription issue is the definite blocking result reported by the coordinator.

## Partial-review completion status

Completed here: complete claim-bearing prose ledger of the165-line primary target; direct supporting code-path inspection; frozen artifact hashes and stored metadata identification;32 fresh literature queries; targeted primary-source reads; explicit source inconsistency; limited older-manuscript conflict review; separate recommendations.

Incomplete here: exhaustive bibliographic coverage, full primary-source transcription, full trust-base audit, independent graph/derivative/Lorentz/degree-twelve executions, complete old-manuscript audit, and visual QA of the compiled PDF. Research and computations ceased when the coordinator issued STOP.

