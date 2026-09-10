"""Exact linear algebra over F_p for the bridge.

The bridge deliberately does not use floating point anywhere.  The spinor
side's construction is integral right up to its final SVD nullspace step, and
that step is the only thing standing between it and exact arithmetic.  Redoing
it over F_p removes the tolerance question entirely: over F_p, zero means zero.

p is small (~2^15) and every routine here reduces aggressively, so int64
accumulation never overflows.
"""

from __future__ import annotations

import numpy as np


def inv(a: int, p: int) -> int:
    """Modular inverse via Fermat's little theorem."""
    a = int(a) % p
    if a == 0:
        raise ZeroDivisionError("no inverse of 0 mod p")
    return pow(a, p - 2, p)


def matmul(A: np.ndarray, B: np.ndarray, p: int) -> np.ndarray:
    """Matrix product mod p, reducing the inputs first to bound the sum."""
    return (np.asarray(A, dtype=np.int64) % p @ (np.asarray(B, dtype=np.int64) % p)) % p


def rref(A: np.ndarray, p: int):
    """Reduced row echelon form over F_p.

    Returns (R, pivots).  R is a fresh array; A is not modified.
    """
    R = np.asarray(A, dtype=np.int64).copy() % p
    rows, cols = R.shape
    pivots: list[int] = []
    r = 0
    for c in range(cols):
        if r >= rows:
            break
        nz = np.nonzero(R[r:, c])[0]
        if nz.size == 0:
            continue
        i = r + int(nz[0])
        if i != r:
            R[[r, i]] = R[[i, r]]
        R[r] = (R[r] * inv(int(R[r, c]), p)) % p
        col = R[:, c].copy()
        col[r] = 0
        nzr = np.nonzero(col)[0]
        if nzr.size:
            R[nzr] = (R[nzr] - np.outer(col[nzr], R[r])) % p
        pivots.append(c)
        r += 1
    return R, pivots


def rank(A: np.ndarray, p: int) -> int:
    if A.size == 0:
        return 0
    _, piv = rref(A, p)
    return len(piv)


def nullspace(A: np.ndarray, p: int) -> np.ndarray:
    """Row-major basis of {x : A x = 0} over F_p."""
    A = np.asarray(A, dtype=np.int64) % p
    R, pivots = rref(A, p)
    cols = A.shape[1]
    free = [c for c in range(cols) if c not in pivots]
    basis = np.zeros((len(free), cols), dtype=np.int64)
    for k, f in enumerate(free):
        basis[k, f] = 1
        for r, pc in enumerate(pivots):
            basis[k, pc] = (-R[r, f]) % p
    return basis


def solve(A: np.ndarray, b: np.ndarray, p: int) -> np.ndarray | None:
    """One solution of A x = b over F_p, or None if inconsistent."""
    A = np.asarray(A, dtype=np.int64) % p
    b = np.asarray(b, dtype=np.int64).reshape(-1, 1) % p
    aug = np.concatenate([A, b], axis=1)
    R, pivots = rref(aug, p)
    if A.shape[1] in pivots:
        return None
    x = np.zeros(A.shape[1], dtype=np.int64)
    for r, pc in enumerate(pivots):
        x[pc] = R[r, -1]
    return x


def row_space_contains(basis: np.ndarray, vectors: np.ndarray, p: int) -> bool:
    """True iff every row of `vectors` lies in the row space of `basis`."""
    if vectors.size == 0:
        return True
    r0 = rank(basis, p)
    r1 = rank(np.concatenate([basis, np.atleast_2d(vectors)], axis=0), p)
    return r0 == r1


def spans_equal(A: np.ndarray, B: np.ndarray, p: int) -> bool:
    """True iff the row spaces of A and B coincide."""
    return row_space_contains(A, B, p) and row_space_contains(B, A, p)


def is_square(a: int, p: int) -> bool:
    a = int(a) % p
    if a == 0:
        return True
    return pow(a, (p - 1) // 2, p) == 1


def sqrt_mod(a: int, p: int) -> int:
    """A square root of a mod p (Tonelli-Shanks).  Raises if a is not a QR."""
    a = int(a) % p
    if a == 0:
        return 0
    if not is_square(a, p):
        raise ValueError(f"{a} is not a quadratic residue mod {p}")
    if p % 4 == 3:
        return pow(a, (p + 1) // 4, p)
    q, s = p - 1, 0
    while q % 2 == 0:
        q //= 2
        s += 1
    z = 2
    while is_square(z, p):
        z += 1
    m, c, t, r = s, pow(z, q, p), pow(a, q, p), pow(a, (q + 1) // 2, p)
    while t != 1:
        i, t2 = 0, t
        while t2 != 1:
            t2 = t2 * t2 % p
            i += 1
        b = pow(c, 1 << (m - i - 1), p)
        m, c = i, b * b % p
        t, r = t * c % p, r * b % p
    return r


def solve_two_square(a: int, b: int, c: int, p: int) -> tuple[int, int]:
    """Find (x, y) with a x^2 + b y^2 = c over F_p.

    Always solvable for a, b, c with a, b nonzero: the sets {a x^2} and
    {c - b y^2} each have (p+1)/2 elements, so they must intersect.
    """
    a, b, c = int(a) % p, int(b) % p, int(c) % p
    lhs = {}
    for x in range(p):
        lhs.setdefault(a * x * x % p, x)
    for y in range(p):
        want = (c - b * y * y) % p
        if want in lhs:
            return lhs[want], y
    raise RuntimeError("unreachable: a x^2 + b y^2 = c is always solvable over F_p")
