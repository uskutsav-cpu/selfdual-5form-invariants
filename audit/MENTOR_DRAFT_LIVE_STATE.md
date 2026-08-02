# Live state at the start of the mentor-draft work

Verified rather than assumed. Every value below was read from the repository on
the day the mentor draft was built, not carried over from an earlier report.

## Repository

| item | value |
|---|---|
| remote | `https://github.com/uskutsav-cpu/selfdual-5form-invariants` |
| local HEAD at start | `aa0f98e9054ab1725d6093ce81a80a4960673e60` |
| remote `publication/jhep-degree10-final` | `aa0f98e9054ab1725d6093ce81a80a4960673e60` |
| local and remote agree | yes |
| working tree at start | clean |
| draft branch created | `publication/jhep-mentor-draft`, from `aa0f98e` |
| worktrees | one (`~/Documents/Codex/2026-07-29/now/work/selfdual-5form-invariants`) |

## Branches present

`degree10/checkpointed-trace-pipeline`, `degree12/mac-exact-optimized`,
`fix/exact-canon-order-8`, `main`, `publication/jhep-degree10-final`,
`research/maximal-chiral-four-form-program`,
`stress-flow/classification-through-degree12`,
`stress-flow/exact-low-degree-map`. All eight exist on the remote at the same
commits as locally.

## Authoritative writer

One. `pgrep -f pytest` returns only this session's own grep command lines; no
science process was running against this tree.

Two stale shell processes were present:

- A wait loop from an earlier session in this repository, polling for a pytest
  run that had already finished. It is passive — it holds no lock and writes
  nothing. An attempt to terminate it was declined by the sandbox; it was left
  alone, having no effect on this work.
- A process belonging to `~/lawworld-verifiable-scientific-discovery`, an
  unrelated repository. **Deliberately left untouched.**

## A finding about the science tag

`jhep-degree10-science-final-v1` points at `b4345075`, which is the tip of
`research/maximal-chiral-four-form-program` and an **ancestor** of `aa0f98e`.
The tag therefore does not include the final publication commits on
`publication/jhep-degree10-final`.

The tagged tree does contain all four headline certificates, including
`results/degree10/B10_P10_intersection_exact.json`; an initial check that
suggested otherwise was looking in the wrong directory, and that check was
wrong, not the tag.

No action was taken. Moving a published tag rewrites history that others may
have fetched, and this goal does not authorise it. If the intent was to freeze
the publication tip, the remedy is a **new** tag at `aa0f98e` rather than a
force-move of this one. That is a human decision.

## Certificate artifacts verified present

Checked by `manuscript/jhep/scripts/build_input_manifest.py`, which records the
SHA-256 of each file it reads and fails if any named input is missing:

- `results/stress_flow/Q10_characteristic_zero.json`
- `results/stress_flow/D10_characteristic_zero.json`
- `results/stress_flow/G10_counterfactual.json`
- `results/stress_flow/G10_publication_certificate.json`
- `results/degree10/B10_P10_intersection_exact.json`
- `results/degree10/B10_P10_intersection_generator.json`
- `results/rank81/full_rank_matrix_publication_final.json`
- `results/rank81/minor81_certificate.json`

Result: 27 of 27 inputs verified, no problems.

## Environment findings

Two, both recorded because they affect reproduction rather than any result.

1. **No TeX engine was installed.** The earlier manuscript PDF was produced by
   pdfTeX from TeX Live 2026, but no TeX binary was present on this machine when
   the mentor draft was built. Tectonic 0.17.0 was installed to compile the
   draft. Because `jheppub.sty` requests `hyperref` with `pdfa=true`, which
   selects the pdfTeX driver and fails under Tectonic's XeTeX engine, the draft
   passes `xetex` to `hyperref` before the class is loaded. The official JHEP
   style file is **not** modified.

2. **`opt_einsum` is imported but was not installed.** It is an optional
   accelerator behind a guarded import with a working fallback, and it is absent
   from `requirements.txt`. The certified results were therefore produced
   *without* it, using the built-in contraction ordering. This is stated in the
   reproduction appendix and in the environment table rather than left for a
   reproducer to discover.

   The repository's `.venv` also carries a stale `pip` shebang pointing at
   `~/Downloads/sdinv/.venv`, a path that no longer exists; `python3 -m pip`
   works. This is cosmetic but will confuse a reproducer.

## Earlier manuscript drafts

`manuscript/main.tex` (982 lines, 25 pages) and the PRL tree under
`manuscript/prl/` are left untouched. The mentor draft is a new, self-contained
tree under `manuscript/jhep/` and does not modify either.
