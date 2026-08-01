#!/usr/bin/env python3
"""Freeze the environment the rank-certificate matrix is being computed in.

Written while the matrix is running, on purpose. The point is to pin what the
cells were produced by, so that a later reader can tell whether a cell belongs
to this execution or to some earlier one -- and so that changing the evaluator
mid-run becomes detectable rather than invisible.

Two artifacts:

    audit/RANK_MATRIX_EXECUTION_FREEZE.json   the frozen environment
    audit/RANK_MATRIX_CELL_PROVENANCE.json    written after the run, binding
                                              each cell to that environment

The second is produced by --stamp once every cell exists. It does not modify a
single cell: cells are immutable by design, and rewriting them to add metadata
would both break their content hashes and mix schemas within one execution.
The binding lives beside them instead.

Usage:
    python scripts/emit_rank_matrix_freeze.py [--repo .]
    python scripts/emit_rank_matrix_freeze.py --stamp
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# Everything whose contents can change what a cell means. A change to any of
# these invalidates cells produced before it.
SOURCE_CRITICAL = [
    "spinor_trace_bridge/src/sdbridge/candidates.py",
    "spinor_trace_bridge/src/sdbridge/jacobian.py",
    "spinor_trace_bridge/src/sdbridge/spinor_invariants.py",
    "spinor_trace_bridge/src/sdbridge/modular.py",
    "spinor_trace_bridge/src/sdbridge/conventions.py",
    "spinor_trace_bridge/scripts/run_rank81_cell.py",
    "spinor_trace_bridge/scripts/run_rank81_matrix.sh",
]


def sha256_file(path: Path) -> str | None:
    if not path.exists():
        return None
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=repo, capture_output=True,
                          text=True, check=False).stdout.strip()


def freeze(repo: Path) -> dict:
    head = git(repo, "rev-parse", "HEAD")
    per_file = {p: sha256_file(repo / p) for p in SOURCE_CRITICAL}
    missing = [p for p, h in per_file.items() if h is None]
    source_tree_hash = sha256_text(
        "\n".join(f"{p}:{per_file[p]}" for p in sorted(per_file) if per_file[p])
    )
    lock = repo / "requirements-lock.txt"
    pids = {
        "matrix_driver": subprocess.run(["pgrep", "-f", "run_rank81_matrix.sh"],
                                        capture_output=True, text=True,
                                        check=False).stdout.split(),
        "cell_worker": subprocess.run(["pgrep", "-f", "run_rank81_cell.py"],
                                      capture_output=True, text=True,
                                      check=False).stdout.split(),
    }
    return {
        "execution_id": "rank81-matrix-" + head[:12] + "-flop1e11",
        "frozen_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "jhep_branch": git(repo, "rev-parse", "--abbrev-ref", "HEAD"),
        "jhep_branch_commit": head,
        "matrix_driver_commit": head,
        "git_tree_object": git(repo, "rev-parse", "HEAD^{tree}"),
        "remote_research_branch_commit_at_start": git(
            repo, "ls-remote", "--heads", "origin",
            "research/maximal-chiral-four-form-program").split("\t")[0] or None,
        "source_critical_files": per_file,
        "source_critical_missing": missing,
        "source_tree_hash": source_tree_hash,
        "dependency_lock": {
            "path": "requirements-lock.txt",
            "sha256": sha256_file(lock),
            "contents": lock.read_text(encoding="utf-8").split() if lock.exists() else [],
        },
        "flop_budget": 1e11,
        "memory_limit": None,
        "memory_limit_note": (
            "No hard limit is imposed. The control is sequencing, not a cap: one "
            "cell per process, so peak RSS is one cell's, recorded per cell. "
            "Measured peaks so far are in the 200-600 MB range on an 8 GiB machine."),
        "fitting_primes": [32749, 32719, 32717],
        "holdout_primes": [32713, 32707],
        "seeds": [11, 22, 33],
        "planned_cells": 15,
        "output_directory": "results/rank81/cells",
        "lock_file_pattern": "results/rank81/cells/cell_p{prime}_s{seed}.lock",
        "cell_file_pattern": "results/rank81/cells/cell_p{prime}_s{seed}.json",
        "active_pids_at_freeze": pids,
        "invalidation_rule": (
            "Any change to a source_critical file invalidates every cell produced "
            "before it. The remedy is to stop the matrix, delete the affected "
            "cells explicitly, and restart them under a NEW execution_id. "
            "Pre-fix and post-fix cells are never mixed."),
        "known_invalidation": {
            "superseded_execution": "rank81-matrix-flop2e10",
            "reason": (
                "The first execution ran at a 2e10 contraction budget, where "
                "c046_portgraph_d12 exceeds the budget on its value contraction and "
                "on its dense-I fallback, yielding 82/83 with one evaluation error. "
                "The committed certificate this matrix extends was computed at 1e11. "
                "All cells from that execution were deleted, not reused."),
            "cells_discarded": ["cell_p32749_s11.json", "cell_p32749_s22.json"],
        },
    }


def stamp(repo: Path) -> int:
    """Bind every produced cell to the frozen environment. Reads only."""
    audit = repo / "audit"
    frozen = json.loads((audit / "RANK_MATRIX_EXECUTION_FREEZE.json").read_text())
    cells_dir = repo / "results" / "rank81" / "cells"
    rows, problems = [], []

    # Re-verify the evaluator surface rather than asserting it from the freeze
    # record. Binding a cell to a commit is circular if the binding is just the
    # commit copied across; what makes it evidence is that the files still hash
    # to what they hashed to when the matrix started. HEAD is allowed to move
    # for commits that touch nothing source-critical, and it did.
    drifted = []
    for rel, want in frozen["source_critical_files"].items():
        if want is None:
            continue
        got = sha256_file(repo / rel)
        if got != want:
            drifted.append({"path": rel, "frozen": want, "now": got})
    if drifted:
        problems.append(
            "source-critical files changed since the freeze, so these cells span "
            "more than one evaluator: " + ", ".join(d["path"] for d in drifted))
    for path in sorted(cells_dir.glob("cell_p*_s*.json")):
        cell = json.loads(path.read_text(encoding="utf-8"))
        budget_ok = cell.get("flop_limit") == frozen["flop_budget"]
        if not budget_ok:
            problems.append(f"{path.name}: flop budget {cell.get('flop_limit')} "
                            f"!= frozen {frozen['flop_budget']}")
        rows.append({
            "file": path.name,
            "prime": cell["cell"]["prime"],
            "seed": cell["cell"]["seed"],
            "role": cell["cell"]["role"],
            "execution_id": frozen["execution_id"],
            "source_commit": frozen["jhep_branch_commit"],
            "source_tree_hash": frozen["source_tree_hash"],
            "dependency_hash": frozen["dependency_lock"]["sha256"],
            "flop_budget": cell.get("flop_limit"),
            "memory_limit": frozen["memory_limit"],
            "candidate_order_hash": cell.get("candidate_order_sha256"),
            "coordinate_dimension": cell.get("coordinate_dimension"),
            "sample_hash": cell.get("inputs", {}).get("selection_sha256"),
            "result_hash": cell.get("content_sha256"),
            "terminal_status": "complete" if cell.get("cell_complete") else "incomplete",
            "budget_matches_freeze": budget_ok,
        })
    orders = {r["candidate_order_hash"] for r in rows}
    dims = {r["coordinate_dimension"] for r in rows}
    if len(orders) > 1:
        problems.append(f"candidate order differs across cells: {sorted(orders)}")
    if len(dims) > 1:
        problems.append(f"coordinate dimension differs across cells: {sorted(dims)}")
    out = {
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "execution_id": frozen["execution_id"],
        "n_cells": len(rows),
        "cells": rows,
        "problems": problems,
        "source_critical_reverified": not drifted,
        "source_critical_drift": drifted,
        "head_at_stamp_time": git(repo, "rev-parse", "HEAD"),
        "head_moved_since_freeze": git(repo, "rev-parse", "HEAD") != frozen[
            "jhep_branch_commit"],
        "head_move_is_benign": not drifted,
        "all_cells_bound_to_freeze": not problems,
        "note": ("Cells are immutable and were not rewritten to carry this "
                 "metadata; rewriting them would break their content hashes and "
                 "mix schemas inside one execution. The binding is recorded here "
                 "instead, and the aggregator checks it."),
    }
    (audit / "RANK_MATRIX_CELL_PROVENANCE.json").write_text(
        json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(f"bound {len(rows)} cells to {frozen['execution_id']}")
    for p in problems:
        print(f"  PROBLEM {p}")
    return 1 if problems else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".", type=Path)
    ap.add_argument("--stamp", action="store_true")
    args = ap.parse_args()
    repo = args.repo.resolve()
    (repo / "audit").mkdir(exist_ok=True)
    if args.stamp:
        return stamp(repo)
    record = freeze(repo)
    (repo / "audit" / "RANK_MATRIX_EXECUTION_FREEZE.json").write_text(
        json.dumps(record, indent=1) + "\n", encoding="utf-8")
    print(f"execution_id      {record['execution_id']}")
    print(f"source tree hash  {record['source_tree_hash'][:16]}")
    print(f"jhep commit       {record['jhep_branch_commit'][:12]}")
    print(f"remote at start   {(record['remote_research_branch_commit_at_start'] or '')[:12]}")
    print(f"flop budget       {record['flop_budget']:.0e}")
    if record["source_critical_missing"]:
        print("MISSING source-critical files: " + ", ".join(record["source_critical_missing"]))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
