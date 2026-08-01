# Coauthor review checklist — bridge and signature

**HUMAN ACTION REQUIRED.** Nothing below is marked resolved. Each item states
exactly what evidence exists and exactly what decision or confirmation is
needed. No item blocks the rest of the programme; each is a confirmation of
something already computed, not a missing computation.

Reviewer: ______________________  Date: ______________

## G-1 — spinor index placement in the archive's `sigma^mu_{ab}`

**What exists.** The archive does not document whether its symmetric
`sigma^mu_{ab}` carries upper or lower spinor indices. The bridge determined the
placement by requiring exact equivariance: of eight candidate placements exactly
one reproduces the transformed image on every component with a single scalar,
under both `GL(5)` and products of Clifford reflections.

**What is needed.** Confirmation that the reconstructed placement is the one the
archive's author intended. If it is not, the bridge is still internally
consistent but its relation to the archive's own invariant formulas would need
restating.

**Consequence if wrong.** The bridge and all `WS-I` span results are unaffected
(they are self-contained). The wording "matches the archive's convention" would
have to become "differs from the archive's convention by a transpose".

- [ ] confirmed  - [ ] correction supplied: ______________________

## G-2 — the split-signature identification

**What exists.** `test_null_frame_signature_is_split` computes all one hundred
anticommutators of the archive's own wedge and contraction operators and
diagonalises the resulting metric: eigenvalues `(+1/2)^5, (-1/2)^5`, real
signature `(5,5)`. This **contradicts** an earlier record in this project that
called the frame Euclidean and treated `*^2 = -1` as a blocker.

**What is needed.** Confirmation that the correction is accepted, since the
earlier (wrong) statement may have been communicated.

- [ ] confirmed  - [ ] disputed: ______________________

## G-3 — invariant dimensions are real-form independent

**What exists.** The argument in `COMPLEX_REPRESENTATION_BRIDGE.md` §3: a real
form `G_R` of a connected reductive `G_C` is Zariski-dense, so
`R[V_R]^{G_R} (x) C = C[V_C]^{G_C}` degreewise. This is what licenses comparing a
Lorentzian implementation's counts with a split one's.

**What is needed.** Confirmation that this standard statement is being applied
correctly here, and a decision on whether the manuscript should cite a textbook
for it or give the one-line density argument inline.

- [ ] confirmed  - [ ] cite instead: ______________________

## G-4 — scope of the equivariance certificate

**What exists.** Equivariance is verified exactly at both primes under (a) the
25-dimensional `GL(5)` subgroup, with character `det(A)`, and (b) products of
two and four Clifford reflections, which by Cartan–Dieudonné generate the full
orthogonal group, with character equal to the inverse product of the reflecting
vectors' norms. Both were solved for, not assumed.

**What is needed.** Confirmation that (b) is accepted as covering the full
group, given that it samples finitely many group elements rather than proving
equivariance as an identity.

**Honest limitation.** The tests establish equivariance at the sampled elements
exactly. They do not constitute a symbolic proof of equivariance for all group
elements. A referee may reasonably ask for the one-line Schur argument instead;
the manuscript states both.

- [ ] accepted as-is  - [ ] add symbolic proof  - [ ] other: ______________

## G-5 — comparison is modular, not characteristic zero

**What exists.** The bridge and the whole `WS-I` comparison are exact over
`F_p` at two primes. They are **not** characteristic-zero statements. Agreement
at two primes does not prove agreement over `Q`; it bounds the failure
probability by `O(degree/p)` per prime under the usual Schwartz–Zippel argument.

**What is needed.** Agreement on the manuscript wording. The draft says
"verified at two primes" and never "proved over the rationals".

- [ ] wording accepted  - [ ] revise to: ______________________

## G-6 — real-form caveat on component-level claims

**What exists.** Over `R`, `(5,5)` and `(1,9)` are inequivalent; a real self-dual
five-form of one is not a real self-dual five-form of the other. All
component-level comparisons in this work are therefore modular, where the
transition exists exactly.

**What is needed.** Confirmation that the manuscript's limitation subsection
states this clearly enough, and that no physical conclusion is being drawn that
requires a real Lorentzian component identification.

- [ ] confirmed  - [ ] strengthen the caveat: ______________________

## G-7 — redistribution of the spinor archive

**What exists.** The spinor archive (`self_dual_5_invariant_enumerator`) is
third-party code. Its logs contain Windows paths under another person's home
directory, so it is not this project's to publish. It has been **excluded** from
the public repository and from the release candidate; only a manifest, file
hashes and adapter instructions are included.

**What is needed.** Either written redistribution permission from the archive's
author, or confirmation that the manifest-only arrangement is the final one.

- [ ] permission obtained  - [ ] manifest-only is final  - [ ] other: ________

## G-8 — what the exact rank-81 certificate is allowed to say

**What exists.** The exact analytic Jacobian over the complete 83-candidate
selection has modular rank 81, with a terminal status for every candidate, zero
evaluation errors, zero zero-rows, Euler homogeneity passing throughout, and an
explicit 81x81 minor whose determinant is nonzero under two independent
routines. Because the coordinate basis is integral the Jacobian is an integer
reduction, so `rank_Q >= 81` holds unconditionally — no height bound, Hadamard
estimate or rational reconstruction is involved, and the number of primes is not
what carries the argument.

**What is needed.** Confirmation of the claim split. The draft attributes the
*upper* bound `126 - 45 = 81` to the analytic trivial-stabiliser argument in the
literature and claims only the lower bound here, at finitely many sample points.
A gate fails the build on "proved rank 81 computationally". Confirm that this is
the right division of credit, and that the literature attribution is to the
intended source.

**Also worth a decision.** 83 candidates of rank 81 means the selection carries
functional dependencies. The draft states this plainly rather than leaving it
implicit; confirm that is wanted.

- [ ] claim split confirmed  - [ ] revise to: ______________________

## G-9 — status of the cardinality proposition

**What exists.** Proposition (manuscript section 6.4): any set closing degree
`d` has at least `dim Q_d` elements, because the quotient map is linear and a
span of `k` vectors has dimension at most `k`. This makes cardinality minimality
basis-independent, where previously it was checked only in the fixed basis and
under relabellings.

**What is needed.** A judgement on how to present it. It is elementary linear
algebra and almost certainly not new as mathematics; it is included because it
discharges half of PO-08 and converts a basis-dependent assertion into a
basis-free one. The draft states it as a proposition with proof and makes no
novelty claim for it. Confirm that this is the right treatment, or say whether
it should be demoted to a remark.

**Note on scope.** It does not give removal-minimality, which stays open under
general `GL`. The manuscript limitation says so; confirm the wording is
sufficient.

- [ ] treatment confirmed  - [ ] demote to a remark  - [ ] other: __________

## Summary for the reviewer

Every item above is a *confirmation* request. None is a request to perform a
calculation. If all nine are confirmed as-is, the bridge, signature and
Jacobian workstreams are complete and no wording in the manuscript changes.
