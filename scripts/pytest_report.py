#!/usr/bin/env python3
"""Parse pytest output into counts that can be reported without hedging.

The reproduction driver's earlier counter did two things this one does not.
It reported only a passed count, so a skipped or xfailed test was invisible;
and its fallback stripped a couple of patterns and then counted every
remaining `.`, which also counts the dot in `12.34s`, in a version string, and
in any prose the suite happens to print.

The rule here is narrower and stated once: a progress line is a line that,
after its `[ NN%]` marker is removed, consists of nothing but pytest's own
progress characters and whitespace. Anything else is not a progress line and
contributes no counts. A line of dots qualifies; `collected 199 items` does
not; `1 passed in 0.34s` does not.

Counts come from the summary line when there is one, because that is pytest's
own arithmetic. The progress fallback is used only when no summary was printed
-- which in this configuration is the normal case, not an edge case.

Usage:
    python scripts/pytest_report.py <logfile> [--json]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

# pytest's single-character progress markers
PROGRESS_CHARS = {
    ".": "passed",
    "s": "skipped",
    "F": "failed",
    "E": "errors",
    "x": "xfailed",
    "X": "xpassed",
}

PERCENT = re.compile(r"\[\s*\d+%\]")
COLLECTED = re.compile(r"collected\s+(\d+)\s+items?")
DESELECTED_ON_COLLECT = re.compile(r"(\d+)\s+deselected")
SUMMARY_TOKEN = re.compile(
    r"(\d+)\s+(passed|failed|error|errors|skipped|deselected|xfailed|xpassed|warning|warnings)")
DURATION = re.compile(r"\bin\s+([\d.]+)s")
INTERRUPT_MARKERS = (
    "KeyboardInterrupt", "!!!!", "Interrupted:", "stopping after",
    "INTERNALERROR",
)


@dataclass
class PytestCounts:
    collected: int | None = None
    passed: int = 0
    failed: int = 0
    errors: int = 0
    skipped: int = 0
    deselected: int = 0
    xfailed: int = 0
    xpassed: int = 0
    warnings: int = 0
    runtime_seconds: float | None = None
    source: str = "none"          # "summary" | "progress" | "none"
    interrupted: bool = False
    contaminated: bool = False
    returncode: int | None = None
    problems: list[str] = field(default_factory=list)
    log_sha256: str | None = None

    @property
    def total_reported(self) -> int:
        return (self.passed + self.failed + self.errors + self.skipped
                + self.xfailed + self.xpassed)

    @property
    def ok(self) -> bool:
        return (not self.interrupted and not self.contaminated
                and self.failed == 0 and self.errors == 0 and not self.problems)


def _is_progress_line(line: str) -> bool:
    body = PERCENT.sub("", line).strip()
    if not body:
        return False
    return all(ch in PROGRESS_CHARS or ch.isspace() for ch in body)


def parse(text: str, returncode: int | None = None) -> PytestCounts:
    """Counts from a pytest log.

    Pass `returncode` when the caller has it. A pytest killed by a signal
    prints no interrupt marker at all, so a log of 113 dots from a suite that
    was SIGKILLed at 34% reads exactly like a suite of 113 tests that passed.
    The exit status is the only thing that distinguishes them.
    """
    out = PytestCounts()
    out.returncode = returncode
    out.log_sha256 = hashlib.sha256(text.encode("utf-8", "replace")).hexdigest()

    collected_hits = COLLECTED.findall(text)
    if collected_hits:
        out.collected = int(collected_hits[0])
        # Two collection headers in one log means two pytest processes wrote to
        # it. Their counts cannot be added and must not be silently summed.
        if len({int(x) for x in collected_hits}) > 1 or len(collected_hits) > 1:
            out.contaminated = True
            out.problems.append(
                f"{len(collected_hits)} collection headers in one log "
                f"({', '.join(collected_hits)} items); output from more than one "
                "pytest process cannot be combined")

    if any(marker in text for marker in INTERRUPT_MARKERS):
        out.interrupted = True
        out.problems.append("interrupt marker present; the run did not finish")

    # The summary line is pytest's own arithmetic; prefer it.
    # "no tests ran in 0.01s" is a summary too, and it carries no digit before
    # a keyword, so it needs its own alternative rather than a looser pattern.
    summary_lines = [
        ln for ln in text.splitlines()
        if re.search(r"=+\s.*(\d+\s+(passed|failed|error|skipped)|no tests ran)", ln)
    ]
    if summary_lines:
        line = summary_lines[-1]
        out.source = "summary"
        for count, word in SUMMARY_TOKEN.findall(line):
            n = int(count)
            if word == "passed":
                out.passed = n
            elif word == "failed":
                out.failed = n
            elif word in ("error", "errors"):
                out.errors = n
            elif word == "skipped":
                out.skipped = n
            elif word == "deselected":
                out.deselected = n
            elif word == "xfailed":
                out.xfailed = n
            elif word == "xpassed":
                out.xpassed = n
            elif word in ("warning", "warnings"):
                out.warnings = n
        m = DURATION.search(line)
        if m:
            out.runtime_seconds = float(m.group(1))
    else:
        # No summary: count progress characters, and only on progress lines.
        tally = {v: 0 for v in PROGRESS_CHARS.values()}
        found = False
        for line in text.splitlines():
            if not _is_progress_line(line):
                continue
            found = True
            for ch in PERCENT.sub("", line):
                if ch in PROGRESS_CHARS:
                    tally[PROGRESS_CHARS[ch]] += 1
        if found:
            out.source = "progress"
            out.passed = tally["passed"]
            out.failed = tally["failed"]
            out.errors = tally["errors"]
            out.skipped = tally["skipped"]
            out.xfailed = tally["xfailed"]
            out.xpassed = tally["xpassed"]

    if out.collected is not None and out.source != "none":
        accounted = out.total_reported + out.deselected
        if accounted > out.collected and not out.contaminated:
            out.contaminated = True
            out.problems.append(
                f"{accounted} outcomes for {out.collected} collected items; the "
                "log holds more results than the run had tests")
        elif accounted < out.collected and not out.interrupted:
            out.problems.append(
                f"{accounted} outcomes for {out.collected} collected items; "
                f"{out.collected - accounted} unaccounted for")

    if out.source == "none":
        out.problems.append("no summary line and no progress line; nothing to count")

    if returncode is not None and returncode != 0:
        # Exit 1 with counted failures is consistent and already reported.
        # Anything else -- a signal, a collection error, an internal error --
        # means the log understates what went wrong.
        if out.failed == 0 and out.errors == 0:
            out.interrupted = True
            signal_note = (f"killed by signal {-returncode}" if returncode < 0
                           else f"exit status {returncode}")
            out.problems.append(
                f"{signal_note} with no failures counted; the run did not "
                "complete and its counts are a lower bound")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("logfile", type=Path)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--returncode", type=int, default=None,
                    help="exit status of the pytest run, when the caller has it")
    args = ap.parse_args()
    counts = parse(args.logfile.read_text(encoding="utf-8", errors="replace"),
                   returncode=args.returncode)
    if args.json:
        print(json.dumps(asdict(counts), indent=1))
    else:
        print(f"source      {counts.source}")
        print(f"collected   {counts.collected}")
        print(f"passed      {counts.passed}")
        print(f"failed      {counts.failed}")
        print(f"errors      {counts.errors}")
        print(f"skipped     {counts.skipped}")
        print(f"deselected  {counts.deselected}")
        print(f"xfailed     {counts.xfailed}")
        print(f"xpassed     {counts.xpassed}")
        print(f"warnings    {counts.warnings}")
        print(f"runtime     {counts.runtime_seconds}")
        print(f"interrupted {counts.interrupted}")
        print(f"contaminated {counts.contaminated}")
        print(f"returncode  {counts.returncode}")
        for p in counts.problems:
            print(f"  PROBLEM {p}")
    return 0 if counts.ok else 1


if __name__ == "__main__":
    sys.exit(main())
