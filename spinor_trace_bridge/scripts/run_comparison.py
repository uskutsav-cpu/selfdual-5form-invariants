"""Run the common-sample trace/spinor comparison and write the certificate.

Usage:
    python spinor_trace_bridge/scripts/run_comparison.py [--primes 32749,32719]
                                                          [--degrees 4,6,8,10]
                                                          [--out PATH]

Writes incrementally, so a long run can be inspected while it is still going and
resumed from the last completed degree if it is interrupted.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "spinor_trace_bridge" / "src"))

from sdbridge import conventions as C           # noqa: E402
from sdbridge.bridge import BridgeMap           # noqa: E402
from sdbridge.comparison import (               # noqa: E402
    check_gamma_traces, compare_degree, grading_table, spinor_fields,
)
from sdbridge.samples import (                  # noqa: E402
    build_registry, registry_hash, verify_selfduality,
)
from sdbridge.spinor_invariants import sample_graphs_until_rank_saturates  # noqa: E402
from sdbridge.traceside import load_registry    # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--primes", default="32749,32719")
    ap.add_argument("--degrees", default="4,6,8,10")
    ap.add_argument("--patience", type=int, default=60)
    ap.add_argument("--max-graphs", type=int, default=400)
    ap.add_argument("--out", default=str(ROOT / "verification" / "spinor_trace_comparison.json"))
    ap.add_argument("--registry-out",
                    default=str(ROOT / "verification" / "COMMON_SAMPLE_REGISTRY.json"))
    args = ap.parse_args()

    primes = [int(x) for x in args.primes.split(",")]
    degrees = [int(x) for x in args.degrees.split(",")]
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    report: dict = {
        "schema": 1,
        "arithmetic": "exact over F_p; no floating point on either side",
        "degrees": degrees,
        "primes": {},
    }
    if out_path.exists():
        try:
            report = json.loads(out_path.read_text())
        except json.JSONDecodeError:
            pass

    trace_registry = load_registry()

    for p in primes:
        key = str(p)
        started = time.time()
        bridge = BridgeMap(p=p)
        samples = build_registry(bridge)
        sd = verify_selfduality(bridge, samples)
        S_batch = spinor_fields(bridge, samples)

        if key not in report["primes"]:
            report["primes"][key] = {"degrees": {}}
        slot = report["primes"][key]
        slot.update({
            "n_samples": len(samples),
            "sample_families": {
                f: sum(1 for s in samples if s.family == f)
                for f in sorted({s.family for s in samples})},
            "registry_sha256": registry_hash(samples),
            "all_samples_selfdual": sd["all_selfdual"],
            "all_images_gamma_traceless": check_gamma_traces(bridge, S_batch),
            "grading": grading_table(trace_registry),
        })

        if p == primes[0]:
            Path(args.registry_out).write_text(json.dumps(
                {"prime": p, "sha256": registry_hash(samples),
                 "samples": [s.to_json() for s in samples]}, indent=1))

        for d in degrees:
            if str(d) in slot["degrees"]:
                print(f"[p={p} deg={d}] already done, skipping", flush=True)
                continue
            t0 = time.time()
            graphs, rows, diag = sample_graphs_until_rank_saturates(
                d, list(S_batch), p, patience=args.patience,
                max_graphs=args.max_graphs)
            diag["wall_seconds"] = round(time.time() - t0, 1)
            entry = compare_degree(bridge, samples, trace_registry, d, rows, diag)
            slot["degrees"][str(d)] = entry
            print(f"[p={p} deg={d}] trace {entry['trace_evaluation_rank']} "
                  f"spinor {entry['spinor_evaluation_rank']} "
                  f"equal={entry['spans_equal_all_samples']} "
                  f"holdout={entry['holdout_validated']} "
                  f"({diag['wall_seconds']}s)", flush=True)
            out_path.write_text(json.dumps(report, indent=1, sort_keys=True))

        slot["wall_seconds"] = round(time.time() - started, 1)
        out_path.write_text(json.dumps(report, indent=1, sort_keys=True))

    print("done ->", out_path, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
