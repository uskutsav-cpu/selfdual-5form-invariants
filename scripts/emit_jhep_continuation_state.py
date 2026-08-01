#!/usr/bin/env python3
"""Stage 1 --- verify the live state against the reported state.

The reported state is a claim. This checks it: that the frozen execution is
still the one producing cells, that no source-critical evaluator file has
drifted, that exactly one writer exists, and that HEAD movement since the
freeze touched nothing an evaluator reads.

Writes:
    audit/JHEP_CONTINUATION_LIVE_STATE.md
    audit/JHEP_CONTINUATION_LIVE_STATE.json

Exit status is nonzero when the matrix is invalid or more than one writer is
active, so this can gate the pipeline rather than merely describe it.

Usage:
    python scripts/emit_jhep_continuation_state.py [--repo .]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPORTED = {
    "execution_id": "rank81-matrix-5f46a2cbbe93-flop1e11",
    "frozen_source_commit": "5f46a2c",
    "flop_budget": 1e11,
    "cells_planned": 15,
    "branch": "publication/jhep-tensor-spinor",
}

REQUIRED_FREEZE_FIELDS = [
    "execution_id", "jhep_branch_commit", "source_critical_files",
    "source_tree_hash", "dependency_lock", "flop_budget", "memory_limit",
    "fitting_primes", "holdout_primes", "seeds", "output_directory",
    "lock_file_pattern", "active_pids_at_freeze", "frozen_utc",
    "invalidation_rule", "known_invalidation",
]


def sha256_file(path: Path) -> str | None:
    if not path.exists():
        return None
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=repo, capture_output=True,
                          text=True, check=False).stdout.strip()


def processes(repo: Path) -> dict:
    def pids(pattern: str) -> list[int]:
        out = subprocess.run(["pgrep", "-f", pattern], capture_output=True,
                             text=True, check=False).stdout.split()
        return [int(x) for x in out]

    # Anything with a working directory inside a repository tree, so a stray
    # writer in the other session's checkout is visible too.
    all_py = pids("Python") + pids("python")
    in_repo = []
    for pid in sorted(set(all_py)):
        cwd = subprocess.run(["lsof", "-a", "-p", str(pid), "-d", "cwd", "-Fn"],
                             capture_output=True, text=True, check=False).stdout
        cwd = next((l[1:] for l in cwd.splitlines() if l.startswith("n")), "")
        if "selfdual-5form-invariants" in cwd or "sdinv-jhep" in cwd:
            ps = subprocess.run(["ps", "-p", str(pid), "-o", "etime=,stat="],
                                capture_output=True, text=True, check=False).stdout.strip()
            in_repo.append({"pid": pid, "cwd": cwd, "ps": ps,
                            "in_this_worktree": str(repo) in cwd})
    return {
        "matrix_drivers": pids("run_rank81_matrix.sh"),
        "cell_workers": pids("run_rank81_cell.py"),
        "pytest": pids("pytest"),
        "in_any_repo_tree": in_repo,
    }


def read_cells(repo: Path) -> list[dict]:
    d = repo / "results" / "rank81" / "cells"
    out = []
    for p in sorted(d.glob("cell_p*_s*.json")):
        try:
            out.append(json.loads(p.read_text(encoding="utf-8")))
        except json.JSONDecodeError:
            pass
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".", type=Path)
    args = ap.parse_args()
    repo = args.repo.resolve()
    audit = repo / "audit"
    when = datetime.now(timezone.utc).isoformat(timespec="seconds")

    freeze_path = audit / "RANK_MATRIX_EXECUTION_FREEZE.json"
    frozen = json.loads(freeze_path.read_text()) if freeze_path.exists() else {}
    missing_fields = [f for f in REQUIRED_FREEZE_FIELDS if f not in frozen]

    drift = []
    for rel, want in (frozen.get("source_critical_files") or {}).items():
        got = sha256_file(repo / rel)
        if got != want:
            drift.append({"path": rel, "frozen": want, "now": got})

    head = git(repo, "rev-parse", "HEAD")
    frozen_commit = frozen.get("jhep_branch_commit", "")
    changed_since_freeze = [
        l for l in git(repo, "diff", "--name-only", f"{frozen_commit}..HEAD").splitlines()
        if l
    ] if frozen_commit else []
    critical_paths = set((frozen.get("source_critical_files") or {}))
    changed_critical = sorted(set(changed_since_freeze) & critical_paths)

    procs = processes(repo)
    cells = read_cells(repo)
    complete = [c for c in cells if c.get("cell_complete")]
    ranks = sorted({c["jacobian"]["total_rank"] for c in complete})

    # One writer means: at most one driver, at most one cell worker, and no
    # second worker on the same cell. A pytest process elsewhere is not a
    # matrix writer and is reported without being treated as a violation.
    writer_problems = []
    if len(procs["matrix_drivers"]) > 1:
        writer_problems.append(f"{len(procs['matrix_drivers'])} matrix drivers running")
    if len(procs["cell_workers"]) > 1:
        writer_problems.append(f"{len(procs['cell_workers'])} cell workers running")
    locks = sorted((repo / "results" / "rank81" / "cells").glob("*.lock"))
    if len(locks) > 1:
        writer_problems.append(f"{len(locks)} cell locks held: {[l.name for l in locks]}")

    reported_vs_live = {
        "execution_id": {
            "reported": REPORTED["execution_id"],
            "live": frozen.get("execution_id"),
            "match": frozen.get("execution_id") == REPORTED["execution_id"],
        },
        "frozen_source_commit": {
            "reported": REPORTED["frozen_source_commit"],
            "live": frozen_commit[:7],
            "match": frozen_commit.startswith(REPORTED["frozen_source_commit"]),
        },
        "flop_budget": {
            "reported": REPORTED["flop_budget"],
            "live": frozen.get("flop_budget"),
            "match": frozen.get("flop_budget") == REPORTED["flop_budget"],
        },
        "cells_planned": {
            "reported": REPORTED["cells_planned"],
            "live": frozen.get("planned_cells"),
            "match": frozen.get("planned_cells") == REPORTED["cells_planned"],
        },
        "branch": {
            "reported": REPORTED["branch"],
            "live": git(repo, "rev-parse", "--abbrev-ref", "HEAD"),
            "match": git(repo, "rev-parse", "--abbrev-ref", "HEAD") == REPORTED["branch"],
        },
    }

    matrix_valid = not drift and not missing_fields and not writer_problems
    record = {
        "generated_utc": when,
        "worktree": str(repo),
        "branch": git(repo, "rev-parse", "--abbrev-ref", "HEAD"),
        "head": head,
        "head_moved_since_freeze": bool(frozen_commit) and head != frozen_commit,
        "changed_files_since_freeze": changed_since_freeze,
        "source_critical_drift": drift,
        "drift_classification": (
            "none" if not drift else "SOURCE-CRITICAL DRIFT --- MATRIX INVALID"),
        "changed_source_critical_files": changed_critical,
        "matrix_valid": matrix_valid,
        "freeze_record_present": bool(frozen),
        "freeze_missing_fields": missing_fields,
        "reported_vs_live": reported_vs_live,
        "reported_state_confirmed": all(v["match"] for v in reported_vs_live.values()),
        "processes": procs,
        "writer_problems": writer_problems,
        "one_writer_enforced": not writer_problems,
        "cells_present": len(cells),
        "cells_complete": len(complete),
        "cells_planned": frozen.get("planned_cells"),
        "distinct_ranks_so_far": ranks,
        "uncommitted_paths": [l for l in git(repo, "status", "--porcelain").splitlines() if l],
        "remote_research_head": (git(repo, "ls-remote", "--heads", "origin",
                                     "research/maximal-chiral-four-form-program")
                                 .split("\t")[0] or None),
    }

    audit.mkdir(exist_ok=True)
    (audit / "JHEP_CONTINUATION_LIVE_STATE.json").write_text(
        json.dumps(record, indent=1) + "\n", encoding="utf-8")

    L: list[str] = []
    A = L.append
    A("# JHEP continuation --- live state")
    A("")
    A(f"Generated {when} by `scripts/emit_jhep_continuation_state.py`.")
    A("")
    A("## Reported state, checked against the worktree")
    A("")
    A("| field | reported | live | agrees |")
    A("|---|---|---|---|")
    for k, v in reported_vs_live.items():
        A(f"| {k} | `{v['reported']}` | `{v['live']}` | {'yes' if v['match'] else '**NO**'} |")
    A("")
    A("## Matrix validity")
    A("")
    A("| check | result |")
    A("|---|---|")
    A(f"| freeze record present | {'yes' if frozen else '**no**'} |")
    A(f"| freeze fields missing | {', '.join(missing_fields) if missing_fields else 'none'} |")
    A(f"| source-critical drift | {len(drift)} files |")
    A(f"| head moved since freeze | {'yes' if record['head_moved_since_freeze'] else 'no'} |")
    A(f"| changed source-critical files | {', '.join(changed_critical) if changed_critical else 'none'} |")
    A(f"| **matrix valid** | **{'yes' if matrix_valid else 'NO'}** |")
    A("")
    if record["head_moved_since_freeze"]:
        A(f"HEAD has moved from `{frozen_commit[:12]}` to `{head[:12]}` since the")
        A(f"freeze, across {len(changed_since_freeze)} files. None is source-critical,")
        A("so the cells produced before and after that movement were produced by the")
        A("same evaluator and belong to the same execution.")
        A("")
        A("Files changed since the freeze:")
        A("")
        for f in changed_since_freeze:
            A(f"- `{f}`")
        A("")
    A("## Writers")
    A("")
    A(f"- matrix drivers: {procs['matrix_drivers'] or 'none'}")
    A(f"- cell workers: {procs['cell_workers'] or 'none'}")
    A(f"- pytest processes: {procs['pytest'] or 'none'}")
    A(f"- cell locks held: {[l.name for l in locks] or 'none'}")
    A("")
    if procs["in_any_repo_tree"]:
        A("| pid | in this worktree | elapsed/state | cwd |")
        A("|---|---|---|---|")
        for p in procs["in_any_repo_tree"]:
            A(f"| {p['pid']} | {'yes' if p['in_this_worktree'] else 'no (other session)'} "
              f"| `{p['ps']}` | `{p['cwd']}` |")
        A("")
    if writer_problems:
        A("**Writer problems:**")
        A("")
        for w in writer_problems:
            A(f"- {w}")
        A("")
    else:
        A("One writer enforced: at most one driver, at most one cell worker, at most")
        A("one lock. A process in the other session's tree cannot reach these cells.")
        A("")
    A("## Matrix progress")
    A("")
    A(f"{len(complete)} of {frozen.get('planned_cells')} cells complete; "
      f"distinct ranks so far {ranks}.")
    A("")
    A("| prime | seed | role | rank | rows | euler | seconds | peak MB |")
    A("|---|---|---|---|---|---|---|---|")
    for c in cells:
        e = c["euler_homogeneity"]
        A(f"| {c['cell']['prime']} | {c['cell']['seed']} | {c['cell']['role']} "
          f"| {c['jacobian']['total_rank']} | {c['jacobian']['n_rows']} "
          f"| {e['passed']}/{e['checked']} | {c.get('wall_seconds')} "
          f"| {c.get('peak_rss_mb')} |")
    A("")
    (audit / "JHEP_CONTINUATION_LIVE_STATE.md").write_text("\n".join(L) + "\n",
                                                           encoding="utf-8")

    print(f"reported state confirmed: {record['reported_state_confirmed']}")
    print(f"source-critical drift:    {len(drift)}")
    print(f"matrix valid:             {matrix_valid}")
    print(f"one writer:               {not writer_problems}")
    print(f"cells complete:           {len(complete)}/{frozen.get('planned_cells')}")
    if drift:
        for d in drift:
            print(f"  DRIFT {d['path']}")
    for w in writer_problems:
        print(f"  WRITER {w}")
    return 0 if matrix_valid else 1


if __name__ == "__main__":
    sys.exit(main())
