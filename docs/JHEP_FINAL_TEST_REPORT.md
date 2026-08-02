# Final test report

Generated 2026-08-02T16:38:50+00:00 by `scripts/emit_final_test_manifest.py`.

Counts come from `scripts/pytest_report.py`, which has 19 regression
tests of its own covering wrapped dots, summary lines, interrupted
output, duplicate-process contamination and empty logs. They are not a
hand tally.

| suite | passed | failed | errors | skipped | source | exit | status |
|---|---|---|---|---|---|---|---|
| tensor | 24 | --- | --- | --- | --- | --- | **INCOMPLETE** |
| bridge | 135 | 0 | 0 | 0 | progress | 0 | **PASS** |

Total passed: **135**. Failed or errored: **0**.

### tensor problems

- no exit= line in the log; the suite has not finished, so its counts are a lower bound

## Log hashes

| suite | sha256 |
|---|---|
| bridge | `f2a2851fd07d932c49660c7f57aef372` |

