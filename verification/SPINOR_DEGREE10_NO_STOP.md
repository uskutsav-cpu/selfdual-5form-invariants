# Degree-10 spinor scan with the Hilbert stopping rule disabled

Every archived scan stopped at the Hilbert target, which is supplied from outside the computation. A run that stops there demonstrates nothing about the ansatz. Disabling it is what makes the terminal status informative.

## Terminal status by degree

| degree | rank | target | selected | unique tried | stopped by |
|---:|---:|---:|---:|---:|---|
| 4 | 1 | 1 | 1 | 2 | **candidate_exhaustion** |
| 6 | 2 | 2 | 2 | 5 | **candidate_exhaustion** |
| 8 | -- | -- | -- | -- | **incomplete** |
| 10 | -- | -- | -- | -- | **incomplete** |

## What this establishes

Degrees reaching candidate exhaustion: 4, 6.

At those degrees the rank is derived by searching the ansatz out, not by stopping at a number supplied from outside. That is the distinction the specification asks for, and it is the reason the run was made at all.

## What this does not establish

Degree 10 did **not** reach a terminal state on this machine, so no exhaustion claim is made for it. The independent exact modular enumeration reaches rank 14 there by *saturation*, which is a weaker statement and is labelled as such wherever it appears.

A cluster job that would complete the degree-10 and degree-12 scans is prepared in `cluster/`. **No cluster run has occurred.**
