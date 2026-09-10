"""Integral (characteristic-zero) structures, so modular ranks become rigorous bounds.

Why this module exists.  A rank computed over `F_p` is only a *probabilistic*
statement about the rank over `Q` when the matrix is assembled from
mod-`p` data.  But if the matrix is the reduction of a genuine INTEGER matrix,
the inequality

    rank_{F_p}(J mod p)  <=  rank_{Q}(J)

is exact and unconditional -- reduction can only drop rank, never raise it.  So
an exact modular rank of 81 becomes a rigorous LOWER bound of 81 on the
characteristic-zero rank, with no probabilistic caveat at all.

To use that, the point and the basis have to be integral.  The gamma-trace
constraint matrix is already integral; this module computes an integral basis of
its kernel over `Z`, so every downstream Jacobian is the reduction of an integer
matrix.

The complementary UPPER bound, `rank <= 126 - dim so(10) = 81`, is the analytic
literature result and is not derived here.
"""

from __future__ import annotations

from fractions import Fraction
from math import gcd

import numpy as np

from . import conventions as C


def rational_rref(A: np.ndarray) -> tuple[list[list[Fraction]], list[int]]:
    """Exact RREF over Q using Fractions.  A is small (10 x 136 here)."""
    rows = [[Fraction(int(x)) for x in row] for row in np.asarray(A, dtype=object)]
    n_rows, n_cols = len(rows), len(rows[0])
    pivots: list[int] = []
    r = 0
    for c in range(n_cols):
        if r >= n_rows:
            break
        piv = next((i for i in range(r, n_rows) if rows[i][c] != 0), None)
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        inv = Fraction(1) / rows[r][c]
        rows[r] = [x * inv for x in rows[r]]
        for i in range(n_rows):
            if i != r and rows[i][c] != 0:
                f = rows[i][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        pivots.append(c)
        r += 1
    return rows, pivots


def _primitive(vec: list[Fraction]) -> list[int]:
    """Clear denominators and divide out the content, giving a primitive integer vector."""
    den = 1
    for x in vec:
        den = den * x.denominator // gcd(den, x.denominator)
    ints = [int(x * den) for x in vec]
    g = 0
    for v in ints:
        g = gcd(g, abs(v))
    if g > 1:
        ints = [v // g for v in ints]
    return ints


def integral_nullspace(A: np.ndarray) -> np.ndarray:
    """A primitive integral basis of ker(A) over Z, as rows.

    Not a Hermite/Smith normal form -- it is the RREF free-variable basis with
    denominators cleared, which is all that is needed: every row is an integer
    vector genuinely annihilated by A over Z.
    """
    rows, pivots = rational_rref(A)
    n_cols = A.shape[1]
    free = [c for c in range(n_cols) if c not in pivots]
    basis: list[list[int]] = []
    for f in free:
        vec = [Fraction(0)] * n_cols
        vec[f] = Fraction(1)
        for r, pc in enumerate(pivots):
            vec[pc] = -rows[r][f]
        basis.append(_primitive(vec))
    return np.array(basis, dtype=object)


def integral_gamma_traceless_basis() -> np.ndarray:
    """126 x 136 integral basis of the gamma-traceless symmetric spinors.

    The constraint matrix is built from the integral sigma matrices, so no prime
    enters.  `verify_integral_basis` checks A B^T = 0 exactly over Z.
    """
    from .clifford import NullFrameClifford, symmetric_pairs
    # rebuild the constraint matrix integrally: no modular reduction anywhere
    cl = NullFrameClifford(p=C.DEFAULT_PRIME)
    sigma_bar_int = _integral_sigma_bar()
    pairs = symmetric_pairs()
    A = np.zeros((C.SPACETIME_DIM, len(pairs)), dtype=object)
    for mu in range(C.SPACETIME_DIM):
        M = sigma_bar_int[mu]
        for k, (i, j) in enumerate(pairs):
            A[mu, k] = M[i, j] if i == j else 2 * M[i, j]
    del cl
    B = integral_nullspace(A)
    if B.shape[0] != C.N_GAMMA_TRACELESS:
        raise RuntimeError(f"integral kernel has dimension {B.shape[0]}, expected 126")
    return B


def _integral_sigma_bar() -> np.ndarray:
    """sigmabar^mu over Q, cleared to integers.

    sigma_bar = h_mu B^{-1}; B is an integral involution-like matrix, so the
    inverse is rational.  We clear the common denominator once, which rescales
    every sigmabar by the same constant and therefore does not change the kernel.
    """
    from .clifford import basis_masks, chevalley_pairing, dirac_gammas
    even, odd = basis_masks(0), basis_masks(1)
    Bp = chevalley_pairing().astype(object)
    G = dirac_gammas()
    h = [M[np.ix_(even, odd)].astype(object) for M in G]

    rows, pivots = rational_rref(
        np.concatenate([Bp, np.eye(len(even), dtype=object)], axis=1))
    if pivots != list(range(len(even))):
        raise RuntimeError("Chevalley pairing is not invertible over Q")
    Binv = np.array([[rows[i][len(even) + j] for j in range(len(even))]
                     for i in range(len(even))], dtype=object)

    out = []
    for hm in h:
        M = np.array([[sum(Fraction(int(hm[i, k])) * Binv[k, j]
                           for k in range(len(odd)))
                       for j in range(len(even))] for i in range(len(even))],
                     dtype=object)
        den = 1
        for x in M.ravel():
            den = den * x.denominator // gcd(den, x.denominator)
        out.append(np.array([[int(x * den) for x in row] for row in M], dtype=object))
    return np.array(out, dtype=object)


def verify_integral_basis(B: np.ndarray | None = None) -> dict:
    """Check the integral kernel really is a kernel, over Z, with no reduction."""
    from .clifford import symmetric_pairs
    if B is None:
        B = integral_gamma_traceless_basis()
    sigma_bar_int = _integral_sigma_bar()
    pairs = symmetric_pairs()
    A = np.zeros((C.SPACETIME_DIM, len(pairs)), dtype=object)
    for mu in range(C.SPACETIME_DIM):
        M = sigma_bar_int[mu]
        for k, (i, j) in enumerate(pairs):
            A[mu, k] = M[i, j] if i == j else 2 * M[i, j]
    product = A @ B.T
    return {
        "dimension": int(B.shape[0]),
        "annihilated_over_Z": bool(np.all(product == 0)),
        "entries_are_integers": bool(all(isinstance(x, (int, np.integer))
                                         for x in B.ravel()[:500])),
        "max_abs_entry": int(max(abs(int(x)) for x in B.ravel())),
    }


def integral_basis_mod(p: int, B: np.ndarray | None = None) -> np.ndarray:
    """Reduce the integral basis mod p.  Downstream Jacobians are then reductions
    of genuine integer matrices, which is what makes the rank bound rigorous."""
    if B is None:
        B = integral_gamma_traceless_basis()
    return np.array([[int(x) % p for x in row] for row in B], dtype=np.int64)
