# Mentor review package

**HUMAN ACTION REQUIRED.** Ten items, G-1 through G-10. Every one is a
*confirmation* of something already computed. None asks for a calculation.

Decision form: `review/MENTOR_DECISION_FORM.md`.
Full item text: `spinor_trace_bridge/docs/MENTOR_REVIEW_ITEMS.md`.

Read in this order. The first three are the ones where a wrong answer changes a
number rather than a sentence.

---

## Priority 1 — G-10: the leading-degree rule

**This is the only unverified analytic input the degree-ten result rests on.**

The stress-flow closure assigns each generated target to a graded piece using a
leading field degree per generator. The rule:

    Tr(tau)    leading field degree 4, not 2
    Tr(tau^k)  leading field degree 2k, k >= 2
    products   additive

All 18 generators at all six primes place their first appearance exactly where
this predicts (`tests/test_leading_degree_rule.py`), so the assignments are no
longer self-referential — they agree with a rule written down separately.

**Since this package was first drafted, G-10 has been derived**, not merely
checked against the table. For any improvement coefficient `c` the trace is
`(1 - cd)<F,F>`, so only `<F,F>` matters; `F ^ F` is a top form built from two
copies of an odd-degree form and so vanishes; `<F,*F>` is proportional to it;
hence `<F,F>` vanishes on either eigenspace. Verified with a control at four
primes by code importing no flow machinery, and shown load-bearing: forcing
degree-2 contribution gives `dim Q10 = 0` instead of `3`.

**What only you can confirm** is narrower than before: that the free theory and
stress convention used are the ones you intend, and that no formulation in use
changes the *quadratic scalar available* — the independence from `c` means a
different trace convention alone cannot change the conclusion.

**If this is wrong:** every target lands in the wrong graded piece, and
`dim D10 = 11` — hence `dim Q10 = 3`, the paper's central number — is wrong with
it. Nothing else in the paper has this property.

- Manuscript: §6.4, and the closure description in §4.
- Certificate: `results/stress_flow/D10_characteristic_zero.json`.

---

## Priority 2 — G-2: the split-signature correction

An earlier record in this project stated the oscillator frame's real form is
Euclidean `SO(10)`, where `*^2 = -1` admits no real self-dual five-form, and
treated that as blocking the bridge.

**That was wrong.** Computing the metric from the archive's own wedge and
contraction operators — all one hundred anticommutators, diagonalised — gives
eigenvalues `(+1/2)^5, (-1/2)^5`: real signature `(5,5)`, split. A null frame
cannot be Euclidean at all, since Euclidean signature has no isotropic vectors.

The distinction the paper draws, in one page:

| | real form | `*^2` on 5-forms | real self-dual 5-forms |
|---|---|---|---|
| Lorentzian | `Spin(1,9)` | `+1` | yes |
| split | `Spin(5,5)` | `+1` | yes |
| Euclidean | `Spin(10)` | `-1` | **no** |
| complexified | `Spin(10,C)` | — | the common ground |

What survives is weaker and precise: `(5,5)` and `(1,9)` are inequivalent **real**
forms, so a real frame transformation between them does not exist. But both
metrics have discriminant `-1` up to squares, so over `C` and over `F_p` they are
congruent, and the bridge constructs that congruence explicitly and checks it.
Every component-level comparison in the paper is therefore modular, where the
transition exists exactly — never a real Lorentzian identification.

**What is needed:** confirmation that the correction is accepted, and — because
the earlier, wrong statement may already have been communicated to you — that it
has not been relied on elsewhere.

- Docs: `spinor_trace_bridge/docs/REAL_FORM_DICTIONARY.md`,
  `COMPLEX_REPRESENTATION_BRIDGE.md`.
- Test: `test_null_frame_signature_is_split`.

---

## Priority 3 — G-8: credit for rank 81

The number 81 is **not ours** and the paper says so. Separating what each party
contributed:

| element | origin |
|---|---|
| the analytic count `126 - 45 = 81` from the trivial generic stabiliser | **literature** (Hutomo–Lechner–Sorokin), cited as the upper bound |
| earlier float64 finite-difference Jacobian evidence | **mentor archive** — two archived runs, reporting 35 and 81 |
| exact analytic amputated derivative, no step size, no tolerance | this project |
| integral gamma-traceless basis making the modular rank a rigorous bound | this project |
| explicit `81 x 81` minor, two independent determinant routines | this project |
| complete 83/83 candidate schedule with terminal statuses | this project |

The claim split in the draft: the *upper* bound is analytic and attributed; only
the *lower* bound `rank_Q >= 81` is claimed here, and only at finitely many
sample points. A wording gate fails the build on "proved rank 81
computationally".

**What is needed:** confirm the division of credit and that the literature
attribution points at the source you intend. Also confirm you want the paper to
state plainly that 83 candidates of rank 81 means the selection carries
functional dependencies — it currently does.

---

## Priority 4 — G-9: how to present the cardinality proposition

Any set closing degree `d` has at least `dim Q_d` elements, because the quotient
map is linear and a span of `k` vectors has dimension at most `k`. Three lines.

It is in the paper because it discharges half of PO-08 and turns a
basis-dependent assertion into a basis-free one — not because it is new. It is
almost certainly not new as mathematics, and the draft makes no novelty claim.

**Options:** proposition with proof (current) · lemma · remark · corollary ·
omit as elementary.

---

## Remaining items

| item | subject | what a wrong answer costs |
|---|---|---|
| G-1 | reconstructed spinor index placement | a wording change; the bridge is self-contained either way |
| G-3 | real-form independence of invariant dimensions | a citation instead of an inline argument |
| G-4 | equivariance verified at sampled group elements | possibly a symbolic proof instead |
| G-5 | comparison is modular, not characteristic zero | wording only |
| G-6 | real-form caveat on component claims; AMB-01/02 source intent | wording; no result depends on the reading |
| G-7 | redistribution of the spinor archive | release contents only |

---

## What is not being asked

No item asks you to approve a submission, an author list, or a novelty claim.
Those are separate and are in `audit/AUTHORSHIP_AND_CREDIT_FINAL.md`. Every
novelty row is `PROVISIONAL` and stays that way until someone who knows the field
says otherwise — a literature search shows absence of evidence, not evidence of
absence.
