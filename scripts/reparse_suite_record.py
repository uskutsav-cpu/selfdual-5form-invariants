#!/usr/bin/env python3
"""Rebuild a suite record from its stored stdout/stderr, without re-running.

The first version of run_authoritative_suite.sh matched only pytest's
decorated summary line ('==== 252 passed ... ===='), not the bare form that -q
prints. Two clean suites were therefore recorded as
'ABSENT -- NO TERMINAL SUMMARY LINE' and claimable_as_passing=False.

Re-running them to fix a parsing bug would discard 17 minutes of compute and
prove nothing new. The logs are the primary evidence, they are intact, and
their sha256 is already in the record -- so this re-derives the parsed fields
from those exact bytes and verifies the hashes still match before writing.
If a hash does not match, the log changed since the run and the record is not
rewritten.

Usage: python3 scripts/reparse_suite_record.py <record.json> [...]
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

SUMMARY = re.compile(
    r'^(?:=+ .*(?:passed|failed|error|no tests ran).* =+'
    r'|[0-9]+ (?:passed|failed|error)[^=]*)$',
    re.MULTILINE,
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b''):
            h.update(chunk)
    return h.hexdigest()


def reparse(record_path: Path) -> int:
    rec = json.loads(record_path.read_text())
    out = Path(rec['stdout_path'])
    err = Path(rec['stderr_path'])

    for path, field in ((out, 'stdout_sha256'), (err, 'stderr_sha256')):
        if not path.exists():
            print(f"{record_path.name}: {path} is gone; not rewriting")
            return 1
        actual = sha256(path)
        if actual != rec[field]:
            print(f"{record_path.name}: {path.name} changed since the run "
                  f"({actual[:12]} != {rec[field][:12]}); not rewriting")
            return 1

    text = out.read_text(encoding='utf-8', errors='replace')
    found = SUMMARY.findall(text)
    summary = found[-1].strip() if found else 'ABSENT -- NO TERMINAL SUMMARY LINE'

    counts = {}
    for kind in ('passed', 'failed', 'error', 'skipped', 'deselected',
                 'xfailed', 'xpassed', 'warning'):
        m = re.search(rf'(\d+)\s+{kind}s?\b', summary)
        if m:
            counts[kind] = int(m.group(1))

    m = re.search(r'collected\s+(\d+)\s+item', text)
    if m:
        rec['collected'] = int(m.group(1))
    elif counts.get('passed') is not None and rec.get('collected') is None:
        # -q suppresses the collected line; the passed count is the floor.
        rec['collected'] = None

    has_summary = not summary.startswith('ABSENT')
    rec['summary_line'] = summary
    rec['has_terminal_summary'] = has_summary
    rec['counts'] = counts
    rec['claimable_as_passing'] = bool(
        has_summary and rec['exit_code'] == 0
        and counts.get('failed', 0) == 0 and counts.get('error', 0) == 0
    )
    rec['reparsed_from_stored_logs'] = True
    rec['reparse_note'] = (
        'Parsed fields re-derived from the stored stdout after a summary-line '
        'regex fix. The suite was NOT re-run; both log hashes were verified '
        'against the original record before rewriting.'
    )

    record_path.write_text(json.dumps(rec, indent=2, sort_keys=True))
    print(f"{rec['suite']}: {summary} claimable={rec['claimable_as_passing']}")
    return 0


if __name__ == '__main__':
    sys.exit(max(reparse(Path(p)) for p in sys.argv[1:]) if len(sys.argv) > 1 else 2)
