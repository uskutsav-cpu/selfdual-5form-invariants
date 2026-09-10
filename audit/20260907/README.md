# Independent audit evidence

The repository root `INDEPENDENT_AUDIT.md` is the controlling report. The
original failure report is preserved byte-for-byte in `phase01/`; phase02
is the separately authorized continuation and repair, starting again from
fresh clones of commit `2b7663bbf5a06d1340973434f195a84ae2773e8f`.

`COMMAND_INDEX.json` records every logged command, exit, duration, and raw
stdout/stderr hash. Failed attempts and interrupted tests are retained. Exact
original working directories are evidence, not portable installation paths.
`EVIDENCE_MANIFEST.json` binds the copied authored evidence. Full primary
papers, their source TeX, and retrieved web responses remain outside the Git
publication; source URLs, download hashes, authored transcription and search
records identify the consulted material.

The numerical certificates and exact source programs are under:

- `results/audit/root-review/`: fresh cells, production recomputation, new
  rotations/boosts, independently implemented infinitesimal orbit action.
- `results/audit/math-review/`: independent Hodge/sign/derivative programs,
  integer Bareiss determinants, degree-12 stacked-gradient certificate.
- `results/audit/source-review/`: independent source transcription/evaluator,
  all fresh dense and binary evaluations, exact CRT certificate and maps.
- `results/audit/frozen-literature/`: preserved frozen maps, explicitly
  superseded for the canonical corrected source interpretation.

Quick portable validation is `python scripts/verify_independent_audit.py`.
It checks saved mathematical certificates; it does not re-evaluate tensors.
`python scripts/verify_rank81.py --recompute` re-evaluates all four frozen
graph/Jacobian cells with production code. The independent programs are
retained exactly as used, with their method/provenance reports, rather than
silently rewritten after the measurements.

For a full independent rerun, use a new workspace with sibling directories
`frozen-checkout`, `repair-checkout`, `environment`, `root-review`,
`math-review`, and `source-review`, as recorded in the command index. Clone
and detach `frozen-checkout` at the frozen commit. Copy authored script
sources from `results/audit/` into the corresponding review directories and
create a new Python environment from `requirements-lock.txt`. The source
review requires the corrected evaluator in `repair-checkout`; its direct
oracle itself imports no production tensor module. Original command records
identify the few absolute script arguments that must be relocated. Never
reuse old numerical caches for a claimed independent rerun. The quick
portable checker accepts the committed locations directly.

The published Hilbert dimensions are external mathematical inputs for the
source-map identity and homogeneous-space completeness conclusions. The
rank-81 lower bound and independent rank-45 orbit certificate do not depend
on these Hilbert counts. Shared NumPy/BLAS primitives, and the shared custom
forward kernel within the independent derivative programs, are disclosed in
the mathematical method report.
