"""Build the audit report from completed command records; never infer a pass."""
from pathlib import Path
import hashlib
import json
import re
import shlex

A = Path(__file__).resolve().parents[1]
OLD = A.parent / "independent-audit-20260907-01"
REPO = A / "repair-checkout"
FROZEN = "2b7663bbf5a06d1340973434f195a84ae2773e8f"


def command(name, phase=2):
    origin = A if phase == 2 else OLD
    directory = origin / "commands" / name
    record = json.loads((directory / "command.json").read_text())
    assert record["status"] == "completed", name
    for filename, info in record["logs"].items():
        assert hashlib.sha256((directory / filename).read_bytes()).hexdigest() == info["sha256"]
    return record


required = ["repaired-root-pytest", "repaired-archived-trace-pytest-final", "archived-bridge-pytest",
            "portable-frozen-pytest", "portable-frozen-recompute", "fresh-rank-and-lorentz",
            "math_verify_exact_source_certificate", "math_portable_all_saved_evidence",
            "repaired-six-dimensional-two-prime", "repaired-final-source-and-cli-regressions",
            "repaired-historical-package-scan", "compile-paper-final", "render-paper-final"]
checks = []
for name in required:
    record = command(name)
    assert record["exit_code"] == 0, name
    checks.append({"name": name, "passed": True, "seconds": record["seconds"],
                   "argv": record["argv"], "logs": record["logs"]})

tests = [(1,"root-pytest","Frozen root"), (1,"bridge-pytest","Frozen root bridge"),
         (2,"archived-trace-pytest","Frozen historical tensor package"),
         (2,"archived-bridge-pytest","Frozen historical bridge package"),
         (2,"portable-frozen-pytest","Freshly extracted frozen portable package"),
         (2,"repaired-root-pytest","Repaired root, full run"),
         (2,"repaired-archived-trace-pytest-final","Restored historical tensor package, full run"),
         (2,"repaired-final-source-and-cli-regressions","Final source and CLI regression modules")]
rows = []
for phase,name,label in tests:
    record = command(name,phase)
    text = ((A if phase == 2 else OLD)/"commands"/name/"stdout.log").read_text()
    summary = [line.strip("= ") for line in text.splitlines() if re.search(r"\b(?:passed|errors|failed|skipped)\b",line)]
    rows.append(f"| {label} | {summary[-1]} | {record['exit_code']} | {record['seconds']:.3f} | `phase0{phase}/commands/{name}` |")

report = r'''# Independent audit and disclosed repair

**Frozen commit: FAIL. Corrected graph and source implementation checks: PASS,
with the explicit assumptions and one unavailable optional integration below.**

The frozen target is `FROZEN_COMMIT` on `roadmap/verified-classification`.
Phase 01 found a real source-transcription mismatch and stopped. Its report
is preserved unchanged at `audit/20260907/phase01/INDEPENDENT_AUDIT.md`.
The subsequent instruction to continue and work around blockers authorized
phase 02: two new remote clones, a new environment, fresh computations, and
a separate repair checkout. This report does not certify the frozen source
reading as correct. No merge to `main` is part of this work.

## Requested audit gates

| Gate | Result | Evidence and boundary |
|---|---|---|
| 1. Fresh frozen checkout | PASS | Both phases clone and detach the exact frozen commit; phase02 keeps its frozen clone immutable and repairs a separate clone. No prior numerical cache/checkpoint is reused. Independently authored script source is reused with provenance, then rerun. |
| 2. Fresh environment; every suite | FAIL in frozen historical packaging; repaired runs PASS with one optional integration SKIP | All discovered suites executed. Exact results appear below. The missing private third-party archive is not synthesized or treated as a passing test. |
| 3. Four frozen graph/Jacobian recomputations | PASS | `phase01/commands/recompute-frozen-four` and phase02 `portable-frozen-recompute`: all 324 graph values and 324 full 126-entry rows recomputed from the graph definitions. |
| 4. Independent four minors | PASS | Python integer Bareiss, no production rank/verifier imports: residues 20345, 30761, 1653, 2167 in the required cell order. `results/audit/math-review/bareiss_results.json`. |
| 5. New prime and postfreeze random seeds | PASS within inspected history | Prime50021 was absent from987 frozen tracked raw/expanded payloads; seeds16999642918068834541 and9932584768098142723 were freshly generated. Same ordered81. New minors35642 (50021),22345 (32749). Uncommitted external history cannot be excluded. |
| 6. Conventions and graph signs | PASS | Independent signature(1,9), star²=+1, dimension126, integral directions, all81 loopless5-valent formulas. All136 weighted automorphisms have positive induced sign;823 adjacent vertex checks,81 numerical relabelings and81 odd-slot swaps pass. |
| 7. Independent derivatives | PASS | Independent forward duals and reverse adjoints match all162 values and20,412 full Jacobian entries at two fresh points; value-only interpolation also checks degrees4,6,8,10,12. Shared arithmetic primitives are disclosed below. |
| 8. New Lorentz transformations | PASS | All81 graphs under four new rational rotations and four genuine boosts across two fresh field/seed cells; exact metric and determinant checks. `results/audit/root-review/fresh_lorentz_checks.json`. |
| 9. Source-paper octic/decic maps | FAIL frozen; corrected conditional certificate PASS | Independent primary PDF/TeX transcription identifies missing red brackets in J10–J12. Corrected source evaluated afresh;98 binary point evaluations reconstruct630 exact integers; independent CRT verifier passes. Octic product correction retained. Corrected decic span12, quotient11, product intersection1. Polynomial-map conclusion uses published Hilbert upper bounds7/14. |
| 10. Degree12 polynomial space | PASS lower bound; completeness conditional on published upper bound | Independent72×252 stacked-gradient matrices for10 products+62 graphs, exact72×72 minors43334 modulo50021 and12699 modulo32749. This proves homogeneous linear independence, separate from functional rank81. |
| 11. Current literature search | PASS for documented broad coverage; not exhaustive |47 recorded query strings and9 relevant primary works, including the 2026 graph-method publication. No prior explicit81 family found in inspected material; no novelty or priority claim follows. |
| 12. Fresh portable extraction | PASS for frozen archive |59 listed hashes verified,21 delivery tests pass, all four graph/Jacobian witnesses recomputed. The corrected archive's post-build hash/test record is a sidecar at `release/classification/PORTABLE_VERIFICATION.json`; it is created after packaging to avoid a circular archive hash. |
| 13. Manuscript claim ledger | PASS for stated review scope | Main graph proof, older draft qualifications, source-map assumptions and local/global distinctions reviewed. Seven PDFs compiled;20-page graph paper and137 older pages visually checked at the documented resolutions. No submission or exhaustive typography certification. |
| 14. Evidence report | PASS | This report, command index, raw logs, method reports, failure history, exact matrices and SHA256 manifests are committed. |

## Test suites and environment

Fresh CPython3.13.5 on macOS26.5.1 arm64; NumPy2.5.1, opt_einsum3.4.0,
pynauty2.8.8.1, pytest9.1.1, pip25.1.1. Tectonic0.17.0 builds the PDFs.
The lockfile now includes the previously unpinned declared opt_einsum
dependency. Every scientific command records exact argv, working directory,
environment overrides, wall-clock duration, exit code, and separate raw
stdout/stderr hashes. Full command metadata is in
`audit/20260907/COMMAND_INDEX.json`; readable commands are in `COMMANDS.md`.

| Suite | Actual pytest summary | Exit | Wrapper seconds | Evidence directory under audit/20260907 |
|---|---|---:|---:|---|
TEST_ROWS

The final root inventory has284 tests. The full repaired run executed279;
the final9-test source/CLI run covers the five newly added tests and the
four source regressions again after the final metadata edit. No284-test
single invocation is claimed. The separate6D command reproduces rank5 and
pattern1,2,1,1 under both primes. The unchanged root and historical bridge
suites each report85 passed and the same one optional test skipped:
`test_full_schedule_has_eighty_three_candidates_with_no_silent_gaps`.
That test requires the excluded third-party spinor archive via `SD5_ARCHIVE`.
It remains unverified; the graph and source certificates do not depend on it.

## Falsifications, repairs and unsuccessful attempts

The primary arXivv2 TeX and colored PDF require a trailing-pair red projector
on J10's first Q factor and trailing-triple red projectors on each of the
last three Q factors in J11/J12. The repaired evaluator applies red after
black, before raising indices. The old optional nested reading was also
insufficient for J11/J12. Only rows10–12 of the corrected decic atlas differ;
their difference has rank3 even in the primitive columns. Earlier claims
that the incomplete variants were harmless are explicitly historical.

The frozen historical tensor package lacked required scripts and result
inputs, causing five collection errors. Restoring the missing files from the
frozen repository exposed a fourth omitted subprocess script; the final
restored package passes254 tests. The127 copied-file hashes are recorded in
`results/audit/root-review/packaging_repair_manifest.json`. One intermediate
test run was terminated after the missing-input diagnosis; the next had
253 passes and one missing-script failure. Both are retained. Its source
readings remain historical, as `release_candidate/trace-code/AUDIT_STATUS.md`
states; the corrected portable classification package uses the root source.

The independent source oracle initially used the inverse shuffle incorrectly;
its block comparison failed before accepting any point. The corrected oracle
was checked against all120 alternating terms. Another pilot failed on an
omitted graph-definition input. Five-prime bounded rational reconstruction
was insufficient for ten large J11/J12 coefficients; no guessed atlas was
accepted. Seven-prime bounded integer CRT resolved the coefficients exactly.
The command index also retains download/build retries, script syntax errors,
and expected corruption-test failures rather than deleting unsuccessful runs.

Two deliberate certificate corruptions are rejected by the independent
checker, with original files unchanged. Four CLI regression cases reject
legacy or different-degree output targeting either canonical map. The CLI's
default validates the corrected exact certificate; historical fitting needs
`--legacy` and a separate output.

Phase01's root pytest completed approximately18.77 seconds after its stop
marker because the first termination attempt lacked process permission.
This was disclosed in that report; it is not represented as an immediate
stop. Phase02 continued only after the later user instruction.

## Exact conclusions and assumptions

The fixed81 graph polynomials are integral in126 explicit self-dual
coordinates. A nonzero modular Jacobian minor proves its determinant
polynomial is nonzero in characteristic zero. The independent integral
orbit-action calculation has45×45 minor residues5222 modulo50021 and10852
modulo32749. The Lorentz algebra has dimension45, so these witnesses give
generic orbit dimension45. Complete metric contractions are analytically
invariant; their differentials annihilate the orbit tangent space. Thus
126−45=81 is the matching maximum. Sampled rotation/boost and tangent
annihilation checks validate implementations; invariance itself is analytic.

The degree12 stacked-gradient minors prove linear independence of72
homogeneous polynomials. Completeness and the62-dimensional quotient by the
ten products additionally use the published Hilbert coefficient72. Its
source has an inconsistent prose count64 in section4.1.4; equation4.2 and
the stated cumulative83 support62. No new Hilbert-series derivation is
claimed.

The source-map CRT modulus is40274678413255193510345405666987, greater than
twice the largest proven numerator bound352866326400000000000000000000.
Exact integer entries, exact rational solving and injectivity of evaluation
give polynomial identities **conditional on the published degree8/10
invariant-space dimensions7/14 and analytic source-tensor invariance**.
The independent audit proves the matching evaluation lower bounds, not
those external representation-theoretic upper bounds.83 additional dense
modular checks are supplementary implementation evidence.

The octic inverse product corrections are
`0, -3/14, 7/72, -1/28, -593/31104, -61543/2612736`.
The corrected decic relation in the recorded graph normalization is
`J6 + 5J5/6 - J2/20 - 11J1/1008 = -13 I4_1 I6_1/63`.
Its source span has dimension12, product span2, union13, intersection1,
and quotient image11. An invertible12×12 map to the graph primitive
complement is therefore unavailable for these literal corrected expressions.

Independence qualifications: independently authored graph evaluators import
no production contraction/Hodge/projection/rank/verifier code. Their forward
and reverse methods share the audit's own forward contraction kernel and
NumPy/BLAS primitives, also used by production. Exact dot-product bounds are
checked below2^53; no approximate tolerance defines equality. Original edge
records are the specified inputs, validated rather than rediscovered. Source
transcription, machine arithmetic, Python/NumPy correctness and the stated
mathematical arguments remain trust assumptions; there is no formal proof
assistant certificate or independently implemented BLAS.

Some bootstrap, edit and read-only commands used `python -`; their exact
argv and output are recorded, but the command logger did not serialize the
tool-supplied standard input. Accepted scientific computations run the
preserved script files. The command ledger is therefore not a fully automatic
replay of every setup/edit operation; scientific inputs, programs and outputs
are retained separately.

The literature search does not cover every database, language, citation path
or unpublished work. The claim ledger does not upgrade archived model-
dependent tensor assertions to corrected-source theorems. No global orbit
separation, rational generation by this81-list, full invariant-ring
presentation, complete syzygy ideal, or priority claim is made.

## Evidence and reproduction

The source certificate SHA256 is
`01f9ab8d8f966827f820541a6e0bfec8e8bf64f710ec5b9f3be6dc825c61ed12`.
All other full hashes are in `audit/20260907/EVIDENCE_MANIFEST.json` and
the source manifests. Raw primary papers and full retrieved web responses
are not republished; their URLs/hashes and the authored transcription/search
records are retained. Full original downloads remain in the local audit
workspace. The original phase01 report is preserved unchanged.

```sh
python -m pytest tests -o addopts='' -q
python scripts/verify_rank81.py --recompute
python scripts/verify_independent_audit.py
python scripts/map_literature_basis.py --degree 8
python scripts/map_literature_basis.py --degree 10
```

The first command runs the suite available in the chosen tree (the portable
archive intentionally carries only its delivery/source/CLI tests). The
independent checker validates saved arithmetic and hashes without tensor
recomputation. Original independent evaluator sources and exact logged
commands are retained for full fresh reruns; see `audit/20260907/README.md`.
The corrected ZIP's post-build verification sidecar is stored beside the
archive rather than embedded recursively within it.
'''.replace("FROZEN_COMMIT",FROZEN).replace("TEST_ROWS","\n".join(rows))
parts = re.split(r"(`[^`]*`)", report)
for i in range(0, len(parts), 2):
    parts[i] = parts[i].replace("arXivv2", "arXiv v2")
    parts[i] = re.sub(r"(?<=[a-z])(?=\d)", " ", parts[i])
    parts[i] = re.sub(r"(?<=\d)(?=[a-zA-Z])", " ", parts[i])
    parts[i] = parts[i].replace("bounds.83", "bounds. 83")
report = "".join(parts)
report = report.replace("macOS26", "macOS 26").replace("arm 64", "arm64").replace("6 D", "6D").replace("arXiv v 2", "arXiv v2")
(REPO / "INDEPENDENT_AUDIT.md").write_text(report)
validation = {"schema": 2, "frozen_commit": FROZEN, "frozen_audit_passed": False,
              "passed": True, "scope": "Verified repaired graph/source scientific payload and restored historical tests; optional private-archive integration skipped. Post-build portable verification is a sidecar, not part of this prebuild ledger.",
              "checks": checks, "external_assumptions": ["Published Hilbert dimensions7,14,72 for source-map/completeness conclusions", "Analytic tensor invariance and stated integral coordinate arguments"],
              "optional_integration": {"status": "SKIP", "reason": "Excluded third-party spinor archive unavailable", "same_test_in_each_bridge_copy": True},
              "new_commit_identity": {"name": "uskutsav-cpu", "email": "uskutsav@gmail.com"}}
(REPO / "results/classification_validation.json").write_text(json.dumps(validation,indent=2)+"\n")
print("Wrote disclosed frozen FAIL / repaired verification report from completed checks.")
