"""Exact Clifford algebra of so(10) in the oscillator (null) frame.

This mirrors the spinor implementation's construction -- Lambda^* of a
five-dimensional space, with the ten vector gammas realised as five wedge and
five contraction operators -- but carries it out over F_p instead of float64.

The point of redoing it rather than importing it: the spinor implementation
takes one float SVD (to get the 126-dimensional gamma-traceless nullspace), and
that SVD is the sole reason a rank tolerance ever has to be chosen.  Everything
before it is integral.  Over F_p the nullspace step is exact, so the bridge has
no tolerance anywhere.

We do NOT rewrite the spinor side's invariant formulas; `crosscheck.py` verifies
this module against `sd5_invariants.gamma10` numerically where the archive is
available.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass
from functools import cached_property

import numpy as np

from . import conventions as C
from .modular import inv, matmul, nullspace, rank


# --- exterior algebra of W = F_p^5 ------------------------------------------

def _bits(x: int) -> int:
    return int(x).bit_count()


def basis_masks(parity: int) -> list[int]:
    """Subsets of {0..4} of the given parity, in increasing mask order."""
    return [m for m in range(1 << C.OSCILLATORS) if _bits(m) % 2 == parity]


def _wedge_sign(mask: int, i: int) -> int:
    """Sign of e_i ^ e_mask in the ascending-subset convention."""
    below = sum(1 for j in range(i) if (mask >> j) & 1)
    return -1 if below % 2 else 1


def _top_wedge_sign(mask_a: int, mask_b: int) -> int:
    """Coefficient of e_A ^ e_B in e_0 ^ ... ^ e_4."""
    if mask_a & mask_b:
        return 0
    inv_count = 0
    for a in range(C.OSCILLATORS):
        if (mask_a >> a) & 1:
            for b in range(C.OSCILLATORS):
                if ((mask_b >> b) & 1) and b < a:
                    inv_count += 1
    return -1 if inv_count % 2 else 1


def wedge_operator(i: int) -> np.ndarray:
    """e_i ^ (-) on the full 32-dimensional Lambda^* W."""
    dim = 1 << C.OSCILLATORS
    M = np.zeros((dim, dim), dtype=np.int64)
    for mask in range(dim):
        if (mask >> i) & 1:
            continue
        M[mask | (1 << i), mask] = _wedge_sign(mask, i)
    return M


def contraction_operator(i: int) -> np.ndarray:
    """iota_{e^i} on the full 32-dimensional Lambda^* W."""
    dim = 1 << C.OSCILLATORS
    M = np.zeros((dim, dim), dtype=np.int64)
    for mask in range(dim):
        if not ((mask >> i) & 1):
            continue
        M[mask & ~(1 << i), mask] = _wedge_sign(mask, i)
    return M


def dirac_gammas() -> list[np.ndarray]:
    """The ten Gamma^mu on the 32-dimensional Dirac module, integral.

    Ordering: index mu = 0..4 are the wedges, mu = 5..9 the contractions.  This
    is the null frame; the metric it induces is `null_metric_rational()`.
    """
    return [wedge_operator(i) for i in range(C.OSCILLATORS)] + [
        contraction_operator(i) for i in range(C.OSCILLATORS)
    ]


def null_metric_rational() -> tuple[np.ndarray, int]:
    """eta^{mu nu} in the null frame as (integer numerator, common denominator).

    Returns (N, den) with eta = N / den.  From {e_i^, iota_j} = delta_ij and
    {Gamma^mu, Gamma^nu} = 2 eta^{mu nu} we get eta = (1/2) [[0, I], [I, 0]].
    """
    n = C.SPACETIME_DIM
    N = np.zeros((n, n), dtype=np.int64)
    for i in range(C.OSCILLATORS):
        N[i, C.OSCILLATORS + i] = 1
        N[C.OSCILLATORS + i, i] = 1
    return N, C.CLIFFORD_NORMALISATION * C.NULL_METRIC_SCALE_DENOMINATOR // 2


def null_metric(p: int) -> np.ndarray:
    """eta^{mu nu} in the null frame, over F_p."""
    N, den = null_metric_rational()
    return (N * inv(den, p)) % p


def null_metric_inverse(p: int) -> np.ndarray:
    """eta_{mu nu}: the inverse of `null_metric`, which is 2 [[0,I],[I,0]]."""
    N, den = null_metric_rational()
    return (N * den) % p


def chevalley_pairing() -> np.ndarray:
    """B : Lambda^even x Lambda^odd -> F_p, integral, 16 x 16.

    Carries the reversal sign (-1)^{p(p-1)/2}; that is what makes the resulting
    sigma^mu symmetric, which `verify()` checks rather than assumes.
    """
    even, odd = basis_masks(0), basis_masks(1)
    ei = {m: i for i, m in enumerate(even)}
    oi = {m: i for i, m in enumerate(odd)}
    top = (1 << C.OSCILLATORS) - 1
    B = np.zeros((len(even), len(odd)), dtype=np.int64)
    for m in even:
        k = _bits(m)
        reversal = -1 if ((k * (k - 1) // 2) % 2) else 1
        for o in odd:
            if (m | o) == top and not (m & o):
                B[ei[m], oi[o]] = reversal * _top_wedge_sign(m, o)
    return B


def _inverse_mod(M: np.ndarray, p: int) -> np.ndarray:
    n = M.shape[0]
    aug = np.concatenate([np.asarray(M, dtype=np.int64) % p, np.eye(n, dtype=np.int64)], axis=1)
    from .modular import rref
    R, piv = rref(aug, p)
    if piv != list(range(n)):
        raise ValueError("matrix is not invertible mod p")
    return R[:, n:] % p


def symmetric_pairs(dim: int = C.SPINOR_DIM) -> list[tuple[int, int]]:
    """Upper-triangular coordinates for a symmetric dim x dim matrix."""
    return [(i, j) for i in range(dim) for j in range(i, dim)]


@dataclass(frozen=True)
class NullFrameClifford:
    """The so(10) Clifford data in the null frame, exact over F_p."""

    p: int = C.DEFAULT_PRIME

    # -- chiral sigma matrices ------------------------------------------------

    @cached_property
    def _blocks(self):
        even, odd = basis_masks(0), basis_masks(1)
        G = dirac_gammas()
        # g_mu : even -> odd   (rows odd, cols even)
        # h_mu : odd  -> even  (rows even, cols odd)
        g = [M[np.ix_(odd, even)] for M in G]
        h = [M[np.ix_(even, odd)] for M in G]
        return g, h

    @cached_property
    def sigma(self) -> np.ndarray:
        """sigma^mu_{ab}: ten symmetric 16 x 16 matrices, integral."""
        g, _ = self._blocks
        B = chevalley_pairing()
        return np.stack([(B @ gm) % self.p for gm in g], axis=0)

    @cached_property
    def sigma_bar(self) -> np.ndarray:
        """sigmabar^{mu, ab} with sigma^mu sigmabar^nu + (mu<->nu) = 2 eta^{mu nu}."""
        _, h = self._blocks
        Binv = _inverse_mod(chevalley_pairing(), self.p)
        return np.stack([matmul(hm, Binv, self.p) for hm in h], axis=0)

    # -- verification ---------------------------------------------------------

    def verify(self) -> dict:
        """Check every structural property this module claims.  Cheap; run it."""
        p = self.p
        out: dict = {}
        s, sb = self.sigma, self.sigma_bar
        out["sigma_symmetric"] = all(
            np.array_equal(s[m], s[m].T % p) for m in range(C.SPACETIME_DIM))
        out["sigma_bar_symmetric"] = all(
            np.array_equal(sb[m], sb[m].T % p) for m in range(C.SPACETIME_DIM))
        eta = null_metric(p)
        I16 = np.eye(C.SPINOR_DIM, dtype=np.int64)
        ok = True
        for m in range(C.SPACETIME_DIM):
            for n in range(C.SPACETIME_DIM):
                lhs = (matmul(s[m], sb[n], p) + matmul(s[n], sb[m], p)) % p
                rhs = (C.CLIFFORD_NORMALISATION * eta[m, n] * I16) % p
                if not np.array_equal(lhs, rhs):
                    ok = False
        out["clifford_relation"] = ok
        out["gamma_trace_rank"] = rank(self.gamma_trace_constraints, p)
        out["gamma_traceless_dim"] = self.gamma_traceless_basis.shape[0]
        return out

    # -- the gamma-traceless 126 ---------------------------------------------

    @cached_property
    def gamma_trace_constraints(self) -> np.ndarray:
        """The 10 x 136 constraint matrix sum_ab sigmabar^{mu,ab} S_ab = 0.

        S is symmetric, stored in the 136 upper-triangular coordinates, so an
        off-diagonal coordinate contributes twice.
        """
        pairs = symmetric_pairs()
        A = np.zeros((C.SPACETIME_DIM, len(pairs)), dtype=np.int64)
        for mu in range(C.SPACETIME_DIM):
            M = self.sigma_bar[mu]
            for k, (i, j) in enumerate(pairs):
                A[mu, k] = M[i, j] if i == j else (2 * M[i, j])
        return A % self.p

    @cached_property
    def gamma_traceless_basis(self) -> np.ndarray:
        """126 x 136 exact basis of the gamma-traceless symmetric spinors."""
        ns = nullspace(self.gamma_trace_constraints, self.p)
        if ns.shape[0] != C.N_GAMMA_TRACELESS:
            raise RuntimeError(
                f"expected {C.N_GAMMA_TRACELESS}-dimensional gamma-traceless space, "
                f"got {ns.shape[0]} mod {self.p}")
        return ns

    def symmetric_to_coords(self, S: np.ndarray) -> np.ndarray:
        """Flatten a symmetric 16 x 16 into the 136 upper-triangular coordinates."""
        pairs = symmetric_pairs()
        return np.array([S[i, j] for (i, j) in pairs], dtype=np.int64) % self.p

    def coords_to_symmetric(self, v: np.ndarray) -> np.ndarray:
        S = np.zeros((C.SPINOR_DIM, C.SPINOR_DIM), dtype=np.int64)
        for val, (i, j) in zip(np.asarray(v, dtype=np.int64), symmetric_pairs()):
            S[i, j] = val % self.p
            S[j, i] = val % self.p
        return S

    # -- antisymmetrised five-gamma ------------------------------------------

    @cached_property
    def gamma5(self) -> dict[tuple[int, ...], np.ndarray]:
        """(Gamma^{mu1...mu5})_{ab} for each sorted index tuple, symmetric 16x16.

        Built as the fully antisymmetrised product
        sigma^{[mu1} sigmabar^{mu2} sigma^{mu3} sigmabar^{mu4} sigma^{mu5]},
        normalised by 1/5! so that it is the standard antisymmetriser with unit
        weight on the identity permutation.
        """
        p = self.p
        s, sb = self.sigma, self.sigma_bar
        inv120 = inv(C.FORWARD_NORMALISATION_DENOMINATOR, p)
        out: dict[tuple[int, ...], np.ndarray] = {}
        perms = list(itertools.permutations(range(5)))
        signs = [_perm_sign(q) for q in perms]
        for idx in itertools.combinations(range(C.SPACETIME_DIM), 5):
            acc = np.zeros((C.SPINOR_DIM, C.SPINOR_DIM), dtype=np.int64)
            for q, sg in zip(perms, signs):
                a, b, c, d, e = (idx[q[0]], idx[q[1]], idx[q[2]], idx[q[3]], idx[q[4]])
                M = matmul(matmul(matmul(matmul(s[a], sb[b], p), s[c], p), sb[d], p), s[e], p)
                acc = (acc + sg * M) % p
            out[idx] = (acc * inv120) % p
        return out


def _perm_sign(q) -> int:
    q = list(q)
    n, seen, sign = len(q), [False] * len(q), 1
    for i in range(n):
        if seen[i]:
            continue
        j, ln = i, 0
        while not seen[j]:
            seen[j] = True
            j = q[j]
            ln += 1
        if ln % 2 == 0:
            sign = -sign
    return sign
