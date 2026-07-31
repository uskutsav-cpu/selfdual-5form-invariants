"""The frame transition between the trace side and the spinor side.

The trace implementation works in an orthonormal frame with metric
diag(-1,+1,...,+1).  The spinor implementation works in a null (oscillator)
frame whose metric is (1/2)[[0,I],[I,0]].  Over R these are DIFFERENT real
forms -- signature (1,9) against signature (5,5) -- and no real matrix relates
them.  Over F_p and over C they are congruent, because a nondegenerate
quadratic form in a fixed dimension is classified by its discriminant alone,
and both discriminants sit in the same square class:

    det diag(-1,+1,...,+1) = -1
    det (1/2)[[0,I],[I,0]] = -2^{-10} = -1 * (2^{-5})^2

This module does not assume that.  It constructs the transition matrix by an
explicit congruence algorithm and `TransitionFrame.verify()` checks
L^T eta_null L == eta_lorentzian exactly.

Direction convention, fixed once:

    v_null^mu = L^mu_nu v_lorentzian^nu           (contravariant vectors)
    F_null_{nu...} = F_lorentzian_{mu...} (L^{-1})^mu_nu   (five-form components)
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property

import numpy as np

from . import conventions as C
from .clifford import null_metric_inverse
from .modular import inv, is_square, matmul, solve_two_square, sqrt_mod


def lorentzian_metric(p: int) -> np.ndarray:
    """eta_{mu nu} = diag(-1, +1, ..., +1) over F_p."""
    return np.diag(np.array(C.LORENTZIAN_SIGNS, dtype=np.int64)) % p


def diagonalise(A: np.ndarray, p: int) -> tuple[np.ndarray, np.ndarray]:
    """Congruence-diagonalise a symmetric A: return (M, d) with M^T A M = diag(d).

    Handles a totally isotropic diagonal (which is exactly the case for the
    null-frame metric, whose diagonal is entirely zero).
    """
    n = A.shape[0]
    A = np.asarray(A, dtype=np.int64) % p
    M = np.eye(n, dtype=np.int64)
    d = np.zeros(n, dtype=np.int64)
    for k in range(n):
        # find a vector with nonzero norm among the remaining directions
        if A[k, k] % p == 0:
            j = next((t for t in range(k + 1, n) if A[t, t] % p), None)
            if j is not None:
                A[[k, j]] = A[[j, k]]
                A[:, [k, j]] = A[:, [j, k]]
                M[:, [k, j]] = M[:, [j, k]]
            else:
                j = next((t for t in range(k + 1, n) if A[k, t] % p), None)
                if j is None:
                    raise ValueError("degenerate quadratic form")
                # e_k <- e_k + e_j makes the diagonal entry 2*A[k,j] != 0
                A[k] = (A[k] + A[j]) % p
                A[:, k] = (A[:, k] + A[:, j]) % p
                M[:, k] = (M[:, k] + M[:, j]) % p
        akk = int(A[k, k]) % p
        d[k] = akk
        ai = inv(akk, p)
        for t in range(k + 1, n):
            c = int(A[k, t]) % p
            if c:
                f = (-c * ai) % p
                A[t] = (A[t] + f * A[k]) % p
                A[:, t] = (A[:, t] + f * A[:, k]) % p
                M[:, t] = (M[:, t] + f * M[:, k]) % p
    return M % p, d % p


def _pair_to_one(a: int, b: int, p: int) -> np.ndarray:
    """2x2 T with T^T diag(a,b) T = diag(1, a*b)."""
    x, y = solve_two_square(a, b, 1, p)
    return np.array([[x, (-b * y) % p], [y, (a * x) % p]], dtype=np.int64) % p


def canonicalise(d: np.ndarray, p: int) -> tuple[np.ndarray, int]:
    """Return (T, disc) with T^T diag(d) T = diag(1,...,1,disc).

    Uses diag(a,b) ~ diag(1, ab) repeatedly, left to right.
    """
    n = len(d)
    d = np.asarray(d, dtype=np.int64) % p
    T = np.eye(n, dtype=np.int64)
    cur = d.copy()
    for k in range(n - 1):
        a, b = int(cur[k]), int(cur[k + 1])
        t2 = _pair_to_one(a, b, p)
        block = np.eye(n, dtype=np.int64)
        block[k:k + 2, k:k + 2] = t2
        T = matmul(T, block, p)
        cur[k], cur[k + 1] = 1, (a * b) % p
    return T, int(cur[-1]) % p


def congruence(A: np.ndarray, B: np.ndarray, p: int) -> np.ndarray:
    """L with L^T A L = B, for nondegenerate symmetric A, B of equal discriminant."""
    MA, dA = diagonalise(A, p)
    MB, dB = diagonalise(B, p)
    TA, discA = canonicalise(dA, p)
    TB, discB = canonicalise(dB, p)
    ratio = (discB * inv(discA, p)) % p
    if not is_square(ratio, p):
        raise ValueError(
            "forms are not congruent over F_p: discriminants lie in different "
            f"square classes (ratio {ratio} is a non-residue mod {p})")
    s = sqrt_mod(ratio, p)
    # A --MA--> diag(dA) --TA--> diag(1..1,discA) --scale--> diag(1..1,discB)
    n = A.shape[0]
    S = np.eye(n, dtype=np.int64)
    S[n - 1, n - 1] = s
    left = matmul(matmul(MA, TA, p), S, p)          # left^T A left = diag(1..1,discB)
    right = matmul(MB, TB, p)                       # right^T B right = diag(1..1,discB)
    from .clifford import _inverse_mod
    return matmul(left, _inverse_mod(right, p), p)


@dataclass(frozen=True)
class TransitionFrame:
    """Exact change of frame between the Lorentzian and null presentations."""

    p: int = C.DEFAULT_PRIME

    @cached_property
    def L(self) -> np.ndarray:
        """L with L^T eta_null L = eta_lorentzian; maps Lorentzian -> null."""
        return congruence(null_metric_inverse(self.p), lorentzian_metric(self.p), self.p)

    @cached_property
    def L_inverse(self) -> np.ndarray:
        from .clifford import _inverse_mod
        return _inverse_mod(self.L, self.p)

    def verify(self) -> dict:
        p = self.p
        eN, eL = null_metric_inverse(p), lorentzian_metric(p)
        lhs = matmul(matmul(self.L.T, eN, p), self.L, p)
        return {
            "congruence_exact": bool(np.array_equal(lhs, eL)),
            "L_invertible": bool(np.array_equal(
                matmul(self.L, self.L_inverse, p),
                np.eye(C.SPACETIME_DIM, dtype=np.int64))),
            "prime": p,
        }

    def five_form_to_null(self, F_dense: np.ndarray) -> np.ndarray:
        """Push a dense Lorentzian-frame five-form into null-frame components."""
        p = self.p
        Li = self.L_inverse
        T = np.asarray(F_dense, dtype=np.int64) % p
        for axis in range(5):
            T = np.moveaxis(np.tensordot(np.moveaxis(T, axis, -1), Li, axes=([-1], [0])), -1, axis) % p
        return T

    def five_form_to_lorentzian(self, F_dense_null: np.ndarray) -> np.ndarray:
        """Inverse of `five_form_to_null`."""
        p = self.p
        Lm = self.L
        T = np.asarray(F_dense_null, dtype=np.int64) % p
        for axis in range(5):
            T = np.moveaxis(np.tensordot(np.moveaxis(T, axis, -1), Lm, axes=([-1], [0])), -1, axis) % p
        return T


def real_form_obstruction() -> str:
    """Why no REAL matrix does what `TransitionFrame.L` does over F_p.

    Kept as a function so the manuscript and the tests quote the same sentence.
    """
    return (
        "Over R the null frame carries signature (5,5) and the trace frame carries "
        "signature (1,9). Sylvester's law makes these inequivalent, so the transition "
        "matrix is necessarily complex (it multiplies four directions by i). Over C, "
        "and over F_p where signature is not defined and only the discriminant "
        "survives, the two are congruent and the transition is exact."
    )
