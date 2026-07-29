"""Evaluate a contraction graph, and build its Jacobian row.

METRIC. sum_mu F^mu G_mu = sum_mu s_mu F[mu] G[mu], so each edge needs
exactly ONE factor of the metric sign. Every edge is oriented and the sign
is applied at the tail. Applying it at both ends gives s^2 = 1 and silently
computes the Euclidean contraction -- a bug that will not announce itself.

JACOBIAN. I is a degree-n contraction of n copies of F, so it is
multilinear in the vertices and

    dI/dA^k = sum_v [ same graph, F at vertex v replaced by P(e_k) ].

The original implementation built each amputated tensor separately, costing
n tensor-network contractions per graph. The production path below contracts
the network once and reverse-differentiates that contraction tree. This gives
all n amputated tensors while reusing the forward intermediates. The older
amputated implementation remains as a small-case correctness oracle.

For 10D order 8, that reuse is the difference between an exhaustive run being
practical and taking many hours.
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


def jacobian_row_amputated(M, F_dense, basis_flat, d, valence,
                           lorentzian=True, mod=P):
    """basis_flat: 2-D array, one flattened dense basis tensor per row."""
    n = M.shape[0]
    row = np.zeros(basis_flat.shape[0], dtype=np.int64)
    for v in range(n):
        A = amputated(M, F_dense, v, d, valence, lorentzian, mod).ravel()
        row = (row + (basis_flat @ A) % mod) % mod  # both < p, safe
    return row


def _optimal_contraction_tree(terms, operand_shapes):
    """Globally optimal binary tree for this small closed tensor network.

    A local greedy choice can create a disastrous later intermediate. There
    are at most eight operands in the runs here, so dynamic programming over
    all subsets is tiny. The score first minimises the largest pairwise work,
    then total forward/reverse work.
    """
    n = len(terms)
    label_dims = {}
    label_sets = []
    for term, shape in zip(terms, operand_shapes):
        labels = set(term)
        label_sets.append(labels)
        for label, size in zip(term, shape):
            old = label_dims.setdefault(label, size)
            assert old == size, f"dimension mismatch for index {label}"

    boundary = [set() for _ in range(1 << n)]
    for mask in range(1, 1 << n):
        bit = mask & -mask
        v = bit.bit_length() - 1
        boundary[mask] = boundary[mask ^ bit] ^ label_sets[v]

    # score[mask] = (largest pair work, total fwd+reverse work).
    score = [(0, 0) for _ in range(1 << n)]
    split = [None for _ in range(1 << n)]
    for size in range(2, n + 1):
        for mask in range(1, 1 << n):
            if mask.bit_count() != size:
                continue
            anchor = mask & -mask
            part = (mask - 1) & mask
            best = None
            while part:
                if part & anchor:
                    other = mask ^ part
                    if other:
                        pair_work = 1
                        for label in boundary[part] | boundary[other]:
                            pair_work *= label_dims[label]
                        candidate = (
                            max(score[part][0], score[other][0], pair_work),
                            score[part][1] + score[other][1] + 3 * pair_work,
                            part,
                            other,
                        )
                        if best is None or candidate[:2] < best[:2]:
                            best = candidate
                part = (part - 1) & mask
            score[mask] = best[:2]
            split[mask] = best[2:]

    return split, boundary, score[(1 << n) - 1]


def contraction_plan_cost(M, d, valence):
    """Return (largest_pair_work, total_forward_reverse_work) without running."""
    slots, _ = _slot_plan(M, valence)
    terms = ["".join(x) for x in slots]
    _, _, score = _optimal_contraction_tree(
        terms, [(d,) * valence for _ in terms])
    return score


def _network_gradient(terms, operands, mod=P):
    """Reverse-differentiate a scalar pairwise tensor contraction.

    Each index label must occur exactly twice across the input terms, as it
    does for a fully contracted graph. The returned list is the derivative
    with respect to each input operand, in the operand's original axis order.
    """
    nodes = [{"term": term, "value": np.asarray(op, dtype=np.int64) % mod,
              "left": None, "right": None}
             for term, op in zip(terms, operands)]
    split, boundary, _ = _optimal_contraction_tree(
        terms, [op.shape for op in operands])

    def forward(mask):
        if mask.bit_count() == 1:
            return (mask & -mask).bit_length() - 1
        left_mask, right_mask = split[mask]
        left, right = forward(left_mask), forward(right_mask)
        lt, rt = nodes[left]["term"], nodes[right]["term"]
        keep_labels = boundary[mask]
        keep = "".join(c for c in dict.fromkeys(lt + rt)
                       if c in keep_labels)
        result = mod_einsum(
            f"{lt},{rt}->{keep}",
            [nodes[left]["value"], nodes[right]["value"]],
            mod,
        )
        parent = len(nodes)
        nodes.append({"term": keep, "value": result,
                      "left": left, "right": right})
        return parent

    root = forward((1 << len(operands)) - 1)
    assert nodes[root]["term"] == "", "network is not fully contracted"
    adjoints = {root: np.array(1, dtype=np.int64)}

    for parent in range(root, len(operands) - 1, -1):
        node = nodes[parent]
        left, right = node["left"], node["right"]
        pt = node["term"]
        lt, rt = nodes[left]["term"], nodes[right]["term"]
        adj = adjoints[parent]
        adjoints[left] = mod_einsum(
            f"{pt},{rt}->{lt}", [adj, nodes[right]["value"]], mod)
        adjoints[right] = mod_einsum(
            f"{pt},{lt}->{rt}", [adj, nodes[left]["value"]], mod)

    return [adjoints[k] for k in range(len(operands))]


def jacobian_row(M, F_dense, basis_flat, d, valence,
                 lorentzian=True, mod=P):
    """Jacobian row from one forward/reverse tensor-network contraction."""
    slots, tails = _slot_plan(M, valence)
    s = metric_signs(d, lorentzian) % mod
    terms = ["".join(x) for x in slots]
    operands = [_signed(F_dense, tails[v], s, mod)
                for v in range(M.shape[0])]
    operand_gradients = _network_gradient(terms, operands, mod)

    gradient = np.zeros_like(F_dense, dtype=np.int64)
    for v, grad in enumerate(operand_gradients):
        # The forward operand is signed(F), so the chain rule applies the
        # same diagonal metric signs once more to map dI/d(signed F) to dI/dF.
        gradient = (gradient + _signed(grad, tails[v], s, mod)) % mod
    return (basis_flat @ gradient.ravel()) % mod


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
