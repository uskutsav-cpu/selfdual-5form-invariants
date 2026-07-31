"""Common-sample comparison of the trace and spinor invariant spans.

Both sides are evaluated at the *same* five-forms, in the *same* field, and the
resulting evaluation spans are compared by two-way containment rather than by
dimension.  Change-of-basis matrices are fitted on the generic samples only and
then validated on holdout samples that took no part in the fit.

Grading note.  The trace side's registry is cumulative in the sense that its
degree-10 basis contains two explicit products of lower-degree invariants; the
spinor side's port graphs at degree 10 are not separated into product and
primitive families.  The comparison is therefore made degree by degree between

    trace  : span of the evaluation vectors of the degree-d registry items
    spinor : span of the evaluation vectors of degree-d port graphs

which is the correct pairing, since both are the full degree-d invariant space
evaluated at the same points.  See `grading_table()`.
"""

from __future__ import annotations

import numpy as np

from . import conventions as C
from .modular import matmul, rank, row_space_contains, spans_equal, rref
from .clifford import _inverse_mod


def trace_evaluation_matrix(bridge, samples, registry, degree: int) -> np.ndarray:
    """Rows = registry items of this degree, columns = samples."""
    p = bridge.p
    items = registry.basis(degree)
    out = np.zeros((len(items), len(samples)), dtype=np.int64)
    for c, s in enumerate(samples):
        # the registry evaluates on dense antisymmetric arrays, not sorted components
        values = registry.evaluate_degree(degree, bridge.traceside_dense(s.as_array()), p)
        for r, value in enumerate(values):
            out[r, c] = int(value) % p
    return out % p


def spinor_fields(bridge, samples) -> np.ndarray:
    """Push every sample through the bridge; shape (n_samples, 16, 16)."""
    return np.array([
        bridge.clifford.coords_to_symmetric(bridge.forward(s.as_array()))
        for s in samples])


def check_gamma_traces(bridge, S_batch) -> bool:
    p = bridge.p
    A = bridge.clifford.gamma_trace_constraints
    for S in S_batch:
        coords = bridge.clifford.symmetric_to_coords(S)
        if np.any(matmul(A, coords.reshape(-1, 1), p) % p):
            return False
    return True


def fit_change_of_basis(source: np.ndarray, target: np.ndarray, p: int):
    """Find X with X @ source = target on the given columns, if one exists.

    `source` and `target` are (rows x samples) evaluation matrices restricted to
    the fitting columns.  Returns None when the target rows do not lie in the
    source row space.
    """
    if not row_space_contains(source, target, p):
        return None
    R, piv = rref(source, p)
    basis = R[:len(piv)]
    sq = _inverse_mod(basis[:, piv], p)
    # coefficients of each target row in the reduced basis
    coeff = matmul(target[:, piv], sq, p)
    # and of the reduced basis in the original rows
    Rs, pivs = rref(source.T, p)
    del Rs, pivs
    return coeff, basis


def compare_degree(bridge, samples, registry, degree: int, spinor_rows: np.ndarray,
                   spinor_diag: dict) -> dict:
    """Full comparison at one degree."""
    p = bridge.p
    fit_idx = [i for i, s in enumerate(samples) if s.family in ("generic", "sparse", "structured")]
    hold_idx = [i for i, s in enumerate(samples) if s.family == "holdout"]

    trace_rows = trace_evaluation_matrix(bridge, samples, registry, degree)

    result = {
        "degree": degree,
        "n_samples": len(samples),
        "n_fitting_samples": len(fit_idx),
        "n_holdout_samples": len(hold_idx),
        "trace_items": [i.id for i in registry.basis(degree)],
        "trace_evaluation_rank": rank(trace_rows, p),
        "spinor_graphs_kept": int(spinor_rows.shape[0]),
        "spinor_evaluation_rank": rank(spinor_rows, p),
        "spinor_enumeration": spinor_diag,
    }

    result["spans_equal_all_samples"] = bool(spans_equal(trace_rows, spinor_rows, p))
    result["trace_contained_in_spinor"] = bool(row_space_contains(spinor_rows, trace_rows, p))
    result["spinor_contained_in_trace"] = bool(row_space_contains(trace_rows, spinor_rows, p))

    # fit on fitting columns only, then validate on holdout columns
    tf, sf = trace_rows[:, fit_idx], spinor_rows[:, fit_idx]
    th, sh = trace_rows[:, hold_idx], spinor_rows[:, hold_idx]
    result["spans_equal_on_fitting_samples"] = bool(spans_equal(tf, sf, p))

    fitted = fit_change_of_basis(sf, tf, p)
    if fitted is None:
        result["change_of_basis"] = None
        result["holdout_validated"] = False
    else:
        coeff, _basis = fitted
        R, piv = rref(sf, p)
        basis_hold = None
        # reconstruct the reduced spinor basis on holdout columns using the same
        # row operations: solve for the transform T with T @ sf = R[:len(piv)]
        T = matmul(R[:len(piv)][:, piv], _inverse_mod(sf[:, piv], p), p)
        basis_hold = matmul(T, sh, p)
        predicted = matmul(coeff, basis_hold, p)
        result["change_of_basis"] = {
            "shape": list(coeff.shape),
            "fitted_on": "generic + sparse + structured samples",
            "validated_on": "holdout samples only",
        }
        result["holdout_validated"] = bool(np.array_equal(predicted % p, th % p))
    return result


def grading_table(registry) -> list[dict]:
    """How the two gradings line up, stated rather than assumed."""
    rows = []
    for d in registry.degrees:
        items = registry.basis(d)
        rows.append({
            "physical_F_degree": d,
            "trace_registry_items": len(items),
            "trace_product_items": sum(1 for i in items if i.kind == "product"),
            "trace_graph_items": sum(1 for i in items if i.kind == "graph"),
            "spinor_I_nodes": d // 2,
            "spinor_F_edges": d,
            "note": ("spinor port graphs are not split into product and "
                     "primitive families; the comparison is against the whole "
                     "degree-d space on both sides"),
        })
    return rows
