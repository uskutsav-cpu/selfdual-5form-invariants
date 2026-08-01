# Public release policy

## Authorised for public push

- User-authored source, tests, derivations, documentation, claim ledgers.
- Manuscript source, figures, tables, bibliography.
- Compact certificates and result matrices needed for reproduction.
- Environment locks, reproduction scripts, release notes.
- Project-authored audit summaries describing the external archive **without**
  redistributing its code or substantial contents.
- Annotated tags and source releases tied to verified commits.

## Prohibited

- The mentor archive in any form: ZIP, source, work directories, substantial
  extracts, raw run outputs.
- Secrets, tokens, keys, credentials.
- Personal absolute paths, caches, bytecode, temporary checkpoints.
- Regenerable large arrays in ordinary Git history.
- Any artifact whose authorship or licence cannot be established.

## Enforcement

| control | mechanism |
|---|---|
| secret scan | pattern match over every text file; build **fails**, not warns |
| absolute path scan | `/Users/<name>/` pattern; build fails |
| archive exclusion | archive lives outside the repository tree; allowlist copy |
| large files | inventory in `results/large_file_inventory.json`; nothing tracked above 1 MB |
| history rewriting | **never force-push**; published scientific history is immutable |

## Current state

Largest tracked file is the compiled manuscript at 378 KB. The two files over
10 MB on this machine (a `nauty` test answer file and a scheduling SQLite
database) are both **untracked** and outside the published tree.

## Licence

**Not yet chosen.** Without one the code is not reusable regardless of where it
is hosted. This is a human decision recorded in
`submission_candidate/AUTHORSHIP_DECISION_REQUIRED.md` item 6, and the release
carries `LICENCE-DECISION-REQUIRED.md` rather than a guessed licence.
