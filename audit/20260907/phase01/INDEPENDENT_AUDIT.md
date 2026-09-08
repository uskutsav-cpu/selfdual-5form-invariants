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

---

# Recorded command appendix

These are the exact child argv rendered with shell quoting. The working directory is recorded separately. Wrapper setup and environment overrides are retained in each command.json. A zero subprocess exit code is not itself a scientific pass: some retrieval helpers catch and record network failures. Source reports identify successful downloads. Post-stop entries are provenance/reporting operations only.

## checkout-frozen

```sh
git checkout --detach 2b7663bbf5a06d1340973434f195a84ae2773e8f
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01/checkout`

UTC start: 2026-09-08T00:21:38.679013+00:00; runtime: 0.506924916 s; exit code: 0.

stdout SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

stderr SHA256: `9ec8c1ebd5e031633603c73c9f9e697b96b0d47a064c483b6cd132909780d4a4` (94 bytes).

## source-status

```sh
git status --porcelain=v1 --untracked-files=all
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01/checkout`

UTC start: 2026-09-08T00:21:39.309758+00:00; runtime: 0.156453125 s; exit code: 0.

stdout SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

stderr SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

## environment-create

```sh
python3 -m venv ../environment
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01/checkout`

UTC start: 2026-09-08T00:21:39.557088+00:00; runtime: 5.514950958 s; exit code: 0.

stdout SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

stderr SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

## math_initial_inspect

```sh
python3 -c 'from pathlib import Path; p=Path("checkout"); print(Path("run_command.py").read_text()); print("CHECKOUT FILES\n"+"\n".join(str(x.relative_to(p)) for x in p.iterdir())); print("CERTIFICATE\n"+(p/"results/rank81_certificate.json").read_text()[:12000])'
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01`

UTC start: 2026-09-08T00:22:52.503673+00:00; runtime: 0.088192042 s; exit code: 0.

stdout SHA256: `2cf7f774565d2ff8300522dc18a96a9940454a01587dbed9775891ac5afc6d61` (14534 bytes).

stderr SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

## source_001_wrapper_info

```sh
python3 -c 'from pathlib import Path; print(Path("run_command.py").read_text())'
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01`

UTC start: 2026-09-08T00:23:08.475324+00:00; runtime: 0.061993500 s; exit code: 0.

stdout SHA256: `9d5f346a817e5ab2827947810c86bc0b340258c57b89eb9b59a694103241603c` (2210 bytes).

stderr SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

## literature-manuscript-initial-read-001

```sh
sh -c 'cat paper/manuscript.tex; printf "\n---FILES---\n"; rg --files paper | sort'
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01/checkout`

UTC start: 2026-09-08T00:23:20.491856+00:00; runtime: 0.071459375 s; exit code: 0.

stdout SHA256: `9b617879ead0c7e3cd80e4ff1de8ecd327e1578fa380ce45711154acce6eda7b` (8331 bytes).

stderr SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

## environment-install

```sh
../environment/bin/python -m pip install --no-cache-dir -r requirements-lock.txt
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01/checkout`

UTC start: 2026-09-08T00:23:21.845525+00:00; runtime: 37.506159083 s; exit code: 0.

stdout SHA256: `9083e8ec8785a5569b864541a5fbf6e4472eddc12a774eaf120aa57cf02387cc` (2884 bytes).

stderr SHA256: `4f109f92d2862477c32271db1f61d4d054842bee7cc58b90b180803f0792b4ba` (230 bytes).

## math_schema_inspect

```sh
python3 -c 'from pathlib import Path; import json; p=Path("checkout"); Path("math-review").mkdir(exist_ok=True); c=json.loads((p/"results/rank81_certificate.json").read_text()); print("WITNESS KEYS",c["witnesses"][0].keys()); print("WITNESS METADATA", [{k:v for k,v in w.items() if k not in ("jacobian","coordinates","values","invariant_ids")} for w in c["witnesses"]]); print("RELEVANT FILES\n"+"\n".join(str(x.relative_to(p)) for d in ["src","tests","docs","results","manuscript"] for x in (p/d).rglob("*") if x.is_file() and not any(s in x.parts for s in ["tmp","checkpoints","caches"]))); print("README\n"+(p/"README.md").read_text())'
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01`

UTC start: 2026-09-08T00:23:37.600936+00:00; runtime: 0.101672041 s; exit code: 0.

stdout SHA256: `80d57d00cc1301650bca96df9871976426a7d580699d555ce1e9836282eb5c07` (41071 bytes).

stderr SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

## math_read_conventions

```sh
python3 -c 'from pathlib import Path; import json; p=Path("../checkout"); files=["src/sdinv/forms.py","src/sdinv/contract.py","paper/manuscript.tex","results/rank81_basis.json"]; print("FILES\n"+"\n".join(str(x) for x in (p/"paper").iterdir())); [(print("FILE",f), print((p/f).read_text()[:65000])) for f in files if (p/f).exists()]'
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01/math-review`

UTC start: 2026-09-08T00:23:56.960371+00:00; runtime: 0.117011708 s; exit code: 0.

stdout SHA256: `5c5216b0806323ba4cc5e731faded0d22157e3548df2031dd14eda6a9d21b398` (101240 bytes).

stderr SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

## source_002_fetch

```sh
python3 -
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01`

UTC start: 2026-09-08T00:24:20.536078+00:00; runtime: 0.561682041 s; exit code: 0.

stdout SHA256: `f360cf84f0393336d83f3ec27bfe84b13254e730973d4dcfe1fb02cd19647eb4` (492 bytes).

stderr SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

## literature-manuscript-artifact-inventory-002

```sh
sh -c 'nl -ba paper/manuscript.tex; cat paper/tables/certificate_cells.tex; rg --files | rg "(rank81|literature|order12|order10|order8|invariant|README|test|\.tex$)"'
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01/checkout`

UTC start: 2026-09-08T00:24:22.890328+00:00; runtime: 0.152780875 s; exit code: 0.

stdout SHA256: `152e8e10b190c3bb07389d94bb63273a0aef48cce11ad7baa37953aa5b24eb77` (20747 bytes).

stderr SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

## math_bareiss_minors

```sh
/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01/environment/bin/python bareiss_minors.py
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01/math-review`

UTC start: 2026-09-08T00:24:49.665773+00:00; runtime: 2.330639291 s; exit code: 0.

stdout SHA256: `63c20c31e82cd89144c2f71a50b050f0d0a86808a873ebdc97798377f143a711` (3809 bytes).

stderr SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

## literature-manuscript-artifact-read-003

```sh
sh -c 'cat scripts/verify_rank81.py; cat scripts/graph_to_latex.py; cat scripts/validate_rank81_lorentz.py; rg -n "^def |def test|oracle|boost|Euler|euler|checkpoint|submit|primitive|product|quotient" scripts/search_rank81.py scripts/map_literature_basis.py src/sdinv/*.py tests/test_core.py tests/test_graph_to_tensor.py tests/test_roadmap.py'
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01/checkout`

UTC start: 2026-09-08T00:24:56.148978+00:00; runtime: 0.074331875 s; exit code: 0.

stdout SHA256: `f2e9fcd0abf8ab3f4ace74e6e2f5d8c38aaaedb227e0dbf2be407267545c06b4` (45845 bytes).

stderr SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

## source_003_fetch_network

```sh
python3 -
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01`

UTC start: 2026-09-08T00:24:59.941685+00:00; runtime: 0.771135042 s; exit code: 0.

stdout SHA256: `dd2011cc9c41b38032f503c191299b51c329825b2d649b70522dde232b7afd22` (666 bytes).

stderr SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

## environment-declared-requirements

```sh
../environment/bin/python -m pip install --no-cache-dir -r requirements.txt
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01/checkout`

UTC start: 2026-09-08T00:25:13.064561+00:00; runtime: 2.136376416 s; exit code: 0.

stdout SHA256: `9f0d99bebff98bdc16aea3d9d90558d02c18764cb0e6da120a42641bbdf8a547` (1890 bytes).

stderr SHA256: `4f109f92d2862477c32271db1f61d4d054842bee7cc58b90b180803f0792b4ba` (230 bytes).

## literature-manuscript-certificate-read-004

```sh
sh -c 'nl -ba src/sdinv/certificate.py; nl -ba scripts/search_rank81.py; nl -ba scripts/map_literature_basis.py; nl -ba tests/test_roadmap.py; rg -n "nonzero|independent|functional|span|basis|rank 81|complet" manuscript/main.tex manuscript/prd/main.tex manuscript/jhep/main.tex manuscript/prl/main.tex submission_candidate/main.tex'
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01/checkout`

UTC start: 2026-09-08T00:25:23.735662+00:00; runtime: 0.076522334 s; exit code: 0.

stdout SHA256: `135f44caa322495940ce34824372e30bacc197d76a20549676a415d2d6dd06a3` (78562 bytes).

stderr SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

## source_004_source_extract

```sh
python3 -
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01`

UTC start: 2026-09-08T00:25:30.187589+00:00; runtime: 0.082826333 s; exit code: 0.

stdout SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

stderr SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

## source_005_curl_pdf

```sh
curl -fL --max-time 45 https://arxiv.org/pdf/2509.14350v2 -o source-review/arxiv-v2.pdf
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01`

UTC start: 2026-09-08T00:25:52.659755+00:00; runtime: 0.399655458 s; exit code: 0.

stdout SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

stderr SHA256: `1cfdb6f8e7b0e3b4f8b35101880bea41378c7e47788a152e8789cad9ee291d2c` (317 bytes).

## math_convention_source_details

```sh
python3 -c 'from pathlib import Path; import json; p=Path("../checkout"); print((p/"src/sdinv/graph_to_tensor.py").read_text()); print((p/"src/sdinv/certificate.py").read_text()[:21000]); print("BASIS TOP KEYS",json.loads((p/"results/rank81_basis.json").read_text()).keys())'
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01/math-review`

UTC start: 2026-09-08T00:25:53.709191+00:00; runtime: 0.105740333 s; exit code: 0.

stdout SHA256: `94591f4ffb46825e488805b8f0eb98fe176499715d520a681a8bae0a771b5627` (15232 bytes).

stderr SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

## source_006_curl_source

```sh
curl -fL --max-time 45 https://arxiv.org/src/2509.14350v2 -o source-review/arxiv-v2-source.tar
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01`

UTC start: 2026-09-08T00:25:55.349464+00:00; runtime: 0.213214666 s; exit code: 0.

stdout SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

stderr SHA256: `3b48aa02c1f7bb98b86f5a8c17b221610188274c0ebf38150ae03a0e19006af4` (396 bytes).

## literature-manuscript-focused-artifacts-005

```sh
sh -c 'nl -ba tests/test_roadmap.py; nl -ba src/sdinv/published_degree8_invariants.py; nl -ba src/sdinv/latex.py; rg -n "gradient|concaten|functional_increment|polynomial|rank|samples|basis" scripts/degree12_pipeline.py | head -90; sed -n "730,825p" manuscript/main.tex; sed -n "345,405p" manuscript/main.tex'
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01/checkout`

UTC start: 2026-09-08T00:26:05.457072+00:00; runtime: 0.116867459 s; exit code: 0.

stdout SHA256: `feeb4d4b1d0e7d44fb81ffef66b8a9490e5e4e516af2fb89b0bafee786f2b7ab` (28558 bytes).

stderr SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

## source_007_pdf_skill_and_extract

```sh
python3 -
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01`

UTC start: 2026-09-08T00:26:14.265128+00:00; runtime: 0.134069333 s; exit code: 0.

stdout SHA256: `74b2b30f897bc4ea0aaf8a996cbc6daa1c345a2e1640f5d2d6b4574acbab2f43` (7425 bytes).

stderr SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

## source_008_tex_and_pdf_tools

```sh
python3 -
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01`

UTC start: 2026-09-08T00:26:31.247412+00:00; runtime: 0.073973084 s; exit code: 0.

stdout SHA256: `06ebfc54d08e4d85d351941892cc5f756624a8f712fc9fe096a0fda6b271e081` (14104 bytes).

stderr SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

## source_009_pdf_text

```sh
pdftotext -layout source-review/arxiv-v2.pdf source-review/arxiv-v2.txt
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01`

UTC start: 2026-09-08T00:26:55.823913+00:00; runtime: 0.690816541 s; exit code: 0.

stdout SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

stderr SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

## source_010_pdf_pages

```sh
python3 -
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01`

UTC start: 2026-09-08T00:26:56.949487+00:00; runtime: 0.119613417 s; exit code: 0.

stdout SHA256: `80c3867fc5f94f8ba2ea06902b09a60c63b7b8383ff177d52a2d86df0e42b24a` (1911 bytes).

stderr SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

## source_011_pdf_render

```sh
pdftoppm -f 22 -l 25 -r 120 -png source-review/arxiv-v2.pdf source-review/page
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01`

UTC start: 2026-09-08T00:27:13.470028+00:00; runtime: 1.671875917 s; exit code: 0.

stdout SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

stderr SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

## literature-manuscript-json-summary-006

```sh
python3 -c 'import json,hashlib, pathlib; paths=["results/10d_order8.json","results/10d_order10.json","results/10d_order12.json","results/rank81_basis.json","results/rank81_certificate.json","results/rank81_lorentz.json","results/order8_change_of_basis.json","results/order10_change_of_basis.json"]; print(json.dumps([{ "path":p,"sha256":hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest(),"keys":list((d:=json.loads(pathlib.Path(p).read_text()))),"summary":{k:(len(v) if isinstance(v,list) and (k in ["generators","invariants"] or len(v)>10) else v) for k,v in d.items() if k not in ["prime_witnesses","directions","jacobian","adjacency_matrix","matrix_12x14","graph_to_literature","literature_to_graph","sources","source_files"] and not isinstance(v,dict) and k not in ["witnesses"]},"witness_summary":[{k:v for k,v in w.items() if k in ["prime","seed","rank","determinant_mod_p","cumulative_rank_by_degree"]} for w in d.get("witnesses",[])]} for p in paths],indent=2))'
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01/checkout`

UTC start: 2026-09-08T00:27:24.519907+00:00; runtime: 0.091568583 s; exit code: 0.

stdout SHA256: `48007b1aef9faa602d5cb7f98b9f694da848cb99bfe32d3a7c7e9e61d632cafa` (14452 bytes).

stderr SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

## math_conventions

```sh
/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01/environment/bin/python independent_conventions.py
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01/math-review`

UTC start: 2026-09-08T00:27:36.825834+00:00; runtime: 0.456143542 s; exit code: 0.

stdout SHA256: `0e515184c6789578d85ec6fa8c9de3bc2c337fcce27b1444bef37679c8700e7f` (1193 bytes).

stderr SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

## environment-freeze

```sh
../environment/bin/python -m pip freeze --all
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01/checkout`

UTC start: 2026-09-08T00:28:17.207773+00:00; runtime: 0.361149458 s; exit code: 0.

stdout SHA256: `74bf254dbe7f7960ff7b6e10909db602924148479c63b911eee6150467c72cf2` (138 bytes).

stderr SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

## root-pytest

```sh
../environment/bin/python -m pytest -x -vv -o addopts= -p no:cacheprovider
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01/checkout`

UTC start: 2026-09-08T00:28:17.733661+00:00; runtime: 461.184354125 s; exit code: 0.

stdout SHA256: `c6e028b0e6cff18f4e1549daa2bf8405bb27a020be1008adbb294100d56d1eff` (27976 bytes).

stderr SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

## recompute-frozen-four

```sh
../environment/bin/python -u scripts/verify_rank81.py --recompute
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01/checkout`

UTC start: 2026-09-08T00:28:18.935380+00:00; runtime: 208.173882916 s; exit code: 0.

stdout SHA256: `1d32792aa7fd338cebef286544f984c64a280cf0f87633cfa67b4de01be34d42` (661 bytes).

stderr SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

## bridge-pytest

```sh
../../environment/bin/python -m pytest -x -vv -o addopts= -p no:cacheprovider
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01/checkout/spinor_trace_bridge`

UTC start: 2026-09-08T00:28:20.289005+00:00; runtime: 225.607319125 s; exit code: 0.

stdout SHA256: `9efd1bec0d090e784e91c13b130c38354c36097f4434e18dea0794f4137a629f` (8163 bytes).

stderr SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

## source_012_freeze_manual_transcription

```sh
python3 -
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01`

UTC start: 2026-09-08T00:28:36.461889+00:00; runtime: 0.081439583 s; exit code: 0.

stdout SHA256: `d630b24d3063693c7c217098adf2bf495304b46874f2c491cb03a13a07b8f40a` (225 bytes).

stderr SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

## source_013_read_frozen

```sh
python3 -
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01/checkout`

UTC start: 2026-09-08T00:29:09.274050+00:00; runtime: 0.073943750 s; exit code: 0.

stdout SHA256: `db6130e8e91ce42d103c7cea1328c6c987d56e55f1ab1668662585ff4d4c76a3` (249093 bytes).

stderr SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

## math_oracle_profile

```sh
/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01/environment/bin/python independent_oracle.py --profile
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01/math-review`

UTC start: 2026-09-08T00:29:43.040184+00:00; runtime: 0.707443375 s; exit code: 0.

stdout SHA256: `dfe1ffd3471cc083c55b96c442f7c88192541d467a74763b1513a7946b7c4de5` (151 bytes).

stderr SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

## math_fresh_point

```sh
/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01/environment/bin/python -c 'import json,secrets,time; from pathlib import Path; seed=secrets.randbits(64); import random; p=32749; rng=random.Random(seed); d={"prime":p,"seed":seed,"created_unix":time.time(),"coordinate_generator":"Python random.Random(fresh secrets.randbits(64) seed), randrange(p) repeated 126 times","coordinates":[rng.randrange(p) for _ in range(126)]}; Path("fresh_point.json").write_text(json.dumps(d,indent=2)+"\n"); print(json.dumps(d))'
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01/math-review`

UTC start: 2026-09-08T00:30:00.221405+00:00; runtime: 0.080921041 s; exit code: 0.

stdout SHA256: `e8392596b184e24b75b28dbc7bee3eeb236ff9a52aa9cfa2c401129e89b444fa` (1046 bytes).

stderr SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

## source_014_package_discrepancy_only

```sh
python3 -
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01`

UTC start: 2026-09-08T00:36:08.735763+00:00; runtime: 0.042005708 s; exit code: 0.

stdout SHA256: `02385072b3e0a5de2f03c88a34220fcebf846808318af732f81a98a271fe075c` (1365 bytes).

stderr SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

## post-stop-source-status

```sh
git status --porcelain=v1 --untracked-files=all
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01/checkout`

UTC start: 2026-09-08T00:37:17.834717+00:00; runtime: 0.260032083 s; exit code: 0.

stdout SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

stderr SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

## post-stop-environment-metadata

```sh
../environment/bin/python -c 'import sys, platform, sysconfig, json, importlib.metadata; print(json.dumps({"python":sys.version,"executable":sys.executable,"platform":platform.platform(),"machine":platform.machine(),"implementation":platform.python_implementation(),"packages":{name:importlib.metadata.version(name) for name in ["numpy","opt_einsum","pynauty","pytest","pip"]}},indent=2))'
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01/checkout`

UTC start: 2026-09-08T00:37:18.236741+00:00; runtime: 0.121268209 s; exit code: 0.

stdout SHA256: `a4fbe76f619febda5f74342514141360a32c5da53843fae2426e94f2b1774ae5` (483 bytes).

stderr SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

## source_015_write_final_discrepancy_report

```sh
python3 -
```

Working directory: `/Users/swethasunilkumar/Documents/Codex/2026-09-07/here/work/independent-audit-20260907-01`

UTC start: 2026-09-08T00:38:04.091121+00:00; runtime: 0.040201833 s; exit code: 0.

stdout SHA256: `8c6652b04f7c051783f8de32c4cc70cb909c8736682d352208253415b3b9e9fb` (185 bytes).

stderr SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes).

