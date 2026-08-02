# Mentor review guide

A short orientation to the draft, written to save you time rather than to
persuade you. If you read only one section of this file, read
"The ten questions, in priority order".

---

## What the paper claims

The degree-ten Lorentz-invariant structure of a self-dual five-form in ten
dimensions, determined exactly:

- the full degree-ten invariant space has dimension **14** over `Q`;
- the subspace reachable by the stress-tensor flow has dimension **11**;
- the quotient therefore has dimension **3** — three directions the flow misses;
- the span of the published degree-ten structures meets the product sector in
  exactly **1** dimension, written out as an explicit integer identity;
- the generic functional rank of the candidate family is **at least 81**,
  certified by an explicit 81×81 minor.

All four dimensions are exact over the rationals, not modulo a prime.

## What is new, and what is not

**Not new, and the paper says so in the introduction and again in §6:** the
enumerate–evaluate–relate workflow (Elamaran–Ferko–Scarlett), the stress-flow
construction (Hutomo–Lechner–Sorokin), the gamma-matrix map, the number 81, and
the elementary cardinality bound of proposition 9.4.

**What we claim:** the exact dimensions, the exact intersection with its
generator, the certified bridge implementation, the exact lower bound with its
minor, and the certification layer generally.

**Every novelty row is PROVISIONAL** (`audit/MENTOR_DRAFT_NOVELTY_LEDGER.md`).
A literature search shows absence of evidence, not evidence of absence. Nothing
is described as new on the strength of that file alone, and no row may be
upgraded without you.

## Which calculations are exact, and in what sense

| result | strength |
|---|---|
| `dim_Q D10 = 11`, `dim_Q Q10 = 3` | exact over `Q` — CRT lift, held-out prime, fixed point in exact rational arithmetic |
| `dim_Q(B10 ∩ P10) = 1` | exact over `Q` — CRT lift, held-out prime, fresh-sample re-verification |
| `dim_Q A10 = 14` | exact over `Q` via the spanning-set argument (§6) |
| generic rank ≥ 81 | exact mod `p`, carried to characteristic zero by an integer minor |
| generic rank = 81 | **analytic and cited** — the upper bound is not ours |
| bridge properties | exact mod `p` at each prime used |
| degree-8 indispensability | ablation within our own families — **qualified, not universal** |

## What remains open

Ten items, listed in §14 and in the claim ledger. The ones most likely to matter
to you: removal minimality outside a fixed basis; the generator-extension
question; no Hilbert-series cross-check; 13 of 15 rank-matrix cells not
independently recomputed; and the source ambiguity AMB-01/02, which we avoid
rather than resolve.

---

## The ten questions, in priority order

Each entry gives where to look, the object to check, the artifact behind it,
what breaks if we have it wrong, and wording we would accept instead. Questions
1–5 are mathematical or physical and can be answered from the manuscript.
Questions 6–10 are judgement calls about framing and credit that only you can
settle.

If you have time for only one, make it **Q4 (G-10)**: it carries the most
mathematical weight, because the counterfactual collapses the headline result.
It is listed fourth only because Q1–Q3 must be true for Q4 to be meaningful.

### Q1. Is the orientation-fixed bridge consistent with the intended spinor conventions?

- **Where:** §5.3, p. 6; appendix B, p. 25.
- **Equation:** the frame congruence (B.1), and the bridge (5.1) on p. 5.
- **Artifact:** `spinor_trace_bridge/tests/test_orientation.py`;
  `results/rank81/full_rank_matrix_publication_final.json` (the 15-cell matrix,
  including the three `p = 32707` cells that exposed the branch).
- **If wrong:** the bridge would map to the anti-self-dual projector, and every
  degree-resolved tensor/spinor comparison in §7 would be comparing the wrong
  two spaces. The rank-126 image and the exact left inverse would still be
  internally consistent — which is exactly why this needs a human with the
  conventions in hand, not another test.
- **Background:** a square-root branch in the congruence was silently selecting
  the anti-self-dual projector at some primes. Three rank-matrix cells failed at
  `p = 32707`. We diagnosed it as a branch rather than an exceptional prime by
  flipping it at both a failing and a working prime, and fixed it by *enforcing*
  the orientation rather than excluding the prime. No published number changed.
- **Alternative wording we would accept:** "with the orientation branch fixed by
  the convention of [your reference]" in place of our internal pinning language.

### Q2. Are the Lorentzian / split-real-form statements correct?

- **Where:** §5, pp. 5–6; appendix A, p. 24.
- **Equation:** the common complexification argument preceding (5.1).
- **Artifact:** `spinor_trace_bridge/tests/test_bridge.py`, in particular
  `test_five_form_frame_round_trip` and
  `test_left_inverse_round_trips_on_selfdual_forms`.
- **If wrong:** the identification of the Lorentzian and split real forms
  through a common complexification is what lets us compute in the split form
  and transport conclusions back. If the transport is invalid, §7 and §8 hold
  only in the split form and the paper must say so throughout.
- **Alternative wording:** restrict every claim to the split real form and state
  the Lorentzian case as a conjecture.

### Q3. Is the definition of the activated flow space `D10` physically correct?

- **Where:** §9.1, p. 13; appendix H, p. 31.
- **Equation:** the flow (9.1), p. 13.
- **Artifact:** `results/stress_flow/D10_characteristic_zero.json` and
  `results/stress_flow/closure_and_minimality.json`; reproduce with
  `scripts/d10_characteristic_zero.py`.
- **If wrong:** this is the whole result. The distinction between the *raw
  target span* (dimension 14) and the *recursively activated closure*
  (dimension 11) is what makes `Q10` three-dimensional. Conflating the two gives
  `Q10 = 0` — the answer this project had before catching the error.
- **Alternative wording:** if "reachable by the stress flow" overstates it, we
  would use "the closure of the seed under the flow's activation rule," which
  claims only what we compute.

### Q4. Is the G-10 stress-tensor trace derivation correct under the intended formulation?

- **Where:** §10, p. 16; appendix I, p. 32.
- **Equations:** the stress tensor (I.1) and the trace (I.2), both p. 33.
- **Artifact:** `results/stress_flow/G10_publication_certificate.json` and
  `results/stress_flow/G10_counterfactual.json` (the `Q10 = 0` counterfactual);
  `tests/test_stress_flow.py`.
- **If wrong:** everything at degree ten depends on it. The theorem says the
  free stress tensor of a self-dual five-form is traceless for *any* improvement
  coefficient, so `Tr(τ)` begins at field degree four. Forcing a degree-two
  contribution changes `Q10` from dimension three to dimension zero.
- **What we are actually asking:** the mathematics is short and we believe it is
  right. The question is whether the flow's `τ` is an object of the shape the
  theorem assumes, *in the formulation the source intends*. We could not settle
  that from the published text, and have flagged it rather than assume the
  favourable reading.
- **Alternative wording:** state the theorem as conditional — "for a stress
  tensor of the form (I.1)" — and move the identification to an open problem.

### Q5. Is the exact quotient `Q10` interpreted correctly?

- **Where:** §9.2–9.4, pp. 14–15.
- **Equation:** the three annihilating covectors and the explicit 11×11 minor in
  §9.3.
- **Artifact:** `results/stress_flow/Q10_characteristic_zero.json`.
- **If wrong:** the arithmetic (14 − 11 = 3) is certified and is not in
  question. What is in question is the reading: we say `Q10` measures degree-ten
  invariants not reachable by the flow. If that reading is wrong, the number
  survives and the physical sentence around it does not.
- **Alternative wording:** present `Q10` as a purely algebraic cokernel and drop
  the reachability language entirely.

### Q6. How should credit for the known rank-81 expectation versus the exact certificate be stated?

- **Where:** §8, p. 11; appendix G, p. 30.
- **Equation:** the 81×81 minor and its two determinant checks in appendix G.
- **Artifact:** `results/rank81/minor81_certificate.json` (the explicit 81x81 minor and its
  two determinant checks) and `results/rank81/full_rank_matrix_publication_final.csv`.
- **If wrong:** this is credit allocation, not mathematics. We claim the
  characteristic-zero lower bound and the explicit certificate, and we cite the
  analytic generic upper bound as prior expectation. Overclaiming here is the
  kind of thing that is remembered.
- **Alternative wording:** if the expectation is more firmly established in the
  literature than we have credited, we will reduce our claim to "we certify the
  expected value exactly" and cite accordingly.

### Q7. Is the `B10 ∩ P10` correction presented fairly?

- **Where:** §11, p. 17.
- **Equation:** the overlap identity (11.1), p. 17.
- **Artifact:** `results/degree10/B10_P10_intersection_exact.json` and
  `results/degree10/B10_P10_intersection_generator.json`; reproduce with
  `scripts/b10_p10_characteristic_zero.py`.
- **If wrong:** the result is that the published span contains exactly one
  product direction. We have tried to frame this as a structural observation
  about the basis, not as a criticism of the earlier paper. Please check that it
  reads that way — we are poorly placed to judge our own tone here.
- **Alternative wording:** we will move the entire discussion to an appendix and
  reduce the body to the dimension count, if that reads better.

### Q8. Is the title and novelty language appropriate?

- **Where:** title page; §1, p. 1; §14, p. 21.
- **Current title:** *Exact degree-ten invariants of a self-dual five-form in
  ten dimensions.*
- **If wrong:** "exact" is doing real work in that title and we should not use
  it if you read it as claiming more than certified characteristic-zero
  arithmetic on a fixed candidate family.
- **Alternative wording:** *Certified degree-ten invariants…* or *Exact
  characteristic-zero computations for degree-ten invariants…*

### Q9. Which results should be central, and which moved to appendices?

- **Where:** the §7–§11 body versus appendices G–J.
- **Our current choice:** rank 81 (§8), `D10`/`Q10` (§9) and G-10 (§10) are
  central; the certificates and reconstructions are in appendices.
- **If wrong:** nothing breaks mathematically. But a reader's sense of what the
  paper is *about* is set by this choice, and we would rather get it right
  before anyone else reads it.
- **Alternative:** promote the degree-resolved equivalence (§7) to the lead
  result and demote rank 81, if you think the equivalence is the more
  interesting contribution.

### Q10. Should you be an author, an acknowledged mentor, or neither?

**This is left entirely for human discussion. We are not proposing an answer.**

The manuscript names no authors: the title page carries "Author list pending
mentor review" and a visible mentor-review banner. Nothing in the draft implies
you have approved the manuscript, the results, authorship, credit allocation,
submission, or repository release. Nothing has been submitted anywhere, and no
release, DOI or licence has been created.

---

## Where the code and certificates are

Repository: `github.com/uskutsav-cpu/selfdual-5form-invariants`
Branch: `publication/jhep-mentor-draft`

| what | where |
|---|---|
| headline certificates | `results/stress_flow/`, `results/degree10/`, `results/rank81/` |
| input manifest with hashes | `results/mentor_draft/scientific_input_manifest.json` |
| claim → certificate map | `audit/MENTOR_DRAFT_CLAIM_CERTIFICATE_MATRIX.md` |
| adversarial reviews and our replies | `audit/MENTOR_DRAFT_REFEREE_{A,B,C,D}.md`, `..._INTERNAL_RESPONSE.md` |
| manuscript source | `manuscript/jhep/` |

## How to reproduce the main results

Python 3.10 or newer is **required** — the source uses PEP 604 union
annotations, so on 3.9 the suites fail at collection before any test runs. The
stock macOS `python3` is 3.9.6; the certified runs used 3.13.

```
git clone https://github.com/uskutsav-cpu/selfdual-5form-invariants
cd selfdual-5form-invariants
git switch publication/jhep-mentor-draft
python3 -m venv .venv   # python3 must be >= 3.10
.venv/bin/python3 -m pip install -r requirements.txt
.venv/bin/python3 -m pytest tests spinor_trace_bridge/tests -q
.venv/bin/python3 scripts/d10_characteristic_zero.py
.venv/bin/python3 scripts/b10_p10_characteristic_zero.py
```

Expected: 254 + 86 tests passing; `dim_Q D10 = 11`, `dim_Q Q10 = 3`;
`dim_Q(B10 ∩ P10) = 1`.

Note: `opt_einsum` is **required** and is in `requirements.txt`. An earlier
version of this guide called it optional and said the certified runs ran without
it; that was wrong. It supplies both the contraction order and the memory and
flop budget the modular contractor enforces, and without it the bridge suite is
killed by the kernel with no traceback rather than raising. The values are
unaffected.

---

## Two things you should know before you start

**On AI assistance.** This work was prepared with substantial AI assistance,
including code generation, debugging, drafting, and — importantly — the
*execution* of the verification scripts. The computations were therefore not
verified by a human independently of the system that produced them. The
manuscript says this plainly in its disclosure section rather than leaving it to
be inferred. No AI system is an author.

**On the errors reported in the paper.** The draft describes six defects found
in this project's own earlier work, including two that produced wrong published
numbers before being caught. That is deliberate. A computational result's
credibility rests as much on the errors that were found as on the checks that
passed, and burying them would make the remaining claims harder, not easier, to
trust.
