# Reproduction quickstart

Every number in the paper comes from a JSON certificate in this repository.
Nothing is typed by hand, and the build fails if an artifact is missing.

## Setup

    git clone <repository>
    cd selfdual-5form-invariants
    python -m venv .venv && .venv/bin/pip install -r requirements-lock.txt

Python 3.13, NumPy 2.5.1, pynauty 2.8.8.1. No other dependency.

## The five checks worth running first

    # 1. the orientation fix, independently verified, ~10 min
    .venv/bin/python scripts/verify_orientation_canonical_independent.py

    # 2. dim_Q D10 = 11 by a route sharing no code with production, ~3 min
    .venv/bin/python scripts/verify_D10_independent.py

    # 3. dim_Q Q10 = 3, constructed rather than inferred, ~3 min
    .venv/bin/python scripts/construct_Q10_exact.py

    # 4. the assembled rank matrix, read-only, seconds
    .venv/bin/python spinor_trace_bridge/scripts/assemble_rank81_matrix.py

    # 5. the science gate over every artifact, seconds
    .venv/bin/python scripts/emit_jhep_science_gate.py

Expected: PROVED, PROVED, MATRIX COMPLETE, VERDICT: PASS.

## Tests

    .venv/bin/python -m pytest tests/ -q                  # tensor side
    cd spinor_trace_bridge && python -m pytest -q          # bridge side

## Rebuilding the paper

    .venv/bin/python manuscript/jhep/make_jhep_assets.py
    cd manuscript/jhep && tectonic -X compile main.tex --outdir .

The asset script regenerates every figure, table and inline number from the
certificates first, so a stale value cannot survive a rebuild.

## The expensive one

Recomputing the full certificate matrix from scratch takes several hours on one
laptop: eighteen cells, one at a time, and the cold ones run 20 to 35 minutes
each.

    sh spinor_trace_bridge/scripts/run_rank81_matrix.sh <archive> <python>

Warm row caches make repeat runs seconds per cell. The archive argument is a
third-party candidate-selection list that is not redistributed; every other
result reproduces without it.

## If a number disagrees

The certificate is authoritative, not the paper. Each claim in the ledger names
the artifact it came from.
