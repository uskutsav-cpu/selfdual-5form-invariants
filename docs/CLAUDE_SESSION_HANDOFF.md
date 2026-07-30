# Session handoff

**Branch** `research/maximal-chiral-four-form-program`. Nothing pushed.

## Active process

    PID 62403  scripts/project_published_degree12.py --primes 32749 32717
    79-98% CPU, RSS 1248-1566 MB, ~39 min elapsed, 36/72 columns (prime 32749)
    log: /private/tmp/.../scratchpad/p12proj2.log

**This run has NO checkpointing** -- it predates the checkpoint layer. If it
dies, all 36 columns are lost and it must restart. Do not launch any other
heavy job while it runs.

Measured deceleration (this is why checkpointing was built):

    cols  1-12:   76 s   ( 6.3 s/col)
    cols 13-24:  609 s   (50.8 s/col)
    cols 25-36: 1086 s   (90.5 s/col)

Extrapolated remaining for prime 32749 alone: ~1.7 h; two primes ~4 h. With
RSS near the 1.5 GB ceiling and ~60 MB free, an OOM kill before completion is
likely.

## Resource triage performed

| | |
|---|---|
| P10 projection PID 63598 | terminated with SIGTERM (clean, no SIGKILL needed) |
| work lost | none measurable -- log was 0 lines, still buffered |
| free RAM before | 62 MB |
| free RAM after | 1030 MB |
| P12 | preserved, healthy |

## Formulas

Implemented: P10_01, P10_02, P10_03, P10_06, P10_07; P12_01, P12_02, P12_03.

Blocked, with reasons:

| id | reason |
|---|---|
| P10_05, P10_08 | black brackets on the M factors, e.g. `(MM)_{[nu1}^{[mu1} M_{nu2]}^{mu2]}`; need BracketOp on the M product |
| P10_04, P10_09 | RED brackets `(mu ... rho]lambda)`; need staged programs |
| P10_10, P10_11, P10_12 | nested black structures, larger index bookkeeping |

## Ranks

- M-only Q10 rank: **0** (six primes, non-vacuous)
- P10 Q10 rank from P10_01/P10_02: **0 / 3**
- P10_03, P10_06, P10_07 projections: **NOT RUN** (killed during triage)
- P12 Q12 rank: **pending**

## Next exact command

Wait for P12 to finish or die. Then, with nothing else running:

    .venv/bin/python scripts/project_published_degree10.py

If P12 died, rewrite it to use `sdinv.projection_checkpoint.ProjectionCheckpoint`
before rerunning -- do NOT rerun the non-checkpointed version.

## Checkpoint capability

`src/sdinv/projection_checkpoint.py` -- one immutable file per
(prime, sample, column) plus an atomic manifest. Corrupt or truncated units
fail their checksum and are recomputed; an atlas-hash mismatch refuses the
resume outright. 8 tests in `tests/test_projection_checkpoint_resume.py`.

**Not yet wired into the projection scripts.** That is the next code task.

## Safety notes

- Bare multi-operand `np.einsum` on modular operands wraps silently; the
  P10_02 incident (9605 -> 4674) is a permanent regression test.
- Homogeneity at several `c` is the detector that catches wrapping.
- `graph_record` vs `graph` caused a RecursionError at degree 12; a `_seen`
  guard now turns self-reference into an explicit error.
