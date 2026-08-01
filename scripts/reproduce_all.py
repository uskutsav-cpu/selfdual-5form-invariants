#!/usr/bin/env python3
"""Run the full reproduction sequence and record what actually happened.

The reproduction record was written by hand twice and went stale both times --
it claimed 199 and 49 tests when the suites were 207 and 72, and 32 gates when
there were 60. A record of a run should be produced by the run.

This script executes each step, captures the real numbers, and writes
`verification/REPRODUCTION_RECORD.json` plus a markdown table beside it. It exits
nonzero if any step fails, so it is a check and not only a report.

    python scripts/reproduce_all.py                  # full sequence
    python scripts/reproduce_all.py --skip-tests     # everything but the suites
    python scripts/reproduce_all.py --skip-build     # no LaTeX required

Archive-dependent artifacts are NOT regenerated: they need a copy of the
third-party spinor archive that is not redistributed. They are committed, so
every number in both manuscripts is present without it. The record says which
steps were skipped rather than implying a fuller run than occurred.
"""

from __future__ import annotations

import argparse
import json
import platform
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENV = ROOT.parent / ".venv" / "bin" / "python"
PY = str(VENV) if VENV.exists() else sys.executable
OUT_JSON = ROOT / "verification" / "REPRODUCTION_RECORD.json"
OUT_MD = ROOT / "verification" / "REPRODUCTION_RECORD.md"


def run(cmd: list[str], cwd: Path = ROOT, timeout: int = 3600):
    t0 = time.time()
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                          timeout=timeout)
    return proc, round(time.time() - t0, 1)


def count_tests(output: str) -> int | None:
    """Passed count from pytest, whether or not it printed a summary line."""
    m = re.search(r"(\d+) passed", output)
    if m:
        return int(m.group(1))
    # `-q` under some plugin sets prints only the progress dots.
    dots = sum(len(re.findall(r"^[.]+", line))
               for line in output.splitlines() if line.startswith("."))
    return dots or None


def step_tests(record: dict) -> bool:
    ok = True
    for label, cwd in (("tensor test suite", ROOT),
                       ("bridge test suite", ROOT / "spinor_trace_bridge")):
        proc, secs = run([PY, "-m", "pytest", "-q", "-p", "no:cacheprovider"],
                         cwd=cwd)
        n = count_tests(proc.stdout)
        passed = proc.returncode == 0
        record["steps"].append({
            "step": label, "passed": passed, "tests": n, "seconds": secs,
            # A killed process exits nonzero with no summary; say so rather than
            # reporting the dots it managed to print as a result.
            "note": None if passed else "nonzero exit; suite did not complete",
        })
        ok = ok and passed
    return ok


def step_regenerate(record: dict) -> bool:
    ok = True
    for label, script in (("numbers", "manuscript/scripts/make_numbers.py"),
                          ("tables", "manuscript/scripts/make_tables.py"),
                          ("figures", "manuscript/scripts/make_figures.py")):
        proc, secs = run([PY, str(ROOT / script)])
        passed = proc.returncode == 0
        detail = None
        if label == "numbers":
            m = re.search(r"\((\d+) lines\)", proc.stdout)
            macros = len(re.findall(r"\\newcommand",
                                    (ROOT / "manuscript/generated/numbers.tex").read_text()))
            missing = len(re.findall(r"ARTIFACTMISSING",
                                     (ROOT / "manuscript/generated/numbers.tex").read_text()))
            detail = {"macros": macros, "artifacts_missing": missing}
            if missing:
                passed = False
        record["steps"].append({"step": f"regenerate {label}", "passed": passed,
                                "seconds": secs, "detail": detail})
        ok = ok and passed
    return ok


def step_build(record: dict) -> bool:
    proc, secs = run([PY, str(ROOT / "scripts/build_submission_package.py")])
    diag = None
    m = re.search(r"isolated build: (\{.*\})", proc.stdout)
    if m:
        diag = json.loads(m.group(1))
    passed = proc.returncode == 0 and bool(diag) and diag.get("errors") == 0 \
        and diag.get("undefined_citations") == 0 \
        and diag.get("undefined_references") == 0
    record["steps"].append({"step": "isolated manuscript build", "passed": passed,
                            "seconds": secs, "detail": diag})
    return passed


def step_gates(record: dict) -> bool:
    proc, secs = run([PY, str(ROOT / "manuscript/scripts/check_manuscript.py")])
    m = re.search(r"manuscript gates: (\d+) checks", proc.stdout)
    passed = proc.returncode == 0
    record["steps"].append({
        "step": "manuscript gates", "passed": passed, "seconds": secs,
        "detail": {"checks": int(m.group(1)) if m else None},
        "note": None if passed else proc.stdout.strip().splitlines()[-1:],
    })
    return passed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-tests", action="store_true")
    ap.add_argument("--skip-build", action="store_true",
                    help="skip the LaTeX build, for a machine with no TeX")
    args = ap.parse_args()

    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    dirty = bool(subprocess.run(["git", "status", "--short"], cwd=ROOT,
                                capture_output=True, text=True).stdout.strip())

    record = {
        "schema": 1,
        "generated_by": "scripts/reproduce_all.py",
        "commit": head,
        "working_tree_clean": not dirty,
        "when": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "environment": {
            "platform": platform.platform(),
            "python": platform.python_version(),
            "interpreter": PY,
        },
        "not_regenerated": {
            "results/rank81/certificate.json": "needs the third-party archive",
            "results/rank81/minor81_certificate.json": "needs the third-party archive",
            "verification/SPINOR_JACOBIAN_RUNS.json": "needs the third-party archive",
        },
        "steps": [],
    }

    ok = True
    if args.skip_tests:
        record["steps"].append({"step": "test suites", "passed": None,
                                "note": "skipped by --skip-tests"})
    else:
        ok &= step_tests(record)
    ok &= step_regenerate(record)
    if args.skip_build:
        record["steps"].append({"step": "isolated manuscript build",
                                "passed": None, "note": "skipped by --skip-build"})
    else:
        ok &= step_build(record)
    ok &= step_gates(record)

    record["all_steps_passed"] = ok
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(record, indent=1) + "\n")

    rows = ["# Reproduction record", "",
            "Generated by `scripts/reproduce_all.py`. Do not edit by hand --",
            "this file was maintained manually twice and went stale both times.",
            "",
            f"Commit `{head}`, working tree "
            f"{'clean' if not dirty else '**dirty**'}, {record['when']}.", "",
            "| step | result | detail | seconds |", "|---|---|---|---:|"]
    for s in record["steps"]:
        mark = {True: "**pass**", False: "**FAIL**", None: "skipped"}[s.get("passed")]
        detail = s.get("detail") or s.get("note") or ""
        if s.get("tests") is not None:
            detail = f"{s['tests']} tests"
        rows.append(f"| {s['step']} | {mark} | {detail} | {s.get('seconds', '')} |")
    rows += ["", "## Not regenerated here", ""]
    for path, why in record["not_regenerated"].items():
        rows.append(f"- `{path}` --- {why}")
    rows += ["",
             "These certificates are committed, so every number in both",
             "manuscripts is present and both build without the archive. Only",
             "their *regeneration* needs it. See",
             "`release_candidate/spinor-archive/MANIFEST.json` and",
             "`scripts/verify_archive.py`.", ""]
    OUT_MD.write_text("\n".join(rows))

    print(f"wrote {OUT_JSON.relative_to(ROOT)} and {OUT_MD.relative_to(ROOT)}")
    print("ALL STEPS PASSED" if ok else "SOME STEPS FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
