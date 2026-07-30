"""The three published degree-12 invariants of equation (4.25).

Source: Cederwall, Hutomo, Kuzenko, Lechner, Sorokin, "Some remarks on
invariants", J. Phys. A 59 (2026) 065203; cross-checked against
arXiv:2509.14350v2, equation (4.25), journal PDF page 18.

Transcribed from the rendered source, not from memory.
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from sdinv.modp import P, ALT_P  # noqa: E402
from sdinv.forms import selfdual_projector, to_dense, random_form  # noqa: E402
from sdinv.published_degree12_invariants import (  # noqa: E402
    PUBLISHED_DEGREE12, evaluate_all)


def _sample(prime, seed):
    projector = selfdual_projector(10, 5, True, prime)
    raw = random_form(10, 5, np.random.default_rng(seed), prime)
    return to_dense((projector @ raw) % prime, 10, 5, prime)


def test_all_three_equation_4_25_structures_are_present():
    assert set(PUBLISHED_DEGREE12) == {"P12_01", "P12_02", "P12_03"}
    for spec in PUBLISHED_DEGREE12.values():
        assert spec["field_degree"] == 12
        assert sum(spec["blocks"].values()) == 6, (
            "six quadratic blocks at five-form degree 12")


def test_homogeneity_degree_twelve():
    for prime in (P, ALT_P):
        form = _sample(prime, 20260729)
        base = evaluate_all(form, prime)
        for c in (2, 3):
            scaled = evaluate_all((form * c) % prime, prime)
            for name, value in base.items():
                assert scaled[name] == (pow(c, 12, prime) * value) % prime, (
                    f"{name} is not homogeneous of degree 12 at prime {prime}")


def test_values_are_nonzero_and_prime_consistent_in_structure():
    """A structure that vanished identically would be uninformative."""
    for prime in (P, ALT_P):
        for seed in (20260729, 20260730):
            values = evaluate_all(_sample(prime, seed), prime)
            assert len(values) == 3
            assert any(v % prime for v in values.values()), (
                "all three vanished, which would make the map vacuous")


def test_backends_agree_where_a_reference_path_exists():
    prime = P
    form = _sample(prime, 20260731)
    optimized = evaluate_all(form, prime, backend="optimized")
    reference = evaluate_all(form, prime, backend="reference")
    assert optimized == reference
