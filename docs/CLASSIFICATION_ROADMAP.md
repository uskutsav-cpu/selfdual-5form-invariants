# Functional classification release

The requested endpoint is an explicit set of 81 generically independent
invariants with exact Jacobian witnesses. It is not a presentation of the
full invariant ring. This release reuses the already discovered graph bases
on the repository's research branches and adds new graph-only witnesses,
interchange formats, literature maps, and a reproducible formula appendix.

## Results

The **same ordered 81 graphs**, of degrees `4, 6, 6, 8×6, 10×12, 12×60`,
have cumulative ranks **1, 3, 9, 21, 81** at seeds 20260907 and 20260908
under both primes 32749 and 32719. The four explicit minor determinants are
20345, 30761, 1653, and 2167, respectively. Each is nonzero in its field.

The coordinate directions are integral `e_I + *e_I`, with `I` containing
the time index 0. The coordinates are exactly the 126 components `F_0abcd`.
No inverse projector denominator is needed. Every graph polynomial is
integral in these coordinates, so a single nonzero modular minor proves
generic characteristic-zero algebraic independence. The known quotient
dimension 81 supplies the matching upper bound. This establishes generic
local coordinates, not global separation of orbits.

| Milestone | Delivered result |
|---|---|
| M0 | Original commit `e84339d` independently retested and tagged `v0.1-low-degree-complete`; catalogs unchanged |
| M1 | Strict `{n, edges}` serialization, old labels/upper-triangle records retained; degree runner separates the two sieves |
| M2 | Rational octic map for six selected published expressions, full product correction and fresh holdouts |
| M3 | Twelve graph primitives, cumulative rank 21; the literature comparison is a qualified 12×14 map |
| M4 | Existing durable degree-10/12 searches retained; bounded optional process workers and raw-row checkpoints in the new runners |
| M5 | Existing 62 primitive degree-12 directions retained; first 60 complete the functional basis |
| M6 | Higher degrees are unnecessary for reaching rank 81; explicit candidate-stream interface remains available |
| M7 | `results/rank81_basis.json`: 81 ordered graphs, adjacency matrices, formulas, and contraction costs |
| M8 | `results/rank81_certificate.json`: full points, Jacobians, columns and nonzero determinants for four fresh cells |
| M9 | `scripts/graph_to_latex.py`, formula appendix, regression tests, Lorentz checks and standalone verifier |
| M10 | `paper/manuscript.tex`, compiled PDF, release manifest and reproducibility archive |

## Two necessary corrections to the original roadmap

**Primitive representatives can differ by products.** At degree eight, use
a seven-dimensional homogeneous atlas that includes `I4_1^2`. The artifact
`results/order8_change_of_basis.json` records the full rational map and its
6×6 block on the quotient by that product. Its literature selection is
explicit: the first five expressions from equations (4.12)–(4.15), plus
the first hatted expression (4.18), in
[Some remarks on invariants](https://arxiv.org/html/2509.14350v2#S4.SS1.SSS3).
This combines expressions from the paper's two displayed lists. No unnamed
trace subtraction or normalization change is used. Fits use five primes;
fresh samples and a sixth prime check the reconstructed map.

**The twelve degree-ten published candidates are not the graph primitive
complement under the repository's recorded source readings.** Reconstructing
the existing atlas coordinates gives dimensions 12 for their span, 2 for
the product span, and 13 for the union. The intersection has dimension one;
their primitive quotient image has dimension eleven. Therefore the requested
invertible 12×12 map cannot be supplied for those readings. The delivered
`results/order10_change_of_basis.json` gives the actual 12×14 rational map,
prime witnesses, and source-reading qualifications. It regenerates the map
from existing evidence and checks an unused reconstruction prime; it does
not claim to have rerun all expensive published tensors at new points.

Both rational maps are supported by exact modular fits and holdouts. Finite
evaluations alone do not constitute a symbolic proof of a polynomial
identity over the rationals. This limitation is separate from the rigorous
nonzero-minor argument for the explicit graph basis.

## Reproduce

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest tests -o addopts='' -q
.venv/bin/python scripts/run_6d.py
.venv/bin/python scripts/graph_to_latex.py
.venv/bin/python scripts/search_rank81.py
.venv/bin/python scripts/verify_rank81.py
.venv/bin/python scripts/validate_rank81_lorentz.py
.venv/bin/python scripts/map_literature_basis.py --degree 8
.venv/bin/python scripts/map_literature_basis.py --degree 10
```

`verify_rank81.py` checks the saved matrix, all graph representations, the
point, Euler homogeneity, and each determinant. Add `--recompute` to repeat
all 324 graph/Jacobian evaluations; the reported mode distinguishes these
operations. The generation run itself evaluated all 324 rows afresh.
Lorentz validation evaluates every fixed graph after both a spatial rotation
and a genuine boost, along with the six selected literature tensors.

`search_rank81.py` resumes after each completed row, checking the basis,
engine, prime, and point against the checkpoint identity. `--workers 2`
allows two bounded worker evaluations; one worker is the conservative
default for memory-constrained machines. The degree runner provides an
independent polynomial sieve using gradients stacked at multiple points:

```bash
.venv/bin/python scripts/run_degree.py --degree 10
.venv/bin/python scripts/run_degree.py --degree 12
.venv/bin/python scripts/run_degree.py --degree 14 --candidates candidates.jsonl
```

Each JSONL candidate may be an edge-list record or an object containing
`id` and `graph`. The preserved nauty pipelines generate exact search shards.
An incomplete search exits nonzero and reports only the evidence collected.
Hilbert factor exponents are recorded separately from polynomial dimensions
and functional rank. Above degree fourteen the supplied lower-degree
inventory is incomplete, which is explicitly reported.

`results/classification_validation.json` records this release's actual checks.
`release/classification/manifest.json` binds the portable package to hashes.
The existing publication branches and their historical attributions are
preserved; new commits use the repository owner's configured Git identity.
