"""The aggregator must refuse a bad matrix, not repair one.

Every test here takes a matrix that would assemble cleanly, breaks exactly one
thing, and asserts the aggregator fails and says why. A read-only aggregator
that quietly drops a bad cell is worse than no aggregator, because the
certificate it emits looks complete.

The cells are synthetic. Nothing here evaluates an invariant; these tests are
about the accounting layer, and they run in under a second so they can guard
every build rather than only the ones where someone remembers to look.
"""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
AGGREGATOR = ROOT / "spinor_trace_bridge" / "scripts" / "assemble_rank81_matrix.py"

FITTING = [32749, 32719, 32717]
HOLDOUT = [32713, 32707]
SEEDS = [11, 22, 33]

SELECTION_SHA = "a" * 64
ORDER_SHA = "b" * 64


def content_hash(cell: dict) -> str:
    body = dict(cell)
    body.pop("content_sha256", None)
    return hashlib.sha256(
        json.dumps(body, indent=1, sort_keys=True).encode("utf-8")
    ).hexdigest()


def make_cell(prime: int, seed: int, role: str) -> dict:
    cell = {
        "schema": 1,
        "cell": {"prime": prime, "seed": seed, "role": role},
        "method": "exact analytic Jacobian; no finite differences, no tolerance",
        "flop_limit": 1e11,
        "schedule_summary": {
            "planned": 83,
            "by_terminal_status": {"evaluated": 83},
            "evaluation_errors": 0,
            "interrupted": 0,
            "structurally_rejected": 0,
            "complete": True,
            "zero_rows": 0,
        },
        "jacobian": {
            "n_rows": 83,
            "n_columns": 126,
            "total_rank": 81,
            "per_degree_block_rank": {"4": {"candidates": 1, "block_rank": 1}},
            "cumulative_rank_by_degree": {"4": 1, "12": 81},
            "pivot_columns": list(range(81)),
            "pivot_rows": list(range(81)),
            "pivot_row_candidate_ids": [f"c{i:03d}" for i in range(81)],
            "row_normalisation_used": False,
            "note": "",
        },
        "euler_homogeneity": {"checked": 83, "passed": 83, "failed": []},
        "zero_rows": [],
        "zero_row_explanations": {},
        "terminal_records": [],
        "candidate_order_sha256": ORDER_SHA,
        "n_candidates_scheduled": 83,
        "coordinate_dimension": 126,
        "inputs": {
            "selection_list": "selected_graphs.json",
            "selection_sha256": SELECTION_SHA,
            "rowcache": f"rowcache_p{prime}_s{seed}.json",
        },
        "environment": {"python": "3.13.5", "numpy": "2.5.1",
                        "platform": "darwin", "host": "test"},
        "wall_seconds": 1.0,
        "peak_rss_mb": 1.0,
        "generated_utc": "2026-08-01T00:00:00+00:00",
        "cell_complete": True,
    }
    cell["content_sha256"] = content_hash(cell)
    return cell


def write_cell(cells_dir: Path, cell: dict, *, rehash: bool = True) -> Path:
    if rehash:
        cell = dict(cell)
        cell.pop("content_sha256", None)
        cell["content_sha256"] = content_hash(cell)
    p = cells_dir / f"cell_p{cell['cell']['prime']}_s{cell['cell']['seed']}.json"
    p.write_text(json.dumps(cell, indent=1, sort_keys=True), encoding="utf-8")
    return p


@pytest.fixture
def good_matrix(tmp_path: Path) -> Path:
    cells = tmp_path / "cells"
    cells.mkdir()
    for p in FITTING:
        for s in SEEDS:
            write_cell(cells, make_cell(p, s, "fitting"))
    for p in HOLDOUT:
        for s in SEEDS:
            write_cell(cells, make_cell(p, s, "holdout"))
    return cells


def run(cells: Path, tmp_path: Path, *extra: str):
    out = tmp_path / "matrix.json"
    proc = subprocess.run(
        [sys.executable, str(AGGREGATOR), "--cells", str(cells), "--out", str(out), *extra],
        capture_output=True, text=True, check=False,
    )
    report = json.loads(out.read_text()) if out.exists() else {}
    return proc.returncode, proc.stdout + proc.stderr, report


def assert_rejected(cells: Path, tmp_path: Path, fragment: str, *extra: str):
    rc, text, report = run(cells, tmp_path, *extra)
    assert rc != 0, f"aggregator accepted a bad matrix; output was:\n{text}"
    assert report.get("matrix_complete") is False
    joined = " | ".join(report.get("problems", []))
    assert fragment in joined, f"expected {fragment!r} among problems: {joined}"


# --------------------------------------------------------------------------
# the matrix that should pass, so a rejection below means the defect, not the
# fixture
# --------------------------------------------------------------------------
def test_a_clean_matrix_assembles(good_matrix: Path, tmp_path: Path):
    rc, text, report = run(good_matrix, tmp_path)
    assert rc == 0, text
    assert report["matrix_complete"] is True
    assert report["n_present"] == 15
    assert report["summary"]["distinct_total_ranks"] == [81]
    assert report["summary"]["all_cells_agree"] is True


# --------------------------------------------------------------------------
# one broken thing per test
# --------------------------------------------------------------------------
def test_missing_cell_is_rejected(good_matrix: Path, tmp_path: Path):
    (good_matrix / "cell_p32717_s22.json").unlink()
    assert_rejected(good_matrix, tmp_path, "missing cell prime=32717 seed=22")


def test_duplicate_cell_is_rejected(good_matrix: Path, tmp_path: Path):
    # Same (prime, seed) under a second filename the glob also picks up.
    dup = json.loads((good_matrix / "cell_p32749_s11.json").read_text())
    (good_matrix / "cell_p32749_s11_copy.json").write_text(json.dumps(dup, indent=1))
    assert_rejected(good_matrix, tmp_path, "duplicate cell")


def test_incomplete_cell_is_rejected(good_matrix: Path, tmp_path: Path):
    cell = json.loads((good_matrix / "cell_p32719_s33.json").read_text())
    cell["cell_complete"] = False
    write_cell(good_matrix, cell)
    assert_rejected(good_matrix, tmp_path, "not marked complete")


def test_eighty_two_of_eighty_three_is_rejected(good_matrix: Path, tmp_path: Path):
    """The exact failure the 2e10 budget produced."""
    cell = json.loads((good_matrix / "cell_p32749_s22.json").read_text())
    cell["schedule_summary"]["by_terminal_status"] = {"evaluated": 82,
                                                      "evaluation_error": 1}
    cell["schedule_summary"]["evaluation_errors"] = 1
    cell["schedule_summary"]["complete"] = False
    cell["cell_complete"] = False
    cell["jacobian"]["n_rows"] = 82
    cell["euler_homogeneity"] = {"checked": 82, "passed": 82, "failed": []}
    write_cell(good_matrix, cell)
    assert_rejected(good_matrix, tmp_path, "evaluation errors")


def test_changed_flop_budget_is_rejected(good_matrix: Path, tmp_path: Path):
    cell = json.loads((good_matrix / "cell_p32717_s11.json").read_text())
    cell["flop_limit"] = 2e10
    write_cell(good_matrix, cell)
    assert_rejected(good_matrix, tmp_path, "flop budget differs")


def test_changed_candidate_order_is_rejected(good_matrix: Path, tmp_path: Path):
    cell = json.loads((good_matrix / "cell_p32713_s11.json").read_text())
    cell["candidate_order_sha256"] = "c" * 64
    write_cell(good_matrix, cell)
    assert_rejected(good_matrix, tmp_path, "candidate ordering differs")


def test_changed_coordinate_order_is_rejected(good_matrix: Path, tmp_path: Path):
    cell = json.loads((good_matrix / "cell_p32707_s22.json").read_text())
    cell["coordinate_dimension"] = 125
    cell["jacobian"]["n_columns"] = 125
    write_cell(good_matrix, cell)
    assert_rejected(good_matrix, tmp_path, "coordinate dimension differs")


def test_mismatched_sample_hash_is_rejected(good_matrix: Path, tmp_path: Path):
    cell = json.loads((good_matrix / "cell_p32719_s22.json").read_text())
    cell["inputs"]["selection_sha256"] = "d" * 64
    write_cell(good_matrix, cell)
    assert_rejected(good_matrix, tmp_path, "candidate selection list differs")


def test_mismatched_output_hash_is_rejected(good_matrix: Path, tmp_path: Path):
    cell = json.loads((good_matrix / "cell_p32749_s33.json").read_text())
    cell["wall_seconds"] = 999.0          # change the content ...
    write_cell(good_matrix, cell, rehash=False)   # ... but keep the old hash
    assert_rejected(good_matrix, tmp_path, "content hash does not match")


def test_nonzero_error_count_is_rejected(good_matrix: Path, tmp_path: Path):
    cell = json.loads((good_matrix / "cell_p32713_s33.json").read_text())
    cell["schedule_summary"]["evaluation_errors"] = 2
    write_cell(good_matrix, cell)
    assert_rejected(good_matrix, tmp_path, "evaluation errors")


def test_interrupted_cell_is_rejected(good_matrix: Path, tmp_path: Path):
    cell = json.loads((good_matrix / "cell_p32707_s11.json").read_text())
    cell["schedule_summary"]["interrupted"] = 1
    write_cell(good_matrix, cell)
    assert_rejected(good_matrix, tmp_path, "interrupted")


def test_failed_euler_homogeneity_is_rejected(good_matrix: Path, tmp_path: Path):
    cell = json.loads((good_matrix / "cell_p32717_s33.json").read_text())
    cell["euler_homogeneity"] = {"checked": 83, "passed": 82,
                                 "failed": [{"candidate": "c046", "lhs": 1, "rhs": 2}]}
    write_cell(good_matrix, cell)
    assert_rejected(good_matrix, tmp_path, "Euler 82/83")


def test_zero_jacobian_row_is_rejected(good_matrix: Path, tmp_path: Path):
    cell = json.loads((good_matrix / "cell_p32719_s11.json").read_text())
    cell["schedule_summary"]["zero_rows"] = 1
    cell["zero_rows"] = ["c046_portgraph_d12"]
    write_cell(good_matrix, cell)
    assert_rejected(good_matrix, tmp_path, "zero rows")


def test_inconsistent_jacobian_dimensions_are_rejected(good_matrix: Path, tmp_path: Path):
    cell = json.loads((good_matrix / "cell_p32713_s22.json").read_text())
    cell["jacobian"]["n_rows"] = 84
    write_cell(good_matrix, cell)
    assert_rejected(good_matrix, tmp_path, "Jacobian dimensions differ")


def test_unplanned_cell_is_rejected(good_matrix: Path, tmp_path: Path):
    write_cell(good_matrix, make_cell(32693, 44, "fitting"))
    assert_rejected(good_matrix, tmp_path, "is not in the planned matrix")


def test_wrong_role_is_rejected(good_matrix: Path, tmp_path: Path):
    cell = json.loads((good_matrix / "cell_p32713_s11.json").read_text())
    cell["cell"]["role"] = "fitting"
    write_cell(good_matrix, cell)
    assert_rejected(good_matrix, tmp_path, "role fitting != holdout")


# --------------------------------------------------------------------------
# provenance cross-checks
# --------------------------------------------------------------------------
def _freeze_and_provenance(tmp_path: Path, cells: Path, *, source_commit="abc123",
                           budget=1e11):
    freeze = {"execution_id": "test-exec", "jhep_branch_commit": source_commit,
              "flop_budget": budget, "source_tree_hash": "t" * 16,
              "dependency_lock": {"sha256": "d" * 64}, "memory_limit": None}
    rows = []
    for path in sorted(cells.glob("cell_p*_s*.json")):
        c = json.loads(path.read_text())
        rows.append({"prime": c["cell"]["prime"], "seed": c["cell"]["seed"],
                     "role": c["cell"]["role"], "source_commit": source_commit,
                     "result_hash": c.get("content_sha256")})
    prov = {"execution_id": "test-exec", "cells": rows}
    fp = tmp_path / "freeze.json"
    pp = tmp_path / "prov.json"
    fp.write_text(json.dumps(freeze, indent=1))
    pp.write_text(json.dumps(prov, indent=1))
    return fp, pp


def test_provenance_cross_check_passes_when_consistent(good_matrix: Path, tmp_path: Path):
    fp, pp = _freeze_and_provenance(tmp_path, good_matrix)
    rc, text, report = run(good_matrix, tmp_path, "--freeze", str(fp),
                           "--provenance", str(pp))
    assert rc == 0, text
    assert report["matrix_complete"] is True


def test_changed_source_commit_is_rejected(good_matrix: Path, tmp_path: Path):
    fp, pp = _freeze_and_provenance(tmp_path, good_matrix)
    prov = json.loads(pp.read_text())
    prov["cells"][0]["source_commit"] = "deadbeef"
    pp.write_text(json.dumps(prov, indent=1))
    assert_rejected(good_matrix, tmp_path, "is not the frozen one",
                    "--freeze", str(fp), "--provenance", str(pp))


def test_unbound_cell_is_rejected(good_matrix: Path, tmp_path: Path):
    fp, pp = _freeze_and_provenance(tmp_path, good_matrix)
    prov = json.loads(pp.read_text())
    prov["cells"] = prov["cells"][1:]
    pp.write_text(json.dumps(prov, indent=1))
    assert_rejected(good_matrix, tmp_path, "not bound to the frozen execution",
                    "--freeze", str(fp), "--provenance", str(pp))


def test_budget_disagreeing_with_freeze_is_rejected(good_matrix: Path, tmp_path: Path):
    fp, pp = _freeze_and_provenance(tmp_path, good_matrix, budget=2e10)
    assert_rejected(good_matrix, tmp_path, "does not match frozen",
                    "--freeze", str(fp), "--provenance", str(pp))


def test_aggregator_never_repairs(good_matrix: Path, tmp_path: Path):
    """A rejected matrix must leave the cells untouched."""
    before = {p.name: p.read_bytes() for p in good_matrix.glob("*.json")}
    (good_matrix / "cell_p32717_s22.json").unlink()
    before.pop("cell_p32717_s22.json")
    run(good_matrix, tmp_path)
    after = {p.name: p.read_bytes() for p in good_matrix.glob("*.json")}
    assert after == before, "aggregator modified cells while rejecting the matrix"
