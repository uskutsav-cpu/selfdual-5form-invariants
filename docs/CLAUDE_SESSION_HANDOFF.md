# Session handoff

Last updated 2026-08-01. Branch `research/maximal-chiral-four-form-program`.

## Where things stand

A complete private scientific and technical submission candidate exists. The
manuscript compiles from the official journal class with zero errors and zero
undefined citations or references, every scientific number in it is generated
from a JSON certificate, and a fresh clone reproduces all of it.

## The three findings a successor should know

1. **The signature blocker was wrong.** The oscillator frame is split `(5,5)`,
   not Euclidean. Real self-dual five-forms exist there, `⋆² = +1`, and the
   bridge was buildable all along. See `spinor_trace_bridge/docs/REAL_FORM_DICTIONARY.md`.

2. **`12 = 12` was a coincidence.** The published degree-ten span is not a
   complement to the products; it contains one product direction, so its
   non-product content is eleven. The structural decomposition is
   `A10 = G10 ⊕ P10`. See `docs/DIMENSION_DICTIONARY.md`.

3. **Degree eight disagrees, and should.** The spinor port-graph stream reaches
   6 where the tensor side reaches 7, with strict containment. This reproduces
   the archive's own finding that structured tensor-word candidates are needed
   there. It is corroboration, not a bug.

4. **The exact Jacobian now covers all 83 candidates and reaches rank 81.** An
   earlier revision of this file said 59 for the port-graph subset; that is
   superseded. See `docs/RANK81_EXACT_CERTIFICATE.md`. The bound is
   `rank_Q >= 81` unconditionally, witnessed by an explicit 81x81 minor. The
   matching upper bound is analytic and stays that way.

## What is deliberately incomplete

| item | state |
|---|---|
| float64 seed/scale/step Jacobian matrix | not run; one configuration costs >10 min. Replaced by an exact analytic Jacobian, which is stronger |
| degree-10 no-stop terminal status | see `verification/SPINOR_DEGREE10_NO_STOP.md`; cluster script prepared, no cluster run has occurred |
| certified rational reconstruction | not done; no claim depends on it, and every modular result is used as a lower bound only |
| PO-03 / PO-05 / PO-07 / PO-09 | open, see `docs/PROOF_OBLIGATIONS.md` |
| PO-08 | now split: the cardinality bound is **discharged analytically**; removal-minimality under general `GL` is still open |
| novelty rows | all PROVISIONAL — the literature sweep is *done* (`audit/RELATED_WORK_COMPLETE.md`); what is missing is coauthor confirmation, which is a human gate |

## Machine constraint worth knowing before you start a long run

This machine has 8 GB. The degree-12 exact contractions run close to that, and
two heavy jobs at once get one of them killed — a `--no-hilbert-stop` scan and
two separate rank-81 runs died that way, in each case silently, with the process
simply gone and no traceback. Run one at a time.

Everything long resumes rather than restarts: the rank-81 runner keys its row
cache by prime, seed, candidate id and formula hash, and the incidence generator
skips primes already recorded. Re-issuing the identical command is the correct
response to a killed run.

## Where the human gates are

- `submission_candidate/AUTHORSHIP_DECISION_REQUIRED.md` — ten items
- `spinor_trace_bridge/docs/MENTOR_REVIEW_ITEMS.md` — G-1 to G-7
- `audit/NOVELTY_MATRIX.md` — every row PROVISIONAL

## How to pick this up

```bash
python -m pytest                                  # 199
cd spinor_trace_bridge && python -m pytest        # 72
python manuscript/scripts/make_numbers.py         # regenerate from artifacts
python manuscript/scripts/make_tables.py
python manuscript/scripts/make_figures.py
python scripts/build_submission_package.py        # isolated build + archives
python manuscript/scripts/check_manuscript.py     # 32 wording and claim gates
```

Long runs write incrementally and skip completed work, so re-issuing the same
command resumes rather than restarts.

## Warnings

- The scratchpad is wiped between sessions. The working virtualenv lives at
  `../.venv`, outside the repository.
- The third-party spinor archive at `../spinor-work` is **not** redistributable
  and is excluded from the repository and the release candidate.
- Run the bridge suite from inside `spinor_trace_bridge/`. Invoking it from the
  repository root with `-c` collects the wrong tests.
