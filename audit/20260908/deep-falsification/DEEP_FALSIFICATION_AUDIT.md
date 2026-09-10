# Adversarial Paper 1 audit — 2026-09-08

Target: `4d194696d707b797127a14a7bd6b3bd1744f9904` on `roadmap/verified-classification`.

This review starts from the null hypothesis that the Paper 1 science is wrong. It separates the central rank/orbit theorem, invariant-space counts, degreewise completeness, tensor conventions, source-paper maps, and nonessential follow-up work.

## Verdict

No fatal defect was found in the Paper 1 theorem or the degree-through-12 classification after static code review, independent mathematical re-derivation of the D5 character calculation, inspection of raw execution logs, and comparison with the current primary literature.

The strongest claims remain correctly scoped: a maximal generically algebraically independent family of 81 explicit polynomial Lorentz invariants and complete homogeneous invariant spaces through degree 12. This is not a presentation of the full invariant ring, its syzygies, global orbit separation, or a classification of nonlinear chiral actions.

## Central theorem

The standalone verifier in `science/rank81/verify.py` was reviewed function by function. It reconstructs the 126-dimensional self-dual five-form from integral coordinates, evaluates the fixed 81 complete contractions, computes all 81x126 derivatives, finds a nonzero 81x81 Jacobian minor modulo 50021, constructs all 45 infinitesimal Lorentz tangent directions, finds a nonzero 45x45 orbit minor, and verifies that all invariant differentials annihilate all orbit tangents.

The mathematical lifting argument is valid: the graph polynomials and their Jacobian minors have integer coefficients in the chosen coordinates, so one nonzero modular specialization proves the determinant polynomial is nonzero over characteristic zero. The Jacobian criterion then gives algebraic independence on a nonempty Zariski-open set. The independent orbit minor gives generic orbit dimension 45, so invariant differential rank is at most 126-45=81. Together the lower and upper bounds prove maximal generic rank 81.

Frozen fresh residues:

- invariant Jacobian minor: 21539 modulo 50021;
- Lorentz-orbit minor: 10547 modulo 50021.

The raw cold-run log enumerates all 81 rows and ends with rank 81 / orbit rank 45 in 55.88 seconds. The command record shows the run was performed in a standalone directory with `verify.py input.json --output certificate.json`.

The use of float64 inside the standalone contraction engine is exact under its explicit guard: every unreduced dot-product sum is an integer below 2^53, hence exactly representable. This is not a floating-tolerance rank computation.

## Tensor and Lorentz conventions

The Hodge convention and metric sign were checked against the standard Lorentzian identity `*^2=(-1)^(p(d-p)+1)` for p=5,d=10, giving `*^2=+1`. The self-dual eigenspace therefore has dimension 126. The production and standalone contraction implementations apply exactly one inverse-metric sign per contracted edge. Complete contractions are analytically SO(1,9)-invariant; numerical rotation/boost tests are implementation checks, not the proof of invariance.

The distinction between 126 algebraic components, 81 generic invariant parameters, and 35 free propagating chiral-four-form polarizations is preserved correctly in the physics note.

## Independent D5 character count

The repository character engine and its Python checker were reviewed independently. The 126-dimensional chiral D5 weight system, Newton recurrence for symmetric powers, Weyl-orbit compression, and trivial-representation extraction are mathematically consistent.

A separate C++ implementation written for this audit, without importing repository code or reading stored Hilbert values, re-derived the invariant multiplicities through degree 22 and reproduced

`1, 2, 7, 14, 72, 247, 1364, 6851, 40170, 227979`

at degrees 4,6,8,10,12,14,16,18,20,22, with odd degrees zero. It independently checked the total symmetric-power dimension at every degree. Its source and output are included beside this report.

This independently supports the repository character result and removes the published-Hilbert coefficient as a premise of degree-12 completeness.

## Degreewise completeness

The logic is sound:

- degree 8: dimension 7 = one lower product + six primitive graph classes;
- degree 10: dimension 14 = two lower products + twelve primitive graph classes;
- degree 12: dimension 72 = ten lower products + sixty-two connected graph classes.

The saved degree-12 stacked-gradient certificate has rank 72 over two primes. Since the independent D5 count gives the matching upper bound 72, the 72 displayed homogeneous polynomials form a complete basis of the degree-12 invariant space. This is linear/homogeneous completeness, not algebraic independence of all 72.

## Corrected source maps

The previously discovered J10-J12 source-transcription failure is correctly retained in the historical audit rather than erased. The corrected source convention and exact maps are separate from the central rank-81 proof. With the independently derived dimensions 7 and 14, the exact evaluation maps become unconditional within the stated analytic-invariance assumptions. The corrected decic source span has dimension 12, its product span dimension 2, their union dimension 13 and intersection dimension 1; the source family therefore contributes eleven primitive quotient classes and misses one degree-10 primitive direction.

## Raw test evidence

The preserved repaired-root test log records `279 passed in 1455.42s (0:24:15)`. The historical independent audit additionally records the frozen/repaired packaging failures and their repairs rather than deleting them. The standalone rank/orbit cold run and character regeneration logs are also preserved in the repository.

## Literature boundary

The current public literature still supports the repository's narrow novelty framing: the number 81 was known analytically, and the low-degree Hilbert coefficients were published, while the central 2026 papers described explicit determination of all 81 invariants / the full 10D self-dual-five-form classification as open or incomplete. No claim of absolute priority over unpublished work follows from a literature search.

## Remaining nonfatal hardening items

1. `science/rank81/validate_input` could be stricter about the frozen scientific profile (degree multiset/order, connectedness, duplicate graph definitions, and maximum edge multiplicity four). The current hash binding and rank proof make this nonfatal, but stricter validation would make accidental input mutation fail earlier.
2. `science/rank81/plan()` retains a diagnostic field named `float64_exact_bound_at_largest_prime` hard-coded to the older prime 32749 although the final fresh witness uses 50021. The actual arithmetic guard uses the runtime prime and is correct; the diagnostic field should be renamed to say it is a reference-prime diagnostic or removed.
3. A clean Linux CI workflow should independently run the root tests, standalone rank/orbit recomputation and D5 character regeneration. Existing audit logs are strong, but remote CI would improve platform-independent reproducibility.
4. Paper 1 should continue to exclude stress-flow/spinor follow-up claims unless their separate mentor gates are closed.

## Execution boundary of this audit

The repository's existing frozen audits include full tensor recomputations and large test suites. In this review environment, direct shell access to GitHub was unavailable and the connected GitHub integration rejected all write operations with HTTP 403. The repository-wide suite and standalone tensor program therefore could not be freshly executed from a clone here. Core source files and frozen evidence were inspected through the connected GitHub interface, raw run logs were checked, and the D5 character result was independently re-derived outside the repository. A future CI run should close this platform-execution boundary.
