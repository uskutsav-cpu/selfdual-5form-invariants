# Bibliography completeness — final audit

12 entries, 12 cited, **0 uncited**, 0 undefined citations.

## The gap this audit found

The manuscript did not cite **Elamaran, Ferko and Scarlett, *Machine Learning
Invariants of Tensors*** (arXiv:2512.23750), the paper whose
enumerate–evaluate–relate method this work uses and extends. It was named in the
repository README as the work being extended and was absent from the article.

That is the most serious kind of citation gap: not a missing background
reference, but the missing attribution of the method. The introduction now
carries a **Method** paragraph naming the authors, saying they introduced the
workflow and applied it to a three-form in six dimensions, and stating plainly:

> We do not claim that workflow as new.

Verified against the arXiv record: Athithan Elamaran, Christian Ferko, Sterling
Scarlett; submitted 26 December 2025; `doi:10.48550/arXiv.2512.23750`; hep-th,
cross-listed math.AC.

## Entries added, and where each is cited

| entry | supports | placed |
|---|---|---|
| `Elamaran:2025mlinv` | the method itself | introduction, Method |
| `Pasti:1995tn`, `Pasti:1997gx` | a covariant action for a chiral form needs auxiliary structure | conventions appendix, G-10 formulation independence |
| `Bandos:2020hgy`, `Townsend:2019ftg` | few invariants in four and six dimensions | introduction, the contrast with low dimensions |
| `Bandos:2024chiral`, `Brizio:2026ttbar` | six-dimensional flow universality | introduction, the baseline the $D=10$ deficit contrasts with |

## One entry was removed

A `p`-form review (arXiv:2504.01421) was added, then removed: its author list
could not be verified from the search record, and there was no place where it was
the *right* citation rather than an additional one. Padding a bibliography to
raise a count is what this audit exists to prevent.

## What the count does and does not mean

Twelve references is small for a 24-page article, and that is a property of the
subject rather than an omission. The paper computes one graded piece of one
invariant ring; its prior-work surface is three primary papers plus the method
paper, the conventions literature, and two algorithmic citations
(Schwartz–Zippel). Every claim about prior work maps to a specific source in
`audit/CLAIM_SOURCE_MAP_FINAL.md`.

The full search record — six papers audited directly at their arXiv or publisher
landing pages, each with a verdict on whether it pre-empts a claim here — is in
`audit/RELATED_WORK_COMPLETE.md`.

## Priority language

Every use of *first*, *complete*, *exact*, *unique*, *canonical*, *minimal*,
*exhaustive* or *previously unknown* is checked by the wording gates in
`manuscript/scripts/check_manuscript.py`, and the novelty positions are in
`audit/NOVELTY_MATRIX.md`, where **every row remains PROVISIONAL** pending
coauthor confirmation.
