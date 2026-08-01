"""Controlled float64 Jacobian experiment matrix, using the ARCHIVE's own method.

This is deliberately not the exact modular computation.  Its purpose is to
characterise the float64 finite-difference procedure the archive actually used,
across seeds, scales and step sizes, so the paper can show *why* two archived
runs reported 35 and 81 and what distinguishes a degenerate sample from a
generic one.

The archive is third-party code and is not redistributed.  Point
`--archive` at a local copy; the manifest and hashes are in
`release_candidate/spinor-archive/`.

Rule enforced throughout: a row whose norm is at or below the declared noise
floor is NEVER normalised.  Normalising such a row rescales pure rounding noise
into a unit vector and manufactures rank out of nothing -- which is exactly what
produced the spurious 83 in the degenerate archived run.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import resource
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]

#: A row is treated as numerically zero when its norm is at or below this
#: multiple of the largest row norm in the same Jacobian.
NOISE_FLOOR_RELATIVE = 1e-12


def peak_rss_mb() -> float:
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r / (1024 * 1024) if sys.platform == "darwin" else r / 1024


def classify(diag: dict) -> str:
    if diag["n_zero_rows"] > 0:
        return "degenerate sample"
    if diag["rank_is_tolerance_stable"] and diag["gap_at_target"] is not None \
            and diag["gap_at_target"] > 1e3:
        return "nondegenerate generic"
    if not diag["rank_is_tolerance_stable"]:
        return "numerically inconclusive"
    return "numerically inconclusive"


def analyse(J: np.ndarray, target: int = 81) -> dict:
    row_norms = np.linalg.norm(J, axis=1)
    max_norm = float(row_norms.max()) if row_norms.size else 0.0
    floor = NOISE_FLOOR_RELATIVE * max_norm
    zero_rows = int((row_norms <= floor).sum())

    s_raw = np.linalg.svd(J, compute_uv=False)

    # Row normalisation is legitimate ONLY when no row sits at the noise floor.
    if zero_rows == 0:
        Jn = J / row_norms[:, None]
        s_norm = np.linalg.svd(Jn, compute_uv=False)
    else:
        s_norm = None

    s_use = s_norm if s_norm is not None else s_raw
    sweep = {}
    for rtol in (1e-6, 1e-7, 1e-8, 1e-9, 1e-10, 1e-11, 1e-12):
        tol = rtol * max(J.shape) * float(s_use[0])
        sweep[f"{rtol:g}"] = int((s_use > tol).sum())
    ranks = sorted(set(sweep.values()))

    gap = None
    if s_use.size > target:
        num, den = float(s_use[target - 1]), float(s_use[target])
        gap = num / den if den > 0 else float("inf")

    return {
        "shape": list(J.shape),
        "row_norm_min": float(row_norms.min()) if row_norms.size else 0.0,
        "row_norm_max": max_norm,
        "row_norm_median": float(np.median(row_norms)) if row_norms.size else 0.0,
        "noise_floor_absolute": floor,
        "n_zero_rows": zero_rows,
        "row_normalisation_applied": zero_rows == 0,
        "row_normalisation_withheld_reason":
            None if zero_rows == 0 else
            f"{zero_rows} rows at or below the noise floor; normalising them "
            f"would fabricate directions from rounding noise",
        "singular_values_raw_head": [float(x) for x in s_raw[:5]],
        "singular_values_used_around_target":
            [float(x) for x in s_use[max(0, target - 3):target + 3]],
        "tolerance_sweep": sweep,
        "distinct_ranks_over_sweep": ranks,
        "rank_is_tolerance_stable": len(ranks) == 1,
        "observed_rank": ranks[0] if len(ranks) == 1 else None,
        "gap_at_target": gap,
        "target": target,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--archive", required=True,
                    help="path to a local copy of the spinor archive")
    ap.add_argument("--graphs", default=None,
                    help="selected_graphs.json; defaults to the tensor_words run")
    ap.add_argument("--seeds", default="11,22,33,44,55")
    ap.add_argument("--scales", default="0.25,0.35,1.0")
    ap.add_argument("--steps", default="1e-4,1e-5,1e-6")
    ap.add_argument("--orderings", type=int, default=2)
    ap.add_argument("--n-jobs", type=int, default=-1,
                    help="joblib workers for candidate evaluation")
    ap.add_argument("--out", default=str(ROOT / "verification" / "SPINOR_JACOBIAN_RUNS.json"))
    args = ap.parse_args()

    archive = Path(args.archive).expanduser().resolve()
    if not (archive / "sd5_invariants").is_dir():
        print(f"error: {archive} does not look like the spinor archive", file=sys.stderr)
        return 2
    sys.path.insert(0, str(archive))

    from sd5_invariants.gamma10 import Spin10Data          # noqa: E402
    from sd5_invariants.io import read_graphs_json         # noqa: E402
    from sd5_invariants.jacobian import finite_difference_jacobian  # noqa: E402

    graphs_path = Path(args.graphs) if args.graphs else (
        archive / "run_4_12_tensor_words_s96" / "selected_graphs.json")
    graphs = read_graphs_json(str(graphs_path))
    print(f"loaded {len(graphs)} candidates from {graphs_path.name}", flush=True)

    spin = Spin10Data()
    report = {
        "schema": 1,
        "method": "archive finite-difference Jacobian, float64",
        "noise_floor_relative": NOISE_FLOOR_RELATIVE,
        "normalisation_rule": "rows at or below the noise floor are never normalised",
        "graphs_source": graphs_path.name,
        "n_candidates": len(graphs),
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "platform": platform.platform(),
        },
        "runs": [],
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    seeds = [int(x) for x in args.seeds.split(",")]
    scales = [float(x) for x in args.scales.split(",")]
    steps = [float(x) for x in args.steps.split(",")]

    for seed in seeds:
        for scale in scales:
            for eps in steps:
                for ordering in range(args.orderings):
                    rng = np.random.default_rng(seed)
                    coeffs = spin.random_coefficients(rng, count=1, scale=scale)[0]
                    order = np.arange(len(graphs))
                    if ordering:
                        order = np.random.default_rng(seed + 1000 * ordering).permutation(
                            len(graphs))
                    ordered = [graphs[i] for i in order]

                    t0 = time.time()
                    res = finite_difference_jacobian(
                        ordered, spin, coeffs=coeffs, eps=eps,
                        n_jobs=args.n_jobs, rank_rtol=1e-8)
                    wall = time.time() - t0

                    diag = analyse(np.asarray(res.jacobian, dtype=float))
                    diag.update({
                        "seed": seed, "scale": scale, "step": eps,
                        "candidate_ordering": "identity" if ordering == 0 else f"permuted-{ordering}",
                        "archive_reported_rank": int(res.rank),
                        "wall_seconds": round(wall, 2),
                        "peak_rss_mb": round(peak_rss_mb(), 1),
                        "jacobian_sha256": hashlib.sha256(
                            np.ascontiguousarray(res.jacobian).tobytes()).hexdigest(),
                    })
                    diag["classification"] = classify(diag)
                    report["runs"].append(diag)
                    print(f"seed={seed} scale={scale} eps={eps:g} ord={ordering}: "
                          f"archive_rank={res.rank} zero_rows={diag['n_zero_rows']} "
                          f"sweep={diag['distinct_ranks_over_sweep']} "
                          f"gap={diag['gap_at_target']} -> {diag['classification']} "
                          f"({wall:.1f}s)", flush=True)
                    out.write_text(json.dumps(report, indent=1))

    by_class: dict = {}
    for r in report["runs"]:
        by_class.setdefault(r["classification"], 0)
        by_class[r["classification"]] += 1
    report["summary"] = {
        "n_runs": len(report["runs"]),
        "by_classification": by_class,
        "nondegenerate_ranks": sorted({
            r["observed_rank"] for r in report["runs"]
            if r["classification"] == "nondegenerate generic"}),
    }
    out.write_text(json.dumps(report, indent=1))
    print("done ->", out, json.dumps(report["summary"]), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
