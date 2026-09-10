# Citation-to-claim map

Every citation in the manuscript, and the exact statement it supports.

| citation | supports | where | is the source's own claim? |
|---|---|---|---|
| `Hutomo:2025chiral` | the count of 81 functionally independent invariants, and that it follows from the trivial generic stabiliser | intro, eq. (1.1); sec. on the Jacobian | yes, stated in the abstract |
| `Hutomo:2025chiral` | the stress-tensor flow construction as the motivating context | physics section | yes |
| `Cederwall:2025invariants` | the twelve explicit degree-ten candidate structures and three degree-twelve structures | intro, "what was previously available" | yes, eq. (4.24) and (4.25) |
| `Kugo:1982bn` | Majorana--Weyl spinors exist in signatures with $s-t\equiv 0 \bmod 8$ | spinor section | yes |
| `Schwartz:1980`, `Zippel:1979` | the $O(\deg/p)$ failure probability for a random specialisation | modular-caveat subsection | yes |

## Checks performed

- No uncited bibliography entries: every entry above appears in the text.
- No unresolved citations: the LaTeX build reports zero undefined citations.
- No duplicates.
- No secondary sources, mirrors or search snippets are cited.
- Every entry was checked against a publisher or arXiv landing page; see
  `BIBLIOGRAPHY_AUDIT.csv` for which fields were verified and which are absent
  upstream.

## Statements deliberately NOT attributed to a citation

- The split-signature identification of the oscillator frame. This is our own
  computation on the archive's operators, not a literature statement.
- The invariant-ring-dimension-independence-of-real-form argument. Standard, and
  given inline as a one-line density argument rather than cited, pending the
  coauthor decision recorded as review item G-3.
