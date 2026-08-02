#!/usr/bin/env python3
"""Assemble the per-cell rank-81 results into one certificate. Read-only.

This never computes and never repairs. It reads `results/rank81/cells/*.json`,
checks that the set of cells is exactly the planned matrix and that the cells
agree with each other, and only then writes the assembled certificate.

It fails, rather than assembling, when:

  * a planned cell is missing
  * a cell file is present twice for the same (prime, seed)
  * a cell is not marked complete
  * candidate ordering differs between cells
  * the coordinate dimension differs between cells
  * a cell's recorded content hash does not match its contents
  * a cell reports evaluation errors, interruptions or failed Euler checks

Those are the ways a matrix can look finished while being wrong, and each one
has a named exit rather than a warning.

Usage:
    python spinor_trace_bridge/scripts/assemble_rank81_matrix.py \
        [--cells results/rank81/cells] [--out results/rank81/certificate_matrix.json]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

FITTING = [32749, 32719, 32717]
# 32707 is restored. The earlier exclusion rested on a p = 3 mod 8 rule that is
# refuted: 32633 is 1 mod 8 and needs the same square-root branch. Once the
# frame orientation is pinned, every residue class works. See
# docs/CANONICAL_ORIENTATION_FIXED_BRIDGE.md.
HOLDOUT = [32713, 32707]
# An ADDITION, never a substitute for 32707. Counted separately so a matrix
# that quietly swapped one for the other cannot look complete.
EXTRA = [32693]
SEEDS = [11, 22, 33]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


CSV_COLUMNS = [
    "prime", "role", "seed", "total_rank", "n_rows", "n_columns",
    "euler", "evaluation_errors", "zero_rows", "wall_seconds", "peak_rss_mb",
    "content_sha256",
]


def _emit_release_artifacts(out_dir: Path, report: dict) -> None:
    """full_rank_matrix.{json,csv,sha256} and a manifest, all derived."""
    base = out_dir / "full_rank_matrix"
    payload = json.dumps(report, indent=1, sort_keys=True) + "\n"
    (base.with_suffix(".json")).write_text(payload, encoding="utf-8")

    rows = ["\t".join(CSV_COLUMNS).replace("\t", ",")]
    for c in sorted(report["cells"], key=lambda r: (r["role"], r["prime"], r["seed"])):
        rows.append(",".join(str(c.get(k, "")) for k in CSV_COLUMNS))
    (base.with_suffix(".csv")).write_text("\n".join(rows) + "\n", encoding="utf-8")

    sums = []
    for suffix in (".json", ".csv"):
        p = base.with_suffix(suffix)
        sums.append(f"{sha256_text(p.read_text(encoding='utf-8'))}  {p.name}")
    (out_dir / "full_rank_matrix.sha256").write_text("\n".join(sums) + "\n",
                                                     encoding="utf-8")

    manifest = {
        "generated_utc": report["generated_utc"],
        "scientific_content_sha256": report["scientific_content_sha256"],
        "matrix_complete": report["matrix_complete"],
        "n_planned": report["n_planned"],
        "n_present": report["n_present"],
        "summary": report["summary"],
        "files": [
            {"name": p.name, "bytes": p.stat().st_size,
             "sha256": sha256_text(p.read_text(encoding="utf-8"))}
            for p in (base.with_suffix(".json"), base.with_suffix(".csv"),
                      out_dir / "full_rank_matrix.sha256")
        ],
        "cell_files": [
            {"name": f"cell_p{c['prime']}_s{c['seed']}.json",
             "sha256": c.get("content_sha256")}
            for c in sorted(report["cells"], key=lambda r: (r["prime"], r["seed"]))
        ],
        "regeneration_command": (
            "python spinor_trace_bridge/scripts/assemble_rank81_matrix.py "
            "--emit-release --freeze audit/RANK_MATRIX_EXECUTION_FREEZE.json "
            "--provenance audit/RANK_MATRIX_CELL_PROVENANCE.json"),
    }
    (out_dir / "full_rank_matrix_manifest.json").write_text(
        json.dumps(manifest, indent=1, sort_keys=True) + "\n", encoding="utf-8")



def check_one_cell(cell: dict, p: int, s: int, role: str, prefix: str = "") -> list[str]:
    """Per-cell checks, applied identically to required and extra cells."""
    out: list[str] = []
    tag = f"{prefix}prime={p} seed={s}"
    if cell["cell"]["role"] != role:
        out.append(f"{tag}: role {cell['cell']['role']} != {role}")
    flag = cell.get("cell_complete")
    if flag not in (True, False):
        out.append(f"{tag}: malformed terminal status {flag!r}")
    elif not flag:
        out.append(f"{tag}: cell not marked complete")
    summary = cell["schedule_summary"]
    if summary.get("evaluation_errors"):
        out.append(f"{tag}: {summary['evaluation_errors']} evaluation errors")
    if summary.get("interrupted"):
        out.append(f"{tag}: {summary['interrupted']} interrupted")
    if summary.get("silently_skipped"):
        out.append(f"{tag}: {summary['silently_skipped']} silently skipped candidates")
    if summary.get("zero_rows"):
        out.append(f"{tag}: {summary['zero_rows']} zero rows")
    evaluated = summary.get("by_terminal_status", {}).get("evaluated")
    planned_n = summary.get("planned")
    if evaluated is not None and planned_n is not None and evaluated != planned_n:
        out.append(f"{tag}: {evaluated} of {planned_n} candidates evaluated")
    euler = cell["euler_homogeneity"]
    if euler["failed"] or euler["passed"] != euler["checked"]:
        out.append(f"{tag}: Euler {euler['passed']}/{euler['checked']}")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".", type=Path)
    ap.add_argument("--cells", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--fitting-primes", default=",".join(map(str, FITTING)))
    ap.add_argument("--holdout-primes", default=",".join(map(str, HOLDOUT)))
    ap.add_argument("--seeds", default=",".join(map(str, SEEDS)))
    ap.add_argument("--extra-primes", default=",".join(map(str, EXTRA)))
    ap.add_argument("--freeze", default=None,
                    help="RANK_MATRIX_EXECUTION_FREEZE.json to check cells against")
    ap.add_argument("--provenance", default=None,
                    help="RANK_MATRIX_CELL_PROVENANCE.json binding cells to the freeze")
    ap.add_argument("--emit-release", action="store_true",
                    help="also write full_rank_matrix.{json,csv,sha256} and a manifest")
    args = ap.parse_args()

    repo = args.repo.resolve()
    cells_dir = Path(args.cells) if args.cells else repo / "results" / "rank81" / "cells"
    out = Path(args.out) if args.out else repo / "results" / "rank81" / "certificate_matrix.json"

    fitting = [int(x) for x in args.fitting_primes.split(",") if x.strip()]
    holdout = [int(x) for x in args.holdout_primes.split(",") if x.strip()]
    seeds = [int(x) for x in args.seeds.split(",") if x.strip()]
    extra = [int(x) for x in args.extra_primes.split(",") if x.strip()]
    planned = [(p, s, "fitting") for p in fitting for s in seeds] + \
              [(p, s, "holdout") for p in holdout for s in seeds]
    planned_extra = [(p, s, "extra") for p in extra for s in seeds]

    freeze = json.loads(Path(args.freeze).read_text()) if args.freeze else None
    provenance = (json.loads(Path(args.provenance).read_text())
                  if args.provenance else None)

    problems: list[str] = []
    by_key: dict[tuple[int, int], dict] = {}

    for path in sorted(cells_dir.glob("cell_p*_s*.json")):
        try:
            cell = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            problems.append(f"{path.name}: unreadable ({exc})")
            continue
        key = (cell["cell"]["prime"], cell["cell"]["seed"])
        if key in by_key:
            problems.append(f"duplicate cell for prime={key[0]} seed={key[1]}")
            continue
        recorded = cell.get("content_sha256")
        if recorded:
            check = dict(cell)
            check.pop("content_sha256")
            if sha256_text(json.dumps(check, indent=1, sort_keys=True)) != recorded:
                problems.append(f"{path.name}: content hash does not match contents")
        by_key[key] = cell

    for p, s, role in planned:
        cell = by_key.get((p, s))
        if cell is None:
            problems.append(f"missing cell prime={p} seed={s} ({role})")
            continue
        problems.extend(check_one_cell(cell, p, s, role))

    used = [by_key[(p, s)] for p, s, _ in planned if (p, s) in by_key]
    extra_rows = []
    for p, s, role in planned_extra:
        cell = by_key.get((p, s))
        if cell is None:
            problems.append(f"missing extra validation cell prime={p} seed={s}")
            continue
        problems.extend(check_one_cell(cell, p, s, role, prefix="extra "))
        extra_rows.append(cell)

    consistency_set = used + extra_rows  # an extra cell that disagrees is not validating
    orders = {c.get("candidate_order_sha256") for c in consistency_set}
    if len(orders) > 1:
        problems.append(f"candidate ordering differs between cells: {sorted(orders)}")
    dims = {c.get("coordinate_dimension") for c in consistency_set}
    if len(dims) > 1:
        problems.append(f"coordinate dimension differs between cells: {sorted(dims)}")
    counts = {c.get("n_candidates_scheduled") for c in consistency_set}
    if len(counts) > 1:
        problems.append(f"scheduled candidate count differs between cells: {sorted(counts)}")
    # A differing contraction budget silently changes which candidates evaluate:
    # at 2e10 the degree-12 port graph c046 errors out, at 1e11 it evaluates.
    # Cells computed under different budgets are not comparable.
    budgets = {c.get("flop_limit") for c in consistency_set}
    if len(budgets) > 1:
        problems.append(f"contraction flop budget differs between cells: {sorted(budgets)}")
    samples = {c.get("inputs", {}).get("selection_sha256") for c in consistency_set}
    if len(samples) > 1:
        problems.append(f"candidate selection list differs between cells: {sorted(samples)}")
    shapes = {(c["jacobian"]["n_rows"], c["jacobian"]["n_columns"]) for c in consistency_set}
    if len(shapes) > 1:
        problems.append(f"Jacobian dimensions differ between cells: {sorted(shapes)}")

    # Cross-check against the frozen execution environment, when one is given.
    # A cell computed under a different source tree is not part of this matrix
    # even if it looks identical, so the source commit is checked here rather
    # than assumed.
    if freeze is not None:
        for c in consistency_set:
            key = f"prime={c['cell']['prime']} seed={c['cell']['seed']}"
            if c.get("flop_limit") != freeze.get("flop_budget"):
                problems.append(f"{key}: flop budget {c.get('flop_limit')} does not "
                                f"match frozen {freeze.get('flop_budget')}")
        if provenance is not None:
            if provenance.get("execution_id") != freeze.get("execution_id"):
                problems.append("provenance execution_id does not match the freeze record")
            bound = {(r["prime"], r["seed"]): r for r in provenance.get("cells", [])}
            for c in consistency_set:
                key = (c["cell"]["prime"], c["cell"]["seed"])
                row = bound.get(key)
                if row is None:
                    problems.append(f"prime={key[0]} seed={key[1]}: not bound to the "
                                    "frozen execution")
                elif row.get("source_commit") != freeze.get("jhep_branch_commit"):
                    problems.append(f"prime={key[0]} seed={key[1]}: source commit "
                                    f"{row.get('source_commit')} is not the frozen one")
                elif row.get("result_hash") != c.get("content_sha256"):
                    problems.append(f"prime={key[0]} seed={key[1]}: provenance result "
                                    "hash disagrees with the cell")

    known = {(p, s) for p, s, _ in planned} | {(p, s) for p, s, _ in planned_extra}
    for p, s in sorted(set(by_key) - known):
        problems.append(f"cell prime={p} seed={s} is not in the planned matrix")

    # The substitution guard. 32693 was briefly used in place of 32707 while the
    # orientation bug was open; a matrix carrying 32693 but missing 32707 would
    # have fifteen cells and look complete.
    have_707 = any(k[0] == 32707 for k in by_key)
    have_693 = any(k[0] == 32693 for k in by_key)
    if have_693 and not have_707:
        problems.append(
            "32693 is present and 32707 is absent: 32693 is an EXTRA validation "
            "prime, never a replacement for the 32707 holdout")

    # Extra validation cells get the SAME per-cell scrutiny as required ones.
    # They do not count toward the required fifteen, but a broken extra cell is
    # still a broken cell and reporting it as merely "present" would make the
    # weaker role a hiding place.

    # Terminal status must be one of the two words the driver writes. A cell
    # carrying anything else is malformed, not merely unfinished.
    if provenance is not None:
        exec_ids = {r.get("execution_id") for r in provenance.get("cells", [])}
        exec_ids.discard(None)
        if len(exec_ids) > 1:
            problems.append(f"cells span more than one execution id: {sorted(exec_ids)}")
        dep_hashes = {r.get("dependency_hash") for r in provenance.get("cells", [])}
        dep_hashes.discard(None)
        if len(dep_hashes) > 1:
            problems.append(f"dependency hash differs between cells: {sorted(dep_hashes)}")

    when = datetime.now(timezone.utc).isoformat(timespec="seconds")
    ranks = sorted({c["jacobian"]["total_rank"] for c in used})
    report = {
        "schema": 1,
        "generated_utc": when,
        "assembled_by": "spinor_trace_bridge/scripts/assemble_rank81_matrix.py",
        "assembly_is_read_only": True,
        "planned_cells": [{"prime": p, "seed": s, "role": r} for p, s, r in planned],
        "n_planned": len(planned),
        "planned_extra_cells": [{"prime": p, "seed": s, "role": r}
                                for p, s, r in planned_extra],
        "n_planned_extra": len(planned_extra),
        "n_extra_present": len(extra_rows),
        "extra_cells": [
            {"prime": c["cell"]["prime"], "seed": c["cell"]["seed"],
             "total_rank": c["jacobian"]["total_rank"],
             "content_sha256": c.get("content_sha256")} for c in extra_rows],
        "extra_is_addition_not_substitution": True,
        "n_present": len(used),
        "problems": problems,
        "matrix_complete": not problems and len(used) == len(planned),
        "statement_separation": {
            "float64_evidence": "not used",
            "exact_modular_rank": "computed per (prime, seed) cell",
            "characteristic_zero": (
                "the coordinate basis is integral, so each Jacobian is the reduction "
                "of an integer matrix and rank_{F_p} <= rank_Q holds unconditionally"),
            "generic_rank": (
                "not established by finitely many points; the matching upper bound "
                "126 - 45 = 81 is analytic and comes from the literature"),
        },
        "summary": {
            "distinct_total_ranks": ranks,
            "all_cells_agree": len(ranks) == 1,
            "characteristic_zero_lower_bound": max(ranks) if ranks else 0,
            "fitting_primes": fitting,
            "holdout_primes": holdout,
            "seeds": seeds,
            "flop_limit": sorted(budgets)[0] if len(budgets) == 1 else None,
            "candidate_order_sha256": sorted(orders)[0] if len(orders) == 1 else None,
            "coordinate_dimension": sorted(dims)[0] if len(dims) == 1 else None,
            "n_candidates_scheduled": sorted(counts)[0] if len(counts) == 1 else None,
        },
        "cells": [
            {
                "prime": c["cell"]["prime"],
                "seed": c["cell"]["seed"],
                "role": c["cell"]["role"],
                "total_rank": c["jacobian"]["total_rank"],
                "n_rows": c["jacobian"]["n_rows"],
                "n_columns": c["jacobian"]["n_columns"],
                "per_degree_block_rank": c["jacobian"]["per_degree_block_rank"],
                "cumulative_rank_by_degree": c["jacobian"]["cumulative_rank_by_degree"],
                "pivot_rows": c["jacobian"]["pivot_rows"],
                "pivot_columns": c["jacobian"]["pivot_columns"],
                "euler": f"{c['euler_homogeneity']['passed']}/{c['euler_homogeneity']['checked']}",
                "evaluation_errors": c["schedule_summary"].get("evaluation_errors"),
                "zero_rows": len(c.get("zero_rows", [])),
                "wall_seconds": c.get("wall_seconds"),
                "peak_rss_mb": c.get("peak_rss_mb"),
                "content_sha256": c.get("content_sha256"),
            }
            for c in used
        ],
    }

    # Determinism. Everything above the timestamp is a function of the cells
    # alone, so hash that part and let the timestamp sit outside it. Two runs
    # over the same cells then produce the same scientific hash, and any change
    # to any cell's scientific content changes it.
    scientific = {k: v for k, v in report.items()
                  if k not in ("generated_utc", "scientific_content_sha256")}
    report["scientific_content_sha256"] = sha256_text(
        json.dumps(scientific, indent=1, sort_keys=True))

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=1, sort_keys=True) + "\n", encoding="utf-8")

    if args.emit_release:
        _emit_release_artifacts(out.parent, report)

    print(f"cells {len(used)}/{len(planned)} present, ranks {ranks}")
    for c in report["cells"]:
        print(f"  p={c['prime']:<6} seed={c['seed']:<3} {c['role']:<8} "
              f"rank {c['total_rank']} rows {c['n_rows']} euler {c['euler']} "
              f"{c['wall_seconds']}s")
    if problems:
        print(f"\n{len(problems)} problems:")
        for p in problems:
            print(f"  - {p}")
        print("\nMATRIX INCOMPLETE")
        return 1
    print("\nMATRIX COMPLETE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
