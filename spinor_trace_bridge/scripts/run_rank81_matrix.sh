#!/bin/sh
# Compute the rank-81 certificate matrix ONE CELL AT A TIME.
#
# Sequential on purpose. This machine has 8 GiB and running several cells at
# once put it into swap, which slowed every cell down and produced nothing
# faster. One process, one cell, then the next.
#
# Every cell is resumable: a completed cell is skipped, and a partial cell
# restarts from its row cache. Interrupting this script at any point loses at
# most the cell in flight.
#
# Usage:
#   sh spinor_trace_bridge/scripts/run_rank81_matrix.sh <archive> [python]

set -u

ARCHIVE="${1:?usage: run_rank81_matrix.sh <archive-dir> [python]}"
PY="${2:-python3}"
HERE="$(cd "$(dirname "$0")/../.." && pwd)"
DRIVER="$HERE/spinor_trace_bridge/scripts/run_rank81_cell.py"

# 32707 is a holdout prime. It was excluded for a while on the theory that
# primes congruent to 3 mod 8 are exceptional, which was wrong: once the frame
# orientation is pinned by signature.orientation_normalised_L, 32633 -- which
# is 1 mod 8 -- needs the same square-root branch as 32707. The branch a prime
# needs is not a function of its residue class, and every class works. See
# docs/CANONICAL_ORIENTATION_FIXED_BRIDGE.md.
#
# 32693 stood in for 32707 during that period. It is kept as an EXTRA
# validation prime, never as a replacement; the aggregator rejects a matrix
# that carries it while missing 32707.
#
# tests/test_duality_channel_primes.py fails if 32707 is dropped again or if a
# residue rule reappears here.
FITTING="32749 32719 32717"
HOLDOUT="32713 32707"
EXTRA="32693"
SEEDS="11 22 33"

echo "matrix start $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "fitting: $FITTING"
echo "holdout: $HOLDOUT"
echo "seeds:   $SEEDS"

failed=0
for role in fitting holdout; do
    case "$role" in
        fitting) primes="$FITTING" ;;
        holdout) primes="$HOLDOUT" ;;
    esac
    for p in $primes; do
        for s in $SEEDS; do
            echo "--- cell p=$p seed=$s role=$role $(date -u +%H:%M:%SZ)"
            "$PY" "$DRIVER" --archive "$ARCHIVE" \
                --prime "$p" --seed "$s" --role "$role"
            rc=$?
            if [ "$rc" -ne 0 ]; then
                echo "CELL FAILED p=$p seed=$s rc=$rc"
                failed=$((failed + 1))
            fi
        done
    done
done

for p in $EXTRA; do
    for s in $SEEDS; do
        echo "--- cell p=$p seed=$s role=extra $(date -u +%H:%M:%SZ)"
        "$PY" "$DRIVER" --archive "$ARCHIVE" --prime "$p" --seed "$s" --role extra
        rc=$?
        if [ "$rc" -ne 0 ]; then
            echo "CELL FAILED p=$p seed=$s rc=$rc"
            failed=$((failed + 1))
        fi
    done
done

echo "matrix end $(date -u +%Y-%m-%dT%H:%M:%SZ) failed_cells=$failed"
exit "$failed"
