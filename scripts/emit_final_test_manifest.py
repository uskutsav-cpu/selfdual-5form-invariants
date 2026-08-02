#!/usr/bin/env python3
"""Phase 6 --- the final test manifest, counted by a parser that has tests.

Every suite's log is parsed by `scripts/pytest_report.py`, which is itself
covered by 19 regression tests, so the counts here are not a hand tally of
dots. Where a log records its exit status the status is used, because a pytest
killed by a signal prints no interrupt marker and 113 dots from a suite that
died at 34% read exactly like 113 passes.

Writes:
    results/tests/final_test_manifest.json
    docs/JHEP_FINAL_TEST_REPORT.md

Usage:
    python scripts/emit_final_test_manifest.py [--repo .]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pytest_report import parse  # noqa: E402

SUITES = [
    ("tensor", "results/tests/final_tensor.log",
     "python -m pytest tests/ -q", "."),
    ("bridge", "results/tests/final_bridge.log",
     "cd spinor_trace_bridge && python -m pytest -q", "spinor_trace_bridge"),
]

EXIT_LINE = re.compile(r"^exit=(-?\d+)\s*$", re.MULTILINE)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".", type=Path)
    args = ap.parse_args()
    repo = args.repo.resolve()
    when = datetime.now(timezone.utc).isoformat(timespec="seconds")

    rows = []
    for name, rel, command, root in SUITES:
        path = repo / rel
        if not path.exists():
            rows.append({"suite": name, "log": rel, "status": "NOT RUN"})
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        m = EXIT_LINE.search(text)
        rc = int(m.group(1)) if m else None
        counts = parse(EXIT_LINE.sub("", text), returncode=rc)
        rows.append({
            "suite": name, "log": rel, "command": command, "root": root,
            "returncode": rc,
            "count_source": counts.source,
            "collected": counts.collected,
            "passed": counts.passed, "failed": counts.failed,
            "errors": counts.errors, "skipped": counts.skipped,
            "deselected": counts.deselected, "xfailed": counts.xfailed,
            "xpassed": counts.xpassed, "warnings": counts.warnings,
            "runtime_seconds": counts.runtime_seconds,
            "interrupted": counts.interrupted,
            "contaminated": counts.contaminated,
            "problems": counts.problems,
            "log_sha256": counts.log_sha256,
            "status": "PASS" if counts.ok else "NOT CLEAN",
        })

    ran = [r for r in rows if r.get("status") not in ("NOT RUN",)]
    total_passed = sum(r.get("passed", 0) for r in ran)
    total_failed = sum(r.get("failed", 0) + r.get("errors", 0) for r in ran)
    all_clean = bool(ran) and all(r["status"] == "PASS" for r in ran) \
        and len(ran) == len(SUITES)

    record = {
        "generated_utc": when,
        "counted_by": "scripts/pytest_report.py (19 regression tests)",
        "suites": rows,
        "total_passed": total_passed,
        "total_failed_or_error": total_failed,
        "all_suites_clean": all_clean,
    }
    (repo / "results" / "tests" / "final_test_manifest.json").write_text(
        json.dumps(record, indent=1) + "\n", encoding="utf-8")

    L = ["# Final test report", "",
         f"Generated {when} by `scripts/emit_final_test_manifest.py`.", "",
         "Counts come from `scripts/pytest_report.py`, which has 19 regression",
         "tests of its own covering wrapped dots, summary lines, interrupted",
         "output, duplicate-process contamination and empty logs. They are not a",
         "hand tally.", "",
         "| suite | passed | failed | errors | skipped | source | exit | status |",
         "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        if r.get("status") == "NOT RUN":
            L.append(f"| {r['suite']} | --- | --- | --- | --- | --- | --- | **NOT RUN** |")
            continue
        L.append(f"| {r['suite']} | {r['passed']} | {r['failed']} | {r['errors']} | "
                 f"{r['skipped']} | {r['count_source']} | {r['returncode']} | "
                 f"**{r['status']}** |")
    L += ["", f"Total passed: **{total_passed}**. "
          f"Failed or errored: **{total_failed}**.", ""]
    for r in rows:
        if r.get("problems"):
            L += [f"### {r['suite']} problems", ""]
            L += [f"- {p}" for p in r["problems"]]
            L.append("")
    L += ["## Log hashes", "", "| suite | sha256 |", "|---|---|"]
    for r in rows:
        if r.get("log_sha256"):
            L.append(f"| {r['suite']} | `{r['log_sha256'][:32]}` |")
    L.append("")
    (repo / "docs" / "JHEP_FINAL_TEST_REPORT.md").write_text("\n".join(L) + "\n",
                                                             encoding="utf-8")

    for r in rows:
        if r.get("status") == "NOT RUN":
            print(f"{r['suite']:8s} NOT RUN")
        else:
            print(f"{r['suite']:8s} {r['status']:10s} passed {r['passed']:4d} "
                  f"failed {r['failed']} errors {r['errors']} "
                  f"skipped {r['skipped']} (exit {r['returncode']})")
    print(f"\ntotal passed {total_passed}, failed/errored {total_failed}, "
          f"all clean {all_clean}")
    return 0 if all_clean else 1


if __name__ == "__main__":
    sys.exit(main())
