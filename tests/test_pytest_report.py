"""The test counter needs tests, because a miscount is invisible.

A reproduction report that says "199 passed" is a scientific claim about how
much was checked. The previous counter reported 1 for a 72-test suite, and
nothing caught it because nothing was watching the counter itself.

Each case below is a shape of pytest output this project has actually produced
or could produce under the conditions the reproduction driver runs in.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from pytest_report import parse  # noqa: E402


def test_one_line_of_dots():
    counts = parse("." * 72 + " [100%]\n")
    assert counts.source == "progress"
    assert counts.passed == 72
    assert counts.failed == 0
    assert counts.ok


def test_wrapped_dots_across_several_lines():
    """The real shape: 72 per line, percentage marker on each."""
    text = (
        "." * 72 + " [ 36%]\n"
        + "." * 72 + " [ 72%]\n"
        + "." * 55 + " [100%]\n"
    )
    counts = parse(text)
    assert counts.source == "progress"
    assert counts.passed == 199
    assert counts.ok


def test_ordinary_summary_line_is_preferred():
    text = (
        "collected 199 items\n\n"
        + "." * 199 + " [100%]\n\n"
        "======================== 199 passed in 171.23s ========================\n"
    )
    counts = parse(text)
    assert counts.source == "summary"
    assert counts.passed == 199
    assert counts.collected == 199
    assert counts.runtime_seconds == pytest.approx(171.23)
    assert counts.ok


def test_summary_with_every_outcome_kind():
    text = (
        "collected 210 items / 3 deselected / 207 selected\n"
        "=== 190 passed, 2 failed, 1 error, 8 skipped, 3 deselected, "
        "4 xfailed, 2 xpassed, 5 warnings in 12.5s ===\n"
    )
    counts = parse(text)
    assert counts.source == "summary"
    assert (counts.passed, counts.failed, counts.errors) == (190, 2, 1)
    assert (counts.skipped, counts.deselected) == (8, 3)
    assert (counts.xfailed, counts.xpassed, counts.warnings) == (4, 2, 5)
    assert not counts.ok, "a run with failures must not report ok"


def test_failed_tests_are_counted_from_progress():
    text = "..F...E..s.. [100%]\n"
    counts = parse(text)
    assert counts.passed == 9
    assert counts.failed == 1
    assert counts.errors == 1
    assert counts.skipped == 1
    assert not counts.ok


def test_skipped_tests_are_not_counted_as_passed():
    text = "....ssss.... [100%]\n"
    counts = parse(text)
    assert counts.passed == 8
    assert counts.skipped == 4
    assert counts.total_reported == 12


def test_interrupted_run_is_flagged():
    text = (
        "collected 199 items\n\n"
        + "." * 41 + "\n"
        "!!!!!!!!!!!!!!!!!!! KeyboardInterrupt !!!!!!!!!!!!!!!!!!!\n"
    )
    counts = parse(text)
    assert counts.interrupted
    assert not counts.ok
    assert any("did not finish" in p for p in counts.problems)


def test_duplicate_process_contamination_is_flagged():
    """Two pytest processes writing one log must not have their counts added."""
    text = (
        "collected 199 items\n" + "." * 199 + " [100%]\n"
        "collected 72 items\n" + "." * 72 + " [100%]\n"
    )
    counts = parse(text)
    assert counts.contaminated
    assert not counts.ok
    assert any("more than one" in p for p in counts.problems)


def test_more_outcomes_than_collected_is_flagged():
    text = "collected 10 items\n" + "." * 25 + " [100%]\n"
    counts = parse(text)
    assert counts.contaminated
    assert not counts.ok


def test_empty_output():
    counts = parse("")
    assert counts.source == "none"
    assert counts.passed == 0
    assert not counts.ok
    assert any("nothing to count" in p for p in counts.problems)


def test_whitespace_only_output():
    counts = parse("\n\n   \n")
    assert counts.source == "none"
    assert not counts.ok


# --------------------------------------------------------------------------
# the miscounts the old counter actually made
# --------------------------------------------------------------------------
def test_dots_in_prose_and_timings_are_not_counted():
    """`0.34s`, a version string and a file path all contain dots."""
    text = (
        "platform darwin -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0\n"
        "rootdir: /Users/someone/work/repo\n"
        "collected 3 items\n\n"
        "tests/test_core.py ... [100%]\n\n"
        "Ran 3 tests in 0.34s. Everything fine.\n"
    )
    counts = parse(text)
    # No summary line here, so the progress path runs. The only line that is
    # nothing but progress characters is none of the above -- the file-path
    # line has letters in it -- so the parser must decline rather than guess.
    assert counts.source == "none"
    assert counts.passed == 0


def test_progress_line_without_percentage_marker():
    counts = parse("." * 30 + "\n")
    assert counts.source == "progress"
    assert counts.passed == 30


def test_unaccounted_tests_are_reported_not_hidden():
    text = "collected 100 items\n" + "." * 90 + " [ 90%]\n"
    counts = parse(text)
    assert counts.passed == 90
    assert not counts.ok
    assert any("unaccounted" in p for p in counts.problems)


def test_log_hash_is_recorded_and_content_sensitive():
    a = parse("." * 10 + "\n")
    b = parse("." * 11 + "\n")
    assert a.log_sha256 and b.log_sha256
    assert a.log_sha256 != b.log_sha256


def test_no_tests_ran_summary():
    counts = parse("===================== no tests ran in 0.01s =====================\n")
    assert counts.source == "summary"
    assert counts.passed == 0


def test_killed_run_with_no_marker_is_flagged_by_returncode():
    """A SIGKILLed pytest prints no interrupt marker at all.

    113 dots from a suite killed at 34% look exactly like 113 tests that
    passed. Only the exit status tells them apart, so the caller must be able
    to supply it.
    """
    text = "." * 113 + "\n"
    clean = parse(text)
    assert clean.passed == 113 and not clean.interrupted, (
        "without a returncode there is nothing in the log to object to")
    killed = parse(text, returncode=-9)
    assert killed.interrupted
    assert not killed.ok
    assert any("signal 9" in p for p in killed.problems)


def test_nonzero_exit_with_counted_failures_is_not_double_reported():
    text = "=== 2 failed, 197 passed in 10.0s ===\n"
    counts = parse(text, returncode=1)
    assert counts.failed == 2
    assert not counts.interrupted, "exit 1 with counted failures is consistent"
    assert not counts.ok


def test_clean_run_with_zero_exit_stays_ok():
    counts = parse("=== 199 passed in 171.2s ===\n", returncode=0)
    assert counts.ok
    assert counts.returncode == 0
