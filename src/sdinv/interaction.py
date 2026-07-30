"""Exact derivatives on the constrained self-dual five-form field space.

This module deliberately sits outside the immutable degree-12 validation
engine.  It reuses that engine's reverse contraction primitive without
changing any file covered by the committed atlas certificate.
"""

import itertools
from math import factorial

import numpy as np

from .contract import (
    _contraction_plan_profile,
    _network_value_gradient,
    _signed,
    _slot_plan,
)
from .forms import (
    basis_tuples,
    hodge_matrix,
    metric_signs,
    perm_sign,
    to_dense,
)
from .modp import P, inv


def value_and_dense_gradient(matrix, five_form, d, valence,
                             lorentzian=True, mod=P,
                             max_memory_bytes=None):
    """Return a graph value and its ambient lower-input dense gradient."""
    slots, tails = _slot_plan(matrix, valence)
    signs = metric_signs(d, lorentzian) % mod
    terms = ["".join(labels) for labels in slots]
    profile = _contraction_plan_profile(
        terms, [(d,) * valence for _ in terms])
    if (
        max_memory_bytes is not None
        and profile["estimated_peak_bytes"] > int(max_memory_bytes)
    ):
        raise MemoryError(
            "exact contraction plan rejected before signed operands: "
            f"estimated {profile['estimated_peak_bytes']} bytes exceeds "
            f"limit {int(max_memory_bytes)} bytes")
    operands = [
        _signed(five_form, tails[vertex], signs, mod)
        for vertex in range(matrix.shape[0])
    ]
    scalar, operand_gradients = _network_value_gradient(
        terms,
        operands,
        mod,
        plan_profile=profile,
        max_memory_bytes=max_memory_bytes,
    )
    ambient = np.zeros_like(five_form, dtype=np.int64)
    for vertex, gradient in enumerate(operand_gradients):
        ambient = (
            ambient + _signed(gradient, tails[vertex], signs, mod)
        ) % mod
    return int(scalar) % mod, ambient


def covariant_antisymmetric_gradient(ambient, d, valence,
                                     lorentzian=True, mod=P):
    """Antisymmetrize an ambient gradient and lower all of its indices."""
    tensor = np.asarray(ambient, dtype=np.int64) % mod
    expected = (int(d),) * int(valence)
    if tensor.shape != expected:
        raise ValueError(
            f"gradient must have shape {expected}, got {tensor.shape}")
    result = np.zeros_like(tensor, dtype=np.int64)
    for permutation in itertools.permutations(range(int(valence))):
        result = (
            result
            + perm_sign(permutation) * tensor.transpose(permutation)
        ) % mod
    result = result * inv(factorial(int(valence)), mod) % mod
    signs = metric_signs(d, lorentzian) % mod
    for axis in range(int(valence)):
        shape = [1] * int(valence)
        shape[axis] = int(d)
        result = result * signs.reshape(shape) % mod
    return np.asarray(result, dtype=np.int64)


def anti_selfdual_projector(d, valence, lorentzian=True, mod=P):
    """Return the exact middle-form projector ``(1-*)/2``."""
    if d != 2 * valence:
        raise ValueError("anti-self-dual projection requires d=2*valence")
    hodge = hodge_matrix(d, valence, lorentzian, mod)
    identity = np.eye(hodge.shape[0], dtype=np.int64)
    return (identity - hodge) * inv(2, mod) % mod


def invariant_value_and_derivative(matrix, five_form, d=10, valence=5,
                                   lorentzian=True, mod=P,
                                   max_memory_bytes=None):
    """Return ``(I, dI/dLambda^upper)`` on the self-dual field space.

    The paper's constrained variation makes the derivative anti-self-dual.
    Its dense covariant components are normalized so that a homogeneous
    invariant of degree ``n`` obeys
    ``Lambda_upper . derivative_lower = n*I``.
    """
    scalar, ambient = value_and_dense_gradient(
        matrix,
        five_form,
        d,
        valence,
        lorentzian,
        mod,
        max_memory_bytes,
    )
    covariant = covariant_antisymmetric_gradient(
        ambient, d, valence, lorentzian, mod)
    tuples = basis_tuples(d, valence)
    compact = np.asarray(
        [covariant[index] for index in tuples],
        dtype=np.int64,
    )
    compact = (
        anti_selfdual_projector(d, valence, lorentzian, mod) @ compact
    ) % mod
    return scalar, to_dense(compact, d, valence, mod)

