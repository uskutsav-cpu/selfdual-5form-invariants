#!/bin/sh
# Phase 2.1/2.2 — ONE authoritative test run, with a terminal record.
#
# The previous attempt (/private/tmp/final2_tensor.log) could not be claimed:
# 320 bytes of dots, no summary line, no exit code, and it ran on the wrong
# branch. This script exists so that failure mode is not repeatable. It waits
# for the rank-81 driver to exit first, so the suite never competes with the
# matrix for memory on an 8 GiB machine, and so there is exactly one heavy
# writer at a time.
#
# Usage: sh scripts/run_authoritative_suite.sh <driver_pid>

set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT" || exit 2

PY="$HOME/Documents/Codex/2026-07-29/now/work/.venv/bin/python"
RUNDIR="$ROOT/results/jhep/authoritative_run"
mkdir -p "$RUNDIR"

DRIVER_PID="${1:-}"
if [ -n "$DRIVER_PID" ]; then
    echo "waiting for rank-81 driver pid=$DRIVER_PID to finish..."
    while kill -0 "$DRIVER_PID" 2>/dev/null; do sleep 30; done
    echo "driver exited; starting authoritative suite"
fi

COMMIT="$(git rev-parse HEAD)"
BRANCH="$(git rev-parse --abbrev-ref HEAD)"
EXEC_ID="auth-$(date -u +%Y%m%dT%H%M%SZ)-$$"

# ---------------------------------------------------------------- aggregate
# The matrix must be aggregated before the gate can see it.
AGG_LOG="$RUNDIR/${EXEC_ID}.aggregate.log"
"$PY" spinor_trace_bridge/scripts/assemble_rank81_matrix.py >"$AGG_LOG" 2>&1
echo "aggregate exit=$? -> $AGG_LOG"

# The multi-sample certificate is the Phase 2.3 deliverable and reads the
# aggregate, so it has to come after it and before the gate.
CERT_LOG="$RUNDIR/${EXEC_ID}.certificate.log"
"$PY" scripts/emit_rank81_multi_sample_certificate.py >"$CERT_LOG" 2>&1
echo "certificate exit=$? -> $CERT_LOG"

# ------------------------------------------------------------ the two suites
# Separate logs. Never a shared file, never two pytest processes at once.
run_suite() {
    name="$1"; shift
    out="$RUNDIR/${EXEC_ID}.${name}.stdout"
    err="$RUNDIR/${EXEC_ID}.${name}.stderr"
    rec="$RUNDIR/${EXEC_ID}.${name}.record.json"

    start_epoch=$(date -u +%s)
    start_iso=$(date -u +%Y-%m-%dT%H:%M:%SZ)

    # /usr/bin/time -l gives peak RSS on macOS.
    /usr/bin/time -l "$PY" -m pytest "$@" -p no:cacheprovider -rN \
        >"$out" 2>"$err"
    code=$?

    end_epoch=$(date -u +%s)
    end_iso=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    elapsed=$((end_epoch - start_epoch))

    # peak RSS in bytes, from time -l
    peak=$(grep -E 'maximum resident set size' "$err" | awk '{print $1}' | tail -1)
    [ -z "$peak" ] && peak=0

    # The summary line is the thing the previous run never produced. If it is
    # absent, this record says so rather than implying a pass.
    #
    # It comes in two shapes and the first version of this only matched one.
    # Verbose pytest decorates it with '=' rules; -q prints a bare
    # '252 passed in 988.63s'. Matching only the decorated form marked two
    # clean suites unclaimable, which is the safe direction to be wrong in but
    # still wrong. Match either.
    summary=$(grep -E '^(=+ .*(passed|failed|error|no tests ran).* =+|[0-9]+ (passed|failed|error)[^=]*)$' "$out" | tail -1)
    [ -z "$summary" ] && summary="ABSENT -- NO TERMINAL SUMMARY LINE"

    "$PY" - "$rec" "$name" "$COMMIT" "$BRANCH" "$EXEC_ID" "$code" \
        "$start_iso" "$end_iso" "$elapsed" "$peak" "$out" "$err" "$summary" <<'PYEOF'
import hashlib, json, re, sys

(rec, name, commit, branch, exec_id, code, start, end, elapsed, peak,
 out, err, summary) = sys.argv[1:14]

def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b''):
            h.update(chunk)
    return h.hexdigest()

text = open(out, encoding='utf-8', errors='replace').read()

counts = {}
for kind in ('passed', 'failed', 'error', 'errors', 'skipped', 'deselected',
             'xfailed', 'xpassed', 'warning', 'warnings'):
    m = re.search(rf'(\d+)\s+{kind}\b', summary)
    if m:
        counts[kind.rstrip('s') if kind in ('errors', 'warnings') else kind] = int(m.group(1))

m = re.search(r'collected\s+(\d+)\s+item', text)
collected = int(m.group(1)) if m else None

has_summary = not summary.startswith('ABSENT')
record = {
    'execution_id': exec_id,
    'suite': name,
    'commit': commit,
    'branch': branch,
    'exit_code': int(code),
    'started_utc': start,
    'ended_utc': end,
    'elapsed_seconds': int(elapsed),
    'peak_rss_bytes': int(peak),
    'collected': collected,
    'counts': counts,
    'summary_line': summary,
    'has_terminal_summary': has_summary,
    'stdout_path': out,
    'stderr_path': err,
    'stdout_sha256': sha256(out),
    'stderr_sha256': sha256(err),
    # A run is claimable only if it terminated AND said so. Both, not either.
    'claimable_as_passing': bool(
        has_summary and int(code) == 0
        and counts.get('failed', 0) == 0 and counts.get('error', 0) == 0
    ),
}
with open(rec, 'w') as fh:
    json.dump(record, fh, indent=2, sort_keys=True)
print(f"{name}: exit={code} {summary} claimable={record['claimable_as_passing']}")
PYEOF
    return $code
}

run_suite tensor tests/
TENSOR=$?
run_suite bridge spinor_trace_bridge/tests/
BRIDGE=$?

# ------------------------------------------------------------------ the gate
"$PY" scripts/emit_jhep_science_gate.py >"$RUNDIR/${EXEC_ID}.gate.log" 2>&1
GATE=$?

echo "=== authoritative run $EXEC_ID @ $COMMIT ($BRANCH) ==="
echo "tensor=$TENSOR bridge=$BRIDGE gate=$GATE"
tail -10 "$RUNDIR/${EXEC_ID}.gate.log"
