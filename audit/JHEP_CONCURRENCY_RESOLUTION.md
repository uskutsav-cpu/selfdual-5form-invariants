# JHEP concurrency resolution

Generated 2026-08-01T20:38:08+00:00 by `scripts/emit_jhep_authoritative_base.py`.

## The situation, stated plainly

Two Claude sessions worked this repository at the same time. The first
indication was not a merge conflict: it was a file written by this session
appearing inside a commit made by the other one, ninety seconds later.

## Authoritative commits

| field | value |
|---|---|
| branch | `publication/jhep-tensor-spinor` |
| authoritative local commit | `9393bf544ab864815edee84b0a657023d95245cf` |
| base it stands on | `5a5ff7a6cb76a8604dbc28ee78cf0a35d2ca973d` |
| previous base | `a962e7f8111fe90cc02f5fb7760b5fd27db5a1d3` |
| remote head when recorded | `035b772aa198ce00ea492be410bd39697fe7f969` |
| remote moved since base | yes |

## 25 commits incorporated from the other session

| sha | date | subject |
|---|---|---|
| `5a5ff7a6cb76` | 2026-08-01T15:14:22-05:00 | Regenerated artifacts from the final build |
| `9050bc2ac1d2` | 2026-08-01T15:12:45-05:00 | Count the dots correctly; the fallback is the normal path here |
| `97f2a3dd4c24` | 2026-08-01T15:10:37-05:00 | Handoff: four findings, not three, and the degree-8 one is stronger now |
| `109a7bbf4f66` | 2026-08-01T15:10:19-05:00 | Handoff: a completed background job may leave live children |
| `7f7753068190` | 2026-08-01T15:09:11-05:00 | A resumed step must not read as a fresh one |
| `43624e8c0b67` | 2026-08-01T15:07:41-05:00 | Ship the rank-81 certificates in the release, and stop leaking a home path |
| `5b381d73fee1` | 2026-08-01T15:06:05-05:00 | The degree-8 row count is prime-dependent; say so instead of quoting one |
| `49256cfedd1b` | 2026-08-01T15:04:07-05:00 | Drop two undefined symbols from the degree-8 paragraph |
| `93a5c77b887c` | 2026-08-01T15:02:11-05:00 | Report the degree-8 drop test, which the package had and the paper did not |
| `8fb73be6ac16` | 2026-08-01T14:59:44-05:00 | Correct the diagnosis: it was orphaned processes, not memory |
| `3f395c0e497f` | 2026-08-01T14:56:54-05:00 | Spec status: record the defect class this revision kept finding |
| `8b0cecec3719` | 2026-08-01T14:55:58-05:00 | Let the reproduction driver resume from a completed step log |
| `81d0dc75d376` | 2026-08-01T14:52:17-05:00 | Write the missing Jacobian stability document, and repair a stale summary |
| `e519cab9f941` | 2026-08-01T14:47:58-05:00 | Put the three unused figures in the paper and generate the arXiv comments field |
| `e39c2e7db687` | 2026-08-01T14:44:47-05:00 | Generate the reproduction record instead of writing it by hand |
| `a68db7dba4ef` | 2026-08-01T14:40:34-05:00 | Gate the overclaim that was just retracted |
| `deb20ca7ee24` | 2026-08-01T14:39:53-05:00 | Retract "not a bound" from the Letter's central consequence |
| `402afeb56b86` | 2026-08-01T14:37:53-05:00 | Make the incidence generator resumable and check each prime before recording it |
| `dd39d990370e` | 2026-08-01T14:36:07-05:00 | Write the degree-10 no-stop cluster job the docs already claimed existed |
| `4751fff28432` | 2026-08-01T14:33:51-05:00 | The same wrong sentence was in the manuscript, not just the dictionary |
| `442b05a427f8` | 2026-08-01T14:32:57-05:00 | Fix the dimension dictionary, which had made the mistake it exists to prevent |
| `68d381b62ec6` | 2026-08-01T14:31:21-05:00 | Collect the test counts instead of typing them, and gate the prose that cannot |
| `94319b63f022` | 2026-08-01T14:26:36-05:00 | Checklist and ledger: record what is deliberately not complete |
| `26d3b719d46e` | 2026-08-01T14:25:24-05:00 | Say which numbers a bad prime could actually change, and which it cannot |
| `c9e03d137cee` | 2026-08-01T14:20:10-05:00 | Bring the audit documents up to the current state |

They touched 93 files. The full list is in
`audit/JHEP_AUTHORITATIVE_BASE.json`.

## Commits authored on this branch

| sha | date | subject |
|---|---|---|
| `9393bf544ab8` | 2026-08-01T15:29:26-05:00 | JHEP Stage 2: a source corpus fetched from registries, not written from memory |
| `2f881463de12` | 2026-08-01T15:29:12-05:00 | JHEP Stage 1: a science entry gate that reads artifacts, not reports |
| `5d447374d761` | 2026-08-01T15:29:12-05:00 | JHEP Stage 0: record the live repository state from the tree, not from prose |

## Conflicts and how each was settled

| path | resolution |
|---|---|
| `audit/JHEP_CLAIM_INPUTS.json` | add/add. Both sessions ran scripts/emit_jhep_live_state.py and committed its output. The file is generated, so neither side was edited by hand: resolved by regenerating against the new base, which is what the file is supposed to describe. |
| `audit/JHEP_LIVE_REPOSITORY_STATE.md` | add/add, same cause and same resolution as JHEP_CLAIM_INPUTS.json. |
| `audit/JHEP_RESULT_INVENTORY.json` | add/add, same cause and same resolution as JHEP_CLAIM_INPUTS.json. |
| `.gitignore` | content conflict at the end of the file. The other session added verification/reproduction-logs/, this branch added audit/.source_cache/. Both rules are wanted; resolved by keeping both lines. |

Every conflict was in a generated file or in an append-only list. No
scientific artifact conflicted, because the two sessions wrote results to
different trees.

## Were concurrent writers eliminated?

**No, and deliberately not.** Terminating the other session's work in
flight was weighed and rejected; the instruction was to reconcile at the
end instead. What makes that safe is isolation, not termination:

| control | how it works |
|---|---|
| Separate working trees | This branch is a clone at ~/Downloads/sdinv-jhep, outside iCloud and outside the other session's tree. No file is shared; nothing either session writes lands in the other's checkout. |
| Per-cell immutable certificate outputs | run_rank81_cell.py writes results/rank81/cells/cell_p{p}_s{seed}.json, one file per cell, never a shared summary. The older loop rewrote a single certificate.json after every cell, which is how a partial run could overwrite a complete one. |
| Atomic writes | Each cell is written to a temporary file in the same directory and moved into place with os.replace, so a reader never sees a half-written cell and a crash cannot truncate a good one. |
| Per-cell lock files | A second driver for the same cell finds the lock, prints who holds it, and exits 2 rather than racing. |
| Refusal to overwrite complete cells | A cell already marked cell_complete is skipped unless --force, so re-running the matrix cannot downgrade a finished result. |
| Read-only aggregation | assemble_rank81_matrix.py only reads cells. It fails on a missing cell, a duplicate, a candidate-ordering difference, a coordinate-dimension difference or an incomplete terminal status, rather than assembling something partial into a certificate. |
| Push deferred | Push is the only operation that can actually race, and it is held until the final reconciliation. |

## Live writers at record time

| pid | elapsed / state | working directory |
|---|---|---|
| 57152 | `06:06 RN` | `/Users/swethasunilkumar/Downloads/sdinv-jhep` |

A process in the other session's tree is not a hazard to this branch;
it cannot reach these files. The list is recorded so the claim can be
checked rather than believed.

