#!/usr/bin/env python3
"""Compute exactly ONE (prime, seed) cell of the rank-81 certificate matrix.

Why this exists alongside `run_rank81_certificate.py`: that script loops over
every cell and rewrites one shared `certificate.json` after each one. Two
runners against the same file means the last writer wins and finished cells
are silently lost, and an interrupted run leaves a summary that disagrees with
its own runs list. Both happened.

This driver does one cell per invocation and obeys the rules that prevent it:

  * one cell per process, named on the command line
  * a unique immutable output path per cell, `cells/cell_p{p}_s{seed}.json`
  * atomic write: temporary file in the same directory, then os.replace
  * a lock file per cell, so a second writer refuses rather than races
  * refuses to overwrite a cell that is already complete, unless --force
  * records runtime, peak RSS, input hashes and output hash

Assembly is a separate read-only step; see `assemble_rank81_matrix.py`.

Usage:
    python spinor_trace_bridge/scripts/run_rank81_cell.py \
        --archive <archive> --prime 32719 --seed 22 --role fitting
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import resource
import socket
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "spinor_trace_bridge" / "src"))

from sdbridge.candidates import (  # noqa: E402
    RowCache, build_context, evaluate_all, load_schedule, schedule_summary,
)
from sdbridge.modular import rank as modrank, rref  # noqa: E402
import sdbridge.spinor_invariants as si  # noqa: E402


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def analyse(schedule, J, p: int) -> dict:
    """Ranks, degree blocks and an independent pivot row set. Same arithmetic as
    run_rank81_certificate.analyse, kept here so a cell is self-contained."""
    evaluated = [c for c in schedule if c.terminal_status == "evaluated"]
    degrees = sorted({c.degree for c in evaluated})
    per_degree, cumulative = {}, {}
    for d in degrees:
        idx = [i for i, c in enumerate(evaluated) if c.degree == d]
        per_degree[str(d)] = {
            "candidates": len(idx),
            "block_rank": int(modrank(J[idx], p)) if idx else 0,
        }
        upto = [i for i, c in enumerate(evaluated) if c.degree <= d]
        cumulative[str(d)] = int(modrank(J[upto], p)) if upto else 0
    _, pivots = rref(J, p)
    total = int(modrank(J, p))
    pivot_rows, seen = [], np.zeros((0, J.shape[1]), dtype=np.int64)
    for i in range(J.shape[0]):
        trial = np.concatenate([seen, J[i:i + 1]], axis=0)
        if modrank(trial, p) > seen.shape[0]:
            seen = trial
            pivot_rows.append(i)
        if len(pivot_rows) == total:
            break
    return {
        "n_rows": int(J.shape[0]),
        "n_columns": int(J.shape[1]),
        "total_rank": total,
        "per_degree_block_rank": per_degree,
        "cumulative_rank_by_degree": cumulative,
        "pivot_columns": [int(c) for c in pivots],
        "pivot_rows": pivot_rows,
        "pivot_row_candidate_ids": [evaluated[i].candidate_id for i in pivot_rows],
        "row_normalisation_used": False,
        "note": ("No row normalisation is applied. Over F_p a row is zero or it is "
                 "not; normalising would be meaningless here and is the mechanism "
                 "that inflated the float64 rank."),
    }


def peak_rss_mb() -> float:
    # macOS reports ru_maxrss in bytes, Linux in kibibytes.
    raw = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return round(raw / (1024 * 1024) if sys.platform == "darwin" else raw / 1024, 1)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--archive", required=True)
    ap.add_argument("--prime", type=int, required=True)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--role", choices=["fitting", "holdout", "extra"], required=True)
    # 1e11, matching the flop_limit recorded in the certificate this matrix
    # extends. At 2e10 the degree-12 port graph c046 exceeds the budget on its
    # value contraction, the dense-I fallback exceeds it too, and the cell comes
    # back 82/83 with an evaluation error -- a budget artifact that looks exactly
    # like a science failure. Cells must share one budget or their candidate sets
    # differ, so the aggregator checks this too.
    ap.add_argument("--flop-limit", type=float, default=1e11)
    ap.add_argument("--cells", default=str(ROOT / "results" / "rank81" / "cells"))
    ap.add_argument("--rowcache-dir", default=str(ROOT / "results" / "rank81"))
    ap.add_argument("--force", action="store_true",
                    help="recompute a cell that is already complete")
    args = ap.parse_args()

    p, seed = args.prime, args.seed
    cells = Path(args.cells)
    cells.mkdir(parents=True, exist_ok=True)
    out = cells / f"cell_p{p}_s{seed}.json"
    lock = cells / f"cell_p{p}_s{seed}.lock"

    if out.exists() and not args.force:
        try:
            existing = json.loads(out.read_text())
            if existing.get("cell_complete"):
                print(f"[p={p} seed={seed}] already complete, rank "
                      f"{existing['jacobian']['total_rank']}; not recomputing")
                return 0
        except json.JSONDecodeError:
            print(f"[p={p} seed={seed}] existing cell is unreadable, recomputing")

    # Lock, so a second driver refuses instead of interleaving writes.
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        holder = lock.read_text().strip() if lock.exists() else "unknown"
        print(f"[p={p} seed={seed}] LOCKED by {holder}; refusing to run. "
              f"Remove {lock} if that process is gone.", file=sys.stderr)
        return 2
    os.write(fd, f"pid={os.getpid()} host={socket.gethostname()} "
                 f"started={datetime.now(timezone.utc).isoformat()}\n".encode())
    os.close(fd)

    try:
        si.MAX_CONTRACTION_FLOPS = args.flop_limit
        si._modular_contract.__defaults__ = (None, si.MAX_INTERMEDIATE_ELEMENTS,
                                             args.flop_limit)
        selection = (Path(args.archive).expanduser().resolve()
                     / "run_4_12_tensor_words_s96" / "selected_graphs.json")
        if not selection.exists():
            print(f"selection list not found: {selection}", file=sys.stderr)
            return 3

        t0 = time.time()
        schedule = load_schedule(selection)
        ctx = build_context(p, seed=seed)
        cache_path = Path(args.rowcache_dir) / f"rowcache_p{p}_s{seed}.json"
        cache = RowCache(cache_path)
        J, schedule = evaluate_all(schedule, ctx, cache=cache, seed=seed)
        summary = schedule_summary(schedule)
        stats = analyse(schedule, J, p)

        euler = {"checked": 0, "passed": 0, "failed": []}
        evaluated = [c for c in schedule if c.terminal_status == "evaluated"]
        for i, c in enumerate(evaluated):
            lhs = int(ctx.coeffs % p @ J[i] % p)
            rhs = (c.degree * int(c.value)) % p
            euler["checked"] += 1
            if lhs == rhs:
                euler["passed"] += 1
            else:
                euler["failed"].append({"candidate": c.candidate_id,
                                        "lhs": lhs, "rhs": rhs})

        candidate_order = [c.candidate_id for c in schedule]
        cell = {
            "schema": 1,
            "cell": {"prime": p, "seed": seed, "role": args.role},
            "method": "exact analytic Jacobian; no finite differences, no tolerance",
            "flop_limit": args.flop_limit,
            "schedule_summary": summary,
            "jacobian": stats,
            "euler_homogeneity": euler,
            "zero_rows": [c.candidate_id for c in evaluated if c.zero_row],
            "zero_row_explanations": {c.candidate_id: c.zero_row_explanation
                                      for c in evaluated if c.zero_row},
            "terminal_records": [c.record() for c in schedule],
            "candidate_order_sha256": sha256_text("\n".join(candidate_order)),
            "n_candidates_scheduled": len(candidate_order),
            "coordinate_dimension": int(stats["n_columns"]),
            "inputs": {
                "selection_list": str(selection.name),
                "selection_sha256": sha256_file(selection),
                "rowcache": cache_path.name,
            },
            "environment": {
                "python": sys.version.split()[0],
                "numpy": np.__version__,
                "platform": sys.platform,
                "host": socket.gethostname(),
            },
            "wall_seconds": round(time.time() - t0, 1),
            "peak_rss_mb": peak_rss_mb(),
            "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }
        # A cell counts as complete only if the schedule really finished and
        # every homogeneity check passed. Anything less stays on disk labelled
        # incomplete rather than being quietly aggregated later.
        cell["cell_complete"] = bool(
            summary.get("complete")
            and summary.get("evaluation_errors") == 0
            and summary.get("interrupted") == 0
            and not euler["failed"]
        )

        payload = json.dumps(cell, indent=1, sort_keys=True)
        cell["content_sha256"] = sha256_text(payload)
        payload = json.dumps(cell, indent=1, sort_keys=True)

        tmp = out.with_suffix(".json.tmp")
        tmp.write_text(payload, encoding="utf-8")
        os.replace(tmp, out)  # atomic within the directory

        print(f"[p={p} seed={seed}] rank {stats['total_rank']} "
              f"rows {stats['n_rows']} errors {summary['evaluation_errors']} "
              f"euler {euler['passed']}/{euler['checked']} "
              f"zero_rows {len(cell['zero_rows'])} "
              f"complete {cell['cell_complete']} "
              f"({cell['wall_seconds']}s, peak {cell['peak_rss_mb']} MB)")
        return 0 if cell["cell_complete"] else 1
    finally:
        lock.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
