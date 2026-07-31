"""Exact modular evaluation of spinor-side port-graph invariants.

The spinor archive represents a degree-`2m` invariant as a port graph: `m` nodes
carrying the invariant tensor `I_{ab,cd}`, each with four ports, and `2m` edges,
each edge being one factor of `F^{ab}`.  This module evaluates such graphs over
`F_p`, so that spinor-side values live in the same field as trace-side values and
the two can be compared exactly.

The archive evaluates in float64.  Nothing here rewrites its formulas: the graph
*specification* is the archive's, the *arithmetic* is modular.  The key
observation making that possible is that the invariant tensor factorises,

    I_{ab,cd} = sum_{i} sigma(e_i)_{ab} sigma(e^i)_{cd} + sigma(e^i)_{ab} sigma(e_i)_{cd}
              = sum_{mu=0}^{9} (sigma_mu)_{ab} (sigma_{flip(mu)})_{cd},
    flip(mu) = mu + 5 mod 10,

with integral `sigma`, so `I` is integral and the whole contraction is exact.

Contractions are executed as a sequence of pairwise `einsum` steps in an order
found by `opt_einsum`, with a reduction mod `p` after every step, so no
intermediate can overflow int64.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass

import numpy as np

from . import conventions as C
from .clifford import NullFrameClifford

try:  # opt_einsum gives much better contraction orders, but is optional
    import opt_einsum as _oe
except ImportError:  # pragma: no cover
    _oe = None


def flip(mu: int) -> int:
    """The null-frame partner index: wedge <-> contraction."""
    return (mu + C.OSCILLATORS) % C.SPACETIME_DIM


def invariant_I(p: int) -> np.ndarray:
    """I_{ab,cd} as a 16^4 integer tensor mod p."""
    sigma = NullFrameClifford(p=p).sigma
    out = np.zeros((C.SPINOR_DIM,) * 4, dtype=np.int64)
    for mu in range(C.SPACETIME_DIM):
        out = (out + np.multiply.outer(sigma[mu], sigma[flip(mu)])) % p
    return out


Port = tuple[int, int]     # (I-node, port 0..3)
Edge = tuple[Port, Port]


@dataclass(frozen=True)
class PortGraph:
    """A degree-2m spinor contraction graph: m I-nodes, 2m F-edges."""

    n_nodes: int
    edges: tuple[Edge, ...]

    @property
    def degree(self) -> int:
        return 2 * self.n_nodes

    def is_locally_zero(self) -> bool:
        """Both ends of an edge on the same I-node makes the contraction vanish.

        Same-pair is the gamma trace F^{ab} sigma^mu_{ab} = 0 directly; the
        cross-pair case is the further local spinor identity the archive relies
        on.  Either way the graph contributes nothing.
        """
        return any(a[0] == b[0] for a, b in self.edges)

    def canonical_key(self) -> tuple:
        """A relabelling-invariant key, used only to drop obvious duplicates.

        This is a cheap invariant, not a full graph canonicalisation: it may
        merge nothing that should be merged, but it never merges two graphs that
        differ.  Rank results do not depend on it.
        """
        deg = tuple(sorted(
            tuple(sorted(
                (b[0] if a[0] == n else a[0])
                for a, b in self.edges if n in (a[0], b[0])))
            for n in range(self.n_nodes)))
        return (self.n_nodes, deg)


def random_port_graph(rng: np.random.Generator, n_nodes: int,
                      max_tries: int = 200) -> PortGraph | None:
    """A uniformly random perfect matching on the 4m ports, rejecting zero graphs."""
    ports = [(i, q) for i in range(n_nodes) for q in range(4)]
    for _ in range(max_tries):
        order = list(rng.permutation(len(ports)))
        edges = tuple(
            tuple(sorted((ports[order[2 * k]], ports[order[2 * k + 1]])))
            for k in range(len(ports) // 2))
        g = PortGraph(n_nodes=n_nodes, edges=edges)  # type: ignore[arg-type]
        if not g.is_locally_zero():
            return g
    return None


#: Largest intermediate, in array elements, that a single contraction step may
#: build.  At 8 bytes per int64 this is about 1.6 GB.  Some port-graph
#: topologies genuinely need more than 10 GB with the batch index attached, and
#: silently attempting those is how a long run dies without a message.
MAX_INTERMEDIATE_ELEMENTS = 200_000_000


class ContractionTooLarge(RuntimeError):
    """Raised when no contraction order fits inside the memory budget.

    Callers treat this as a skipped candidate and record it, rather than
    crashing: the graph sampling is random anyway, so declining an expensive
    topology costs nothing as long as the count is reported.
    """


def _modular_contract(operands: list[np.ndarray], subscripts: list[list[int]],
                      p: int, output: list[int] | None = None,
                      memory_limit: int = MAX_INTERMEDIATE_ELEMENTS):
    """Contract, reducing mod p after every pairwise step so nothing overflows.

    With entries below p ~ 2^15, a product is below 2^30, and reducing after each
    pairwise contraction keeps the accumulation depth low enough that int64 never
    wraps.  Returns a scalar when `output` is empty, otherwise an array.
    """
    out_labels = [] if output is None else list(output)
    ops = [np.asarray(o, dtype=np.int64) % p for o in operands]
    subs = [list(s) for s in subscripts]

    if _oe is not None:
        interleaved: list = []
        for o, s in zip(ops, subs):
            interleaved.extend([o, s])
        path, info = _oe.contract_path(*interleaved, out_labels, optimize="auto")
        if int(info.largest_intermediate) > memory_limit:
            raise ContractionTooLarge(
                f"largest intermediate {int(info.largest_intermediate):,} elements "
                f"exceeds the budget of {memory_limit:,}")
    else:  # pragma: no cover - fallback order
        path = [(0, 1)] * (len(ops) - 1)

    for step in path:
        idx = sorted(step, reverse=True)
        chosen_ops = [ops.pop(i) for i in idx][::-1]
        chosen_subs = [subs.pop(i) for i in idx][::-1]
        remaining = [x for s in subs for x in s] + out_labels
        present = [x for s in chosen_subs for x in s]
        out_sub = sorted({x for x in present
                          if remaining.count(x) > 0 or present.count(x) == 1})
        args: list = []
        for o, s in zip(chosen_ops, chosen_subs):
            args.extend([o, s])
        args.append(out_sub)
        ops.append(np.einsum(*args, optimize=True) % p)
        subs.append(out_sub)

    while len(ops) > 1:
        a, sa = ops.pop(0), subs.pop(0)
        b, sb = ops.pop(0), subs.pop(0)
        out_sub = sorted(set(sa) | set(sb))
        ops.insert(0, np.einsum(a, sa, b, sb, out_sub, optimize=True) % p)
        subs.insert(0, out_sub)

    result, final = ops[0], subs[0]
    if final != out_labels:
        result = np.einsum(result, final, out_labels, optimize=True) % p
    return int(result) % p if not out_labels else np.asarray(result) % p


def evaluate_graph(graph: PortGraph, S: np.ndarray, I: np.ndarray, p: int) -> int:
    """Contraction with one distinct index per half-edge, using the full I tensor.

    Each I-node contributes four indices, one per port.  Each edge contributes an
    S carrying the two indices of the ports it joins.  Every index therefore
    appears exactly twice -- once on an I and once on an S.

    Kept as the reference implementation: it is the literal transcription of the
    port-graph definition.  `evaluate_graph_batch` computes the same numbers
    faster and is checked against this one.
    """
    port_index: dict[Port, int] = {}
    counter = itertools.count()
    for node in range(graph.n_nodes):
        for q in range(4):
            port_index[(node, q)] = next(counter)

    operands: list[np.ndarray] = []
    subs: list[list[int]] = []
    for node in range(graph.n_nodes):
        operands.append(I)
        subs.append([port_index[(node, q)] for q in range(4)])
    for a, b in graph.edges:
        operands.append(S)
        subs.append([port_index[a], port_index[b]])
    return _modular_contract(operands, subs, p)


def sigma_stacks(p: int) -> tuple[np.ndarray, np.ndarray]:
    """(sigma[mu], sigma[flip(mu)]) as 10 x 16 x 16 stacks."""
    sigma = NullFrameClifford(p=p).sigma % p
    return sigma, sigma[[flip(mu) for mu in range(C.SPACETIME_DIM)]] % p


def evaluate_graph_batch(graph: PortGraph, S_batch: np.ndarray, p: int,
                         stacks: tuple[np.ndarray, np.ndarray] | None = None,
                         chunk: int = 8) -> np.ndarray:
    """Values of one port graph at every sample at once.

    Two changes make this tractable at degree 8 and 10:

    1.  The invariant tensor is used in factorised form,
        I_{ab,cd} = sum_mu sigma_mu(ab) sigma_flip(mu)(cd), so each I-node becomes
        two 10 x 16 x 16 stacks sharing one ten-valued index instead of one
        65536-entry tensor.  Intermediates shrink by orders of magnitude.
    2.  All samples are carried along a single free batch index, so a graph is
        contracted once rather than once per sample.

    `S_batch` has shape (n_samples, 16, 16).
    """
    if stacks is None:
        stacks = sigma_stacks(p)
    sig, sig_flip = stacks

    Sb_all = np.asarray(S_batch, dtype=np.int64) % p
    if chunk and Sb_all.shape[0] > chunk:
        # the batch axis multiplies every intermediate, so slice it: the same
        # numbers come out, with a memory ceiling that does not grow with the
        # number of samples
        return np.concatenate([
            evaluate_graph_batch(graph, Sb_all[i:i + chunk], p, stacks, chunk=0)
            for i in range(0, Sb_all.shape[0], chunk)])

    BATCH = -1                      # reserved label for the sample axis
    port_index: dict[Port, int] = {}
    counter = itertools.count()
    for node in range(graph.n_nodes):
        for q in range(4):
            port_index[(node, q)] = next(counter)
    vector_label = {node: next(counter) for node in range(graph.n_nodes)}

    operands: list[np.ndarray] = []
    subs: list[list[int]] = []
    for node in range(graph.n_nodes):
        operands.append(sig)
        subs.append([vector_label[node], port_index[(node, 0)], port_index[(node, 1)]])
        operands.append(sig_flip)
        subs.append([vector_label[node], port_index[(node, 2)], port_index[(node, 3)]])
    for a, b in graph.edges:
        operands.append(Sb_all)
        subs.append([BATCH, port_index[a], port_index[b]])
    return _modular_contract(operands, subs, p, output=[BATCH])


def evaluation_matrix(graphs: list[PortGraph], spinor_fields: list[np.ndarray],
                      p: int) -> np.ndarray:
    """Rows = graphs, columns = samples.  Entry = invariant value mod p."""
    I = invariant_I(p)
    out = np.zeros((len(graphs), len(spinor_fields)), dtype=np.int64)
    for r, g in enumerate(graphs):
        for c, S in enumerate(spinor_fields):
            out[r, c] = evaluate_graph(g, S % p, I, p)
    return out % p


def sample_graphs_until_rank_saturates(
        degree: int, spinor_fields: list[np.ndarray], p: int,
        seed: int = 20260731, patience: int = 40,
        max_graphs: int = 600) -> tuple[list[PortGraph], np.ndarray, dict]:
    """Draw random port graphs until the evaluation rank stops growing.

    Returns (kept graphs, their evaluation matrix, diagnostics).  `patience` is
    the number of consecutive draws that must fail to raise the rank before the
    search stops, so the stopping rule is a saturation observation and is
    reported as such -- it is NOT a claim of exhaustive enumeration.
    """
    from .modular import rank as modrank

    if degree % 2:
        raise ValueError("spinor port graphs realise even degrees only")
    n_nodes = degree // 2
    rng = np.random.default_rng(seed)
    stacks = sigma_stacks(p)
    S_batch = np.array([np.asarray(S, dtype=np.int64) % p for S in spinor_fields])

    kept: list[PortGraph] = []
    rows: list[np.ndarray] = []
    seen: set = set()
    current_rank = 0
    since_gain = 0
    drawn = zero_valued = duplicate = local_zero = too_large = 0

    while drawn < max_graphs and since_gain < patience:
        g = random_port_graph(rng, n_nodes)
        drawn += 1
        if g is None:
            local_zero += 1
            continue
        key = tuple(sorted(g.edges))
        if key in seen:
            duplicate += 1
            continue
        seen.add(key)
        try:
            row = evaluate_graph_batch(g, S_batch, p, stacks).astype(np.int64)
        except ContractionTooLarge:
            too_large += 1
            since_gain += 1
            continue
        if not np.any(row % p):
            zero_valued += 1
            since_gain += 1
            continue
        trial = np.array(rows + [row], dtype=np.int64)
        r = modrank(trial, p)
        if r > current_rank:
            kept.append(g)
            rows.append(row)
            current_rank = r
            since_gain = 0
        else:
            since_gain += 1

    matrix = np.array(rows, dtype=np.int64) if rows else np.zeros((0, len(spinor_fields)), np.int64)
    return kept, matrix, {
        "degree": degree,
        "n_I_nodes": n_nodes,
        "graphs_drawn": drawn,
        "graphs_kept": len(kept),
        "duplicates_rejected": duplicate,
        "locally_zero_rejected": local_zero,
        "identically_zero_on_samples": zero_valued,
        "skipped_intermediate_too_large": too_large,
        "evaluation_rank": current_rank,
        "stopping_reason": ("rank saturation (patience exhausted)"
                            if since_gain >= patience else "draw budget exhausted"),
        "patience": patience,
        "exhaustive": False,
    }
