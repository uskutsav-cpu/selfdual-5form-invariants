# Exact graph classification package

Create a Python environment, install requirements.txt, then run:

    python -m pytest tests -o addopts='' -q
    python scripts/verify_rank81.py
    python scripts/verify_rank81.py --recompute
    python scripts/verify_independent_audit.py
    python scripts/map_literature_basis.py --degree 8
    python scripts/map_literature_basis.py --degree 10
    python scripts/validate_rank81_lorentz.py

The first verification command checks saved matrices; --recompute repeats
every graph evaluation. All 81 functions and all 126 coordinates are explicit.
See docs/CLASSIFICATION_ROADMAP.md for proof boundaries and literature maps.
manifest.json records SHA-256 hashes of every payload file.
The independent checker verifies saved minors, exact CRT evaluations and
rational maps without recomputing the tensor contractions. Source polynomial
identities rely on the explicitly cited Hilbert upper bounds. The frozen
literature transcription failed and was repaired; its historical matrices
remain under results/audit/frozen-literature/.

This portable delivery suite is distinct from the full historical tensor
suite in the repository. No external spinor archive is required.
