"""Structured tensor-word invariants, exact over F_p.

These are the thirteen candidates the port-graph stream cannot produce, and they
are the reason the port-only family stalls one short at degree 8.  They are
independently re-implemented here from the mathematical description --- no
implementation text is copied from the external archive; see
`docs/THIRD_PARTY_ARCHIVE_BOUNDARY.md`.

Construction.  From a self-dual five-form F in the null frame build two
quadratic tensors,

    M_mu{}^nu      = F_{mu a b c d} F^{nu a b c d}
    N_{abc}{}^{def} = F_{a b c l m} F^{d e f l m}

`N` is already an endomorphism of Lambda^3 V (dimension 120).  `M` is promoted to
one by acting as a derivation --- replacing one index of a 3-form at a time.  A
degree-2L invariant is then the trace of a length-L word in those two
endomorphisms, and cyclic words related by rotation give the same trace, so the
candidates are indexed by binary necklaces.

Everything is polynomial in F with integer coefficients once the index-raising
convention is fixed, so the whole construction is exact over F_p.  No floating
point appears.

Index raising.  In the null frame, raising swaps the wedge block with the
contraction block: mu -> mu + 5 mod 10.  This is the convention that makes
`M` and `N` scalars under the frame group; `verify_raising_convention` checks it
against the metric rather than assuming it.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass
from functools import cached_property

import numpy as np

from . import conventions as C
from .modular import inv, matmul

VECTOR_DIM = C.SPACETIME_DIM
TRIFORM_DIM = 120          # C(10,3)


def raise_index_permutation() -> np.ndarray:
    """mu -> mu + 5 mod 10, the null-frame index-raising permutation."""
    return np.array([(mu + C.OSCILLATORS) % VECTOR_DIM for mu in range(VECTOR_DIM)],
                    dtype=np.intp)


def verify_raising_convention(p: int) -> dict:
    """Check that the permutation really is index raising for the null metric.

    Raising with eta^{mu nu} = (1/2)[[0,I],[I,0]] sends a lower index mu to the
    upper index mu+5 with a factor of 1/2.  The permutation therefore implements
    raising up to that overall constant, which rescales M and N by a fixed power
    of two and cannot affect any rank or span statement.  We check the
    permutation part exactly and record the constant.
    """
    from .clifford import null_metric
    eta = null_metric(p)
    perm = raise_index_permutation()
    half = inv(2, p)
    expected = np.zeros((VECTOR_DIM, VECTOR_DIM), dtype=np.int64)
    for mu in range(VECTOR_DIM):
        expected[mu, perm[mu]] = half
    return {
        "permutation": [int(x) for x in perm],
        "matches_metric_up_to_scale": bool(np.array_equal(eta % p, expected % p)),
        "omitted_scale": "1/2 per raised index; rescales M and N by a constant",
    }


def triples() -> list[tuple[int, int, int]]:
    return list(itertools.combinations(range(VECTOR_DIM), 3))


def _perm_sign(seq) -> int:
    inv_count = 0
    seq = list(seq)
    for i in range(len(seq)):
        for j in range(i + 1, len(seq)):
            if seq[i] > seq[j]:
                inv_count += 1
    return -1 if inv_count % 2 else 1


def necklaces(length: int, alphabet: str = "AB") -> tuple[str, ...]:
    """Binary necklaces: one representative per cyclic class, lexicographically least.

    Traces of words in two matrices are invariant under cyclic rotation, so words
    in the same class define the same invariant and must not be double counted.
    """
    out = []
    for chars in itertools.product(alphabet, repeat=length):
        word = "".join(chars)
        if word == min(word[k:] + word[:k] for k in range(length)):
            out.append(word)
    return tuple(out)


def tensor_word_names_for_degree(degree: int) -> tuple[str, ...]:
    """Only even degrees with an integral word length carry tensor words."""
    if degree % 2 or degree // 2 < 1:
        return ()
    return tuple(f"sd5_tensor_word_{w}" for w in necklaces(degree // 2))


@dataclass(frozen=True)
class TensorWordEvaluator:
    """Exact evaluation and exact differentiation of the tensor-word family."""

    p: int = C.DEFAULT_PRIME

    @cached_property
    def triples(self) -> list[tuple[int, int, int]]:
        return triples()

    @cached_property
    def triple_index(self) -> dict[tuple[int, int, int], int]:
        return {t: i for i, t in enumerate(self.triples)}

    @cached_property
    def derivation_terms(self):
        """Sparse structure of the derivation that promotes M to Lambda^3 V.

        Returns (rows, cols, old, new, signs) so that
            A[row, col] += sign * M[old, new]
        replaces one index of the 3-form indexed by `col`.
        """
        rows, cols, old, new, signs = [], [], [], [], []
        for col, triple in enumerate(self.triples):
            for pos in range(3):
                for fresh in range(VECTOR_DIM):
                    out = list(triple)
                    out[pos] = fresh
                    if len(set(out)) < 3:
                        continue
                    rows.append(self.triple_index[tuple(sorted(out))])
                    cols.append(col)
                    old.append(triple[pos])
                    new.append(fresh)
                    signs.append(_perm_sign(out))
        return (np.asarray(rows, dtype=np.intp), np.asarray(cols, dtype=np.intp),
                np.asarray(old, dtype=np.intp), np.asarray(new, dtype=np.intp),
                np.asarray(signs, dtype=np.int64))

    # -- the two quadratic tensors -------------------------------------------

    def M_tensor(self, F_lo: np.ndarray, G_lo: np.ndarray | None = None) -> np.ndarray:
        """M_mu{}^nu, or its polarisation in (F, G) when G is given."""
        p = self.p
        perm = raise_index_permutation()
        G = F_lo if G_lo is None else G_lo
        G_up = G[np.ix_(perm, perm, perm, perm, perm)]
        return np.einsum("mabcd,nabcd->mn", F_lo % p, G_up % p, optimize=True) % p

    def N_matrix(self, F_lo: np.ndarray, G_lo: np.ndarray | None = None) -> np.ndarray:
        """N as a 120 x 120 endomorphism: row = upper triple, column = lower triple."""
        p = self.p
        perm = raise_index_permutation()
        G = F_lo if G_lo is None else G_lo
        G_up = G[np.ix_(perm, perm, perm, perm, perm)]
        N6 = np.einsum("abclm,deflm->abcdef", F_lo % p, G_up % p, optimize=True) % p
        t = np.asarray(self.triples, dtype=np.intp)
        lo0, lo1, lo2 = t[:, 0][None, :], t[:, 1][None, :], t[:, 2][None, :]
        up0, up1, up2 = t[:, 0][:, None], t[:, 1][:, None], t[:, 2][:, None]
        return N6[lo0, lo1, lo2, up0, up1, up2] % p

    def A_matrix(self, M: np.ndarray) -> np.ndarray:
        """Promote M to an endomorphism of Lambda^3 V by derivation."""
        p = self.p
        rows, cols, old, new, signs = self.derivation_terms
        A = np.zeros((TRIFORM_DIM, TRIFORM_DIM), dtype=np.int64)
        np.add.at(A, (rows, cols), (signs * M[old, new]) % p)
        return A % p

    def blocks(self, F_lo: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        return self.A_matrix(self.M_tensor(F_lo)), self.N_matrix(F_lo)

    def polarised_blocks(self, F_lo: np.ndarray, B_lo: np.ndarray):
        """d/dt of (A, B) at t=0 along F -> F + t*B.

        Both tensors are quadratic, so the derivative is the symmetrised
        polarisation: dM(F; B) = M(B, F) + M(F, B).
        """
        p = self.p
        dM = (self.M_tensor(B_lo, F_lo) + self.M_tensor(F_lo, B_lo)) % p
        dN = (self.N_matrix(B_lo, F_lo) + self.N_matrix(F_lo, B_lo)) % p
        return self.A_matrix(dM), dN

    # -- word values and derivatives -----------------------------------------

    def word_value(self, word: str, A: np.ndarray, B: np.ndarray) -> int:
        p = self.p
        mats = {"A": A, "B": B}
        acc = np.eye(TRIFORM_DIM, dtype=np.int64)
        for ch in word:
            acc = matmul(acc, mats[ch], p)
        return int(np.trace(acc) % p)

    def word_derivative(self, word: str, A: np.ndarray, B: np.ndarray,
                        dA: np.ndarray, dB: np.ndarray) -> int:
        """d/dt tr(X_1...X_L) = sum_k tr(X_1...dX_k...X_L), exactly."""
        p = self.p
        mats = {"A": A, "B": B}
        dmats = {"A": dA, "B": dB}
        total = 0
        for k in range(len(word)):
            acc = np.eye(TRIFORM_DIM, dtype=np.int64)
            for j, ch in enumerate(word):
                acc = matmul(acc, dmats[ch] if j == k else mats[ch], p)
            total = (total + int(np.trace(acc))) % p
        return total % p

    def evaluate(self, words: list[str], F_lo: np.ndarray) -> dict[str, int]:
        A, B = self.blocks(F_lo)
        return {w: self.word_value(w, A, B) for w in words}

    def jacobian_rows(self, words: list[str], F_lo: np.ndarray,
                      basis_lo: np.ndarray) -> np.ndarray:
        """Exact dI/dc_r for each word.  `basis_lo` is (n_basis,)+(10,)*5.

        The derivative is analytic: no step size, no tolerance.  Cost is one
        polarisation per basis direction, which is why the basis is passed in
        dense form rather than re-derived per word.
        """
        p = self.p
        A, B = self.blocks(F_lo)
        out = np.zeros((len(words), basis_lo.shape[0]), dtype=np.int64)
        for r in range(basis_lo.shape[0]):
            dA, dB = self.polarised_blocks(F_lo, basis_lo[r])
            for i, w in enumerate(words):
                out[i, r] = self.word_derivative(w, A, B, dA, dB)
        return out % p

    # -- self-check ------------------------------------------------------------

    def euler_check(self, words: list[str], F_lo: np.ndarray,
                    coeffs: np.ndarray, basis_lo: np.ndarray) -> dict:
        """Euler homogeneity: sum_r c_r dI/dc_r = deg * I, exactly.

        This is the single strongest self-check available for a derivative
        implementation, because it fails for almost any sign or normalisation
        error while costing one extra contraction.
        """
        p = self.p
        A, B = self.blocks(F_lo)
        rows = self.jacobian_rows(words, F_lo, basis_lo)
        results = {}
        for i, w in enumerate(words):
            degree = 2 * len(w)
            lhs = int(np.asarray(coeffs, dtype=np.int64) % p @ rows[i] % p)
            rhs = (degree * self.word_value(w, A, B)) % p
            results[w] = {"degree": degree, "lhs": lhs, "rhs": rhs, "ok": lhs == rhs}
        return results
