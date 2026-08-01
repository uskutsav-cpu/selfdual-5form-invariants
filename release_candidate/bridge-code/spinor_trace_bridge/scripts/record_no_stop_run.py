"""Record a `--no-hilbert-stop` scan as a certificate, including if it is partial.

The scientifically important field is `stopped_by`.  Four terminal states are
distinguished and must not be conflated:

    candidate_exhaustion  every candidate in the declared ansatz was tried
    hilbert_target        the externally supplied target rank was reached
    stagnation            no new rank for the configured number of batches
    incomplete            the run did not reach a terminal state here

Only the first is evidence that the ansatz was searched out.  A run that stopped
at the Hilbert target proves nothing about the ansatz, because the target came
from outside the computation.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rundir", required=True)
    ap.add_argument("--out-json",
                    default=str(ROOT / "verification" / "spinor_degree10_no_stop.json"))
    ap.add_argument("--out-md",
                    default=str(ROOT / "verification" / "SPINOR_DEGREE10_NO_STOP.md"))
    args = ap.parse_args()

    rundir = Path(args.rundir).expanduser().resolve()
    summary = rundir / "summary.json"
    degrees: list[dict] = []
    if summary.exists():
        try:
            data = json.loads(summary.read_text())
            degrees = data if isinstance(data, list) else [data]
        except json.JSONDecodeError:
            pass

    seen = {int(d["degree"]) for d in degrees if "degree" in d}
    for d in (4, 6, 8, 10):
        if d not in seen:
            degrees.append({"degree": d, "stopped_by": "incomplete",
                            "note": "the run did not reach this degree on this machine"})
    degrees.sort(key=lambda d: d["degree"])

    reached_ten = any(d["degree"] == 10 and d.get("stopped_by") != "incomplete"
                      for d in degrees)
    exhausted = [d["degree"] for d in degrees
                 if d.get("stopped_by") == "candidate_exhaustion"]

    report = {
        "schema": 1,
        "run_directory": rundir.name,
        "stopping_rule": "Hilbert target DISABLED (--no-hilbert-stop)",
        "why_that_matters": (
            "Every archived scan stopped at the Hilbert target, which is supplied "
            "from outside the computation. A run that stops there demonstrates "
            "nothing about the ansatz. Disabling it is what makes the terminal "
            "status informative."),
        "terminal_states": {
            "candidate_exhaustion": "the declared ansatz was searched out",
            "hilbert_target": "stopped at an externally supplied rank; uninformative",
            "stagnation": "no rank gain within the configured patience",
            "incomplete": "no terminal state reached on this machine",
        },
        "degrees": degrees,
        "degrees_reaching_candidate_exhaustion": exhausted,
        "degree_ten_completed": reached_ten,
        "independent_cross_check": (
            "Independently of this scan, the exact modular enumeration in "
            "verification/spinor_trace_comparison.json reaches evaluation rank 14 "
            "at degree 10 by rank saturation, and its span equals the tensor-side "
            "span with holdout validation. That is a saturation observation, not "
            "an exhaustion proof, and is reported as such."),
    }
    Path(args.out_json).write_text(json.dumps(report, indent=1))

    lines = [
        "# Degree-10 spinor scan with the Hilbert stopping rule disabled",
        "",
        report["why_that_matters"],
        "",
        "## Terminal status by degree",
        "",
        "| degree | rank | target | selected | unique tried | stopped by |",
        "|---:|---:|---:|---:|---:|---|",
    ]
    for d in degrees:
        lines.append(
            f"| {d['degree']} | {d.get('final_rank', '--')} | "
            f"{d.get('hilbert_target', '--')} | {d.get('selected_new', '--')} | "
            f"{d.get('attempted_unique_graphs', '--')} | "
            f"**{d.get('stopped_by', 'incomplete')}** |")
    lines += [
        "",
        "## What this establishes",
        "",
        f"Degrees reaching candidate exhaustion: "
        f"{', '.join(map(str, exhausted)) if exhausted else 'none'}.",
        "",
        "At those degrees the rank is derived by searching the ansatz out, not by "
        "stopping at a number supplied from outside. That is the distinction the "
        "specification asks for, and it is the reason the run was made at all.",
        "",
        "## What this does not establish",
        "",
    ]
    if not reached_ten:
        lines += [
            "Degree 10 did **not** reach a terminal state on this machine, so no "
            "exhaustion claim is made for it. The independent exact modular "
            "enumeration reaches rank 14 there by *saturation*, which is a weaker "
            "statement and is labelled as such wherever it appears.",
            "",
            "A cluster job that would complete the degree-10 and degree-12 scans "
            "is prepared in `cluster/`. **No cluster run has occurred.**",
        ]
    else:
        lines += [
            "Exhaustion is relative to the declared ansatz. The port-graph family "
            "is known to miss a degree-eight direction, so 'exhausted' means the "
            "family was searched out, not that the invariant space was.",
        ]
    Path(args.out_md).write_text("\n".join(lines) + "\n")
    print(f"recorded -> {Path(args.out_md).name}; exhausted at degrees {exhausted}; "
          f"degree 10 complete: {reached_ten}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
