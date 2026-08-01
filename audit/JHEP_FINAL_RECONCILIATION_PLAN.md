# Final reconciliation plan

How this branch rejoins the shared research branch, decided before the
reconciliation rather than during it.

## The situation

Two sessions have been working this repository. This one has been isolated in
a separate clone since the concurrency was discovered; the other has continued
to commit and push to `research/maximal-chiral-four-form-program`. Neither is
wrong to exist, but only one integration order is safe, and improvising it at
the end is how a certificate gets orphaned from the code that produced it.

## What must not happen

**No rebase of anything already pushed or used as a public base.** The three
Stage 0-2 commits were rebased once, before any of them was pushed and while
the only consumer was this working tree. That was legitimate. It is not
legitimate a second time: the matrix cells are bound by hash to commit
`5f46a2c`, and rewriting that commit would strand every cell's provenance
against a commit that no longer exists.

**No force-push.** Published scientific history is immutable here. This is a
standing repository rule, not a preference for this reconciliation.

**No rebase while the matrix runs.** Cells are produced against a frozen
source tree; moving the branch under a running evaluator is how pre-fix and
post-fix cells get mixed.

## Order of operations

1. Finish all 15 matrix cells.
2. Stamp cell provenance and assemble the matrix.
3. Reverify the 81x81 minor from the frozen artifacts.
4. Regenerate the science entry gate; require `PASS`.
5. Run the full validation suite once memory is released.
6. Fresh-clone science reproduction from the freeze candidate.
7. **Commit the completed science locally.** This commit is the one the
   certificate belongs to and it is never rewritten afterwards.
8. Fetch the remote **once**.
9. Inspect every intervening commit before integrating anything.
10. Integrate **once**.
11. Rerun the lightweight tests affected by whatever came in.
12. Tag and push.

Steps 8 through 10 happen after step 7, not before, so that the science commit
exists independently of whatever the other session has been doing.

## Integration method

**Merge, not rebase.** A merge keeps both parents, so the provenance chain from
the matrix-generation commit to the reconciled commit stays walkable:

    git fetch origin
    git merge --no-ff origin/research/maximal-chiral-four-form-program

A rebase would replay this branch's commits onto new bases, changing their
hashes and breaking the binding recorded in
`audit/RANK_MATRIX_CELL_PROVENANCE.json`. That binding is the only thing
connecting the certificate to the evaluator that produced it.

Preferred delivery is a pull request from `publication/jhep-tensor-spinor`
rather than a direct push to the shared branch, so the integration is
reviewable and the other session is not surprised by it.

## Expected conflict classes, and how each is settled

| class | files | resolution |
|---|---|---|
| generated audit files | `audit/JHEP_LIVE_REPOSITORY_STATE.md`, `JHEP_RESULT_INVENTORY.json`, `JHEP_CLAIM_INPUTS.json` | regenerate after the merge; never hand-merge a generated file |
| generated manuscript numbers | `manuscript/generated/numbers.tex`, `manuscript/prl/generated/numbers.tex` | regenerate from artifacts after the merge |
| append-only lists | `.gitignore`, claim ledgers, proof-obligation lists | keep both sides |
| status prose | `docs/JHEP_SPEC_STATUS.md`, `docs/CLAUDE_SESSION_HANDOFF.md` | take the other session's version, then append what this branch changed; their copy is the one their work describes |
| certificate artifacts | `results/rank81/**` | **this branch wins.** The other session's certificate has two cells; this one has the full matrix under a recorded execution id. Take theirs only if their cells carry a newer execution id, which would mean re-running the matrix |
| evaluator source | `spinor_trace_bridge/src/sdbridge/**` | **stop and assess.** See below |

## If evaluator source changed on the other branch

A change under `spinor_trace_bridge/src/sdbridge/` to any of the seven files
listed in `audit/RANK_MATRIX_EXECUTION_FREEZE.json` invalidates the matrix, and
the matrix has to be re-run under a new execution id. There is no version of
this where the old cells are kept and the new code is merged.

The decision procedure:

1. diff the source-critical files between the two branches;
2. if they are identical, the certificate survives the merge unchanged;
3. if they differ, determine whether the difference can change a Jacobian entry
   -- a comment or a docstring cannot, a contraction plan can;
4. if it can, discard the cells, bump the execution id, re-run;
5. record the decision either way, because "we looked and it was only
   comments" is a finding a referee is entitled to see.

## Provenance that must survive

| what | value |
|---|---|
| matrix execution id | `rank81-matrix-5f46a2cbbe93-flop1e11` |
| matrix generation commit | `5f46a2c` |
| source tree hash | recorded in `audit/RANK_MATRIX_EXECUTION_FREEZE.json` |
| final reconciled commit | recorded after integration |

The connection between the first and the last of these is what a reader needs
in order to believe the certificate, so both ends and the path between them are
recorded rather than left implicit in the graph.

## Branch protection

Force pushes disabled, pull requests required, status checks required, and
conversation resolution required on the shared research branch. Linear history
is deliberately **not** required: it would forbid the merge commit this plan
depends on.

Configuring this needs repository admin rights and is a human action; it is
recorded here as a request, not as something done.
