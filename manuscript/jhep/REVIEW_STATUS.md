# Manuscript review status

`main.tex` is a **draft for internal review**. It is not a submission and it
carries a draft banner on every page. This file says what would have to change
before that banner comes off.

## Authorship — listed, provenance of consent still thin

| slot | name | state |
|---|---|---|
| author | Utsav Sunil Kumar, Heritage High School, Frisco, TX | listed |
| corresponding author | Christian Ferko, MIT / IAIFI | listed on reported agreement |

Christian Ferko is now on the author line. The basis is that the first author
reported in conversation, on 2026-08-01, that Dr. Ferko had agreed. That is
recorded here as exactly what it is — a report — because
`audit/AUTHOR_APPROVAL_CHECKLIST.md` asks for a written record and no written
record has been supplied to this repository.

**Three things still have to happen before submission, and none is a
formality:**

1. **Retain the actual reply.** File Dr. Ferko's written agreement in
   `audit/AUTHOR_APPROVAL_CHECKLIST.md`. Reported consent is enough to draft
   with; it is not enough to file with.
2. **He must read this text.** Corresponding author means he handles the
   submission, answers the referees, and vouches for the contents. Agreeing to
   co-author before seeing a draft is not agreement to *this* draft — in
   particular to the AI-assistance disclosure, to the exactness qualifiers, and
   to section 6, which states what the paper does not establish. He files it,
   not the first author.
3. **Verify the affiliation.** "MIT / IAIFI" was supplied in conversation and
   has **not** been checked against a current source. The `.tex` carries a
   comment marking it unverified. A wrong affiliation in print is its own
   problem, and it is trivially avoidable.

Both email addresses on the author lines are placeholders.

`AUTHORSHIP_INVITATION.md` is retained. If the agreement was informal, it is
still a reasonable thing to send — it states the AI assistance and the credit
position plainly, which is what the written record needs to show he saw.

## Science gate — PASSED

At commit `0206f4e` on `publication/jhep-tensor-spinor`:

```
1.1  PASS  16/16    Exact Clifford and real-form structure
1.2  PASS  22/22    Exact tensor-spinor bridge and its inverse
1.3  PASS  154/154  Candidate accounting and the rank-81 certificate
1.4  PASS  55/55    Degree-resolved tensor-spinor span equivalence
1.5  PASS  10/10    Degree-ten application
1.6  N/A            Degree-twelve scope decision (out of claim scope)

VERDICT: PASS
```

Test suites at the same commit, with full terminal records in
`results/jhep/authoritative_run/`:

| suite | result | claimable |
|---|---|---|
| tensor (`tests/`) | 252 passed | yes |
| bridge (`spinor_trace_bridge/tests/`) | 115 passed | yes |

Rank-81 matrix: 15/15 cells, 9 fitting and 6 holdout, all rank 81, all Euler
83/83, 81 stable pivot rows and 81 stable pivot columns with none unstable.

Section 4 has been re-read against the final aggregate and now quotes the
completed 15-cell numbers, the pivot-stability result, and the exceptional-prime
observation of §4.4.

## Not yet done

- **Literature novelty matrix** (`docs/LITERATURE_NOVELTY_MATRIX.md`) is
  NOT STARTED. The manuscript is written to need it: it makes no novelty or
  priority claim anywhere, and uses none of "first", "complete", "unique",
  "canonical", "minimal" or "previously unknown" as a claim. If a novelty claim
  is ever added, that file has to be populated from primary sources first.
- **Bibliography verification.** Two entries in `references.bib` are marked
  `FIELDS UNVERIFIED` and must be checked against publisher landing pages
  before submission.
- **Figures.** None are included. The prior manuscript in the canonical tree
  has seven; whether any survive the narrower claim scope of this draft has not
  been assessed.
- **Author email.** The address on the author line is a placeholder.

## Deliberately excluded

- Degree twelve as a central claim (it is an input to theorem 4.1 only).
- Any type IIB effective-action correction.
- Any causality, hyperbolicity, SUSY-completion or positivity statement.
- Rational `Tr(M^6)` coordinates — the rank is certified, the coordinates are
  not.
