"""Implemented equation-(4.24) candidates and their Q10 projections.

Source: "Some remarks on invariants", J. Phys. A 59 (2026) 065203, eq (4.24),
journal PDF page 17. Transcribed from a rendered page image because the
red/black bracket distinction -- which fixes the order of the nested
(anti)symmetrisations -- is invisible in extracted text.

Only P10_01 and P10_02 are implemented. The other ten carry nested bracket
structures that need a dedicated symmetrisation engine and are deliberately
not guessed.
"""

import json
import os
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from sdinv.modp import P, ALT_P  # noqa: E402
from sdinv.forms import selfdual_projector, to_dense, random_form  # noqa: E402
from sdinv.published_degree10_invariants import (  # noqa: E402
    NOT_IMPLEMENTED, PUBLISHED_DEGREE10, evaluate_implemented)

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "results" / "intrinsic_candidates" / "published_degree10_map.json"


def _sample(prime, seed):
    projector = selfdual_projector(10, 5, True, prime)
    raw = random_form(10, 5, np.random.default_rng(seed), prime)
    return to_dense((projector @ raw) % prime, 10, 5, prime)


def test_only_unambiguous_candidates_are_implemented():
    assert set(PUBLISHED_DEGREE10) == {"P10_01", "P10_02"}
    assert len(NOT_IMPLEMENTED) == 10, (
        "the other ten must stay explicitly unimplemented, not guessed")


def test_homogeneity_degree_ten():
    """Guards the int64 overflow that a bare np.einsum would reintroduce."""
    for prime in (P, ALT_P):
        form = _sample(prime, 20260729)
        base = evaluate_implemented(form, prime)
        for c in (2, 3, 5):
            scaled = evaluate_implemented((form * c) % prime, prime)
            for name, v in base.items():
                assert scaled[name] == (pow(c, 10, prime) * v) % prime, (
                    f"{name} not homogeneous of degree 10 at prime {prime}; a "
                    f"bare np.einsum on int64 silently wraps here")


def test_trM5_matches_the_M_only_result():
    """P10_01 = tr M^5 must land in the closure, as the M-only test found."""
    if not MAP.exists():
        return
    with MAP.open() as stream:
        payload = json.load(stream)
    for record in payload["per_prime"].values():
        p1 = record["projections"]["P10_01"]
        assert p1["status"] == "solved"
        assert all(v == 0 for v in p1["quotient_vector"]), (
            "tr M^5 must project to zero in Q10, matching C-MONLY-01 via an "
            "independent code path")


def test_published_q10_rank_is_zero_and_consistent():
    if not MAP.exists():
        return
    with MAP.open() as stream:
        payload = json.load(stream)
    assert payload["consistent"] is True
    assert payload["Q10_rank_from_implemented_published"] == 0
    for record in payload["per_prime"].values():
        assert record["dim_Q10"] == 3
        for proj in record["projections"].values():
            assert proj["status"] == "solved", (
                "a rank of 0 from an unsolved system would be uninformative")
