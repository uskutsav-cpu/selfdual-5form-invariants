# Independent audit — FAIL / STOPPED

Frozen target: [`2b7663bbf5a06d1340973434f195a84ae2773e8f`](https://github.com/uskutsav-cpu/selfdual-5form-invariants/tree/2b7663bbf5a06d1340973434f195a84ae2773e8f), branch `roadmap/verified-classification`. Audit date: 7 September 2026, America/Chicago.

**The audit did not pass. A fresh source-paper transcription differs from the frozen degree-ten implementation for candidates 10–12.** The requested stop rule was invoked. No frozen data or code was repaired, no audit commit was made, no PR was opened, and nothing was merged to `main`. This report records a failed release gate, not a refutation of the rank-81 graph result and not a new scientific claim.

The full frozen graph recomputation and four independent integer determinants passed. Several further required checks were not reached. An incomplete audit cannot be promoted to PASS because the completed numerical checks agree.

## Blocking discrepancy: source transcription

An independent reviewer downloaded the original [arXiv v2 PDF](https://arxiv.org/pdf/2509.14350v2) and [TeX source](https://arxiv.org/src/2509.14350v2), visually inspected the colored brackets, and wrote `source-review/manual-transcription.md` **before reading the frozen implementation**. Command `source_012_freeze_manual_transcription` recorded its SHA256; the implementation was first read in `source_013_read_frozen`.

The relevant source is PDF printed page 25, §4.1.4, the degree-ten list around equation (4.24), TeX labels `I1010`, `I1011`, `I1012`. Original TeX lines 1642–1653 explicitly encode red brackets and specify that red operations act after black operations. Let Q be the tensor already antisymmetrized in its first five slots, using zero-based array axes 0–4.

| Candidate | Independently read source operation | Frozen implementation |
|---|---|---|
| `P10_10` | Antisymmetrize the final two slots, axes `(4,5)`, of the first Q after its first-five antisymmetrization. | Default `reading="outer"` leaves it unchanged. The optional `nested` variant supplies this pair operation. |
| `P10_11` | Antisymmetrize the trailing triple, axes `(3,4,5)`, on **each of the final three Q factors**, after the black operations. | Default leaves all three unchanged. The optional `nested` variant antisymmetrizes only axes `(4,5)` on the third factor, and does not supply the other two triple operations. |
| `P10_12` | The same three trailing-triple operations, with its own displayed index arrangement. | The same missing/default and incomplete/optional operations as candidate 11. |

Exact frozen locations are [`published_degree10_invariants.py:395`](https://github.com/uskutsav-cpu/selfdual-5form-invariants/blob/2b7663bbf5a06d1340973434f195a84ae2773e8f/src/sdinv/published_degree10_invariants.py#L395), the candidate functions at lines 406, 429, 451, primary registry entries at lines 529–549, and `BRACKET_STAGES` at lines 578–584. The last table labels these entries “black only (nested)”, contradicting the explicitly colored source. The code already marks these readings `AMB-02` and does not assert that either is definitively the source formula; the new source read resolves the bracket-color issue and shows that its two implemented alternatives do not exhaust the printed triple operations.

This establishes a **source/program transcription mismatch**. No corrected tensor evaluations were run after discovery. It does **not** establish that the resulting scalar polynomials are unequal, that the atlas rank changes, or that the product-space intersection changes. Redundancies or identities could affect that numerical consequence; they require a separately authorized repair and fresh evaluation. Therefore the frozen 12×14 atlas and one-dimensional product intersection cannot be certified here as statements about the literal source list. Their possible validity for the frozen qualified implementation is a separate question.

Evidence: `source-review/source-conflict-evidence.json`, `source-review/manual-transcription.md`, and the source review report. The exact original downloads are preserved in the local audit workspace; download URLs, SHA256 hashes, extracted evidence, and retrieval logs are supplied with this report. The evidence bundle does not need the entire original paper to reproduce the discrepancy.

## Requested gates

“PARTIAL” and “NOT RUN” are unsatisfied requirements, not passes. Individual passed checks do not change the overall FAIL / STOPPED disposition.

| # | Requested check | Status | Evidence / limit |
|---:|---|---|---|
| 1 | Completely fresh frozen checkout | PASS | Remote clone with `--no-checkout`, detached checkout of exact hash; clean status before setup and after stop. No earlier work/checkpoints/intermediates imported. |
| 2 | Fresh environment and every test suite | PARTIAL | New isolated venv. Root: **275 passed**. Bridge: **85 passed, 1 skipped**. Both release-candidate copies and the portable archive suite were not run. |
| 3 | Recompute all 81 values and Jacobian rows at all four frozen cells | PASS | `recompute-frozen-four`, exit 0; all **324 graph evaluations and 324 rows**, using frozen production code. |
| 4 | Independent four minor determinants | PASS | New standard-library-only integer Bareiss implementation; all four residues exactly match. No repository imports. |
| 5 | New prime and post-freeze seed, identical ordered 81 functions | NOT RUN | A new random seed/point was generated but not evaluated. No new prime witness was produced. |
| 6 | Mathematical conventions and graph/sign audit | PARTIAL | Independent star², dimension, integral directions, graph topology and ordered formulas pass. Graph-relabeling/automorphism sign tests were not completed. |
| 7 | Independent derivative oracle at fresh random points | NOT RUN | Candidate forward-dual evaluator written and contraction paths profiled only; no oracle value or derivative comparisons executed. Existing production tests are not a substitute. |
| 8 | Multiple fresh exact rotations and genuine boosts, all 81, multiple cells | NOT RUN | Existing suite checks ran; requested new all-81 transform campaign did not. |
| 9 | Source-paper degree-eight and degree-ten mappings | **FAIL** | Independently transcribed source conflicts with degree-ten bracket programs. Degree-eight matrix/product correction and degree-ten atlas/intersection were not independently numerically validated. |
| 10 | Independent degree-twelve polynomial rank 10+62=72 | NOT RUN | No independent polynomial-space computation performed. This is separate from the rank-81 functional check. |
| 11 | Comprehensive current prior-literature search | PARTIAL | 32 queries and primary-source reads; no prior explicit basis identified in reviewed sources. Coverage remains bounded; no novelty or absence claim. |
| 12 | Separate clean portable extraction, all manifest hashes, entire suite | NOT RUN | Stopped before extraction. |
| 13 | Claim-by-claim manuscript proof audit and downgrades | PARTIAL | A partial claim ledger and proposed qualification language were prepared. No frozen manuscript edits made after stop. |
| 14 | Audit report, evidence, commands, hashes, weaknesses | COMPLETE REPORT OF FAILURE | This report, command appendix, source evidence, partial reviewer reports and hashed bundle. |

## Completed numerical observations

| Prime | Seed | Frozen expected determinant | Independent integer Bareiss residue | Full production graph recomputation |
|---:|---:|---:|---:|---|
| 32749 | 20260907 | 20345 | 20345 | PASS |
| 32749 | 20260908 | 30761 | 30761 | PASS |
| 32719 | 20260907 | 1653 | 1653 | PASS |
| 32719 | 20260908 | 2167 | 2167 | PASS |

The independent determinant script computes each complete integer determinant before reducing modulo its prime; it is independent of `RankSieve`, `determinant_mod`, and the verifier. Its inputs are the stored matrices, so the production recomputation is a distinct necessary check. The independent derivative oracle was not completed; common evaluator risk therefore remains despite agreement.

The independent convention implementation counts permutation inversions directly and verifies the output-first Hodge convention with metric `diag(-1,+1,...,+1)`, all 252 complement relations, star²=+1, and the identity block of the 252×126 integral coordinate matrix. Its direction digest matches the certificate. It independently validates every ordered edge list and reconstructs the corresponding adjacency matrix and displayed Einstein formula. The graph audit verifies all 81 are connected, loopless and five-valent, with exactly one metric per contracted edge. The report carefully distinguishes commutative scalar-factor ordering from parity induced by permutations of alternating tensor slots; full numerical relabeling checks remain unfinished.

## Environment, recording and stop behavior

Audit root:

`/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01`

The immutable source is `checkout/`; the isolated new venv is `environment/`. New audit scripts, source downloads, logs, caches and reports all live under this newly created root. No old virtual environment or system-site packages were used. Package downloads used `--no-cache-dir`; source artifacts and fresh Python state came from the frozen checkout and new processes.

Platform: macOS 26.5.1, arm64. CPython 3.13.5, Clang 16.0.0; NumPy 2.5.1; opt_einsum 3.4.0; pynauty 2.8.8.1; pytest 9.1.1; pip 25.1.1. `environment-freeze` captures all installed packages, including transitive versions. The frozen lock file omits opt_einsum although `requirements.txt` declares it; after installing the lock, the declared requirements were installed without changing the source. This is a reproducibility weakness: the lock alone is incomplete, and the additional dependency was not pinned by it.

`run_command.py` records exact argv, working directory, process ID, environment overrides, start/end timestamps, wall runtime, exit code, separate stdout/stderr, and both log SHA256 hashes. Each command uses a unique directory and refuses overwrite. `PYTHONNOUSERSITE=1`; Python/cache paths point inside this new audit root; BLAS/OpenMP thread limits are 1. The record captures task-specific environment overrides, not a dump of secret-bearing inherited environment variables. Scientific computations and tests used this recorder. Bootstrap cloning, ordinary directory/source/log reads, tool-driven web searches, stop attempts and report assembly were not themselves recursively wrapped; web searches have separate retrieval logs. Thus the record is comprehensive for executed scientific commands, not a claim that every UI/tool action has a subprocess exit code.

The bridge skip is `test_full_schedule_has_eighty_three_candidates_with_no_silent_gaps[32749]`: its optional third-party historical archive was absent. Its code checks `SD5_ARCHIVE` or an old workspace default and skips if the file does not exist. The archive was neither imported nor reconstructed. This skipped boundary check remains unverified.

The stop marker records Unix time 1788827740.1471748. The graph recomputation and bridge suite had already completed. An immediate attempt to terminate the still-running root suite received sandbox `PermissionError`; the escalated retry found it already exited. Its recorded finish is 1788827758.913698, approximately 18.77 seconds after the stop marker. No new scientific command was launched after the stop. This termination race is disclosed rather than silently calling the root suite aborted. Subsequent commands only inspected provenance, recorded environment metadata, preserved evidence, and assembled reports. Final `git status --porcelain=v1 --untracked-files=all` is empty.

## Weaknesses, unproved assumptions and required qualifications

1. The source transcription discrepancy blocks source-identification claims. Its numerical consequences remain unmeasured. Existing `AMB-02` qualifications do not establish that the frozen default implements the visibly colored formula.
2. Four production recomputations and independent determinants passed, but no new-prime witness or independently executed derivative evaluator was produced. Production tests can share implementation assumptions.
3. Exactness still depends on correctness of the frozen bounded arithmetic, tensor contraction planning/execution, coordinate construction and graph-to-polynomial conventions. Independent conventions and integer determinants reduce, but do not eliminate, common-path risk.
4. Characteristic-zero inference from a correctly computed nonzero modular minor is an algebraic argument about an integral polynomial. It does not establish a full invariant ring, all syzygies, rational generation, global orbit separation, or completeness of a literature mapping. The upper bound and generic-orbit argument require their own stated mathematical evidence; see the partial manuscript ledger.
5. Degree-eight rational reconstruction and holdouts are empirical identity evidence unless an exact polynomial identity or a fully certified spanning basis establishes the identity. The product correction cannot be dropped merely because the quotient matrix is square. Neither its independent numerical checks nor a symbolic proof was completed here.
6. The degree-ten reconstruction pipeline uses inherited modular coordinate files and an inherited holdout. Its rank/intersection evidence must be described as applying to explicitly defined frozen candidate readings; it is not a fresh source-paper tensor evaluation. Correct source transcription must precede a renewed atlas computation.
7. The degree-twelve 72-dimensional polynomial statement was not independently checked. It must not be inferred from functional rank 81 or from a single-point Jacobian rank. Attaining the supplied Hilbert bound also depends on the applicability of that bound.
8. The primary paper itself has a prose inconsistency: §4.1.4 says 64 degree-twelve invariants and cumulative 83, while equation (4.2) has exponent 62. The frozen 62 agrees with the equation and the cumulative arithmetic. This is a source inconsistency, not an observed failure of the frozen degree-twelve numerical result.
9. Literature search was broad but incomplete: some leads were abstract-only, some retrievals failed, and there was no exhaustive MathSciNet/zbMATH or citation-database traversal. “First” or “no prior equivalent exists” is not supported.
10. Archived test copies, portable manifest verification, new Lorentz tests, and the complete manuscript ledger remain outstanding. The bridge suite also has one explicit skip.
11. No corrected result may inherit this frozen certificate's approval. Any authorized repair needs separate provenance, a new frozen target, reruns of affected checks and all unfinished gates. This report does not authorize a repair, commit, PR or merge.

The partial reviewer reports preserve finer distinctions and proposed wording. They are advisory failure evidence, not edits to the frozen manuscript. The user requested stopping at any differing result; preserving the target takes precedence over silently making the audit pass.

## Evidence navigation

- `COMMANDS.md`: exact recorded commands, working directories, runtimes, exit codes, and SHA256 of both output streams.
- `commands/<name>/command.json`, `stdout.log`, `stderr.log`: raw execution records.
- `math-review/PARTIAL_MATH_REPORT.md`: independent method, mathematical conventions, observed passes and unfinished checks.
- `source-review/`: frozen manual transcription, mismatch evidence, source report, source hashes and retrieval records.
- `literature-review/`: partial primary literature search, queries/retrieval logs, and partial manuscript ledger.
- `ARTIFACTS.sha256`: hashes of evidence-bundle files; the manifest excludes itself.

No PASS certificate, commit, PR, or merge follows from this report.
