#!/usr/bin/env python3
"""Collect every scientific input the mentor draft relies on into one manifest.

The manifest is not a summary written by hand. Each entry names the artifact it
came from, the value read out of that artifact, and the hash of the artifact at
the time of reading, so a reviewer can re-read the same file and get the same
number or else see immediately that something moved.

Entries whose artifact is missing are recorded as `missing`, never silently
dropped. A missing input is a finding, and the draft must not be able to hide
one by omission.

    python3 manuscript/jhep/scripts/build_input_manifest.py
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "results" / "mentor_draft" / "scientific_input_manifest.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def dig(obj, path):
    """Walk a dotted path through nested dicts; return None if absent."""
    cur = obj
    for key in path.split("."):
        if isinstance(cur, dict) and key in cur:
            cur = cur[key]
        else:
            return None
    return cur


# (claim id, artifact, dotted field, expected value or None to just record)
INPUTS = [
    ("A10-dim", "results/stress_flow/Q10_characteristic_zero.json",
     "A10_dim_over_Q", 14),
    ("D10-dim", "results/stress_flow/Q10_characteristic_zero.json",
     "D10_dim_over_Q", 11),
    ("Q10-dim", "results/stress_flow/Q10_characteristic_zero.json",
     "Q10_dim_over_Q", 3),
    ("Q10-status", "results/stress_flow/Q10_characteristic_zero.json",
     "status", "exact"),
    ("D10-settled", "results/stress_flow/D10_characteristic_zero.json",
     "settled", True),
    ("D10-holdout-prime", "results/stress_flow/D10_characteristic_zero.json",
     "lift.holdout_prime", 32771),
    ("D10-holdout-mismatches", "results/stress_flow/D10_characteristic_zero.json",
     "lift.holdout_mismatches", []),
    ("D10-minor-size", "results/stress_flow/D10_characteristic_zero.json",
     "lower_bound_certificate.size", 11),
    ("D10-minor-nonzero", "results/stress_flow/D10_characteristic_zero.json",
     "lower_bound_certificate.nonzero", True),
    ("G10-counterfactual-Q10", "results/stress_flow/G10_counterfactual.json",
     "counterfactual_Q10", 0),
    ("G10-derived-Q10", "results/stress_flow/G10_counterfactual.json",
     "as_derived_Q10", 3),
    ("G10-load-bearing", "results/stress_flow/G10_counterfactual.json",
     "activation_is_load_bearing", True),
    ("rank81-rank", "results/rank81/full_rank_matrix_publication_final.json",
     "rank", 81),
    ("rank81-cells", "results/rank81/full_rank_matrix_publication_final.json",
     "cells_complete", 15),
    ("rank81-agree", "results/rank81/full_rank_matrix_publication_final.json",
     "all_cells_agree", True),
    ("rank81-coord-dim", "results/rank81/full_rank_matrix_publication_final.json",
     "coordinate_dimension", 126),
    ("rank81-cumulative", "results/rank81/full_rank_matrix_publication_final.json",
     "cumulative_rank_by_degree", None),
    ("rank81-primes", "results/rank81/full_rank_matrix_publication_final.json",
     "primes", None),
    ("minor81", "results/rank81/minor81_certificate.json", None, None),
    ("BP-cap-dim", "results/degree10/B10_P10_intersection_exact.json",
     "dim_B10_cap_P10_over_Q", 1),
    ("BP-B10-dim", "results/degree10/B10_P10_intersection_exact.json",
     "dim_B10_over_Q", 12),
    ("BP-P10-dim", "results/degree10/B10_P10_intersection_exact.json",
     "dim_P10_over_Q", 2),
    ("BP-settled", "results/degree10/B10_P10_intersection_exact.json",
     "settled", True),
    ("BP-holdout-prime", "results/degree10/B10_P10_intersection_exact.json",
     "holdout_prime", 32783),
    ("BP-holdout-mismatches", "results/degree10/B10_P10_intersection_exact.json",
     "holdout_mismatches", []),
    ("BP-generator", "results/degree10/B10_P10_intersection_generator.json",
     None, None),
    ("G10-certificate", "results/stress_flow/G10_publication_certificate.json",
     None, None),
]


def main() -> int:
    entries, problems = [], []
    for claim, rel, field, expected in INPUTS:
        path = ROOT / rel
        rec = {"claim": claim, "artifact": rel}
        if not path.exists():
            rec["status"] = "missing"
            problems.append(f"{claim}: artifact absent ({rel})")
            entries.append(rec)
            continue
        rec["sha256"] = sha256(path)
        try:
            data = json.loads(path.read_text())
        except json.JSONDecodeError as exc:
            rec["status"] = "unreadable"
            problems.append(f"{claim}: {exc}")
            entries.append(rec)
            continue
        if field is not None:
            value = dig(data, field)
            rec["field"] = field
            rec["value"] = value
            if value is None:
                rec["status"] = "field-absent"
                problems.append(f"{claim}: field {field} absent in {rel}")
            elif expected is not None and value != expected:
                rec["status"] = "mismatch"
                rec["expected"] = expected
                problems.append(
                    f"{claim}: {rel}:{field} is {value!r}, draft expects {expected!r}")
            else:
                rec["status"] = "ok"
        else:
            rec["status"] = "ok"
            rec["keys"] = sorted(data)[:24] if isinstance(data, dict) else None
        entries.append(rec)

    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
            text=True, check=True).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        commit = "unavailable"

    manifest = {
        "schema": 1,
        "generated_by": "manuscript/jhep/scripts/build_input_manifest.py",
        "commit": commit,
        "n_inputs": len(entries),
        "n_ok": sum(1 for e in entries if e["status"] == "ok"),
        "problems": problems,
        "clean": not problems,
        "inputs": entries,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(manifest, indent=1, sort_keys=True) + "\n")

    print(f"{manifest['n_ok']}/{manifest['n_inputs']} inputs verified")
    for p in problems:
        print("  PROBLEM:", p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
