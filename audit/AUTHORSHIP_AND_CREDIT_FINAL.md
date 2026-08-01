# Authorship and credit — factual record, no decisions

**No authorship decision is made here, and none may be inferred from this file.**
What follows is a record of who contributed what, assembled from git history,
run artifacts and the third-party archive's own provenance. Turning it into an
author list is a human decision, recorded in
`audit/AUTHOR_APPROVAL_CHECKLIST.md`.

Nobody may be added or removed by inference. In particular, none of the following
is by itself a basis for authorship: seniority, supervision in general, providing
code, providing compute, or courtesy.

## Parties

| label | who | how identified |
|---|---|---|
| **U** | the repository owner | git author of the commit history |
| **M** | the mentor / archive author | provenance of `self_dual_5_invariant_enumerator`; Windows paths under a different user account |
| **L** | the source-paper authors | arXiv:2509.14350, arXiv:2509.14351 — cited, not contributors |
| **AI** | Claude, as a tool | disclosed in `submission_candidate/ai_use_disclosure.md`; **not an author** |

## Contribution matrix

`•` = substantive contribution, `◦` = partial or supporting, blank = none.

| category | U | M | AI | evidence |
|---|:--:|:--:|:--:|---|
| conceptualization | • | • |  | problem posed jointly; repository history predating this work |
| invariant-theory analysis | • | • | ◦ | graph representation and quotient formulation predate the AI work |
| tensor construction | • |  | ◦ | `src/sdinv`, git history |
| spinor construction |  | • |  | third-party archive; 22 enumeration runs |
| bridge construction |  |  | • | `spinor_trace_bridge/` written in-session; conventions reconstructed from the archive |
| software | • | • | • | split as above |
| exact certification | ◦ |  | • | rank-81, `D10` characteristic-zero, incidence, degree-8 span |
| validation | ◦ |  | • | tests, gates, holdout primes |
| interpretation | ◦ | ◦ | ◦ | drafted by AI, **requires coauthor confirmation** |
| writing | ◦ |  | • | full draft AI-written; requires author rewriting |
| supervision | | • | | |
| funding / resources | | | | none recorded; one laptop, no institutional compute, no cluster |

## What each party contributed to the headline results

**`dim_Q Q10 = 3`** — the flow construction and its certificates are M's and U's;
the exact characteristic-zero closure, the CRT lift, the held-out-prime
validation and the minor certificate are AI-implemented. The analytic input the
result rests on (G-10) is M's to confirm.

**Exact rank 81** — the number is **L's**, analytic, and cited. Earlier float64
evidence is **M's** archive. The exact evaluator, the integral-basis argument and
the explicit minor are AI-implemented. See G-8; the paper claims only the lower
bound.

**The bridge** — the gamma-matrix map is standard and is L's setting. Its
convention-controlled implementation, the certified kernel and image, and the
equivariance characters are AI-implemented. One convention was *reconstructed*,
not read (G-1).

**Degree-8 drop test** — M's archive supplied the observation that structured
candidates are needed; the exact four-prime span equality and the family ablation
are AI-implemented.

## Things that are not contributions to this paper

- The number 81 (literature).
- The Hilbert-series dimensions (literature).
- The stress-flow construction itself (literature).
- The gamma-matrix map itself (standard).
- The cardinality proposition (elementary; explicitly not claimed as novel).

## AI status

Claude is a tool and is **not listed as an author**. It did not independently
verify any result: where a result was checked, the check was written by the same
system in the same session under the same assumptions. The adversarial referee
and editor simulations carry the same limitation and say so. Full disclosure:
`submission_candidate/ai_use_disclosure.md`.

## Unresolved and human-only

- Whether M is an author or is acknowledged — depends on the intellectual
  contribution to *this* paper, which M is best placed to state.
- Author order.
- Corresponding author.
- Affiliations for every listed author.
- Whether L should be contacted before posting, given that the work extends
  their published expressions and one source ambiguity (AMB-01/02) can only be
  settled by them.
- Funding and competing-interest statements.

## Redistribution, which is separate from authorship

The spinor archive is M's and is **excluded** from the repository and the release
candidate; only a manifest with per-file hashes and adapter instructions ships.
Redistribution permission is item G-7 and is not implied by any authorship
decision.
