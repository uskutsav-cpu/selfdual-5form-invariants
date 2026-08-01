# Authorship and disclosure decisions — HUMAN ACTION REQUIRED

Nothing in this file may be filled in by inference. Each item states exactly what
decision is needed and what evidence exists.

## 1. Author list and order — UNRESOLVED

**Decision needed:** who is an author, and in what order.

**Evidence available:** `CONTRIBUTION_LEDGER.csv` records what was done and by
which agent, from commit history and run records. It deliberately does not name
people, because contribution records do not by themselves determine authorship.

- [ ] author list agreed
- [ ] order agreed
- [ ] every listed author has seen the final manuscript and consents

## 2. Corresponding author — UNRESOLVED

Currently `corresponding.author@placeholder.invalid`, chosen so that the file
compiles and so that an accidental send fails rather than reaching a real inbox.

- [ ] corresponding author named and email supplied

## 3. Affiliations — UNRESOLVED

- [ ] affiliation supplied for each author

## 4. Acknowledgments and funding — UNRESOLVED

No funding source may be stated without documentation.

- [ ] acknowledgments text supplied, or confirmed empty
- [ ] funding statement supplied, or confirmed none

## 5. Competing interests — UNRESOLVED

- [ ] competing-interests statement supplied

## 6. Licence for the code release — UNRESOLVED

The tensor and bridge code have no licence file. Without one, "public repository"
does not imply reusable.

- [ ] licence chosen for the tensor code
- [ ] licence chosen for the bridge code

## 7. Redistribution of the spinor archive — UNRESOLVED, BLOCKING FOR RELEASE

The archive is third-party. Its logs contain another person's home-directory
paths. It is **excluded** from the repository and from the release candidate;
only a manifest with per-file hashes and adapter instructions is shipped.

**Decision needed:** obtain written redistribution permission, or confirm the
manifest-only arrangement is final.

- [ ] permission obtained, in writing
- [ ] manifest-only confirmed as final

## 8. Data DOI — NOT CREATED

No DOI has been created. Doing so is a public act and requires authorisation.

- [ ] archival repository chosen
- [ ] DOI creation authorised

## 9. Mentor scientific approval — NOT OBTAINED

See `spinor_trace_bridge/docs/MENTOR_REVIEW_ITEMS.md`, items G-1 to G-9, and
`audit/NOVELTY_MATRIX.md`, every row of which is marked PROVISIONAL.

- [ ] formulas and dimension definitions confirmed
- [ ] signature derivation confirmed
- [ ] spinor conventions confirmed (in particular the reconstructed index placement)
- [ ] novelty wording confirmed
- [ ] physics interpretation confirmed

## 10. Submission authorisation — NOT GIVEN

- [ ] public repository push authorised
- [ ] arXiv upload authorised
- [ ] journal submission authorised

## Current status

**Complete private scientific and technical submission candidate, awaiting only
the listed human decisions, approvals and authorised public actions.**
