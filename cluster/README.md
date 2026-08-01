# Cluster jobs

**No cluster run has occurred.** No cluster was available for this work, and
nothing in the manuscript depends on one. These files are prepared so that a
human with access can launch the degree-12 extension without re-deriving the
setup, and so that the claim "this needs a cluster" is backed by an actual job
script rather than an assertion.

Both scripts are deterministic: fixed commit, fixed dependency lock, fixed seed
per shard, immutable output directory, checkpoint interval, memory cap and time
cap. A shard that is re-run produces the same output or refuses to overwrite.

## Order of operations

1. Run `spinor_degree10_smoke.slurm` on one node. It must finish and reproduce
   the degree 4/6/8/10 ranks 1, 2, 7, 14 before anything larger is launched.
2. Only then submit `spinor_degree12_production.slurm`.

## What the smoke test proves

That the environment on the cluster reproduces results already established on a
laptop. If it does not, the discrepancy is in the environment, and the production
job would have inherited it silently.
