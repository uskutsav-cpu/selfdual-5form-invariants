"""The complete selected candidate set: 70 port graphs + 13 tensor words, exactly.

Every scheduled candidate gets a terminal record.  There are four terminal
states and they are not interchangeable:

    evaluated              a value and a derivative row were produced
    structurally_rejected  the candidate is mathematically zero by construction
    evaluation_error       an exception was raised; the exception is serialised
    interrupted            the run stopped before this candidate was reached

A certificate is complete only when there are no `evaluation_error` and no
`interrupted` records.  A silently missing candidate is not permitted, which is
why the schedule is built first and then filled in, rather than accumulated as
results happen to arrive.
"""

from __future__ import annotations

import hashlib
import json
import resource
import sys
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path

import numpy as np

from . import conventions as C
from .modular import matmul
from .spinor_invariants import (
    ContractionTooLarge, PortGraph, evaluate_graph_batch, sigma_stacks,
)
from .jacobian import graph_jacobian_row
from .tensor_words import TensorWordEvaluator


def peak_rss_mb() -> float:
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return round(r / (1024 * 1024) if sys.platform == "darwin" else r / 1024, 1)


def _hash(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()[:32]


@dataclass
class Candidate:
    candidate_id: str
    degree: int
    family: str                     # "port_graph" | "tensor_word"
    formula_hash: str
    graph: PortGraph | None = None
    word: str | None = None
    evaluator: str = ""
    derivative_evaluator: str = ""
    terminal_status: str = "interrupted"
    runtime_seconds: float = 0.0
    peak_rss_mb: float = 0.0
    output_hash: str | None = None
    exception: str | None = None
    value: int | None = None
    zero_row: bool | None = None
    zero_row_explanation: str | None = None

    def record(self) -> dict:
        d = asdict(self)
        d.pop("graph", None)
        return d


def load_schedule(archive_selection: Path) -> list[Candidate]:
    """Build the full schedule from the archive's selected candidate list.

    The ORDER is preserved exactly as stored, because every archived Jacobian,
    summary and pivot index refers to positions in this list.  Re-sorting it
    would silently invalidate every cross-reference.
    """
    raw = json.loads(Path(archive_selection).read_text())
    out: list[Candidate] = []
    for position, d in enumerate(raw):
        degree = int(d["degree"])
        if d.get("kind") == "structured":
            name = str(d["name"])
            if name.startswith("sd5_tensor_word_"):
                out.append(Candidate(
                    candidate_id=f"c{position:03d}_{name}",
                    degree=degree, family="tensor_word",
                    formula_hash=_hash({"name": name, "degree": degree}),
                    word=name.removeprefix("sd5_tensor_word_"),
                    evaluator="tensor_words.word_value (exact mod p)",
                    derivative_evaluator="tensor_words.word_derivative (analytic, exact mod p)",
                ))
            else:
                out.append(Candidate(
                    candidate_id=f"c{position:03d}_{name}",
                    degree=degree, family="structured_degree8",
                    formula_hash=_hash({"name": name, "degree": degree}),
                    word=name,
                    evaluator="structured_degree8.values (exact mod p)",
                    derivative_evaluator=("structured_degree8.directional_derivative "
                                          "(exact modular interpolation)"),
                ))
            continue
        edges = tuple(tuple(sorted((tuple(a), tuple(b)))) for a, b in d["edges"])
        g = PortGraph(n_nodes=int(d["n_I"]), edges=edges)  # type: ignore[arg-type]
        out.append(Candidate(
            candidate_id=f"c{position:03d}_portgraph_d{degree}",
            degree=degree, family="port_graph",
            formula_hash=_hash({"n_I": d["n_I"], "edges": sorted(map(str, edges))}),
            graph=g,
            evaluator="spinor_invariants.evaluate_graph_batch (exact mod p)",
            derivative_evaluator="jacobian.graph_jacobian_row (amputated, exact mod p)",
        ))
    return out


@dataclass
class EvaluationContext:
    """Everything a candidate needs, built once."""
    p: int
    bridge: object
    S: np.ndarray                     # spinor point, 16x16
    F_null: np.ndarray                # same point as a null-frame five-form
    basis_spinor: np.ndarray          # 126 x 16 x 16, integral basis reduced
    basis_null: np.ndarray            # 126 x (10,)*5, same basis as five-forms
    stacks: tuple = field(default=None)
    tensor: TensorWordEvaluator = field(default=None)

    def __post_init__(self):
        if self.stacks is None:
            self.stacks = sigma_stacks(self.p)
        if self.tensor is None:
            self.tensor = TensorWordEvaluator(p=self.p)


def build_context(p: int, seed: int, n_basis: int = C.N_GAMMA_TRACELESS) -> EvaluationContext:
    """A generic sample point plus the integral coordinate basis, in both pictures."""
    from .bridge import BridgeMap
    from .clifford import NullFrameClifford, symmetric_pairs
    from .integral import integral_gamma_traceless_basis

    b = BridgeMap(p=p)
    cl = NullFrameClifford(p=p)
    IB = integral_gamma_traceless_basis()
    basis_mod = np.array([[int(x) % p for x in row] for row in IB], dtype=np.int64)

    rng = np.random.default_rng(seed)
    coeffs = rng.integers(0, p, size=n_basis).astype(np.int64)
    coords = (coeffs @ basis_mod) % p
    S = cl.coords_to_symmetric(coords)

    F_lor = b.inverse(coords)
    F_null = b.frame.five_form_to_null(b.traceside_dense(F_lor))

    basis_spinor = np.array([cl.coords_to_symmetric(basis_mod[r]) for r in range(n_basis)])
    basis_null = np.array([
        b.frame.five_form_to_null(b.traceside_dense(b.inverse(basis_mod[r])))
        for r in range(n_basis)])

    ctx = EvaluationContext(p=p, bridge=b, S=S, F_null=F_null,
                            basis_spinor=basis_spinor, basis_null=basis_null)
    ctx.coeffs = coeffs          # type: ignore[attr-defined]
    return ctx


def evaluate_all(schedule: list[Candidate], ctx: EvaluationContext,
                 progress=None) -> tuple[np.ndarray, list[Candidate]]:
    """Fill in every terminal record and return the exact Jacobian.

    Rows of the returned matrix correspond to candidates whose status is
    `evaluated`, in schedule order.  Candidates in any other state contribute no
    row, and their absence is explained by their record rather than by omission.
    """
    p = ctx.p
    rows: list[np.ndarray] = []
    tw_words = [c for c in schedule if c.family == "tensor_word" and c.word]
    sd8 = [c for c in schedule if c.family == "structured_degree8"]

    # the structured degree-8 family shares its interpolation sweep
    sd8_rows: dict[str, np.ndarray] = {}
    sd8_vals: dict[str, int] = {}
    if sd8:
        from .structured_degree8 import StructuredDegree8
        ev = StructuredDegree8(p=p)
        names = [c.word for c in sd8]
        try:
            vals = ev.values(ctx.S)
            sd8_vals = {n: vals[n] for n in names}
            J8 = ev.jacobian_rows(ctx.S, ctx.basis_spinor, names)
            sd8_rows = {n: J8[i] for i, n in enumerate(names)}
        except Exception as exc:            # noqa: BLE001
            for c in sd8:
                c.terminal_status = "evaluation_error"
                c.exception = f"{type(exc).__name__}: {exc}"

    # tensor words share their expensive polarisations, so evaluate them together
    tw_rows: dict[str, np.ndarray] = {}
    tw_vals: dict[str, int] = {}
    if tw_words:
        t0 = time.time()
        words = sorted({c.word for c in tw_words})
        try:
            A, B = ctx.tensor.blocks(ctx.F_null)
            for w in words:
                tw_vals[w] = ctx.tensor.word_value(w, A, B)
            J = ctx.tensor.jacobian_rows(words, ctx.F_null, ctx.basis_null)
            for i, w in enumerate(words):
                tw_rows[w] = J[i]
            shared = time.time() - t0
        except Exception as exc:            # noqa: BLE001 - recorded, not swallowed
            for c in tw_words:
                c.terminal_status = "evaluation_error"
                c.exception = f"{type(exc).__name__}: {exc}"
            shared = time.time() - t0
            tw_rows, tw_vals = {}, {}

    for c in schedule:
        if c.terminal_status == "structurally_rejected":
            continue
        if c.terminal_status == "evaluation_error":
            continue
        t0 = time.time()
        try:
            if c.family == "port_graph":
                val = int(evaluate_graph_batch(c.graph, ctx.S[None, ...], p,
                                               ctx.stacks)[0])
                row = graph_jacobian_row(c.graph, ctx.S, ctx.basis_spinor, p,
                                         ctx.stacks)
            elif c.family == "tensor_word":
                if c.word not in tw_rows:
                    raise RuntimeError("tensor-word batch did not produce a row")
                val, row = tw_vals[c.word], tw_rows[c.word]
            else:
                if c.word not in sd8_rows:
                    raise RuntimeError("structured degree-8 batch did not produce a row")
                val, row = sd8_vals[c.word], sd8_rows[c.word]
            c.value = int(val) % p
            c.zero_row = not bool(np.any(row % p))
            if c.zero_row:
                c.zero_row_explanation = (
                    "identically zero candidate" if c.value % p == 0 else
                    "nonzero value with vanishing gradient: nongeneric sample or "
                    "a candidate constant along the sampled directions")
            c.output_hash = _hash([int(x) % p for x in row])
            c.terminal_status = "evaluated"
            rows.append(np.asarray(row, dtype=np.int64) % p)
        except ContractionTooLarge as exc:
            c.terminal_status = "evaluation_error"
            c.exception = f"ContractionTooLarge: {exc}"
        except Exception as exc:            # noqa: BLE001
            c.terminal_status = "evaluation_error"
            c.exception = f"{type(exc).__name__}: {exc}"
        c.runtime_seconds = round(time.time() - t0, 3)
        c.peak_rss_mb = peak_rss_mb()
        if progress:
            progress(c)

    J = (np.array(rows, dtype=np.int64) if rows
         else np.zeros((0, ctx.basis_spinor.shape[0]), dtype=np.int64))
    return J % p, schedule


def schedule_summary(schedule: list[Candidate]) -> dict:
    by_status: dict[str, int] = {}
    by_family: dict[str, int] = {}
    for c in schedule:
        by_status[c.terminal_status] = by_status.get(c.terminal_status, 0) + 1
        key = f"{c.family}/{c.terminal_status}"
        by_family[key] = by_family.get(key, 0) + 1
    return {
        "planned": len(schedule),
        "by_terminal_status": by_status,
        "by_family_and_status": by_family,
        "evaluation_errors": by_status.get("evaluation_error", 0),
        "interrupted": by_status.get("interrupted", 0),
        "structurally_rejected": by_status.get("structurally_rejected", 0),
        "complete": (by_status.get("evaluation_error", 0) == 0
                     and by_status.get("interrupted", 0) == 0),
        "zero_rows": sum(1 for c in schedule if c.zero_row),
    }
