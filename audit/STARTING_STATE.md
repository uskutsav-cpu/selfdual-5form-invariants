# Starting state, verified from the repositories

Verified on 2026-07-31 by direct inspection, not from the task description.
Two items in the description did not survive verification and are recorded here
because a silent discrepancy is worse than a corrected one.

## Tensor repository

| item | claimed | verified |
|---|---|---|
| frozen scientific commit | `5c6a883` | present in history |
| tag `q10-freeze-v1` | resolves to `5c6a883` | confirmed |
| dimension-dictionary commit | `e1530f5` | present |
| product-decomposition commit | — | `76dabaf` present |
| working tree | clean | clean |
| test suite | 198 passing | **199 passing** (the product regression test added at `76dabaf` brought it to 199) |

## Spinor repository — DISCREPANCY

The description states a frozen spinor commit `b70bf33`. **That commit does not
exist anywhere on this machine.** Every git repository under the user's home
directory was searched with `git cat-file -t b70bf33`; none contains it. Only the
raw mentor archive survives, as a plain directory with no `.git`.

Action taken: the archive was copied to a work directory, committed verbatim as a
fresh repository, and the baseline reproduction was re-run from scratch. The new
import commit is `2a53370`. **No result in this work is attributed to `b70bf33`**,
and the earlier hash is not reported as if it still existed.

Re-verified after the rebuild:

- `check-spinors` reproduces: gamma-trace constraints satisfied at `6.66e-16`.
- Archive test suite: 2 passed.
- 132 files in the archive after excluding `.pytest_cache` and `.DS_Store`.

## Environment

The default `python3` on this machine has no NumPy, and conda is not usable from
tooling. A dedicated virtual environment was built with the locked versions
(`numpy==2.5.1`, `pytest==9.1.1`, `pynauty==2.8.8.1`) plus `opt_einsum`,
`networkx`, `joblib`, `python-igraph` and `matplotlib`.

No LaTeX toolchain was present. TinyTeX was installed to the user's home
directory (no administrator rights required) and the official JHEP class and
bibliography style were downloaded from the publisher.

## Third-party code

The spinor archive contains logs with Windows paths under another person's home
directory. It is third-party code and redistribution permission has not been
granted. It is therefore **excluded** from the public repository and from the
release candidate; only a manifest with per-file hashes and adapter instructions
is included.
