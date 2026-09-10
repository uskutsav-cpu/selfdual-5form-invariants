# Data and code release — PREPARED, NOT DEPOSITED

Supporting material for *An exact degree-ten classification of local invariants
of the ten-dimensional self-dual five-form*.

**Nothing here has been deposited and no DOI exists.** Deposition requires an
authenticated human action and prior authorship, licence and release approval:
`audit/AUTHOR_APPROVAL_CHECKLIST.md`.

## Contents

| directory | what |
|---|---|
| `trace-code/` | the tensor-side package and its tests |
| `bridge-code/` | the spinor–tensor bridge and its tests |
| `certificates/` | every result JSON the manuscript reads |
| `reproduction/` | the scripts that regenerate numbers, tables and figures |
| `spinor-archive/` | a **manifest only** — see below |

`SHA256SUMS` and `DATA_AND_CODE_MANIFEST.json` cover all 170 files.

## What is deliberately absent

The third-party spinor enumeration archive is **not** redistributed.
Redistribution permission has not been granted (coauthor item G-7), and its logs
carry another person's home paths. What ships instead is a manifest with per-file
hashes, the expected local path, and adapter instructions, so a reader holding
their own copy can reproduce the archive-dependent results and verify their copy
matches ours.

Everything else regenerates without it: the atlas, the subspace incidence, the
exact characteristic-zero closure, the bridge, the degree-eight span equality and
the common-sample comparison. Only regeneration of the rank-81 certificates needs
the archive, and those certificates are included, so every number in the
manuscript is present regardless.

## Reproducing

```
python -m pytest                                   # tensor side
cd spinor_trace_bridge && python -m pytest         # bridge
python scripts/reproduce_all.py                    # the whole sequence, recorded
```

`scripts/reproduce_all.py` writes `verification/REPRODUCTION_RECORD.{json,md}`
recording what actually ran, including which steps were skipped or resumed. It
exits nonzero on any failure.

## Evidence strengths

`audit/FINAL_CLAIM_CERTIFICATE_MATRIX.md` maps every number in the manuscript to
its artifact and states whether it is analytic, exact over `Q`, exact over
`F_p`, numerical, or a stated limitation. The typeset number does not show this
and the distinction matters: `126 - 45 = 81` is a cited literature result, not
ours.

## Licence

**Not yet chosen.** Without one this code is not reusable regardless of where it
is hosted. It is a human decision and it is item 6 of the approval checklist.
