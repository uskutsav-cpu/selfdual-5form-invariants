# Session handoff

**Branch** `research/maximal-chiral-four-form-program`. **Nothing pushed.**
Protected branches untouched.

## 1. State

All twelve equation-(4.24) degree-10 candidates are implemented in
`src/sdinv/published_degree10_invariants.py`. Every one passes boost
invariance and homogeneity at two primes. `NOT_IMPLEMENTED` is empty.

## 2. The defect that shaped this session

`P10_07` was **not a Lorentz scalar** as shipped. It raised all six axes on both
inner `N^(1050)` factors, so three of its edges contracted with `delta` rather
than `eta`.

It was caught by the degree-10 projection reporting `not_in_atlas_span` on all
six primes — a consistent failure across independent moduli is structural, not
modular bad luck. Confirmed by a boost: rotation-invariant but boost-violating,
which is the unambiguous signature of a metric misplacement.

**No test would have caught it.** The suite checked homogeneity, which catches
int64 overflow, and nothing that constrains index placement. Three tests now
close that gap:

    test_every_published_candidate_is_boost_invariant
    test_p10_07_alpha_edge_placement_is_free
    test_the_original_p10_07_placement_really_was_broken

The general lesson is recorded as `C-P10-METHOD-01`: **index placement is
derived, not read.** PDF extraction returns stacked scripts in glyph-position
order and cannot distinguish `M_a{}^b` from `M^a{}_b`. The rule "every
contracted edge carries exactly one raised end" has a unique answer, and it
independently reproduces the placement that the boost test verified.

## 3. Results established

| result | value | primes | artifact |
|---|---|---|---|
| P10_01/02/03/06/07 → Q10 | all `[0,0,0]`, rank **0** | 6 | `published_degree10_map.json` |
| Level-A representatives → Q10 | rank **3 of 3** | 6 | `degree10_positive_control.json` |
| M-only family → Q10 | rank 0 | 6 | `M_only_quotient_test_deg10.json` |
| P12_01/02/03 → Q12 | rank 0 | 2 | `published_degree12_map.json` |

The positive control is what makes the zero rows meaningful: the projector
demonstrably *can* return rank 3, so a zero is a statement about the candidate
rather than about the pipeline. Without it, a projector stuck at zero would
print an identical table.

Every zero entry has `status = "solved"`, meaning the candidate lies in the
atlas span and its coordinates were obtained exactly. A candidate that merely
failed to solve would also contribute rank 0, for an uninformative reason.

## 4. Open source ambiguities — recorded, not guessed

Bracket **colour** does not survive PDF extraction, and colour is exactly what
fixes operation order in equation (4.24).

- **AMB-01** — extent of the red bracket in I^(4) and I^(9). Measured: the two
  readings give **different** values for I^(4).
- **AMB-02** — nested bracket association in I^(10), I^(11), I^(12). Measured:
  the two readings differ for I^(10) and I^(11), and **agree exactly** for
  I^(12), so AMB-02 is harmless for that candidate.

Both readings of each are implemented and projected separately, in a distinct
checkpoint column-id band, so a reading can never be confused with the
candidate it varies. Resolving either needs a colour render of journal page 17
/ arXiv page 25.

## 5. Infrastructure

`scripts/project_published_degree10_ckpt.py` supersedes the uncheckpointed
runner. Every evaluation is an immutable checkpoint unit, so adding a candidate
no longer re-pays the atlas. The artifact is rewritten after each prime, so a
kill loses at most one prime.

**Checkpoints must not live in iCloud.** The canonical tree is under
`~/Documents`, which is synced. Default root is a local temp path; override
with `SDINV_CKPT_ROOT`. Restrict primes with `SDINV_PRIMES`.

`peak_rss_mb` now decides its unit by `sys.platform`, not by magnitude.
`ru_maxrss` is bytes on Darwin and KiB on Linux, and at ~1 GB the two are
indistinguishable by value — the old heuristic reported 958576 MB.

## 6. Cost

~6 s per candidate evaluation at degree 10. A full six-prime, sixteen-evaluator
pass is ~2.6 h of evaluation plus the atlas. Budget accordingly, or use
`SDINV_PRIMES` for a first pass and let the checkpoints make the rest
incremental.

Do not run two memory-heavy jobs at once; this machine has 8 GB and has
silently killed pytest at ~60 MB free.

A process whose stdout is redirected is **block buffered**: an empty log does
not mean an idle job. Check `ps -p <pid> -o time` for CPU accumulation, and
check the output artifact's mtime — a run killed after it wrote its artifact
loses only the buffered log. That happened here and briefly looked like lost
work.

## 7. Next

1. Finish the twelve-candidate projection across all six primes.
2. If the published Q10 rank is 0, that is a **bounded negative result**, not a
   failure: the twelve published candidates lie in D10 and a compact Level-B
   basis for Q10 must be sought outside them. Write it as a failure
   certificate with the exact scope.
3. Build the reverse graph-to-block enumeration as an independent search. The
   positive control already shows the graph side reaches rank 3; the reverse
   engine's job is to find a *compact block* expression that does.
4. Clean-clone QUICK reproduction outside iCloud.
