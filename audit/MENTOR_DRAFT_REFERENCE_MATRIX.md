# Reference matrix for the mentor draft

Every entry in `manuscript/jhep/references.bib` was checked against a primary
landing page — arXiv, the publisher, ACM or JOSS — during preparation of this
draft. No entry is reconstructed from memory or from a search-result snippet.

Verification status legend:

- **landing page** — the arXiv or publisher abstract page was fetched and the
  title, author list and journal reference read off it.
- **indexed record** — the bibliographic record was confirmed through a search
  index that quoted the volume, page and year, where the publisher page itself
  blocks automated access.

| key | verified | how | notes |
|---|---|---|---|
| `Cederwall:2025invariants` | yes | landing page (carried from the audited earlier bibliography) | J. Phys. A 59 (2026) 065203 |
| `Hutomo:2025chiral` | yes | landing page | no journal reference exists yet; field left absent rather than guessed |
| `Elamaran:2025mlinv` | yes | landing page | the method paper this work builds on |
| `Marcus:1982yu` | yes | indexed record | Phys. Lett. B 115 (1982) 111 |
| `Henneaux:1988gg` | yes | indexed record | Phys. Lett. B 206 (1988) 650 |
| `Pasti:1995tn` | yes | landing page | |
| `Pasti:1997gx` | yes | landing page | |
| `Sen:2019qit` | yes | landing page | J. Phys. A; DOI read from the arXiv record |
| `Mkrtchyan:2019wnk` | yes | landing page | JHEP 12 (2019) 076 |
| `Townsend:2019ftg` | yes | landing page | |
| `Bandos:2020hgy` | yes | landing page | full author list confirmed |
| `Ferko:2024chiral` | yes | landing page | **corrected entry, see below** |
| `Brizio:2026ttbar` | yes | landing page | no journal reference yet |
| `Green:1997as` | yes | landing page | |
| `Paulos:2008tn` | yes | landing page | five-form higher-derivative terms; the closest Type IIB work to this paper's subject |
| `Liu:2022bfg` | yes | landing page | JHEP 08 (2022) 267 |
| `Kugo:1982bn` | yes | carried from the audited earlier bibliography | |
| `McKay:2013` | yes | indexed record | J. Symb. Comput. 60 (2014) 94; the citation `nauty` itself asks for |
| `Bareiss:1968` | yes | indexed record | Math. Comp. 22 (1968) 565 |
| `Wang:1982` | yes | indexed record | SIGSAM Bull. 16 (1982) 2; ACM blocks automated fetch |
| `Zippel:1979` | yes | carried from the audited earlier bibliography | |
| `Schwartz:1980` | yes | carried from the audited earlier bibliography | |
| `Harris:2020` | yes | landing page (arXiv record of the Nature paper) | |
| `Smith:2018` | yes | landing page (JOSS) | |

## A corrected entry

The bibliography used by the earlier manuscript contained:

```bibtex
@article{Bandos:2024chiral,
  title   = {Interacting chiral form field theories and ...},
  eprint  = {2402.06947},
  ...
}
```

with **no `author` field at all**, under a key naming Bandos. Bandos is not an
author of that paper. The actual author list, read from the arXiv landing page,
is Ferko, Kuzenko, Lechner, Sorokin and Tartaglino-Mazzucchelli, and the paper
appeared as JHEP 05 (2024) 320.

The mentor draft uses the key `Ferko:2024chiral` with the correct authors. The
earlier bibliography at `manuscript/references.bib` is left as it stands, since
this goal does not authorise changing the earlier manuscript; the defect is
recorded here so it is not carried into a submission.

## Coverage check

Run by `manuscript/jhep/scripts/check_draft.py`:

- every entry in the `.bib` is cited in the text — **pass** (this gate initially
  failed on `Bandos:2020hgy`, which was uncited; it is now cited in the
  introduction);
- every `\cite` key resolves to an entry — **pass**;
- undefined citations reported by LaTeX — **0**.

## Software citation discipline

Only software the repository actually uses is cited: NumPy, `nauty` (through
`pynauty`), and `opt_einsum`. The last is cited with an explicit statement that
it is optional and was **not** installed for the certified runs, because citing
it without that qualification would overstate what the certified pipeline
actually exercised. `pytest` is used but is a test runner rather than a
scientific dependency, and is named in the reproduction appendix rather than
cited.

## Limits of this audit

A reference matrix establishes that the works cited exist and are cited
correctly. It does not establish that no relevant work was missed. Absence of
evidence is not evidence of absence, and a mentor who knows the field may
recognise a result that no search would surface. See the novelty ledger.
