# Referee C — computational mathematics and reproducibility

**C1. "Modular arithmetic hides overflow."** It did, once: the structured
evaluator reduced only at the end of each einsum and wrapped `int64` at `~2^72`.
It was caught by a homogeneity test, not by inspection, and there is now a
permanent test that performs the unreduced contraction deliberately and asserts
the failure. *Answered by a regression test that reproduces the defect.*

**C2. "Prime selection could be adversarial."** Five primes, two reserved as
holdout and never used for fitting. The rank-lower-bound argument does not depend
on the number of primes at all — it depends on integrality. *Answered.*

**C3. "Your determinant could be wrong."** Two independent routines — modular LU
with pivoting and fraction-free Bareiss — agree. They use different recurrences,
so a shared mistake is unlikely. *Answered.*

**C4. "Contraction correctness."** Two contraction plans exist for the port-graph
derivative (factorised and dense-`I`) and a test requires identical rows. The
tensor-word derivative has an optimized polarisation and a literal interpolation
evaluator, required to agree. Euler homogeneity holds for all 83. *Answered.*

**C5. "Independence from the third-party archive."** Import audits in both
directions return zero. The shipped package runs without the archive. The
strongest evidence is positive rather than negative: the bridge's
spinor-to-five-form map reproduces the archive's independent float `pinv`-based
map exactly, ratio 1 on all 25 800 nonzero components. *Answered.*

**C6. "Clean-clone claims."** A fresh clone reproduces the tensor and bridge test
suites, all generated numbers, tables and figures, and an isolated manuscript
build. It does **not** reproduce the archive-dependent results, which need a
private copy; a manifest of hashes and adapter instructions is shipped.
*Answered, with the limitation named.*

**C7. "Mutation coverage."** 17 adversarial tests, each injecting a specific
defect. Three reproduce defects this project actually had. Coverage is of the
defect classes encountered, not of all possible errors, and mutation testing is
not a correctness proof. *Conceded.*

**C8. "Large data accessibility."** Nothing tracked exceeds 1 MB; certificates
are compact JSON; the row caches are gitignored and regenerable. *Answered.*
