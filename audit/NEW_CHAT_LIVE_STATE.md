# New-chat live state — Phase 0

Generated 2026-08-01 by a fresh execution context. Nothing below is carried
over from another chat; every line was re-derived from the filesystem, from
`git`, from `ps`/`lsof`, or from artifact JSON in this tree.

## The single most important correction

**The reported commit `b77ef4d` is not on the science branch.** It is an
ancestor of `7e4ea08` on `research/maximal-chiral-four-form-program`, and it
lives in the **iCloud canonical tree**, not here.

The handoff prompt's "reported scientific state" bundles together two
different lines of work that were never the same tree:

| reported item | where it actually is | status |
|---|---|---|
| 24-page manuscript, 7 figures, 118 macros, 72 gates, `b77ef4d` | `~/Documents/Codex/2026-07-29/now/work/selfdual-5form-invariants` (iCloud), branch `research/…`, head `7e4ea08` | exists, compiled at some earlier date |
| rank-81 matrix, exact D10/Q10, G-10, proof obligations, novelty ledger | `~/Downloads/sdinv-jhep`, branch `publication/jhep-tensor-spinor`, head `c480b35` | **authoritative science tree**, 18 unpushed commits |

`manuscript/jhep/` in the authoritative tree contains exactly one file,
`ai_assistance_disclosure.md`. There is no `main.tex` here. That is **correct
and intentional**: the prompt forbids drafting before the Science Completion
Gate passes, and the previous execution obeyed it. The manuscript in the
iCloud tree is a *prior* artifact built on the un-hardened science; it is a
reference, not the deliverable, and it must be regenerated from certified
results after the gate.

## Authoritative tree

```
~/Downloads/sdinv-jhep
branch  publication/jhep-tensor-spinor
head    c480b35  "Phase 5: final domain-qualified status for every degree-10 space"
```

Branch is **not on the remote**. Remote has 7 branches and 8 tags; the newest
remote science branch head is `research/…` = `7e4ea08`. Working tree carries
4 modified/untracked paths, all of them live matrix output.

Other trees found and classified: `~/Downloads/sdinv` (stale, `7ed4645`),
`~/Downloads/sdinv-classification` (stale, `d7d22e4`, 30 dirty),
`~/Downloads/sdinv-phase0-clone` (stale, detached `3ed3280`),
`~/Downloads/sdinv 2` (not a repo), `/private/tmp/jhep-final2` (clean-clone
test run, `ba311a0`).

## Writers — one per artifact, nothing killed

| pid | job | writes | verdict |
|---|---|---|---|
| 60151 | `run_rank81_matrix.sh`, 2h13m, orphaned to launchd | `results/rank81/cells/` | **keep** — this *is* the Phase 2.3 job |
| 93680 | `run_rank81_cell.py --prime 32717 --seed 33` | `cell_p32717_s33.*` | **keep** — cell in flight, holds the one lock |
| 87504 | `pytest -q` in `/private/tmp/jhep-final2`, 30m | `/private/tmp/final2_tensor.log` | **keep** — Phase 2.1 tensor suite |

No stale writer was found and none was terminated. The duplicate-writer
contamination recorded earlier (six concurrent pytest processes) has cleared:
`lsof` confirms `final2_tensor.log` now has exactly one writer. At most one
matrix driver, one cell worker, and one lock are live. **The one-authoritative-writer
condition holds.**

The two running jobs are exactly the work Phases 2.1 and 2.3 demand. Killing
them would discard ~2h20m of compute and re-derive nothing. They are left to
finish.

## Rank-81 matrix — 8 of 15 cells complete, all clean

Design: fitting primes 32749/32719/32717 × seeds 11/22/33, then holdout
primes 32713/32707 × the same seeds. Sequential by design (8 GiB machine;
parallel cells swapped and were slower). Every cell resumable from its row
cache; a completed cell is skipped.

Every one of the 8 completed cells reports identically:

```
cell_complete            true
n_candidates_scheduled   83
by_terminal_status       {evaluated: 83}      0 errors, 0 interrupted, 0 skipped
euler_homogeneity        83 passed, 0 failed
zero_rows                []
coordinate_dimension     126
rank                     81
method                   exact analytic Jacobian; no finite differences, no tolerance
```

Cumulative rank by degree is identical across all 8 cells:
`{4: 1, 6: 3, 8: 9, 10: 21, 12: 81}`. Degree 12 contributes 60 of the 81 —
so degree-12 data is **load-bearing** for the rank-81 theorem, which is
consistent with the Phase 10 scope ruling (degree 12 is a certified *input*
to rank 81, not a tensor–spinor equivalence claim).

Remaining: `p32717/s33` in flight, then 6 holdout cells. At the observed
cadence this finishes in roughly 1.5–2 h.

## Clean-clone tensor suite

`/private/tmp/jhep-final2`, branch `research/…`, head `ba311a0`. Running
under `pytest -q -p no:cacheprovider`, sole writer of its log, ~96% through
with all dots — no `F`, no `E`. Not yet terminal, so no pass is claimed yet.
Note this clone is on `research/…`, **not** the science branch, so when it
finishes it certifies that branch, not `publication/jhep-tensor-spinor`. A
final authoritative suite still has to be run at the actual proposed science
commit (Phase 2.1 requirement).

## Hard external blocker — no TeX on this machine

```
pdflatex latexmk tectonic xelatex lualatex   ALL MISSING
/usr/local/texlive  /Library/TeX  brew tex   ABSENT
```

`manuscript/main.pdf` in the iCloud tree (443 KB) proves LaTeX was available
at some earlier point; it is not available now. This blocks **Phase 13**
(compile), **18** (JHEP format), **19** (clean-clone must compile with zero
LaTeX errors), and **21** (arXiv/JHEP source archives must build in
isolation). No amount of science work removes it.

Free disk is **11 GiB**, so full MacTeX (~7–8 GiB installed) is tight;
BasicTeX (~100 MB, plus `tlmgr` for `revtex`/`jheppub` dependencies) is the
realistic option. Installing either needs the user's password.

## Phase 0 verdict

Phase 0 complete. One authoritative writer confirmed. Two required
long-running jobs left running. The manuscript-side reported state was
traced to a different tree and reclassified as a reference artifact. The
science branch is intact with 18 unpushed commits and its `manuscript/`
correctly still empty.
