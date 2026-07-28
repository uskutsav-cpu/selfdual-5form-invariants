"""Contraction graphs.

A fully-contracted scalar built from n copies of a p-form is a perfect
matching on the n*p index slots. The induced multigraph has every vertex of
valence p, and the multigraph determines the scalar up to sign.

So enumerating candidate invariants at order n is exactly:

    symmetric n x n non-negative integer matrices,
    zero diagonal, every row sum = p.

Pruning rules, both exact:
  * no self-loops -- contracting two slots of the same antisymmetric form
    gives zero;
  * m_ij <= p-1 FOR THE SELF-DUAL CASE ONLY -- multiplicity p between two
    vertices means those two forms fully contract, giving a factor F.F,
    which vanishes identically for a self-dual 5-form in 10D. For a
    GENERIC form (e.g. the 6D 3-form) F.F is a perfectly good invariant,
    so pass max_mult=valence there. This is the default.

Only CONNECTED graphs are kept: a disconnected graph is a product of lower
invariants and can never raise the Jacobian rank.

Dedup is an OPTIMISATION, not a correctness requirement -- a duplicate
graph just yields a duplicate Jacobian row, which the sieve discards for
free. So for large n we use a cheap Weisfeiler-Lehman hash and accept
occasional collisions rather than paying n! for an exact canonical form.
"""

import itertools
import numpy as np

EXACT_CANON_MAX_N = 6


def _connected(M):
    n = M.shape[0]
    seen, stack = {0}, [0]
    while stack:
        v = stack.pop()
        for w in range(n):
            if w not in seen and M[v, w]:
                seen.add(w)
                stack.append(w)
    return len(seen) == n


def _canonical_exact(M):
    n = M.shape[0]
    iu = np.triu_indices(n, 1)
    best = None
    for perm in itertools.permutations(range(n)):
        key = tuple(M[np.ix_(perm, perm)][iu])
        if best is None or key < best:
            best = key
    return best


def _canonical_wl(M, rounds=3):
    n = M.shape[0]
    colors = [hash(tuple(sorted(M[v]))) for v in range(n)]
    for _ in range(rounds):
        colors = [
            hash((colors[v], tuple(sorted(
                (int(M[v, w]), colors[w]) for w in range(n) if M[v, w]))))
            for v in range(n)
        ]
    return (tuple(sorted(colors)),
            tuple(sorted(int(M[i, j]) for i in range(n)
                         for j in range(i + 1, n) if M[i, j])))


def canonical(M):
    n = M.shape[0]
    return (_canonical_exact(M) if n <= EXACT_CANON_MAX_N
            else _canonical_wl(M))


def enumerate_graphs(n, valence, max_mult=None, connected_only=True):
    """All valence-regular multigraphs on n vertices, deduped up to
    isomorphism (exactly for small n, heuristically for large n)."""
    if max_mult is None:
        max_mult = valence
    M = np.zeros((n, n), dtype=np.int64)
    out = {}

    def rec(i, j):
        if i == n - 1:
            if int(M[n - 1].sum()) != valence:
                return
            if connected_only and not _connected(M):
                return
            key = canonical(M)
            if key not in out:
                out[key] = M.copy()
            return
        if j == n:
            if int(M[i].sum()) != valence:
                return
            return rec(i + 1, i + 2)
        used_i = int(M[i].sum())
        used_j = int(M[j].sum())
        hi = min(max_mult, valence - used_i, valence - used_j)
        for m in range(hi + 1):
            M[i, j] = M[j, i] = m
            rec(i, j + 1)
        M[i, j] = M[j, i] = 0

    rec(0, 1)
    return list(out.values())


def graph_label(M):
    n = M.shape[0]
    return f"n{n}[" + ",".join(
        f"{i}{j}^{int(M[i, j])}" for i in range(n) for j in range(i + 1, n)
        if M[i, j]) + "]"
