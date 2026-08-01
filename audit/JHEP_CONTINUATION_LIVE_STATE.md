# JHEP continuation --- live state

Generated 2026-08-01T21:20:20+00:00 by `scripts/emit_jhep_continuation_state.py`.

## Reported state, checked against the worktree

| field | reported | live | agrees |
|---|---|---|---|
| execution_id | `rank81-matrix-5f46a2cbbe93-flop1e11` | `rank81-matrix-5f46a2cbbe93-flop1e11` | yes |
| frozen_source_commit | `5f46a2c` | `5f46a2c` | yes |
| flop_budget | `100000000000.0` | `100000000000.0` | yes |
| cells_planned | `15` | `15` | yes |
| branch | `publication/jhep-tensor-spinor` | `publication/jhep-tensor-spinor` | yes |

## Matrix validity

| check | result |
|---|---|
| freeze record present | yes |
| freeze fields missing | none |
| source-critical drift | 0 files |
| head moved since freeze | yes |
| changed source-critical files | none |
| **matrix valid** | **yes** |

HEAD has moved from `5f46a2cbbe93` to `28bc57984231` since the
freeze, across 5 files. None is source-critical,
so the cells produced before and after that movement were produced by the
same evaluator and belong to the same execution.

Files changed since the freeze:

- `audit/JHEP_FINAL_RECONCILIATION_PLAN.md`
- `audit/RANK_MATRIX_EXECUTION_FREEZE.json`
- `scripts/emit_rank_matrix_freeze.py`
- `spinor_trace_bridge/scripts/assemble_rank81_matrix.py`
- `spinor_trace_bridge/tests/test_matrix_aggregator.py`

## Writers

- matrix drivers: [60151]
- cell workers: [67806]
- pytest processes: [38503, 68851, 69145]
- cell locks held: ['cell_p32719_s22.lock']

| pid | in this worktree | elapsed/state | cwd |
|---|---|---|---|
| 60151 | yes | `37:19 SN` | `/Users/swethasunilkumar/Downloads/sdinv-jhep` |
| 67588 | no (other session) | `06:07 RN` | `/Users/swethasunilkumar/Documents/Codex/2026-07-29/now/work/selfdual-5form-invariants` |
| 67806 | yes | `05:02 RN` | `/Users/swethasunilkumar/Downloads/sdinv-jhep` |

One writer enforced: at most one driver, at most one cell worker, at most
one lock. A process in the other session's tree cannot reach these cells.

## Matrix progress

4 of 15 cells complete; distinct ranks so far [81].

| prime | seed | role | rank | rows | euler | seconds | peak MB |
|---|---|---|---|---|---|---|---|
| 32719 | 11 | fitting | 81 | 83 | 83/83 | 1076.3 | 607.9 |
| 32749 | 11 | fitting | 81 | 83 | 83/83 | 4.0 | 233.3 |
| 32749 | 22 | fitting | 81 | 83 | 83/83 | 268.7 | 508.9 |
| 32749 | 33 | fitting | 81 | 83 | 83/83 | 586.3 | 591.1 |

