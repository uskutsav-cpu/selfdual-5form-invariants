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

# Every prime here must be NON-congruent to 3 mod 8. For p = 3 (mod 8) the
# bridge's duality channel inverts and the cell cannot complete -- see
# docs/EXCEPTIONAL_PRIMES_DUALITY_CHANNEL.md. 32707 was the original third
# holdout and is 3 mod 8; it is replaced by 32693 (5 mod 8).
# tests/test_duality_channel_primes.py parses this block and fails if a prime
# in the bad class is ever added back.
FITTING="32749 32719 32717"
HOLDOUT="32713 32693"
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

echo "matrix end $(date -u +%Y-%m-%dT%H:%M:%SZ) failed_cells=$failed"
exit "$failed"
