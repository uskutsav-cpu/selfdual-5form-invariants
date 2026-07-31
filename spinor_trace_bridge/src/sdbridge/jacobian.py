"""Exact modular Jacobian of the spinor invariants.

The archive computes `dI/dc_r` by central finite differences in float64 with
`eps = 1e-5`, and then has to choose a rank tolerance.  That is the sole reason
the reported rank was ever tolerance-sensitive, and the reason one archived run
reported 35 and another 81.

Here the derivative is computed exactly instead.  A port-graph invariant is a
multilinear contraction in its `2m` factors of `F`, so

    dI/dF^{(k)}_{ab} = the same contraction with the k-th F amputated,
    dI/dc_r          = sum_k  <amputated_k , B_r>,

where `B_r` is the r-th basis element of the 126-dimensional gamma-traceless
space.  No step size, no tolerance, no floating point.

What this settles, and what it does not:

  * The analytic upper bound `rank <= 126 - dim so(10) = 126 - 45 = 81` is a
    literature result and is NOT re-derived here.
  * An exact modular rank of 81 at an explicit point gives the matching LOWER
    bound, since rank over F_p at a specialisation never exceeds the generic rank
    over Q.
  * Together they pin the generic functional dimension at exactly 81 -- but the
    upper half of that argument remains the cited analytic one.
"""

from __future__ import annotations

import numpy as np

from . import conventions as C
from .clifford import NullFrameClifford
from .modular import rank as modrank
from .spinor_invariants import (
    ContractionTooLarge, PortGraph, _modular_contract, sigma_stacks,
)

import itertools


def gamma_traceless_matrix_basis(p: int) -> np.ndarray:
    """The 126 basis elements as symmetric 16 x 16 matrices, exact."""
    cl = NullFrameClifford(p=p)
    return np.array([cl.coords_to_symmetric(v) for v in cl.gamma_traceless_basis])


def graph_jacobian_row(graph: PortGraph, S: np.ndarray, basis: np.ndarray, p: int,
                       stacks: tuple[np.ndarray, np.ndarray] | None = None
                       ) -> np.ndarray:
    """dI/dc_r for one port graph at the point S: a vector of length 126.

    Two steps, in this order for a reason:

    1.  Amputate.  For each of the 2m edges, contract everything *except* that
        edge, leaving a bare 16 x 16 tensor A_k = dI/dF^{(k)}.  By multilinearity
        the full gradient is A = sum_k A_k.
    2.  Project.  dI/dc_r = <A, B_r>, a single 126 x 256 matrix-vector product.

    Doing it the other way round -- carrying all 126 basis elements through the
    contraction on a batch index -- multiplies every intermediate by 126 and
    makes degree 10 and 12 intractable.  Amputating first keeps the largest
    intermediate the same size as a plain evaluation.
    """
    if stacks is None:
        stacks = sigma_stacks(p)
    sig, sig_flip = stacks

    port_index: dict = {}
    counter = itertools.count()
    for node in range(graph.n_nodes):
        for q in range(4):
            port_index[(node, q)] = next(counter)
    vector_label = {node: next(counter) for node in range(graph.n_nodes)}

    S = np.asarray(S, dtype=np.int64) % p
    gradient = np.zeros((C.SPINOR_DIM, C.SPINOR_DIM), dtype=np.int64)

    for k, (ea, eb) in enumerate(graph.edges):
        operands: list[np.ndarray] = []
        subs: list[list[int]] = []
        for node in range(graph.n_nodes):
            operands.append(sig)
            subs.append([vector_label[node], port_index[(node, 0)], port_index[(node, 1)]])
            operands.append(sig_flip)
            subs.append([vector_label[node], port_index[(node, 2)], port_index[(node, 3)]])
        for j, (a, b) in enumerate(graph.edges):
            if j == k:
                continue
            operands.append(S)
            subs.append([port_index[a], port_index[b]])
        out = [port_index[ea], port_index[eb]]
        gradient = (gradient + _modular_contract(operands, subs, p, output=out)) % p

    B = np.asarray(basis, dtype=np.int64) % p
    return (B.reshape(B.shape[0], -1) @ gradient.reshape(-1) % p).astype(np.int64)


def jacobian_matrix(graphs: list[PortGraph], S: np.ndarray, p: int) -> np.ndarray:
    """Rows = graphs, columns = the 126 coefficients.  Exact over F_p."""
    basis = gamma_traceless_matrix_basis(p)
    stacks = sigma_stacks(p)
    return np.array([graph_jacobian_row(g, S, basis, p, stacks) for g in graphs],
                    dtype=np.int64) % p


def random_spinor_point(p: int, seed: int) -> np.ndarray:
    """A random gamma-traceless symmetric S, i.e. a random point of the 126."""
    cl = NullFrameClifford(p=p)
    rng = np.random.default_rng(seed)
    c = rng.integers(0, p, size=C.N_GAMMA_TRACELESS)
    coords = (c @ cl.gamma_traceless_basis) % p
    return cl.coords_to_symmetric(coords)


def accumulate_jacobian_rank(degrees: list[int], p: int, seed: int = 20260731,
                             patience: int = 40, max_graphs_per_degree: int = 250,
                             cap: int = 81, progress=None) -> dict:
    """Grow a graph set degree by degree, tracking the exact modular Jacobian rank.

    Stops early once `cap` is reached, since the analytic upper bound makes any
    further growth impossible; the stopping reason is recorded either way.
    """
    basis = gamma_traceless_matrix_basis(p)
    stacks = sigma_stacks(p)
    S = random_spinor_point(p, seed)
    rng = np.random.default_rng(seed + 7)

    from .spinor_invariants import random_port_graph

    rows: list[np.ndarray] = []
    per_degree: list[dict] = []
    current = 0
    stop_reason = "degrees exhausted"

    for d in degrees:
        n_nodes = d // 2
        drawn = kept = zero = dup = too_large = 0
        since_gain = 0
        seen: set = set()
        before = current
        while drawn < max_graphs_per_degree and since_gain < patience and current < cap:
            g = random_port_graph(rng, n_nodes)
            drawn += 1
            if g is None:
                continue
            key = tuple(sorted(g.edges))
            if key in seen:
                dup += 1
                continue
            seen.add(key)
            try:
                row = graph_jacobian_row(g, S, basis, p, stacks)
            except ContractionTooLarge:
                too_large += 1
                since_gain += 1
                continue
            if not np.any(row % p):
                zero += 1
                since_gain += 1
                continue
            r = modrank(np.array(rows + [row], dtype=np.int64), p)
            if r > current:
                rows.append(row)
                current = r
                kept += 1
                since_gain = 0
            else:
                since_gain += 1
        per_degree.append({
            "degree": d, "graphs_drawn": drawn, "rows_kept": kept,
            "duplicates": dup, "zero_rows": zero,
            "skipped_intermediate_too_large": too_large,
            "rank_before": before, "rank_after": current,
            "stopped_on": ("cap reached" if current >= cap else
                           "rank saturation" if since_gain >= patience else
                           "draw budget"),
        })
        if progress:
            progress(per_degree[-1])
        if current >= cap:
            stop_reason = f"analytic cap {cap} reached"
            break

    J = np.array(rows, dtype=np.int64) if rows else np.zeros((0, C.N_GAMMA_TRACELESS), np.int64)
    return {
        "prime": p,
        "point_seed": seed,
        "degrees_used": degrees,
        "per_degree": per_degree,
        "n_rows": int(J.shape[0]),
        "n_columns": int(C.N_GAMMA_TRACELESS),
        "exact_modular_rank": int(modrank(J, p)) if J.size else 0,
        "analytic_upper_bound": cap,
        "upper_bound_source": "126 - dim so(10) = 126 - 45; literature, not re-derived here",
        "stopping_reason": stop_reason,
        "zero_rows_present": bool(J.size and np.any(np.all(J % p == 0, axis=1))),
        "arithmetic": "exact over F_p; no finite differences, no tolerance",
    }
