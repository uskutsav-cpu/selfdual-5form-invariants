"""Full SO(10) equivariance of the bridge, exact over F_p, via Clifford reflections.

The GL(5) test in `covariance.py` covers a 25-dimensional subgroup of the
45-dimensional orthogonal algebra.  This module closes the remaining 20
directions by working with reflections instead, which by Cartan-Dieudonne
generate the whole orthogonal group:

    Gamma(u) Gamma(x) Gamma(u)^{-1} = -Gamma(R_u x),
        R_u x = x - 2 (u.x)/Q(u) u

so a product of an even number of reflections gives an element of the special
orthogonal group together with its spinor lift, and both are exact over F_p as
long as every reflecting vector has nonzero norm.  Nothing here is transcendental
-- no exponentials, no Lie-algebra series -- which is why it survives modular
arithmetic intact.
"""

from __future__ import annotations

import numpy as np

from . import conventions as C
from .clifford import _inverse_mod, basis_masks, dirac_gammas, null_metric
from .modular import inv, matmul


def gamma_of_covector(u: np.ndarray, p: int) -> np.ndarray:
    """Gamma(u) = u_mu Gamma^mu on the full 32-dimensional module."""
    G = dirac_gammas()
    out = np.zeros((C.FULL_SPINOR_DIM, C.FULL_SPINOR_DIM), dtype=np.int64)
    for mu in range(C.SPACETIME_DIM):
        c = int(u[mu]) % p
        if c:
            out = (out + c * G[mu]) % p
    return out


def norm_of_covector(u: np.ndarray, p: int) -> int:
    """Q(u) = eta^{mu nu} u_mu u_nu in the null frame."""
    eta = null_metric(p)
    u = np.asarray(u, dtype=np.int64) % p
    return int(u @ eta % p @ u % p) % p


def reflection_matrix(u: np.ndarray, p: int) -> np.ndarray:
    """R with (x R)_nu = (R_u x)_nu, acting on lower-index components."""
    eta = null_metric(p)
    u = np.asarray(u, dtype=np.int64) % p
    Q = norm_of_covector(u, p)
    if Q == 0:
        raise ValueError("cannot reflect in a null vector")
    factor = (2 * inv(Q, p)) % p
    return (np.eye(C.SPACETIME_DIM, dtype=np.int64)
            - factor * np.outer((eta @ u) % p, u)) % p


def random_nonnull_covector(rng: np.random.Generator, p: int) -> np.ndarray:
    while True:
        u = rng.integers(0, p, size=C.SPACETIME_DIM).astype(np.int64)
        if norm_of_covector(u, p) != 0:
            return u


def random_rotation(rng: np.random.Generator, p: int, n_reflections: int = 2):
    """An element of the special orthogonal group with its spinor lift.

    Returns (R, rho_even, norm) where R acts on lower-index vector components,
    rho_even is the 16 x 16 restriction of the Clifford lift to Lambda^even W,
    and norm is the product of the reflecting vectors' norms.  Since
    Gamma(u)^2 = Q(u), that product is exactly the normalisation the unnormalised
    Clifford lift carries; `rotation_report` checks that the observed character is
    its inverse rather than assuming so.

    `n_reflections` must be even so that parity is preserved.
    """
    if n_reflections % 2:
        raise ValueError("need an even number of reflections to stay in Spin")
    even = basis_masks(0)
    R = np.eye(C.SPACETIME_DIM, dtype=np.int64)
    g = np.eye(C.FULL_SPINOR_DIM, dtype=np.int64)
    norm = 1
    for _ in range(n_reflections):
        u = random_nonnull_covector(rng, p)
        R = matmul(R, reflection_matrix(u, p), p)
        g = matmul(g, gamma_of_covector(u, p), p)
        norm = norm * norm_of_covector(u, p) % p
    return R, g[np.ix_(even, even)] % p, norm


def rotation_report(bridge, n_elements: int = 3, n_samples: int = 2,
                    n_reflections: int = 2, seed: int = 20260731) -> dict:
    """Check bridge equivariance under products of reflections.

    The verified law, with the placement determined the same way as in
    `covariance.py` (by scanning candidates, not by assumption), is

        forward(R . F) = (prod_i Q(u_i))^{-1} * rho^T forward(F) rho

    where rho is the unnormalised Clifford lift.  The scalar is solved for and
    then compared against the predicted normalisation.
    """
    import itertools
    p = bridge.p
    rng = np.random.default_rng(seed)
    tuples = list(itertools.combinations(range(C.SPACETIME_DIM), C.FORM_DEGREE))
    elements = []
    all_ok = True

    for _ in range(n_elements):
        R, rho, norm = random_rotation(rng, p, n_reflections)
        scalars = set()
        for _ in range(n_samples):
            c = rng.integers(0, p, size=C.N_SELFDUAL_COMPONENTS)
            F = matmul(c.reshape(1, -1), bridge.selfdual_basis, p).reshape(-1)

            T = bridge.frame.five_form_to_null(bridge.traceside_dense(F))
            for axis in range(5):
                T = np.moveaxis(np.tensordot(
                    np.moveaxis(T, axis, -1), R, axes=([-1], [0])), -1, axis) % p
            dense = bridge.frame.five_form_to_lorentzian(T)
            Ft = np.array([dense[t] for t in tuples], dtype=np.int64) % p

            S_rot = bridge.forward(Ft)
            Sm = bridge.clifford.coords_to_symmetric(bridge.forward(F))
            expect = bridge.clifford.symmetric_to_coords(
                matmul(matmul(rho.T, Sm, p), rho, p))

            nz = np.nonzero(expect % p)[0]
            if nz.size == 0:
                continue
            k = int(nz[0])
            lam = int(S_rot[k] * inv(int(expect[k]), p) % p)
            scalars.add(lam)
            if not np.array_equal(S_rot % p, (lam * expect) % p):
                all_ok = False
        predicted = inv(norm, p)
        elements.append({
            "n_reflections": n_reflections,
            "scalar": sorted(scalars),
            "scalar_single_valued": len(scalars) == 1,
            "predicted_scalar": predicted,
            "scalar_matches_clifford_normalisation":
                len(scalars) == 1 and next(iter(scalars)) == predicted,
        })
    return {
        "equivariant_on_every_component": all_ok,
        "generates": "the full special orthogonal group (Cartan-Dieudonne)",
        "elements": elements,
    }
