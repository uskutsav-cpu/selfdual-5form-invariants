# Reproduction quickstart

Everything needed to re-run the results in the mentor-review draft, in the order
a reviewer would want them.

## 1. Get the source

```
git clone https://github.com/uskutsav-cpu/selfdual-5form-invariants
cd selfdual-5form-invariants
git switch publication/jhep-mentor-draft
```

## 2. Environment

```
python3 -m venv .venv
.venv/bin/python3 -m pip install -r requirements.txt
```

Dependencies are NumPy, `pynauty` and `pytest`.

Two notes that will otherwise cost you time:

- `opt_einsum` is imported by the spinor code but is **optional**, is **not** in
  `requirements.txt`, and was **not installed** in the environment that produced
  the certified results. The built-in contraction ordering was used. Installing
  it should change speed and not values, but that was not certified both ways.
- If you use the repository's committed `.venv`, its `pip` shebang points at a
  path that no longer exists. Use `.venv/bin/python3 -m pip` rather than
  `.venv/bin/pip`.

## 3. Test suites

```
.venv/bin/python3 -m pytest tests -q
.venv/bin/python3 -m pytest spinor_trace_bridge/tests -q
```

Expected: **254** tensor tests and **86** bridge tests, no failures.

## 4. The exact rational certificates

```
.venv/bin/python3 scripts/d10_characteristic_zero.py
.venv/bin/python3 scripts/b10_p10_characteristic_zero.py
```

Expected:

| quantity | value |
|---|---|
| `dim_Q A10` | 14 |
| `dim_Q D10` | 11 |
| `dim_Q Q10` | 3 |
| `dim_Q(B10 ∩ P10)` | 1 |

The first script lifts 9 non-integral rows by CRT across 5 primes, validates at
held-out prime 32771, and runs the closure to a fixed point in `Fraction`
arithmetic (3 sweeps). The second lifts all 12 published structures across 7
primes, validates at held-out prime 32783, and re-verifies the generator identity
at fresh prime 32869 on 6 fresh samples.

## 5. The rank matrix

```
.venv/bin/python3 scripts/aggregate_rank_matrix.py --self-test
```

Read-only with respect to the cells and order-independent, so it is safe to run
at any time. Expected: 15 cells, rank 81 in every one, 81 stable pivot rows and
81 stable pivot columns, 0 unstable.

**Caution.** Individual cells may be run in parallel but must not share a row
cache. Two processes writing one cache is a failure this project has actually
experienced.

## 6. Rebuild the manuscript

```
.venv/bin/python3 manuscript/scripts/make_numbers.py
.venv/bin/python3 manuscript/jhep/scripts/make_figures.py
.venv/bin/python3 manuscript/jhep/scripts/make_tables.py
.venv/bin/python3 manuscript/jhep/scripts/check_draft.py
cd manuscript/jhep && tectonic -X compile main.tex
```

The macro, figure and table steps must precede the compile: the manuscript
contains no scientific value of its own, only macros that expand to values read
from artifacts.

`check_draft.py` runs 52 gates covering LaTeX health, citation coverage,
placeholder discipline, and the wording restrictions (no unscoped completeness or
canonicality claims, rank 81 scoped to the selected family, degree-eight claim
qualified, degree-twelve scope stated).

Expected: **52 gates passed, 0 failed**, and a 41-page PDF with zero overfull
boxes, zero underfull boxes, zero undefined citations and zero undefined
references.

## 7. A note on TeX

The draft compiles with **Tectonic**. Because `jheppub.sty` requests `hyperref`
with `pdfa=true` — which selects the pdfTeX driver and fails under Tectonic's
XeTeX engine — `main.tex` passes `xetex` to `hyperref` before the class is
loaded. The official JHEP style file is not modified. Compiling with pdfLaTeX
instead should also work and does not need that line.

## 8. Determinism

Figures are byte-identical across runs; matplotlib's PDF creation timestamp is
suppressed explicitly. Archives use a fixed epoch and normalised member metadata.
If you regenerate the figures and the hashes differ, that is a finding, not
noise.
