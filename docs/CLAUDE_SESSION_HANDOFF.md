# Session handoff

**Current commit**: see `git log -1`. Branch
`research/maximal-chiral-four-form-program`. Nothing pushed.

## Running processes
None.

## Completed this session

| item | result |
|---|---|
| primary sources downloaded + hashed | journal `0437ffc2…` (35 pp), arXiv v2 `ec51d9e2…` (52 pp) |
| eq (4.25) transcribed + implemented | P12_01/02/03, homogeneity verified 2 primes |
| eq (4.24) transcribed from **rendered image** | twelve candidates readable |
| M-only Q10 rank | **0**, six primes, non-vacuous |
| P10_01 = tr M^5 implemented | projects to `[0,0,0]` in Q10 |
| P10_02 = (MM)MM·N^(4125) implemented | projects to `[0,0,0]` in Q10 |
| Q10 rank from implemented published candidates | **0 / 3** |

## Failed / corrected

- **int64 overflow.** P10_02 first used a bare `np.einsum`; four operands at
  ~p give products ~1.15e18 over 1e6 terms and wrap past 2^63 silently. Value
  changed 9605 -> 4674 after switching to `mod_einsum`. The homogeneity test
  caught it. This is the trap documented in the README.
- An earlier session wrongly called eq (4.24) an external blocker. It is
  public; that claim is retracted in `docs/PRIMARY_SOURCE_INGEST.md`.

## Next exact command

Implement the nested-bracket engine, then P10_03..P10_12:

    # the ten remaining candidates need correct red-after-black bracket order
    # see docs/PRIMARY_SOURCE_INGEST.md section 2 for the quoted convention

Then reproject:

    .venv/bin/python scripts/project_published_degree10.py

## Unresolved ambiguities

1. **P10_03..P10_12 bracket ordering.** The paper fixes it in words ("red upon
   black"), but implementing nested normalized (anti)symmetrisations requires
   an engine plus tests against tensors of known symmetry. Not guessed.
2. **Source arithmetic**: paper says order 12 has 64 while totalling 83;
   1+2+6+12+62 = 83 matches the repository. Logged, unresolved.
3. **PO-03**: the paper conjectures >= 2 *non-linear relations*; the repository
   established *Jacobian dependence*. Not the same statement.

## Memory / checkpoints

Peak observed this session ~800 MB. Primary PDFs live in
`/private/tmp/sd5-primary-sources/` (not committed, not in iCloud).
