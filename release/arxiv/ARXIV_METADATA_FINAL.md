# arXiv submission metadata — PREPARED, NOT POSTED

Fill the bracketed fields from the approved decisions, then submit **manually**.
Nothing here may be posted without every author's approval.

## Title

    An exact degree-ten classification of local invariants of the
    ten-dimensional self-dual five-form

No formulas, no citations, no priority language. Retained from the current draft:
the novelty audit gave no reason to change it.

## Authors

    [AUTHOR LIST — HUMAN ACTION REQUIRED]

See `audit/AUTHOR_APPROVAL_CHECKLIST_FINAL.md`. Order, corresponding author,
affiliations, emails and ORCIDs are all undecided and none may be inferred.

## Abstract

Take verbatim from `submission_candidate/main.tex`. It contains no equations and
no citations, as arXiv and the journal both prefer.

## Comments

Take `comments_field` verbatim from
`submission_candidate/package_manifest.json` — the packaging script derives it
from the build it just performed. **Do not type it**: this field once read
"18 pages, 6 figures" against a 22-page, 7-figure build because it was
maintained by hand.

Append: `Code and certificates available; see the data and code availability
statement.`

## Categories

    Primary:     hep-th
    Cross-list:  math-ph, math.RT

## Licence

    [PENDING — depends on the repository licence decision]

arXiv's licence choice should not contradict the software licence. Since the
software licence is unresolved, this is too.

## Linked identifiers

    Software / data DOI:  [PENDING ZENODO DEPOSITION]
    Report number:        [none, unless an institution assigns one]

## Before posting — checks the package already satisfies

- source-only archive, 25 files, no cover letter inside;
- master `main.tex` at the archive root; `main.bbl` included;
- all seven figures present;
- isolated compilation clean: 0 errors, 0 undefined citations, 0 undefined
  references, 0 overfull boxes;
- no absolute paths, no private comments, no internal TODOs;
- archive byte-reproducible, so the uploaded bytes can be re-derived.

## Before posting — checks that require humans

- [ ] every author approves the exact PDF;
- [ ] author order and corresponding author fixed;
- [ ] licence chosen;
- [ ] DOI inserted and the archives rebuilt afterwards.

**Do not post until all four are ticked.**
