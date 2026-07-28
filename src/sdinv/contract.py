"""Evaluate a contraction graph, and build its Jacobian row.

METRIC. sum_mu F^mu G_mu = sum_mu s_mu F[mu] G[mu], so each edge needs
exactly ONE factor of the metric sign. Every edge is oriented and the sign
is applied at the tail. Applying it at both ends gives s^2 = 1 and silently
computes the Euclidean contraction -- a bug that will not announce itself.

JACOBIAN, the fast way. I is a degree-n contraction of n copies of F, so it
is multilinear in the vertices and

    dI/dA^k = sum_v [ same graph, F at vertex v replaced by P(e_k) ].

Naively that is (#basis * n) einsums per graph. Instead, for each vertex v
contract everything EXCEPT v, leaving v's p slots free. Call that the
amputated tensor A_v. Then

    dI/dA^k = sum_v <A_v, P(e_k)>

so it costs n einsums plus cheap inner products. For 10D that is the
difference between hours and minutes.
"""

import string
import numpy as np

from .modp import P, mod_einsum
from .forms import basis_tuples, to_dense, metric_signs

LETTERS = string.ascii_letters


def _apply_sign(T, axis, s, mod):
    shape = [1] * T.ndim
    shape[axis] = len(s)
    return (T * s.reshape(shape)) % mod


def _slot_plan(M, valence):
    """Assign a letter to each edge-slot; record which axes are tails."""
    n = M.shape[0]
    slots = [[] for _ in range(n)]
    tails = [[] for _ in range(n)]
    li = 0
    for i in range(n):
        for j in range(i + 1, n):
            for _ in range(int(M[i, j])):
                L = LETTERS[li]
                li += 1
                tails[i].append(len(slots[i]))
                slots[i].append(L)
                slots[j].append(L)
    for v in range(n):
        assert len(slots[v]) == valence, "valence mismatch"
    return slots, tails


def _signed(T, axes, s, mod):
    for ax in axes:
        T = _apply_sign(T, ax, s, mod)
    return T


def evaluate(M, tensors, d, valence, lorentzian=True, mod=P):
    slots, tails = _slot_plan(M, valence)
    s = metric_signs(d, lorentzian) % mod
    ops = [_signed(T, tails[v], s, mod) for v, T in enumerate(tensors)]
    sub = ",".join("".join(sl) for sl in slots) + "->"
    return int(mod_einsum(sub, ops, mod))


def amputated(M, F_dense, v, d, valence, lorentzian=True, mod=P):
    """Contract every vertex except v, leaving v's slots free."""
    slots, tails = _slot_plan(M, valence)
    s = metric_signs(d, lorentzian) % mod
    ops, subs = [], []
    for u in range(M.shape[0]):
        if u == v:
            continue
        ops.append(_signed(F_dense, tails[u], s, mod))
        subs.append("".join(slots[u]))
    sub = ",".join(subs) + "->" + "".join(slots[v])
    A = mod_einsum(sub, ops, mod)
    return _signed(A, tails[v], s, mod)


def jacobian_row(M, F_dense, basis_flat, d, valence,
                 lorentzian=True, mod=P):
    """basis_flat: 2-D array, one flattened dense basis tensor per row."""
    n = M.shape[0]
    row = np.zeros(basis_flat.shape[0], dtype=np.int64)
    for v in range(n):
        A = amputated(M, F_dense, v, d, valence, lorentzian, mod).ravel()
        row = (row + (basis_flat @ A) % mod) % mod  # both < p, safe
    return row


def value(M, F_dense, d, valence, lorentzian=True, mod=P):
    return evaluate(M, [F_dense] * M.shape[0], d, valence, lorentzian, mod)


def build_basis_flat(d, p_deg, projector=None, mod=P):
    """Flattened dense basis directions, stacked as rows."""
    tuples = basis_tuples(d, p_deg)
    N = len(tuples)
    rows = []
    for k in range(N):
        vec = np.zeros(N, dtype=np.int64)
        vec[k] = 1
        if projector is not None:
            vec = (projector @ vec) % mod
        rows.append(to_dense(vec, d, p_deg, mod).ravel())
    return np.array(rows, dtype=np.int64)
