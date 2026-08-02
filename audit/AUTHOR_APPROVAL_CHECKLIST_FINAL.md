# Author approval checklist

**Nothing here may be ticked by anyone but the named person.** No item is
pre-filled. An unticked box is not an oversight; it is the current state.

Factual basis: `audit/AUTHORSHIP_AND_CREDIT_FINAL.md`.

## Step 1 — decide the author list

This cannot be derived from the contribution matrix. Decide, then record:

    Author 1: ______________________  affiliation: ______________________
    Author 2: ______________________  affiliation: ______________________
    Author 3: ______________________  affiliation: ______________________

    Corresponding author: ______________________
    Email:                ______________________

- [ ] Every person listed has agreed to be listed.
- [ ] Every person who contributed substantively is listed or acknowledged.
- [ ] Author order agreed by all listed authors.
- [ ] The mentor's status (author vs acknowledgement) decided **by the mentor**.

## Step 2 — per-author approval

One column per author. Every author ticks every row for themselves.

| item | A1 | A2 | A3 |
|---|:--:|:--:|:--:|
| inclusion as an author | [ ] | [ ] | [ ] |
| author order | [ ] | [ ] | [ ] |
| own affiliation as printed | [ ] | [ ] | [ ] |
| corresponding author | [ ] | [ ] | [ ] |
| exact title | [ ] | [ ] | [ ] |
| abstract | [ ] | [ ] | [ ] |
| final manuscript, in full | [ ] | [ ] | [ ] |
| data and code availability statement | [ ] | [ ] | [ ] |
| AI-use disclosure as written | [ ] | [ ] | [ ] |
| acknowledgments | [ ] | [ ] | [ ] |
| funding statement | [ ] | [ ] | [ ] |
| competing interests | [ ] | [ ] | [ ] |
| arXiv posting | [ ] | [ ] | [ ] |
| JHEP submission | [ ] | [ ] | [ ] |

## Step 3 — release and licensing

- [ ] Software licence chosen (currently **none**, which makes the code
      non-reusable regardless of where it is hosted).
- [ ] Public repository contents approved.
- [ ] Spinor-archive arrangement approved (manifest-only, or permission granted).
- [ ] Zenodo deposition authorised.
- [ ] DOI creation authorised.

## Step 4 — the two actions no automation may take

- [ ] **arXiv upload** — authorised by the corresponding author.
- [ ] **JHEP submission** — authorised by the corresponding author.

## Blocking conditions

Submission must not proceed while any of these holds:

1. Any Step 2 box is unticked for any listed author.
2. The mentor's G-1..G-10 responses are unrecorded (`review/MENTOR_DECISION_FORM.md`),
   G-10 in particular, since a wrong answer there invalidates `dim Q10 = 3`.
3. Any novelty row is still `PROVISIONAL` while the manuscript asserts novelty.
4. No licence is chosen.
5. The repository is public but the release contents are unapproved.

## Note on the current public state

The repository is already public and carries GitHub releases. That was done on
explicit instruction and is recorded here because it changes what "approval
before release" can still mean: the code and certificates are already visible.
What remains genuinely unreleased is the arXiv posting, the journal submission,
and the DOI.
