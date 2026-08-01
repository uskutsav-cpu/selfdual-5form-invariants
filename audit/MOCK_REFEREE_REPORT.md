# Mock referee report (adversarial)

Written against the current draft, deliberately hostile. Each objection is graded
and answered with evidence or conceded. Where an objection was valid, the
manuscript was changed and the change is named.

---

## Fatal issues

**None identified.** This is asserted only because each candidate for "fatal" was
checked and downgraded below, not because none was looked for.

---

## Major issues

### M1. "This is a computation, not physics."

*Objection.* The paper computes dimensions of vector spaces. Where is the physics?

*Response.* Partly conceded, and the framing was changed. The physics content is
the deficit of the stress-flow construction: `dim D10 = 11` inside
`dim A10 = 14`, so exactly three degree-ten directions are unreachable, with
explicit representatives. The sharper statement is `P10 ⊂ D10` --- products are
all reachable, so the missing directions cannot be built by composing lower
degrees. Section 12 now states what calculation becomes possible that was not
before, in four concrete items.

*Residual risk.* A referee may still find this insufficiently physical. The
manuscript does not oversell it, and the interpretation is flagged as requiring
coauthor confirmation. **This is the objection most likely to survive.**

### M2. "Finite fields do not prove anything in characteristic zero."

*Objection.* Everything is computed at two primes. That is not a proof.

*Response.* Accepted as stated, and the manuscript already separates the two
directions rather than blurring them:
- Modular rank is an **unconditional lower bound** on the characteristic-zero
  rank when the matrix is an integer reduction. The gamma-traceless basis is
  computed over `Z` with entries in `{-1,0,+1}`, so this applies.
- The **upper** direction is not modular. Where an upper bound is needed it is
  taken from the analytic argument `126 - 45 = 81`.
Section 4.2 states this and a wording gate blocks "exact over `Q`".

### M3. "The generic dimension 81 is not yours."

*Objection.* The abstract could be read as claiming 81.

*Response.* Valid, and guarded. The manuscript attributes 81 to the analytic
trivial-stabiliser argument with a citation, states that the computation "did not
discover 81 and is not claimed to prove it by itself", and an automated gate
fails the build on any phrasing of the form "proved rank 81 computationally".

### M4. "The reverse search proves nothing if it is not exhaustive."

*Objection.* A bounded search that finds the expected answer is weak evidence.

*Response.* Accepted, and the paper's structure already reflects it. The reverse
search is corroboration, not the primary derivation; the atlas and quotient are
established independently. The word "exhaustive" is gated: it may appear only
adjacent to an explicit denial.

### M5. "The degree-eight comparison fails. Why should I trust degree ten?"

*Objection.* The spinor and tensor spans disagree at degree eight (6 versus 7).
That undermines the degree-ten agreement.

*Response.* This is the sharpest objection and it has a clean answer. The
disagreement is strict containment: every spinor invariant lies in the tensor
span; one tensor direction is unreached. That is a property of the port-graph
candidate family, not of the bridge --- the bridge is separately certified to be
an isomorphism with kernel exactly the anti-self-dual `126` and image exactly the
gamma-traceless `126`, by two-way span equality. The original spinor
implementation reached the same conclusion independently and supplied the missing
direction from structured tensor-word candidates that this work does not
re-implement. Reproducing the shortfall is evidence the implementation is
faithful, not evidence it is broken. **Manuscript changed:** a dedicated
paragraph now states this, rather than leaving a bare "no" in the table.

### M6. "The spinor implementation uses the wrong signature."

*Objection.* The oscillator frame is Euclidean; there are no real self-dual
five-forms there.

*Response.* Refuted, with a computation. The frame's real signature is `(5,5)`,
computed from all one hundred anticommutators of the archive's own operators. In
split signature `⋆² = +1` on five-forms exactly as in Lorentzian, so real
self-dual five-forms exist. A null frame cannot be Euclidean at all, since
Euclidean signature has no nonzero isotropic vectors. What does survive is that
`(5,5)` and `(1,9)` are inequivalent **real** forms, so the transition is complex
over `R` and exact over `F_p`; the manuscript says exactly this.

### M7. "One convention was guessed."

*Objection.* The spinor index placement was not read from documentation.

*Response.* Conceded and disclosed. It was determined by requiring exact
equivariance: of eight candidate placements, one reproduces the transformed image
on every component with a single scalar, under both `GL(5)` and Clifford
reflections. The manuscript calls this a reconstruction, not a citation, and it
is coauthor review item G-1.

---

## Minor issues

### m1. Equivariance is checked at finitely many group elements.

Conceded, stated in the limitations. Reflections generate the full orthogonal
group, so the sampling is not confined to a subgroup, but the certificate is not
a symbolic identity. Listed as G-4.

### m2. The float64 Jacobian matrix over seeds/scales/steps was not run.

Conceded and stated in the text, with the reason (a single configuration costs
more than ten minutes). The archived pair is analysed instead, which is the data
those runs actually produced, and it exhibits both behaviours cleanly: one sample
with no rows at the noise floor, rank stable across six orders of magnitude of
tolerance and a `2×10⁷` gap; one with 48 of 83 rows at the noise floor, no gap,
honest rank 35, and a fabricated 83 if the normalisation rule is broken.

### m3. The exact Jacobian reaches 59, not 81. — **RESOLVED by computation**

This objection was raised against an intermediate state in which only the
port-graph subset had been re-implemented exactly. The remaining structured
tensor-word candidates have since been implemented in the same exact arithmetic.
The certificate now covers the complete selection: 83 scheduled, 83 evaluated,
zero evaluation errors, zero zero-rows, exact modular rank 81, witnessed by an
explicit 81×81 minor with non-vanishing determinant under two independent
routines. See `docs/RANK81_EXACT_CERTIFICATE.md` and
`results/rank81/certificate.json`.

The claim is still the lower half only. `rank_Q ≥ 81` is unconditional because
the matrix is an integer reduction; the matching upper bound `126 − 45 = 81`
remains analytic and from the literature, and the wording gate continues to fail
the build on "proved rank 81 computationally".

### m4. Only two primes.

Conceded for the subspace certificates. Note the distinction: for the rank
certificate the number of primes is not what carries the argument. A single
prime at which an integer minor has non-vanishing determinant already proves the
integer minor is nonzero, hence the characteristic-zero bound; further primes
guard against an indexing error in selecting the minor, not against a
probabilistic failure. For the subspace dimensions, which are equalities rather
than lower bounds, additional primes do reduce risk and the incidence
certificate is now regenerated at every prime with a stress-flow closure
certificate by `scripts/emit_degree10_space_incidence.py`.

### m5. The compact basis is called compact, not canonical.

Deliberate. A gate fails the build if "canonical" appears without scope.

### m6. Novelty is not established.

Conceded, prominently. Every novelty row is PROVISIONAL, no result is called
"new" or "first", and `audit/RELATED_WORK_SEARCH.md` states exactly which
literature was and was not searched.

### m7. Reproducibility depends on third-party code.

Partly. The archive-dependent results need a private copy; everything else
reproduces without it. A manifest with hashes and adapter instructions is shipped.

---

## Summary

| grade | count | resolved in manuscript | conceded and disclosed |
|---|---:|---|---|
| fatal | 0 | — | — |
| major | 7 | M1, M3, M4, M5, M6 | M2, M7 |
| minor | 7 | m5 | m1, m2, m3, m4, m6, m7 |

No objection was answered by weakening a test. Two were answered by adding
manuscript text (M1, M5); one by refuting the premise with a computation (M6).
