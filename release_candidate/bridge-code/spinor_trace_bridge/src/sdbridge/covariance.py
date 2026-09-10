"""Exact covariance of the bridge under the GL(5) subgroup of the frame group.

The oscillator realisation carries a manifest GL(5) action: for A in GL(5, F_p),

    e_i -> A e_i,      e^i -> A^{-T} e^i

preserves the null metric (1/2)[[0,I],[I,0]], so V(A) = blockdiag(A, A^{-T}) sits
in the orthogonal group of the null frame.  On the spinor module it lifts to the
induced map on Lambda^* W, whose matrix entries are the minors of A -- integral,
so the whole check stays exact over F_p.

GL(5) is a genuinely 25-dimensional subgroup of the 45-dimensional so(10), which
makes this a real equivariance test rather than a discrete spot check.  The
Chevalley pairing carries a det(A) weight, so the bridge is equivariant up to a
character; `covariance_report` solves for that character instead of assuming it.
"""

from __future__ import annotations

import itertools

import numpy as np

from . import conventions as C
from .clifford import basis_masks
from .modular import inv, matmul


def _det_mod(M: np.ndarray, p: int) -> int:
    """Determinant over F_p by fraction-free elimination on a copy."""
    A = np.asarray(M, dtype=np.int64).copy() % p
    n = A.shape[0]
    if n == 0:
        return 1
    det = 1
    for c in range(n):
        nz = np.nonzero(A[c:, c])[0]
        if nz.size == 0:
            return 0
        r = c + int(nz[0])
        if r != c:
            A[[c, r]] = A[[r, c]]
            det = (-det) % p
        det = det * int(A[c, c]) % p
        ai = inv(int(A[c, c]), p)
        A[c] = A[c] * ai % p
        below = np.nonzero(A[c + 1:, c])[0]
        for k in below:
            rr = c + 1 + int(k)
            A[rr] = (A[rr] - A[rr, c] * A[c]) % p
    return det % p


def exterior_power_matrix(A: np.ndarray, p: int, parity: int) -> np.ndarray:
    """Lambda^{even or odd}(A) on the 16-dimensional chiral module.

    Entry [n, m] is the minor of A on rows n and columns m, which is exactly the
    coefficient of e_n in A(e_m).
    """
    masks = basis_masks(parity)
    idx = {m: k for k, m in enumerate(masks)}
    out = np.zeros((len(masks), len(masks)), dtype=np.int64)
    for m in masks:
        cols = [i for i in range(C.OSCILLATORS) if (m >> i) & 1]
        for n in masks:
            rows = [i for i in range(C.OSCILLATORS) if (n >> i) & 1]
            if len(rows) != len(cols):
                continue
            sub = A[np.ix_(rows, cols)] if rows else np.zeros((0, 0), dtype=np.int64)
            out[idx[n], idx[m]] = _det_mod(sub, p)
    return out % p


def vector_action(A: np.ndarray, p: int) -> np.ndarray:
    """V(A) = blockdiag(A, A^{-T}) on the ten null directions (contravariant)."""
    from .clifford import _inverse_mod
    n = C.OSCILLATORS
    V = np.zeros((2 * n, 2 * n), dtype=np.int64)
    V[:n, :n] = np.asarray(A, dtype=np.int64) % p
    V[n:, n:] = _inverse_mod(np.asarray(A, dtype=np.int64) % p, p).T % p
    return V


def random_gl5(rng: np.random.Generator, p: int) -> np.ndarray:
    while True:
        A = rng.integers(0, p, size=(C.OSCILLATORS, C.OSCILLATORS)).astype(np.int64)
        if _det_mod(A, p) != 0:
            return A


def covariance_report(bridge, n_group: int = 3, n_samples: int = 4, seed: int = 20260731) -> dict:
    """Check forward(V(A).F) = chi(A) * Lambda(A)^{-1} forward(F) Lambda(A)^{-T}.

    The index placement above is not taken on faith.  The spinor archive does not
    document whether its symmetric sigma^mu_{ab} carries upper or lower spinor
    indices, so the placement was FIXED by requiring exact GL(5)-equivariance and
    then verified: of the eight candidate placements only this one reproduces the
    transformed image on every component, and it does so with a single scalar.

    Returns the solved character chi(A) alongside det(A), so the caller can see
    that chi is the determinant rather than an unexplained fudge factor.
    """
    from .clifford import _inverse_mod
    p = bridge.p
    rng = np.random.default_rng(seed)
    tuples = list(itertools.combinations(range(C.SPACETIME_DIM), C.FORM_DEGREE))
    tuple_index = {t: i for i, t in enumerate(tuples)}
    entries = []
    consistent = True

    for _ in range(n_group):
        A = random_gl5(rng, p)
        detA = _det_mod(A, p)
        V = vector_action(A, p)
        Vi = _inverse_mod(V, p)
        Lam = exterior_power_matrix(A, p, parity=0)
        Lami = _inverse_mod(Lam, p)
        chis = set()
        for _ in range(n_samples):
            c = rng.integers(0, p, size=C.N_SELFDUAL_COMPONENTS)
            F = matmul(c.reshape(1, -1), bridge.selfdual_basis, p).reshape(-1)

            # transform the five-form in the null frame, then come back
            T = bridge.frame.five_form_to_null(bridge.traceside_dense(F))
            for axis in range(5):
                T = np.moveaxis(np.tensordot(
                    np.moveaxis(T, axis, -1), V, axes=([-1], [0])), -1, axis) % p
            Fp_components = bridge.frame.five_form_to_lorentzian(T)
            Ft = np.array([Fp_components[t] for t in tuples], dtype=np.int64) % p

            S_transformed = bridge.forward(Ft)
            Sm = bridge.clifford.coords_to_symmetric(bridge.forward(F))
            expect = matmul(matmul(Lami, Sm, p), Lami.T, p)
            expect_coords = bridge.clifford.symmetric_to_coords(expect)

            nz = np.nonzero(expect_coords % p)[0]
            if nz.size == 0:
                continue
            k = int(nz[0])
            chi = int(S_transformed[k] * inv(int(expect_coords[k]), p) % p)
            if not np.array_equal(S_transformed % p, (chi * expect_coords) % p):
                consistent = False
            chis.add(chi)
        entries.append({
            "det_A": int(detA),
            "chi": sorted(chis),
            "chi_is_single_valued": len(chis) == 1,
            "chi_equals_det": len(chis) == 1 and next(iter(chis)) == int(detA),
            "chi_equals_det_inverse": len(chis) == 1 and next(iter(chis)) == inv(int(detA), p),
        })
    return {"equivariant_up_to_character": consistent, "elements": entries}
