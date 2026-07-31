# Session handoff

**Branch** `research/maximal-chiral-four-form-program`.
`origin/research/...` is at `5b48209`; everything after that is **local only**.

## 1. Where the degree-10 work stands

| result | value | evidence |
|---|---|---|
| twelve published candidates implemented | 12/12 | `published_degree10_invariants.py` |
| published atlas rank | **12 / 14** | both primes |
| published Q10 rank | **3 / 3** | fit 32749, holdout 32717 |
| reverse-recovered Q10 rank | **3 / 3** | independent search |
| reverse span = published span | **proven** | union rank 3, both primes |
| Level-A ↔ Level-B maps | both directions, mutually inverse | exact, modular |
| removal minimality | verified | removing any member drops rank |

### The basis, in the only permitted wording

> **Preferred ambiguity-minimal Level-B basis among the twelve published
> degree-10 candidates under the documented deterministic simplicity rule.**

    { P10_10, P10_11, P10_12 }

**Never** "ambiguity-robust", "universally canonical", or "the unique compact
basis". `tests/test_q10_wording_freeze.py` enforces this across every doc and
artifact; negated mentions stay allowed because they are the correct statement.

| candidate | status |
|---|---|
| `P10_10` | **forced** — in every independent triple; sole carrier of the third quotient coordinate |
| `P10_09` | source-reading dependent (AMB-01); excluded from the basis, **retained** as a valid implemented interpretation |
| `P10_11` | source-reading dependent (AMB-02); in the basis only because at least one such member is unavoidable |
| `P10_12` | tested alternative reading gives **identical** evaluations and quotient vectors |

**No fully ambiguity-robust published triple exists.** `P10_10` is forced and
only `P10_12` of the remainder is robust, so two robust members cannot be
found. That is PO-11 and it is a binding prerequisite for an unconditional
basis, not a tidiness item.

## 2. The reverse benchmark

> **A formula-independent bounded reverse search independently recovered the
> full three-dimensional quotient Q10.**

All three recovered directions come from the **`N4125`x5** sector — pure
`N^(4125)`, no `N^(1050)`, no `M`. Every published basis element is
`N^(1050)`-based, so the search found a **different** compact basis spanning
the same quotient rather than rediscovering the published one.

Independence is enforced by AST inspection, not promised in prose.

**Not exhaustive**: 5 of 21 sectors are capped at 30 000 raw topologies, and
even exhausted sectors were sampled at 40 candidates for evaluation. Recovery
goal met; exhaustion goal not (PO-12). Never write "complete enumeration of
every M/N contraction".

## 3. Two defects found, both the same kind

Both were invisible to homogeneity and to rotations, and both were caught by a
**boost** — `delta` and `eta` agree on the spatial block, so only a boost sees
a metric misplacement.

1. **`P10_07`** raised all six axes on both inner `N` factors, making three
   edges `delta`-contractions. Symptom: `not_in_atlas_span` on all six primes.
2. **The reverse engine's `M` block.** `make_blocks` returned `mixed`, which is
   already `M_{a}{}^{b}`, to a routine that assumes all-lower operands and
   raises one end itself. Symptom: 129 of 579 pilot candidates not in the atlas
   span. Pure-N sectors were 100% boost invariant, M sectors were not, which
   localised it in one step. **The recovery result was unaffected** — it lives
   entirely in `N4125`x5 — but the M-sector statistics were invalid and were
   regenerated.

Boost tests now guard both the published evaluators and the generated ones.

## 4. Infrastructure notes

- **Checkpoint validity** is semantic, not commit-based. Fingerprints are
  derived from source (`evaluator_fingerprint`, `block_fingerprint`), so a
  reimplemented formula invalidates exactly its own units and the expensive
  atlas cache survives. Cold two-prime run 912 s, resumed 55 s.
- **Checkpoints must never live in iCloud.** The tree is under `~/Documents`,
  which is synced. Use `SDINV_CKPT_ROOT`.
- **Reverse generation is streamed**: 2611 MB → 33 MB for the same sector.
  Evaluation still peaks ~2.9 GB holding the candidate plan; that is the next
  memory target if the sweep is widened.
- **`python -m pytest` works bare** — `pytest.ini` scopes collection past the
  `scripts/`↔`tests/` module-name collision.
- A redirected process is **block buffered**: an empty log does not mean an
  idle job. Check `ps -p <pid> -o time` for CPU, and the artifact's mtime. A
  run killed after writing its artifact loses only the buffered log; that
  happened here and briefly looked like lost work.

## 5. Next

1. Collect the pilot rerun (valid M-sector statistics) and refresh the
   benchmark artifact.
2. Clean-clone QUICK reproduction.
3. **Do not launch the degree-12 search.** It is prepared and refuses to run
   without `--i-mean-it`; see `DEGREE12_REVERSE_PILOT_PLAN.md`. Run
   `--measure-only` first — the degree-10 cost per contraction does not
   transfer.
4. Resolve PO-11 (bracket colour) if an unconditional basis is wanted.
