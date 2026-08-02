# The duality channel inverts for p ≡ 3 (mod 8)

Found 2026-08-02 while completing the rank-81 holdout cells. All three cells at
`p = 32707` failed identically:

```
RuntimeError: image has dimension 0, not 126; cannot build a left inverse
```

This is not a resource failure and not a bad-luck sample point. It is a
property of the prime.

## The observation

`BridgeMap.forward_matrix` is 252×136 with rank 126 at every prime tested, so
the map itself is fine everywhere. What changes is *which* 126-dimensional
subspace it annihilates.

| prime | p mod 4 | p mod 8 | rank(SD · F) | rank(ASD · F) |
|---:|---:|---:|---:|---:|
| 32713 | 1 | 1 | **126** | 0 |
| 32749 | 1 | 5 | **126** | 0 |
| 32717 | 1 | 5 | **126** | 0 |
| 32693 | 1 | 5 | **126** | 0 |
| 32719 | 3 | 7 | **126** | 0 |
| 32707 | 3 | **3** | **0** | **126** |
| 32771 | 3 | **3** | **0** | **126** |

The split is exactly `p mod 8`. For `p ≡ 1, 5, 7` the forward map is injective
on the self-dual subspace and kills the anti-self-dual one, which is the
intended convention. For `p ≡ 3 (mod 8)` the two are exchanged: the subspace
the code labels self-dual is precisely the kernel.

Note that `p mod 4` does not separate the cases — 32719 and 32707 are both
`3 mod 4` and behave differently — so this is not simply about whether `−1` is
a square. Among the four classes mod 8, `p ≡ 3` is the one where `−1` and `2`
are *both* non-residues. Identifying the precise mechanism in the null-frame
Clifford construction is left open; the empirical statement is reproducible and
is what the pipeline needs.

**Status: observed, across seven primes, deterministically.** It is not proved
from the construction, and this document does not claim it holds for every
prime in the class. It is a rule for choosing primes, not a theorem.

## Why it did not corrupt anything

Every one of the twelve completed cells used a prime in `{32749, 32719, 32717,
32713}`, all of which are `1, 5, 7 mod 8`. All twelve are on the intended
channel, all report rank 81, and the rank-81 certificate is unaffected.

The failure mode was also loud rather than silent. `left_inverse` checks the
image dimension against 126 and raises; it does not fall back, does not
substitute the other channel, and does not emit a cell file. Three cells
failed, three cells were recorded as missing, and the aggregator refused to
call the matrix complete. That is the behaviour we want, and it is worth
saying so explicitly: had the code quietly used whichever channel had rank 126,
the certificate would have silently mixed two conventions and nothing would
have objected.

## What changed

The third holdout prime is now **32693** (`5 mod 8`) rather than 32707.
`spinor_trace_bridge/scripts/run_rank81_matrix.sh` is updated accordingly, and
`tests/test_duality_channel_primes.py` pins the observation so that a future
change to the Clifford construction cannot move the channel without failing a
test.

## What was deliberately not done

The construction was **not** changed to auto-select whichever channel has rank
126. That would make `p ≡ 3 (mod 8)` usable, but it would also mean cells at
different primes could silently sit on different conventions, and a certificate
assembled from them would be comparing objects that are not the same object.
Choosing primes on one convention is the safer fix and costs nothing — the
class `p ≡ 3 (mod 8)` is a quarter of the primes, and the pipeline needs only
a handful.

Changing `bridge.py` would also have invalidated the frozen source hash carried
by all twelve completed cells, forcing a full recomputation of about four hours
to fix something that was not wrong.
