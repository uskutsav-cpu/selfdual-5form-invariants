# Claim ledger for paper/manuscript.tex — partial independent audit

Frozen commit: `2b7663bbf5a06d1340973434f195a84ae2773e8f`. Date: 2026-09-07. Target: `checkout/paper/manuscript.tex` (165 lines), its two included tables, and directly supporting frozen artifacts. No frozen source was edited. There are **no numbered theorem, proposition or proof environments** in the target, so every substantive sentence or tightly related group is indexed below by source line.

**Final audit status: STOP / no overall PASS.** The coordinator subsequently reported a definite source-transcription mismatch for the frozen degree-ten J10–J12 antisymmetrizers, established by a separate source reviewer against primary PDF and TeX after freezing a manual transcription. I did not independently reproduce that finding; the source review is the authoritative evidence for its exact details. It blocks certifying the literature comparisons as readings of the published formulas. It does not by itself contradict the graph-only determinant claim. No further research or computation was performed after that stop instruction; only these reports were finalized.

## Status definitions and audit boundary

- **P — mathematical proof/definition:** the stated implication follows analytically with its assumptions. This is not an execution claim.
- **C — conditional proof:** the mathematical argument is sound if the specified computational and/or cited inputs are correct.
- **E — empirical/computational evidence:** exact finite arithmetic at samples, which is proof of a nonzero polynomial when applicable, but is not generally proof that a polynomial vanishes identically.
- **I — inherited unverified evidence:** assertions read from frozen result files or supplied by the literature, not freshly recomputed in this reviewer task.
- **O — overstatement or ambiguity:** scope exceeds, or can be read as exceeding, the established argument; see the separate downgrade report.
- **F — reported definite source mismatch:** reported by the coordinator after separate review; not independently verified by this reviewer.

I reviewed the mathematical implication and source paths, not the entire trusted computing base. No regression suite, graph Jacobian recomputation, rational-map regeneration, or Lorentz reevaluation was executed by this reviewer. JSON summaries and hashes were computed only to identify frozen artifacts. Any independent successful numerical checks elsewhere in the audit must be cited separately; none are silently incorporated here.

## Proof chain for the central claim

The actual proof obligation is a chain, not simply a matrix-rank calculation:

1. The ordered graph record must define the displayed contraction with exactly five slots at every vertex and exactly one inverse metric per edge.
2. The Hodge convention must give the claimed integral coordinate embedding into the real self-dual module.
3. The contraction evaluator must compute those integer polynomials and their derivatives in those coordinates.
4. At least one saved Jacobian must be freshly linked to those polynomials, and its indicated minor must have a nonzero residue modulo a verified prime.
5. An integer polynomial with a nonzero evaluation modulo a prime is nonzero over characteristic zero. The characteristic-zero Jacobian criterion then gives algebraic independence.
6. Maximality and local quotient-coordinate language additionally use the cited generic orbit/quotient dimension. A 126-minus-45 subtraction alone does not prove that the orbit dimension is 45.

A correctly recomputed nonzero determinant is an exact certificate, not a probabilistic independence inference. Multiple points help detect implementation or indexing problems; a single valid point suffices for the mathematical lower bound. Euler checks are necessary consistency checks for homogeneous derivatives, not sufficient proofs that all 126 derivative entries are correct.

## Sentence-by-sentence ledger

Paths below are relative to the frozen checkout, never to previous audit output.

| Source lines | Claim or sentence | Exact mathematical argument and artifact | Status / limitation |
|---|---|---|---|
| 5–6 | Title: explicit graph basis and exact Jacobian certificates | Ordered list in `results/rank81_basis.json`; graph export in `scripts/graph_to_latex.py:25–50`; certificate `results/rank81_certificate.json`. | C/O: “basis” must mean a maximal generically independent family, not a polynomial-ring basis or global separating basis. |
| 12–13 | Reproducible certificate for 81 real self-dual contractions | Definition, coordinate convention and archived graph records; `src/sdinv/certificate.py:89–106` validates list size, degrees and graph/formula agreement. | C/I: reproducibility requires fresh execution and correct evaluator; not established by merely reading a complete flag. |
| 13–15 | Degree inventory 1,2,6,12,60 | `certificate.py:93–94` enforces this exact ordered inventory; `rank81_basis.json` contains 81 items. | I, plus inspected validation rule. |
| 15–17 | Same functions have nonzero 81×81 minors at four finite-field points | Saved witnesses identify primes, points, basis hash and ordered invariant IDs. `verify_witness:145–188` checks ordering, minor and optionally graph values/rows. | C/I: saved four-cell evidence, not freshly recomputed here. |
| 17–18 | Integral coordinates turn each nonzero minor into a characteristic-zero witness | Reduction of an integer polynomial commutes with differentiation and evaluation; nonzero reduction cannot come from the zero integer polynomial. | P, conditional on correct polynomial/derivative correspondence. |
| 18–20 | Construction completes functional-independence problem using known quotient bound | Lower bound from determinant plus cited generic upper bound. | C/O: only the stated maximal generic independence problem; “completes” is broader without an explicit definition. |
| 20 | Does not determine all polynomial generators or syzygies | The certificate provides differential rank, not a ring presentation. | P, appropriate limitation. |
| 24–26 | Alternating five-form, almost-plus metric, self-duality; dimension 126 | Complementary 5-index subsets pair under Hodge star; choosing those containing 0 yields 126 coordinates. Code: `forms.py:hodge_matrix`, `certificate.py:33–47`. | P/C. Orientation/epsilon normalization is not explicitly written in the target text. |
| 27–28 | Literature supplies quotient dimension and Hilbert coefficients | Citation to two papers; precise main input is Cederwall et al. §4 and Eq. (4.2). | I: literature input, not independently derived. Source §4.1.4 has 64/62 arithmetic inconsistency recorded separately. |
| 28–30 | Present certificate supplies matching lower bound | Proof chain above; graph witnesses and recomputation code. | C/I. |
| 30–32 | Catalogs/bases inherited, functions reevaluated at new points | `graph_to_latex.export_basis` reads three frozen results; `search_rank81.evaluate_cell` generates points and reevaluates fixed graph records. | I: code supports workflow, but chronology and novelty of points relative to all prior work were not independently audited. |
| 34–36 | Graph definition, valence and edge contractions | `graphs.validate_graph`; `serialize.from_record`; `contract._slot_plan`; every vertex supplies one alternating tensor. | P/C: mathematical definition plus implementation correspondence obligation. |
| 36–38 | Ordered edges/slots and hash retain odd-form signs | Lexicographic edges assign slot order; permutation of slots can change alternating-tensor sign. `latex.py:7–19`, `certificate.py:98–105`. | P/C: identifier is an encoding hash, not a proof of invariance or independence. |
| 39 | Disconnected contractions are products | Index sets of disconnected components sum independently, so the contraction factors. | P. |
| 39–40 | Quadratic contraction vanishes on self-dual space | (F\wedge\star F=F\wedge F=0) for an odd form in characteristic zero; equivalent metric contraction is zero. Test: `tests/test_core.py:388`. | P; test execution remains I. |
| 42–47 | Coordinates are (A_I=F_I) and (F=\sum A_I(e_I+\star e_I)) | Complement of a tuple containing 0 omits 0; (star^2=1); `certificate.integral_directions`. | P/C. |
| 48–49 | 126 columns have entries 0,±1 and an identity coordinate block | Hodge matrix in an orthonormal metric maps each compact basis component to its complement with a sign. Code asserts identity block and self-duality. | P/C; assertions are not a fresh execution in this review. |
| 49–50 | All graph polynomials have integer coefficients, no projector denominators | Integer coordinate substitution into products/contractions using metric entries ±1. | P, assuming the stated graph convention is the evaluator convention. |
| 53–56 | Nine low-degree, twelve degree-ten, first sixty functional degree-twelve functions | Export iterates the three result files and includes degree-12 rows with true `functional_increment`. | I/C: “first sixty” should refer to that stored filter/order. No independent discovery needed to use explicit formulas. |
| 57–59 | Two remaining degree-twelve primitive directions excluded from Jacobian | `10d_order12.json` lists 62; graph selection includes 60. “Primitive” refers to a complement to products in a homogeneous degree. | I/C: the homogeneous 62-direction claim uses a separate computation and upper bound. |
| 59 | Dependent Jacobian row does not identify a polynomial syzygy | A sampled dependence supplies neither global coefficient functions nor a polynomial equation among invariants. | P, appropriate. |
| 64–70 | Cumulative ranks 1,3,9,21,81 | `make_witness:128–142`; `verify_witness:176–181`; same metadata in all four saved cells. | I/C: follows for lower prefixes if a full correctly ordered 81-row minor is nonzero. |
| 75 | Jacobian is derivative with respect to independent A-coordinates | `context` builds the compact derivative basis and `evaluate_item:109–117` calls `value_and_jacobian_row`. | C: evaluator's derivative implementation must be checked. |
| 75–78 | Every cell records p, 126 coordinates, 252 components, IDs, 81×126 J, pivots, determinant | `make_witness:137–142`; archived cell schema. | I, verified as schema/metadata presence by source and JSON inspection. |
| 79 | Four table rows show ranks/determinants | Table entries: (32749,20260907,20345), (32749,20260908,30761), (32719,20260907,1653), (32719,20260908,2167); each rank 81. They match the saved JSON summary. | I: table-versus-JSON agreement; no fresh determinant recomputation by this reviewer. |
| 80–81 | Independent Python-integer determinant elimination | `determinant_mod:64–86` uses Python integer Gaussian elimination, separate from `RankSieve`. | Source-inspected implementation claim; independence of algorithms is narrower than independence of input/evaluator. |
| 81–82 | Euler homogeneity checked every row | `evaluate_item:114–115`, `verify_witness:165–169`. | E/I: exact consistency check, not a derivative proof. |
| 84–85 | Nonzero saved determinant implies nonzero integer determinant polynomial | True only if saved entries really are the derivatives of the fixed integer graph polynomials. | C: “saved” should be “verified evaluation”; arbitrary saved full-rank matrices do not suffice. |
| 85–87 | Nonvanishing locus is nonempty Zariski open and 81 polynomials algebraically independent | Nonzero polynomial defines nonempty principal open; Jacobian criterion in characteristic zero. | P/C. More precise: independence is a global algebraic property; differentials are independent on this open. |
| 87–88 | Invariance and quotient dimension give upper bound | Invariant differentials annihilate orbit directions; quotient transcendence degree bounds independent invariant functions. | C/I: upper bound inherited; generic orbit dimension needs its own justification. |
| 88–90 | Generic local coordinates, no global separation or generation | On a regular local quotient/transverse slice, full differential rank permits local coordinate use. | C/O: clarify local analytic/regular quotient sense; it does not prove invariant-field generation or a global rational parametrization. |
| 93–94 | Homogeneous dimensions 1,2,7,14,72 | Literature Hilbert coefficients at degrees 4,6,8,10,12. | I: cite exact equation; do not claim these were freshly recomputed. |
| 94 | Products must enter value-space comparisons | Homogeneous invariant space includes decomposable invariants, so comparing only primitive representatives can miss product corrections. | P. |
| 95–96 | Ten degree-twelve product monomials | Degree partitions 4+4+4, 6+6, 4+8 give 1+3+6 monomials from chosen lower generators. `tests/test_roadmap.py:68–75`; `degree12_pipeline._degree12_products`. | P/C: counts monomials; their linear independence is a separate obligation. |
| 96–98 | Inherited degree-twelve computation rank72 with 62 graphs plus products | `results/10d_order12.json`; `scripts/degree12_pipeline.py:704–716,934–994`. | I: no inherited checkpoint reused or this rank rerun here. With a correct modular lower bound and trusted Hilbert upper bound, the dimension conclusion would be exact. |
| 98–99 | Homogeneous polynomial sieve concatenates gradients across points; functional Jacobian one point | `degree12_pipeline.py:704–710,934–954` explicitly builds different sieves. | Source-inspected workflow; correct distinction. |
| 100–101 | Hilbert product exponents need not equal generator counts at high degree | Generator/relationship contributions can cancel in a product representation. | P; correctly avoids extrapolating 62-style counts to arbitrary degree. |
| 103–105 | Octic selection uses first five expressions plus hatted (4.18) | `published_degree8_invariants.py:18–22,35–44`; map `literature_basis` matches named selection. | I/C: description of implemented selection; this reviewer did not independently transcribe all source indices. |
| 105–106 | Exact machine-readable map retains quartic square | `results/order8_change_of_basis.json`; `map_literature_basis.py:116–129`. | E/I/O: rational entries are exact numbers; polynomial identity remains sampled evidence. |
| 107–108 | 6×6 quotient block and 7×7 product-corrected matrix | `map_literature_basis.py:121–125`; saved product correction is not zero. | E/I/C: interpretation as actual polynomial maps is conditional on identity validity. |
| 110–113 | Implemented degree-ten readings have ranks12,2 and intersection1 in reconstructed coordinate matrix | Exact rational matrix-rank operation in `map_literature_basis.py:134–159`; frozen output ranks12,2,13, hence 12+2−13=1. | E/I; F blocks identifying these with published J10–J12 until the separate source mismatch is resolved. |
| 113–114 | Invertible 12×12 primitive-complement identification would be incorrect for those readings | If the asserted subspace intersection is one-dimensional, quotient image has dimension11, so cannot identify a 12-dimensional complement invertibly. | C on correctness of implemented-polynomial maps; exact as a statement about the reconstructed matrix. |
| 115–116 | Delivered degree-ten map is12×14 and has source qualifications | Output field `matrix_12x14`, `source_readings`; source points to `docs/PUBLISHED_DEGREE10_INDEX_AUDIT.md`. | I; qualifications do not themselves validate the source transcription. |
| 116–118 | Rational reconstruction and fresh modular holdouts check maps, not Q-identities | Octic function creates new value samples; degree-ten function reads inherited per-prime coordinates and tests a held-out stored prime. | E/I/O: “fresh” is imprecise collectively. No polynomial-identity theorem from sampling alone. |
| 118–119 | Literature-map qualifications do not affect graph-only minor proof | Graph evaluation imports graph and coordinate machinery, not degree-ten literature tensor formulas. | P/C: separation of proof dependencies by inspected call paths. Does not certify graph evaluator correctness. |
| 122–124 | Dependencies/regression prerequisite; original low-degree tag preserved | Reproduction instructions, not a mathematical theorem. Tag itself not independently inspected by this reviewer. | I/unfinished provenance check. |
| 126–132 | Release command sequence | Scripts exist and referenced entry points were inspected. Several commands write to frozen default result paths unless overridden or run on a copy. | Workflow only; no claim this sequence was executed here. |
| 134–136 | Default saved-matrix and recompute modes distinguished | `verify_rank81.verify`; `verify_witness:182–186` only reevaluates graphs when requested. | Source-inspected, accurate distinction. “Recompute” uses the same production evaluator, not a fully independent oracle. |
| 136–137 | Checkpoints raw rows/pivots, identity on resume, bounded submissions | `search_rank81.py:34–73` stores evaluated raw rows, prime/seed/engine hashes, restores sieve and submits at most worker-count batches. | Source-inspected workflow; interruption/resume behavior not executed here. |
| 138–140 | Nauty discovery, JSONL input, separate rank concepts | `graphs.py:iter_graphs_nauty`; `scripts/run_degree.py`; `tests/test_roadmap.py:160–169`. | I/source-location evidence; full runner not reviewed line-by-line here. |
| 142–145 | Regression suite covers enumerated subjects | Tests: `test_core.py:58,69,82,94,349,364,378,388,537`; `test_roadmap.py:34,78,95,125`; `test_graph_to_tensor.py:68`. | Test-presence claim supported; pass status and coverage completeness not established in this reviewer task. |
| 145–146 | Final selection checked under spatial rotation and genuine boost without tolerances | `validate_rank81_lorentz.py` uses rational-parameter matrices reduced modulo p; checks metric preservation, reevaluates81 graphs, tests exact equality; saved `rank81_lorentz.json` says passed. | E/I: one prime/point and two selected transformations. This is not a proof of full Lorentz invariance; tensor contraction supplies the analytic argument. |
| 159–160 | Every repeated Einstein index corresponds to one edge and upper/lower endpoints give metric | `latex.py:7–19`; graph edge labels unique by vertex pair and multiplicity index. | P/C: generated formula/evaluator correspondence must preserve slot order. |
| 160–162 | JSON companion has edges, adjacency, formula hashes, costs | `graph_to_latex.export_basis:25–50` and frozen manifest fields. | I/source-inspected structure. Costs describe chosen plans; they are not mathematical proof data. |
| 164 | Appendix is the list of ordered formulas | Included `paper/tables/rank81_formulas.tex`; generated from fixed manifest source list. | I: no full rendered-PDF visual review or independent transcription of all81 formulas was performed here. |

## Artifact identity and execution evidence

The exact commands, stdout/stderr and SHA-256 hashes for this review are under sibling `commands/`:

- `literature-manuscript-initial-read-001`: target manuscript and paper inventory.
- `literature-manuscript-artifact-inventory-002`: line-numbered manuscript, certificate table and targeted file inventory.
- `literature-manuscript-artifact-read-003`: verifier, exporter, Lorentz script and supporting symbol/test locations.
- `literature-manuscript-certificate-read-004`: certificate, search, map code and older-manuscript claim locations.
- `literature-manuscript-focused-artifacts-005`: regression coverage, octic definitions, LaTeX exporter, degree-twelve sieve locations and older proof paragraphs.
- `literature-manuscript-json-summary-006`: frozen result metadata and content hashes.

Raw-file SHA-256 identities read in command006:

| Artifact | SHA-256 of raw file bytes |
|---|---|
| results/10d_order8.json | e780f0972fb8bfcfbed0dcda89361fe9810763549bc6f2ac9bf0833585e7f16c |
| results/10d_order10.json | 92b02433d82e641cce0d2dbb5f1bec9878c191ccbda7e906f27ef1f555b0fee5 |
| results/10d_order12.json | 9a784dc56a2bc8186a4abb59e9177051be05640e95b4d7d24a4538bb45335113 |
| results/rank81_basis.json | 59848eb1e3024f33da8b8235796b0ea99429f21c88243070437172b50a6473fb |
| results/rank81_certificate.json | c329edc407c0624633abeda7e9de097fc92ed0b17224d2f19d1aba43d54d656d |
| results/rank81_lorentz.json | 973a982ab0100a967050251386c84d8b7f466cfb13606752d3ea3183496494f0 |
| results/order8_change_of_basis.json | 30140fa0bef549b6f6c221e3fcc5f971416930ca3802084ca3d40933f782beec |
| results/order10_change_of_basis.json | 429dbf74b37f84baf3b14c8e64bb718d74a0d88b25221848e7f547dc1fd3cb89 |

The certificate's internal basis digest `ef6d64e6e71a0468c4b2e1ba878cb8a25fcdde1d6788d3a6bca5da6bf7fb20d6` hashes canonical JSON, so its difference from the raw-file SHA-256 above is not a mismatch.

## Process disclosure and unfinished work

The first bootstrap inventory used an unwrapped read-only `pwd && ls -la .../independent-audit-20260907-01`, reading only cwd and new audit directory names. I immediately disclosed it. The coordinator then clarified that plain reads of newly created audit logs/inventories are permitted and do not need recursive wrappers. All subsequent source-inspection/metadata shell commands were wrapped by the audit runner; log-viewing commands were plain reads. No prior audit, old working directory, old checkpoint or prior model discussion was read. Frozen result artifacts were treated as objects under review, not reused as fresh evidence.

Incomplete at STOP: full numerical reevaluation in this reviewer task, independent character/Hilbert computation, complete source-formula transcription, exhaustive forward-citation traversal, full older-manuscript audit and PDF visual QA. The literature source arithmetic inconsistency is separate from the coordinator's definite J10–J12 source mismatch. Neither is being silently converted into a claim about the graph certificate's true rank.

