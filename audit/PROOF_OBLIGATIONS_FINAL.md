# Proof obligations — final classification for the JHEP submission

Every obligation in `docs/PROOF_OBLIGATIONS.md` is given exactly one status here.
Statuses used: `PROVED`, `CERTIFIED`, `DISPROVED`, `COUNTEREXAMPLE FOUND`,
`REMOVED FROM CLAIMS`, `OPEN AND EXPLICITLY DELIMITED`, `NOT APPLICABLE`.

`NOT APPLICABLE` is used only where the manuscript makes no claim the obligation
supports **and** the degree-ten results do not depend on it. That second half was
checked rather than assumed — see "Dependency audit" below.

Machine-readable: `audit/PROOF_OBLIGATIONS_FINAL.json`.

---

## Dependency audit

The manuscript's degree-ten results rest on the stress-flow closure, so before
declaring any obligation irrelevant it had to be established what the closure
actually consumes. At degrees 4 through 10 it uses exactly these generators:

    tr_tau, tr_tau2, tr_tau3, tr_tau4, tr_tau5,
    tr_tau^2, tr_tau*tr_tau2, tr_tau*tr_tau3, tr_tau2^2, tr_tau2*tr_tau3

`Tr(M^6)` does **not** appear. Neither do `I12_61`/`I12_62`, `K6` as a physical
statement, or any all-orders induction. The manuscript searched for each of
these terms and they occur only inside explicit denials.

---

## PO-01 — canonicalisation is exact at every degree used

**Statement.** Graph canonicalisation must not collide, or the atlas
under-counts.
**Why it matters.** Every dimension in the paper is a rank over canonicalised
graphs.
**Status: `PROVED`** (Phase 0). The Weisfeiler–Leman fallback that collided —
49 order-6 classes collapsing to 39 keys — was replaced by exact canonicalisation
at every degree actually used.
**Manuscript consequence.** None; the atlas dimensions stand.

## PO-02 — `leading_field_degree` is correct, not merely self-consistent

**Statement.** The per-generator leading field degrees are computed by the same
code that validates them, so internal consistency proves nothing.
**Why it matters.** A misassigned target would land in the wrong graded piece and
corrupt `D10` — a live dependency for this manuscript, not a legacy one.
**Attempt performed.** The rule was stated independently — `Tr(tau)` has leading
degree 4 (not 2, because the free stress tensor is traceless), `Tr(tau^k)` has
`2k` for `k >= 2`, products add — and every generator's first appearance in every
certificate was checked against it.
**Result.** All 18 generators agree, at all six primes, with no exceptions.
`tests/test_leading_degree_rule.py`.
**Status: `CERTIFIED`, with one analytic input flagged.** The assignments are no
longer self-referential. The *derivation* of the rule — specifically why `Tr(tau)`
begins at degree 4 — is a one-line physics statement and is coauthor review item
**G-10**.
**Manuscript consequence.** None while G-10 is confirmed. If `Tr(tau)` began at
degree 2 the closure bookkeeping would be wrong; the test names that consequence
so it cannot fail quietly.

## PO-03 — are `I12_61` and `I12_62` polynomial syzygies?

**Statement.** A Jacobian dependence gives functional dependence, not a
polynomial identity; "syzygy" may not be used without one.
**Status: `NOT APPLICABLE`.** Degree twelve is background in this manuscript. The
words `syzygy`, `I12_61` and `I12_62` do not occur in it. The degree-ten closure
does not consume either element.
**Manuscript consequence.** None. Remains open for any future degree-twelve work.

## PO-04 — the `K6` ↔ `Sigma_2` identification (external)

**Statement.** The change of basis between the spinor sextic basis and
`(Tr(M^3), K6)` is inferred, not published.
**Status: `NOT APPLICABLE`.** `K6` and `sextic` do not occur in this manuscript.
**Manuscript consequence.** None. It is genuinely external — it needs the source
authors, not a computation — and is retained for future work.

## PO-05 — `Tr(M^6)`: analytic reduction or basis-independent formulation

**Statement.** 29 of 72 columns exceed the CRT uniqueness bound even at 15
primes, so `Tr(M^6)` has no certified rational lift.
**Status: `NOT APPLICABLE`.** `Tr(M^6)` does not appear in the manuscript and is
not among the generators the degree-ten closure consumes. This was checked
explicitly because it is the project's most serious unresolved height problem and
"not applicable" would otherwise be a convenient answer.
**Manuscript consequence.** None. No coefficient of `Tr(M^6)` is quoted anywhere.

## PO-06 — second independent holdout prime

**Status: `PROVED`** (already discharged before this session).

## PO-07 — does the `K6` statement survive field redefinitions and EOM?

**Statement.** An off-shell, convention-dependent obstruction is not a physical
obstruction.
**Status: `NOT APPLICABLE` to this manuscript, and enforced.** No `K6` statement
appears, and the physics section draws no consequence that would need it. The
manuscript's physics claim is about what the flow reaches at degree ten, which is
a statement about a construction, not about nature — and it says so.
**Manuscript consequence.** The existing prohibition stands: no physical or Type
IIB consequence is drawn. A wording gate enforces it.

## PO-08 — minimality under basis change

Four distinct properties were being conflated. Separated:

| property | status |
|---|---|
| **cardinality minimality** — no closing set has fewer than `dim Q_d` elements, in any basis | **`PROVED`** |
| **removal minimality** — no element of the exhibited set may be dropped | **`OPEN AND EXPLICITLY DELIMITED`** — shown in the fixed graph basis and under the permutation subgroup only |
| **minimality under arbitrary basis change** of the exhibited set | **`OPEN AND EXPLICITLY DELIMITED`** — requires regenerating the certificates in the new basis (~530 s/prime plus generator changes); not attempted |
| **uniqueness / canonicality** of the exhibited set | **`REMOVED FROM CLAIMS`** — never claimed, and a wording gate fails the build on unscoped "canonical" |

The proved half is elementary: applying the quotient map to `D + span(S) = A`
gives `span(pi(S)) = Q`, and a span of `|S|` vectors has dimension at most `|S|`.
It is stated in the manuscript as a proposition with no novelty claim
(review item **G-9**).
**Manuscript consequence.** The limitations section states cardinality
minimality as basis-independent and removal minimality as basis-fixed. Nothing
claims uniqueness.

## PO-09 — exceptional primes

**Statement.** Rank mod `p` equals rank over `Q` unless `p` divides a relevant
minor; agreement across primes makes a coincidence unlikely but proves nothing.
**Attempt performed, in two stages.**

*Stage 1 — narrowing.* A space spanned by exactly `k` explicit invariants has
`dim_Q <= k` for free, so a modular rank of `k` pins it over `Q` with no prime
excluded. This removes `A10`, `P10`, `G10` and `B10` from the obligation
entirely. The exact Jacobian bound is likewise unexposed, being one-sided over an
integer reduction. What remained exposed was `D10`, and through it `Q10` and
`B10 cap P10`.

*Stage 2 — closing `D10`.* The closure was re-run in exact rational arithmetic
after lifting its 9 non-integral targets by CRT and rational reconstruction,
validated against a held-out prime. Result: `dim_Q D10 = 11`, `dim_Q Q10 = 3`,
with an explicit non-vanishing `11 x 11` integer minor.
`results/stress_flow/D10_characteristic_zero.json`.

**Status: `CERTIFIED` for every degree-ten claim in the manuscript, except one.**
`dim_Q(B10 cap P10) <= 1` remains an inequality — see
`docs/B10_P10_INTERSECTION_STATUS.md` for its final state. The direction is the
one that would weaken, never strengthen, the paper's claim about the published
span, so no result depends on the equality.
**Manuscript consequence.** The limitation entry now separates "settled by exact
computation" from "still a bound", by name.

## PO-10 — the induction for any all-orders claim

**Status: `REMOVED FROM CLAIMS`.** No all-orders statement is made. The phrase
occurs twice in the manuscript, both times in an explicit denial, and a wording
gate fails the build on any assertion of one.

## PO-11 — bracket colour in equation (4.24)

**Statement.** `AMB-01` and `AMB-02` are unresolvable from the PDF because
bracket colour, which fixes operation order, does not survive text extraction.
**Status: `OPEN AND EXPLICITLY DELIMITED`, and made harmless.** Both readings of
every ambiguous candidate are implemented and projected, and the consequences of
each are reported. The compact `Q10` basis is chosen to be free of the ambiguity
altogether, so no result depends on which reading is correct.
**Manuscript consequence.** Stated as a limitation: the ambiguity is *avoided*,
not resolved. A wording gate fails the build on "AMB-02 is resolved". Confirming
the source's intent needs its authors — review item **G-6**.

---

## Summary

| status | obligations |
|---|---|
| `PROVED` | PO-01, PO-06, PO-08 (cardinality half) |
| `CERTIFIED` | PO-02 (pending G-10), PO-09 (except `B10 cap P10`) |
| `OPEN AND EXPLICITLY DELIMITED` | PO-08 (removal / general `GL`), PO-11 |
| `REMOVED FROM CLAIMS` | PO-08 (uniqueness), PO-10 |
| `NOT APPLICABLE` | PO-03, PO-04, PO-05, PO-07 |
| `DISPROVED` / `COUNTEREXAMPLE FOUND` | none |

No obligation is unresolved and hidden. Every one either supports no claim in
this manuscript, is discharged, or appears in the limitations section in the
words this table uses.
