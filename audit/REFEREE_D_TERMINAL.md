# Referee D — computational proof

## D1. "Where did the rank-matrix cells come from?"

A separate working tree of this project, and they carry no source-critical hash.
Rather than assert provenance, it was closed empirically: the two cells
overlapping this repository's own certificate — `(32749, 11)` and `(32749, 22)` —
agree field by field including pivot rows, pivot columns and pivot row candidate
ids. All fifteen share one candidate-ordering hash.

**Stated limitation**: the other thirteen were not independently recomputed here.
The document says so rather than implying they were.

## D2. "An aggregator that only ever succeeds proves nothing."

`--self-test` mutates a copy of the cells eleven ways and requires each to be
rejected: missing cell, duplicate cell, mixed candidate ordering, mixed
coordinate dimension, mixed flop budget, 82 of 83 candidates, an evaluation
error, a zero row, a failed Euler check, a malformed hash, a cell not marked
complete. It then re-reads the cells to prove none was mutated, and re-renders
from reversed input to prove order independence. All eleven fire.

## D3. "Duplicate writers and shared caches."

Real history, and recorded rather than hidden: two rank-81 processes once shared
a row cache, and two test runs shared a log. The second test log was **discarded
rather than trusted**, even though its content matched, and the suite was re-run
alone.

Current state: one authoritative writer, verified with `pgrep -f` on script
names. A first attempt using `ps aux | grep` inside `bash -lc` reported eight and
was wrong — the shell's own command line matched the pattern. That correction is
in the live-state record because an inflated count would have caused a pointless
kill.

## D4. "Are the builds reproducible?"

Now yes, and they were not. A clean clone produced different archive hashes; a
file-by-file comparison showed the same 25-file set, all eighteen non-figure
files byte-identical, and all seven figures differing **solely** in matplotlib's
embedded `/CreationDate`. Fixed by pinning `SOURCE_DATE_EPOCH` and normalising
tar/zip timestamps, ownership and modes. Both archives now rebuild to identical
bytes from an independent clone.

The point is not tidiness: a hash check that fails on every rebuild teaches you
to ignore it.

## D5. "CRT reconstruction without a height bound is a guess."

Which is why every lift is **validated at a held-out prime** that took no part in
it, and the intersection generator is additionally verified at a further prime on
six freshly drawn samples. The first attempt at `B10 cap P10` lifted only 9 of
12 and was reported as not settled, with the bound standing, until seven fitting
primes sufficed.

A verification of that generator also **failed** first, on all six samples.
Testing each lifted vector individually showed the lift was sound and the check
was comparing two separately gcd-reduced sides. Recorded, because a check that
fails and is quietly adjusted until it passes is worthless.

## D6. "Source cleanliness."

626 tracked files classified: 289 user-authored, 333 generated, 4 third-party
(LPPL), **0 unknown**, **0 mentor-derived**. One stray file committed by a
shell-quoting accident was found and removed during the audit. Secret and
private-path scans clean — the path scan caught a home directory in a file this
work had just created.

## Verdict

D3, D4 and D5 all describe defects that existed. Each is fixed, and each is
recorded with what went wrong rather than only what is now true.
