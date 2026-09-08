# Source repair and independent exact evaluation verification

This is phase 02, explicitly authorized after phase 01 returned FAIL for the frozen commit `2b7663bbf5a06d1340973434f195a84ae2773e8f`. The frozen source-reading failure remains part of the audit. No old evaluated tensor values were reused as new evidence.

## Findings

The original arXiv v2 TeX and colored PDF resolve red brackets in candidates J10–J12. J10 requires a normalized trailing-pair projector on the first Q. J11 and J12 require normalized trailing-triple projectors on each of their last three Q factors. The corrected production registry selects these source programs; old defaults and old variants are explicitly legacy. Candidate 4's red group has four slots; candidate 9's has three. All source metric edges carry one inverse metric and all projectors retain their normalizations.

The freshly computed exact octic map agrees with the frozen product-corrected 7×7 map, in both directions. The six inverse product corrections are `0, -3/14, 7/72, -1/28, -593/31104, -61543/2612736`.

The freshly computed corrected decic map has 12×14 entries, source rank 12, primitive quotient rank 11, union with the two products rank 13, and a one-dimensional product intersection. Its exact witness is

`J6 + (5/6)J5 - J2/20 - (11/1008)J1 = -(13/63) I4_1 I6_1`.

Only rows 10,11,12 differ from the frozen decic map. Their difference has rank 3 even in the first twelve, primitive graph coordinates. Thus old claims about harmless quotient changes from incomplete bracket variants do not establish the behavior of the corrected source programs.

The literal primary octic list has rank 6 and rank 6 after adjoining the quartic square. The literal hatted list H1–H6 has rank 5, or rank 6 with the quartic square. The selected list T1–T5,H1 plus the square has rank 7. These are validation observations about the literal source lists; the source's irrep trace-subtraction prose does not define an extra projector to impose silently.

## Evidence chain and scope

1. `manual-transcription-preimplementation.md` was authored from original source before the phase 01 implementation reads. It specifies source equation identifiers, dummy index order, trace conventions, and bracket colors. Its authorized reuse is disclosed; old evaluated arrays are not used.
2. `source_scalar_oracle.py` independently builds F,M,N,Q,T,P and the 24 source scalars. It imports no production source/block/bracket code. It uses exact modular binary contractions, with integer and floating-point dot-product bounds checked before execution.
3. A fresh pilot compares Q's ten-shuffle implementation to full 120-term antisymmetrization, then compares M,N,Q,P and all 24 source scalars against the production implementations. Small direct five-factor contractions in dimension 3 separately check the repaired red programs on arbitrary covariant arrays and distinguish their legacy counterparts.
4. Five fitting primes each use fourteen fresh dense points and two held-out points. Three further fresh points use the distinct prime 32771 and disjoint seeds. All83 points agree with the final exact maps. This is useful crosschecking, but it is not the polynomial identity proof.
5. Fourteen new common binary coordinate vectors were evaluated at seven primes, yielding 98 new modular evaluations. The exact certificate stores every vector, point-file hash, denominator, absolute bound, residue, and reconstructed integer numerator. The CRT modulus is 40274678413255193510345405666987, strictly greater than twice every relevant numerator bound; the maximum bound is 352866326400000000000000000000.
6. Exact Fraction elimination gives graph evaluation ranks 7 and 14, exact source coordinate matrices, the octic inverse, and the decic intersection algebra. The identity implication is CONDITIONAL ON THE PUBLISHED HILBERT DIMENSIONS 7 AND 14 and the analytic invariance of the displayed tensor contractions. This subtask does not independently derive those Hilbert dimensions. Evaluation is injective on each invariant space under those upper bounds, so exact evaluation equality then gives a polynomial identity.

The graph-only rank81 minors are a separate certificate. The frozen source-reading mismatch does not itself invalidate them.

## Corrections and unsuccessful attempts retained

The first independent Q shuffle implementation used a transpose rather than its inverse. Its explicit block-comparison check failed before any point was accepted, and it was corrected; the accepted pilot additionally compares with the full 120-term projector. A subsequent pilot reached successful tensor comparisons but failed because the graph definition loader omitted degree8 generators; the union of the degree8 and degree10 definition manifests fixed the loader. Both failed command logs remain intact.

Five-prime bounded rational reconstruction succeeded for the octics and J1–J10 but was insufficient for ten coefficients in J11/J12. No partial rational atlas was emitted as verified. The exact binary-point CRT approach avoided guessing those coefficients. `diagnostic-fiveprime-*.json` preserves the diagnostic, including null entries where bounded reconstruction failed. It is not the authoritative map.

A source module docstring cleanup and the H8_2 equation citation update occurred after dense evaluation, with no scalar logic changes. Dense point files retain the hashes of the files present at evaluation. The binary source values use the independent oracle, which remained unchanged throughout accepted evaluations. `exact-certificate-sha256.json` pins the final exact certificate/maps; older hash snapshots are explicitly historical.

## Main execution records

All execution is logged under the phase 02 audit `commands/` directory, using fresh environment dependencies and one tensor process with numerical threads set to 1. The key names are `source2_011_small_source_tests`, `source2_017` (accepted pilot), `source2_019`, `source2_021`, `source2_023`, `source2_025`, `source2_028_prime32717`, `source2_031_holdout32771`, `source2_034_binary_pilot`, `source2_037_binary_pilot_rank`, `source2_038_binary_six_primes`, `source2_050_build_qualified_exact_certificate`, and `source2_051_compare_qualified_exact_to_frozen`. See each `command.json` for exact arguments, timestamps, exit status, and stdout/stderr hashes; full command names for early sequence numbers are preserved there.

The certificate input files are frozen after verification. Its local calculation scripts preserve the original phase 02 directory assumptions. The independently written portable verifier checks the certificate without rerunning tensor contractions; replay instructions are supplied by the parent integration.

Independent second-verifier result: PASS. It checks all 98 hashed point files, 630 integer CRT entries, exact graph minors, rational maps, ranks, and intersection. Its record is `math-review/source_crt_independent_verification.json`; final source certificate SHA256 is `01f9ab8d8f966827f820541a6e0bfec8e8bf64f710ec5b9f3be6dc825c61ed12`. The final direct source tests pass (4 tests), and the independent integral coordinate convention matches the repository portable context at a disjoint held-out point.

Post-certificate metadata correction (`source2_058`): the legacy J10–J12 registry now describes its actual no-red outer programs instead of inheriting the corrected red descriptions. Only `src/sdinv/published_degree10_invariants.py` metadata and `tests/test_published_degree10_source_reading.py` registry assertions changed. Three targeted registry/stage tests passed (`source2_059`). No evaluator scalar logic, independent oracle, certificate input hash, exact map, or CRT value changed. `final-production-source-sha256.json` records the final production source hashes; earlier production snapshots retain their historical meanings.

The independent portable verifier (`python scripts/verify_independent_audit.py`, or `--source-only`) passed against the integrated files and canonical maps. Its deliberate certificate and map corruption checks both rejected altered data at the intended checks; originals remained unchanged.
