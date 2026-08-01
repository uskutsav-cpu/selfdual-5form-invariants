"""Analyse the ARCHIVED float64 Jacobians under an explicit noise-floor rule.

Two Jacobians were produced by the original spinor runs and stored as `.npy`.
They differ only in the random sample point and the tensor scale, and they
reported ranks of 35 and 81.  This script re-analyses both from the stored
matrices, so the comparison rests on the data actually produced rather than on a
re-run.

The rule enforced, and the whole point of the exercise:

    a row whose norm is at or below the declared noise floor is NEVER normalised.

Normalising such a row rescales pure rounding noise into a unit vector.  Do that
to enough rows and the singular spectrum loses its gap and the reported rank
becomes whatever the tolerance says it is.  That is the mechanism behind the
discrepancy, and it is reported rather than hidden.

Usage:
    python spinor_trace_bridge/scripts/analyse_archived_jacobians.py --archive PATH
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]

#: A row counts as numerically zero at or below this multiple of the largest row
#: norm in the same matrix.
NOISE_FLOOR_RELATIVE = 1e-12

TARGET = 81


def analyse(J: np.ndarray, label: str, source: str) -> dict:
    row_norms = np.linalg.norm(J, axis=1)
    max_norm = float(row_norms.max())
    floor = NOISE_FLOOR_RELATIVE * max_norm
    zero_rows = int((row_norms <= floor).sum())

    s_raw = np.linalg.svd(J, compute_uv=False)

    if zero_rows == 0:
        s_used = np.linalg.svd(J / row_norms[:, None], compute_uv=False)
        normalisation = "applied: no row sits at the noise floor"
    else:
        s_used = s_raw
        normalisation = (f"WITHHELD: {zero_rows} rows at or below the noise floor; "
                         f"normalising them would rescale rounding noise into unit "
                         f"vectors and manufacture rank")

    sweep = {}
    for rtol in (1e-6, 1e-7, 1e-8, 1e-9, 1e-10, 1e-11, 1e-12):
        tol = rtol * max(J.shape) * float(s_used[0])
        sweep[f"{rtol:g}"] = int((s_used > tol).sum())
    ranks = sorted(set(sweep.values()))

    gap = None
    if s_used.size > TARGET:
        num, den = float(s_used[TARGET - 1]), float(s_used[TARGET])
        gap = (num / den) if den > 0 else float("inf")

    # what happens if the rule is broken -- reported so the reader can see the
    # size of the effect rather than take the rule on trust
    forced = None
    if zero_rows:
        safe = np.where(row_norms > 0, row_norms, 1.0)
        s_forced = np.linalg.svd(J / safe[:, None], compute_uv=False)
        tol = 1e-8 * max(J.shape) * float(s_forced[0])
        forced = {
            "rank_if_rule_broken": int((s_forced > tol).sum()),
            "comment": "this is the number row normalisation fabricates",
        }

    if zero_rows > 0:
        classification = "degenerate sample"
    elif len(ranks) == 1 and gap is not None and gap > 1e3:
        classification = "nondegenerate generic"
    else:
        classification = "numerically inconclusive"

    return {
        "label": label,
        "source": source,
        "shape": list(J.shape),
        "sha256": hashlib.sha256(np.ascontiguousarray(J).tobytes()).hexdigest(),
        "row_norm_min": float(row_norms.min()),
        "row_norm_max": max_norm,
        "row_norm_median": float(np.median(row_norms)),
        "noise_floor_relative": NOISE_FLOOR_RELATIVE,
        "noise_floor_absolute": floor,
        "n_zero_rows": zero_rows,
        "row_normalisation": normalisation,
        "singular_values_used_around_target":
            [float(x) for x in s_used[max(0, TARGET - 3):TARGET + 3]],
        "singular_values_used_head": [float(x) for x in s_used[:5]],
        "singular_values_used_tail": [float(x) for x in s_used[-5:]],
        "tolerance_sweep": sweep,
        "distinct_ranks_over_sweep": ranks,
        "rank_is_tolerance_stable": len(ranks) == 1,
        "observed_rank": ranks[0] if len(ranks) == 1 else None,
        "gap_at_target": gap,
        "target": TARGET,
        "if_normalisation_rule_is_broken": forced,
        "classification": classification,
        # the fields the run-matrix schema carries, so both feed the same table
        "seed": None, "scale": None, "step": None,
        "candidate_ordering": "as archived",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--archive", required=True)
    ap.add_argument("--out", default=str(ROOT / "verification" / "SPINOR_JACOBIAN_RUNS.json"))
    args = ap.parse_args()

    archive = Path(args.archive).expanduser().resolve()
    runs_meta = [
        ("run_4_12_tensor_words_s96_jacobian", "tensor-words run"),
        ("run_4_12_full_dense_safe_s96_jacobian", "full-dense-safe run"),
    ]

    report = {
        "schema": 2,
        "method": "re-analysis of the archived float64 finite-difference Jacobians",
        "why_not_recomputed": (
            "a single finite-difference Jacobian over these 83 candidates takes "
            "more than ten minutes even with parallel evaluation, so a full "
            "seed x scale x step matrix was not run here. The archived matrices "
            "are the data those runs actually produced and are analysed directly."),
        "noise_floor_relative": NOISE_FLOOR_RELATIVE,
        "normalisation_rule":
            "rows at or below the noise floor are never normalised",
        "environment": {"python": platform.python_version(), "numpy": np.__version__},
        "runs": [],
    }

    for folder, label in runs_meta:
        path = archive / folder / "jacobian.npy"
        if not path.exists():
            print(f"skip {folder}: no jacobian.npy", flush=True)
            continue
        J = np.load(path).astype(float)
        entry = analyse(J, label, f"{folder}/jacobian.npy")
        # the run summaries record seed and scale; carry them through if present
        summary = archive / folder / "summary.json"
        if summary.exists():
            try:
                meta = json.loads(summary.read_text())
                if isinstance(meta, dict):
                    entry["seed"] = meta.get("seed")
                    entry["scale"] = meta.get("scale")
                    entry["step"] = meta.get("eps")
            except json.JSONDecodeError:
                pass
        report["runs"].append(entry)
        print(f"{label}: shape {entry['shape']} zero_rows {entry['n_zero_rows']} "
              f"sweep {entry['distinct_ranks_over_sweep']} "
              f"gap {entry['gap_at_target']} -> {entry['classification']}", flush=True)
        if entry["if_normalisation_rule_is_broken"]:
            print(f"    breaking the rule would report rank "
                  f"{entry['if_normalisation_rule_is_broken']['rank_if_rule_broken']}",
                  flush=True)

    by_class: dict = {}
    for r in report["runs"]:
        by_class[r["classification"]] = by_class.get(r["classification"], 0) + 1
    report["summary"] = {
        "n_runs": len(report["runs"]),
        "by_classification": by_class,
        "nondegenerate_ranks": sorted({
            r["observed_rank"] for r in report["runs"]
            if r["classification"] == "nondegenerate generic"
            and r["observed_rank"] is not None}),
        "scope": ("two archived samples, not a seed/scale/step matrix; the "
                  "exact modular Jacobian supersedes this as evidence and this "
                  "analysis is retained to document the failure mode"),
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=1))
    print("done ->", out, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
