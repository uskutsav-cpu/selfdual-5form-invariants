# Manuscript review status

`main.tex` is a **draft for internal review**. It is not a submission and it
carries a draft banner on every page. This file says what would have to change
before that banner comes off.

## Authorship — unresolved

| slot | name | state |
|---|---|---|
| author | Utsav Sunil Kumar, Heritage High School, Frisco, TX | listed |
| corresponding author | — | **empty** |

The corresponding-author slot is deliberately empty. It was requested that
Christian Ferko (prior-art author on arXiv:2512.23750, the source of the
enumerate–evaluate–relate workflow this paper uses) be listed there. That has
not been done, for two reasons already recorded in this repository:

- the project's own operating rules forbid fabricating author approval;
- `audit/AUTHORSHIP_AND_CREDIT_FINAL.md` states that mentorship, code access,
  discussion and institutional position are not, by themselves, authorship.

Corresponding author is a role with content: that person handles submission,
answers referees, and vouches for the work. Assigning it to someone who has not
agreed in writing would misrepresent them to the journal.

**To resolve:** send `AUTHORSHIP_INVITATION.md`. If written agreement comes
back, add the author line and record the agreement in
`audit/AUTHOR_APPROVAL_CHECKLIST.md`. The email placeholder on the existing
author line must also be replaced with a real address.

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
