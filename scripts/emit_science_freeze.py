#!/usr/bin/env python3
"""Phase 8 --- record the science freeze, and refuse to record a false one.

Writes the provenance chain connecting the matrix-generation commit to the
freeze commit, and checks the preconditions rather than assuming them. If the
science entry gate is not PASS, or a suite is incomplete, or the matrix is not
assembled, this says so and exits nonzero instead of writing a freeze record
that reads like a result.

Writes:
    results/jhep/science_freeze.json
    docs/JHEP_SCIENCE_FREEZE.md

Usage:
    python scripts/emit_science_freeze.py [--repo .]
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=repo, capture_output=True,
                          text=True, check=False).stdout.strip()


def load(repo: Path, rel: str):
    p = repo / rel
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".", type=Path)
    args = ap.parse_args()
    repo = args.repo.resolve()
    when = datetime.now(timezone.utc).isoformat(timespec="seconds")

    gate = load(repo, "results/jhep/science_entry_gate.json")
    matrix = load(repo, "results/rank81/certificate_matrix.json")
    freeze = load(repo, "audit/RANK_MATRIX_EXECUTION_FREEZE.json")
    prov = load(repo, "audit/RANK_MATRIX_CELL_PROVENANCE.json")
    tests = load(repo, "results/tests/final_test_manifest.json")
    d10 = load(repo, "results/stress_flow/D10_exact_rational_final.json")
    q10 = load(repo, "results/stress_flow/Q10_exact_rational_final.json")
    equiv = load(repo, "results/rank81/evaluator_equivalence.json")

    blockers = []
    if not gate or gate.get("verdict") != "PASS":
        blockers.append(f"science entry gate is {gate.get('verdict') if gate else 'absent'}")
    if not matrix or not matrix.get("matrix_complete"):
        blockers.append("rank matrix is not assembled complete")
    if not prov or prov.get("problems"):
        blockers.append(f"cell provenance has problems: {prov.get('problems') if prov else 'absent'}")
    if not tests or not tests.get("all_suites_clean"):
        incomplete = [s["suite"] for s in (tests or {}).get("suites", [])
                      if s.get("status") in ("INCOMPLETE", "NOT RUN", "NOT CLEAN")]
        blockers.append(f"test suites not all clean: {incomplete or 'absent'}")
    if not d10 or d10.get("status") != "PROVED":
        blockers.append("exact rational D10 is not PROVED")
    if not q10 or q10.get("status") != "PROVED":
        blockers.append("exact rational Q10 is not PROVED")
    if not equiv or not equiv.get("equivalence_established"):
        blockers.append("evaluator equivalence is not established")

    record = {
        "generated_utc": when,
        "science_generation_commit": git(repo, "rev-parse", "HEAD"),
        "matrix_generation_commit": (freeze or {}).get("jhep_branch_commit"),
        "matrix_execution_id": (freeze or {}).get("execution_id"),
        "matrix_source_tree_hash": (freeze or {}).get("source_tree_hash"),
        "matrix_artifact_hash": (matrix or {}).get("scientific_content_sha256"),
        "branch": git(repo, "rev-parse", "--abbrev-ref", "HEAD"),
        "science_entry_gate": (gate or {}).get("verdict"),
        "cells": f"{(matrix or {}).get('n_present')}/{(matrix or {}).get('n_planned')}",
        "distinct_ranks": (matrix or {}).get("summary", {}).get("distinct_total_ranks"),
        "tests": {s["suite"]: {"status": s.get("status"), "passed": s.get("passed")}
                  for s in (tests or {}).get("suites", [])},
        "exact_D10": (d10 or {}).get("rank"),
        "exact_Q10": (q10 or {}).get("Q10", {}).get("dimension"),
        "evaluator_equivalence": (equiv or {}).get("equivalence_established"),
        "remote_head_at_freeze": (git(repo, "ls-remote", "--heads", "origin",
                                      "research/maximal-chiral-four-form-program")
                                  .split("\t")[0] or None),
        "blockers": blockers,
        "freeze_valid": not blockers,
        "not_included": [
            "public push -- held; the branch carries a manuscript naming a "
            "third party as corresponding author on verbal report only",
            "submission tag -- the goal forbids it while approvals are open",
            "arXiv or JHEP submission -- never automatic",
        ],
    }

    (repo / "results" / "jhep").mkdir(parents=True, exist_ok=True)
    (repo / "results" / "jhep" / "science_freeze.json").write_text(
        json.dumps(record, indent=1) + "\n", encoding="utf-8")

    L = ["# Science freeze", "", f"Generated {when}.", ""]
    if blockers:
        L += ["## NOT FROZEN", "",
              "The preconditions are not met, so this is a status note rather",
              "than a freeze:", ""]
        L += [f"- {b}" for b in blockers]
        L.append("")
    else:
        L += ["## Frozen", "", "All preconditions met.", ""]
    L += ["## Provenance chain", "", "| field | value |", "|---|---|",
          f"| matrix execution id | `{record['matrix_execution_id']}` |",
          f"| matrix generation commit | `{(record['matrix_generation_commit'] or '')[:12]}` |",
          f"| matrix source tree hash | `{(record['matrix_source_tree_hash'] or '')[:24]}` |",
          f"| matrix artifact hash | `{(record['matrix_artifact_hash'] or '')[:24]}` |",
          f"| science generation commit | `{record['science_generation_commit'][:12]}` |",
          f"| branch | `{record['branch']}` |",
          f"| remote head at freeze | `{(record['remote_head_at_freeze'] or '')[:12]}` |",
          "", "## Results frozen", "", "| item | value |", "|---|---|",
          f"| science entry gate | **{record['science_entry_gate']}** |",
          f"| matrix cells | {record['cells']} |",
          f"| distinct ranks | {record['distinct_ranks']} |",
          f"| exact dim_Q D10 | {record['exact_D10']} |",
          f"| exact dim_Q Q10 | {record['exact_Q10']} |",
          f"| evaluator equivalence | {record['evaluator_equivalence']} |"]
    for suite, info in record["tests"].items():
        L.append(f"| {suite} tests | {info['status']}, {info['passed']} passed |")
    L += ["", "## Deliberately not included", ""]
    L += [f"- {x}" for x in record["not_included"]]
    L.append("")
    (repo / "docs" / "JHEP_SCIENCE_FREEZE.md").write_text("\n".join(L) + "\n",
                                                          encoding="utf-8")

    print(f"gate {record['science_entry_gate']}, cells {record['cells']}, "
          f"D10 {record['exact_D10']}, Q10 {record['exact_Q10']}")
    for b in blockers:
        print(f"  BLOCKER {b}")
    print("FREEZE VALID" if not blockers else "NOT FROZEN")
    return 0 if not blockers else 1


if __name__ == "__main__":
    sys.exit(main())
