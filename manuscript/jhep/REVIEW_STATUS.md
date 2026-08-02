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

## Blocked on the science gate

At the time of writing, `scripts/emit_jhep_science_gate.py` reports:

```
1.1  PASS  16/16    Exact Clifford and real-form structure
1.2  PASS  22/22    Exact tensor-spinor bridge and its inverse
1.3  FAIL  103/109  Candidate accounting and the rank-81 certificate
1.4  PASS  55/55    Degree-resolved tensor-spinor span equivalence
1.5  PASS  10/10    Degree-ten application
1.6  N/A            Degree-twelve scope decision (out of claim scope)
```

All six failures in 1.3 are `missing cell` for the five unfinished holdout
cells of the rank-81 matrix. There is no unresolved mathematics behind the
FAIL. `scripts/run_authoritative_suite.sh` is chained to the matrix driver and
will aggregate, emit the multi-sample certificate, run both suites and re-run
the gate when the driver exits.

**Section \ref{sec:rank} of the manuscript must be re-read against the final
aggregate before the draft banner is removed.** The per-cell numbers quoted
there are from the completed cells and have been identical across all of them,
but the holdout cells have not reported yet.

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
