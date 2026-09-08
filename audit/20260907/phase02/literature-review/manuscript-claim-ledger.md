# Manuscript claim ledger — phase 02

Audit date: 2026-09-07. Frozen reference: `2b7663bbf5a06d1340973434f195a84ae2773e8f`. Primary target: `paper/manuscript.tex`; this ledger uses the 198-line repaired snapshot printed in command `literature_10_ledger_artifacts`. The original target had no theorem/proposition/proof environments; every claim-bearing sentence, displayed count, and proof implication is covered below. Repository paths are relative to `repair-checkout/` unless specified. This is a claim audit, **not an overall audit-pass report**.

The repaired target is supported by the same archived numerical inputs as the frozen target. Fresh graph, derivative, transformation, source-map, packaging and orbit-tangent execution belongs to the other reviewers and must be cited through their separate logs. This reviewer performed source/prose inspections, metadata identification, literature retrieval and a PRD prose-conversion check; it did not execute the scientific Jacobian, degree-twelve or source-map computations. No cached computation was treated as a new result.

## Status key

- **P:** analytic proof or definition, with stated hypotheses.
- **C:** valid conditional argument whose named computational or mathematical inputs must be established.
- **E:** exact finite computation or finite-sample evidence; not automatically a vanishing polynomial identity.
- **I:** inherited or externally reported result not recomputed by this reviewer.
- **F:** definite source mismatch reported by the dedicated source reviewer.
- **O → fix:** claim exceeded its evidence in the frozen text and was qualified in the repair.

Statuses can coexist: an exact rank calculation is a proof about its matrix, while identification of that matrix with polynomial functions can remain conditional.

## Central proof chain

1. Every ordered graph record defines a complete contraction of alternating five-tensors with inverse metrics. Invariance follows by cancellation of the group matrices on each contracted pair. There is no appeal to random tests for this theorem.
2. The chosen self-dual coordinates are integral: the complementary index tuple to one containing 0 omits 0, and the Hodge map has signed-permutation entries with square 1. Thus the 126 selected columns have an identity coordinate block.
3. Substitution into complete contractions produces integer polynomials. The evaluator and differentiation routine must compute precisely those polynomials in precisely those 126 coordinates.
4. A correctly evaluated nonzero Jacobian minor modulo a prime proves the associated integer determinant polynomial is nonzero. Saved full-rank numbers without the derivative correspondence do not prove this.
5. The characteristic-zero Jacobian criterion gives algebraic independence of the selected 81 polynomials. Their differentials have rank 81 on the principal open where the minor is nonzero.
6. A matching upper bound uses the generic orbit dimension, not bare subtraction of group dimension from module dimension. The coordinator supplied a separate direct 45-generator orbit-tangent certificate, recorded in the addendum below and added to the manuscript after the 198-line snapshot. Its integral nonzero minor gives generic action rank45, and invariance gives the upper bound81.
7. Local-coordinate language is restricted to a regular local quotient. No global orbit separation, invariant-field generation, homogeneous system of parameters, polynomial ring presentation, or syzygy list follows from the minor alone.

A successful finite nonzero witness is a proof of nonidentity of one polynomial, with the computational correspondence as its trust boundary. By contrast, finitely many zeros of a proposed relation do not prove a polynomial identity. Repeating points/primes helps test implementation and reconstruction; it is not a substitute for that distinction.

## Complete claim ledger for the graph manuscript

| Repaired lines | Claim | Exact argument and computational artifact | Status and disposition |
|---|---|---|---|
| 5–6 | Title describes explicit graph invariants and exact Jacobian certificates | Ordered formulas and fixed-list witness; `results/rank81_basis.json`, `results/rank81_certificate.json`. | C/I. O → fix: removed ambiguous “graph basis” from title. |
| 12–13 | Certificate for 81 real self-dual contractions | Graph records; coordinate embedding; `certificate.validate_basis` checks 81 unique IDs and each graph encoding. | C/I. Correctness requires definition–code–witness correspondence. |
| 13–15 | Degrees contribute 1, 2, 6, 12, 60 polynomials | Export filter in `scripts/graph_to_latex.py`; `certificate.py:93` enforces exact degree list. | I plus source-inspected schema. No numerical count changed. |
| 15–17 | Four nonzero 81×81 minors for the same ordered functions | Archived certificate stores IDs and basis digest per cell; `verify_witness` checks them. | C/I. Four cells are described as archived witnesses, not independently calculated by this reviewer. |
| 17–19 | Integral coordinates make verified minors characteristic-zero witnesses | Reduction commutes with polynomial evaluation and differentiation. The zero integer polynomial reduces to zero at every point. | P/C. O → fix: explicitly requires entries to be verified derivatives. |
| 19–21 | Maximal generically independent family using cited quotient dimension | Nonzero minor plus upper bound; proof chain above. | C/I. O → fix: replaces “completes the functional-independence problem.” |
| 21 | No full generators or syzygies claimed | Differential rank is not a ring presentation. | P; appropriate scope. |
| 25–27 | Almost-plus metric and self-dual module of dimension 126 | Complement pairing of the 252 sorted five-tuples gives 126 signed Hodge eigencoordinates; `forms.py:71–101`, `certificate.py:33–47`. | P/C. The executable Hodge map fixes epsilon orientation; the text does not spell out epsilon components. |
| 28–29 | Quotient and Hilbert inputs come from literature | Cederwall section 4, Eq. (4.2), and Hutomo section 2.1. | I. Exact source links in literature report; no fresh character calculation claimed. |
| 29–33 | Explicit graph contractions supply lower bound; catalogs inherited and reevaluated | Exporter reads the three existing order files; search evaluates a fixed manifest at specified points. | C/I. No new discovery or clean-room catalog claim. |
| 34–37 | Prior graph/numerical methodology; 10D application future work in Elamaran et al. | Primary article abstract, graph algorithm and conclusion; DOI 10.1103/ny3m-drnj, arXiv:2512.23750. | Verified primary-literature attribution. Newly added citation. |
| 38 | No priority claim | Scope statement rather than scientific assertion. | Appropriate; absence of search hits is not evidence of firstness. |
| 40–41 | Vertex, valence and edge-metric definitions | Each vertex contributes five tensor slots; edge multiplicity counts paired contractions. `graphs.validate_graph`, serialized edge record. | P/C. Full catalog exhaustiveness is not required for independence of this explicit list. |
| 42–44 | Slot order and formula hash account for odd-form signs | Alternating tensor changes sign under odd slot permutations. Ordered edge serialization and `latex.py:7–19` specify slots. | P/C. A hash binds an encoding; it does not prove its evaluation. |
| 45 | Disconnected contractions factor | Disjoint component index sums factor into a product. | P. |
| 45–47 | Quadratic contraction vanishes | Odd-degree skew-commutativity gives F∧F=0; self-duality identifies F∧*F with it. Metric norm is therefore zero. | P. Analytic argument added rather than relying only on tests. |
| 47–48 | Complete contraction is Lorentz invariant | Each inverse metric contracts two transformation matrices to the metric; all slots are paired. Restrict to the orientation-preserving action that preserves the self-dual module. | P/C for evaluator correspondence. |
| 50–55 | Coordinates A_I are actual compact components; formula for F(A) | Hodge complement of an I containing 0 omits 0, so the selected identity block gives A_I=F_I. | P/C. `integral_directions` asserts this and self-duality. |
| 56–57 | Columns contain only 0,±1 and form an identity block | Hodge map is a signed permutation under the orthonormal metric. | P/C. No projector denominator is used in the coordinate list. |
| 57–58 | Graph polynomial coefficients are integral | Integral linear substitution into tensor products, sums and metric entries ±1. | P. Requires the same normalization in evaluator and displayed formula. |
| 61–64 | Provenance of 9+12+60 selected functions | `results/10d_order8.json`, `10d_order10.json`, `10d_order12.json`; exporter includes degree-12 entries with `functional_increment`. | I/source-inspected. Explicit selection can be audited without rerunning discovery. |
| 65–67 | Two further directions are labeled primitive in inherited inventory | Stored 62 versus selected 60; homogeneous computation is distinct. | I/C. O → fix: attribution to inherited label rather than an unqualified new theorem. |
| 67 | A dependent Jacobian row does not identify a syzygy | A row relation at one point supplies no global polynomial relation coefficients. | P. |
| 72–78 | Cumulative ranks 1,3,9,21,81 | Ordered 81-row full rank implies every row prefix independent. `make_witness` and `verify_witness` record ranks by degree. | C/I. Table entries are not changed. |
| 83 | Jacobian uses independent A-coordinates | `certificate.context` creates `CompactDerivativeBasis`; `evaluate_item` calls `value_and_jacobian_row`. | C. Independent derivative correspondence is a separate verification obligation. |
| 83–86 | Cell contains prime, points, IDs, all J entries, pivots and determinant | Schema construction `certificate.py:137–142`; shape and bounds checked at 145–188. | I/source-inspected schema, not an arbitrary “complete” flag. |
| 87 | Included four-cell table | Original tuples (prime, seed, determinant): (32749,20260907,20345), (32749,20260908,30761), (32719,20260907,1653), (32719,20260908,2167). All rank 81. | I; fresh metadata read in command 14. Root owns independent recomputations. |
| 88–89 | Python-integer determinant independent of rank sieve | `determinant_mod` is a separate Gaussian elimination routine using Python integers; streaming `RankSieve` is separate. | Source-inspected implementation claim. Independence of elimination is not independence of matrix input. |
| 89–90 | Euler identity checked for every row | Homogeneous Euler theorem; checks at `certificate.py:114–115,165–169`. | P for identity; E/I for execution. Passing Euler is insufficient to identify all derivatives. |
| 92–95 | Verified nonzero modular minor gives a nonzero integer polynomial | Proof chain step 4. | P/C. Key repair removes the invalid inference from an arbitrary saved determinant. |
| 95–97 | Algebraic independence; nonempty open locus of independent differentials | Characteristic-zero Jacobian criterion and nonzero principal open. | P/C. Repaired text distinguishes global algebraic independence from its open differential-rank locus. |
| 98–99 in pre-addendum snapshot | Matching upper bound; regular local quotient coordinates | Invariants annihilate tangent directions to orbits; generic quotient dimension controls rank. | C with separate direct orbit certificate now supplied, as detailed below. Regular local qualification added. |
| 99–101 | No global separating family, field generation or ring generation | A dominant map to affine 81-space may have more than one generic preimage; nonzero Jacobian does not give birationality or ring generation. | P; appropriate limitation. |
| 104–106 | Homogeneous dimensions 1,2,7,14,72 | Cited Eq. (4.2), separately from differential rank. | I. Explicitly external representation-theoretic input. |
| 106 | Products enter homogeneous comparisons | Decomposable invariant products belong to the homogeneous piece. | P. |
| 107–108 | Ten product monomials at degree 12 | Degree partitions 4+4+4, 6+6 and 4+8 give 1+3+6 choices. | P/C. Counting monomials alone does not prove independence. |
| 108–110 | Inherited rank72 from products and62 graphs | `results/10d_order12.json`; `scripts/degree12_pipeline.py` uses concatenated gradients and a separate functional sieve. | I in the manuscript snapshot; a separate fresh independent rank72 certificate is now supplied, as detailed below. No scientific rank computation was performed by this prose reviewer. |
| 110–113 | Correct rank72 lower bound plus Hilbert upper bound proves homogeneous completeness | Linear relation of same positive-degree homogeneous polynomials differentiates to a row relation; verified full row rank excludes it. Trusted Hilbert dimension supplies the upper bound. | P/C/I. Added explicit required inputs; no claim of new independent degree12 completion. |
| 113–115 | Multi-point polynomial sieve versus single-point functional sieve | Separate data matrices and objectives in degree12 pipeline; the former tests constant linear dependence of homogeneous polynomials. | Source-inspected workflow in phase 01; not rerun here. |
| 115–118 | Cederwall 64/62 source inconsistency | Primary section 4.1.4 versus Eq. (4.2). | Verified source prose discrepancy, not a license to change frozen62. |
| 119–120 | Hilbert-factor exponents do not always count generators | Generator/relation contributions can cancel in a product presentation. | P. |
| 122–124 | Octic selection from stated six displayed contractions | `published_degree8_invariants.SELECTED_BASIS` and `map_literature_basis.py:23,80–129`. | I/C. Independent transcription belongs to source reviewer. |
| 125–128 | Matrix has rational entries; finite fits/holdouts support its polynomial interpretation | Order8 routine fits at five primes, evaluates new samples and validates at a sixth; exact reconstruction is numerical arithmetic on coefficients. | E/I/C. O → fix: matrix exactness separated from polynomial-identity proof. |
| 129–130 | 6×6 primitive block and full7×7 correction | `primitive_quotient_matrix_6x6`, `product_correction`, full matrix fields. | E/I/C. Meaning as polynomial quotient map remains subject to identity validity. |
| 132–134 | Archived12×14 matrix rank12; products rank2; intersection1 | Exact rational inclusion–exclusion: 12+2−13=1; archived map routine lines134–159. | Exact as reconstructed-matrix claim; E/I as polynomial map. |
| 135–138 | J10–J12 archived antisymmetrizers differ from primary source; cannot assign ranks to publication | Separate source review reported through coordinator. | F. This reviewer cites that result rather than claiming its own transcription. |
| 138–140 | Repaired source map must have separate registry/evidence | Changed formulas define a different computational object. | P/provenance requirement. No old result is silently relabeled. |
| 140–142 | Archived degree10 regeneration uses stored prime coordinates, no new tensor evaluation | `order10` opens `B10_coordinates_per_prime.json`, reconstructs stored rows and checks the last stored prime. | Direct source-inspected fact. O → fix: collective “fresh holdouts” wording removed. |
| 142–144 | Fresh finite holdouts alone would not prove identities | A nonzero polynomial can vanish on any prescribed finite sample set. | P. |
| 144–145 | Source-map failure is separate from graph minor | Graph evaluator imports complete-contraction/coordinate machinery, not the degree-ten source candidate formulas. | P/C dependency separation, not a blanket graph implementation pass. |
| 148–150 | Dependency/regression instructions and original tag | Workflow instructions; tag existence/history is not a scientific proof. | I; this reviewer did not independently verify the tag. |
| 152–158 | Commands exist and regenerate relevant outputs | Export/search/verify/transform/map entrypoints inspected. | Workflow only. Their default output paths are repository-relative; use the repair checkout or explicit output overrides. |
| 160–163 | Default verification versus production reevaluation | `verify_witness(recompute=True)` reevaluates rows with production `evaluate_item`. | Direct source inspection. O → fix: no claim that reevaluation is an independent derivative implementation. |
| 163–164 | Raw-row/pivot checkpoint, identity validation, bounded workers | `search_rank81.py` stores complete evaluated rows and restores streaming ranks; bounded submission batches. | Source-inspected; interruption/resume behavior not run by this reviewer. |
| 165–167 | Nauty discovery, extra JSONL candidates, separated rank goals | `scripts/run_degree.py` and degree-specific graph pipelines. | Source-inspected workflow. Does not prove catalog exhaustiveness. |
| 169–172 | Listed regression subjects exist | `tests/test_core.py`, `test_roadmap.py`, graph-to-tensor tests; bridge suite separate. | Test-presence claim; fresh execution owned by root/math reviewer. |
| 172–175 | Rotation/boost check all81 at recorded point; exact finite arithmetic | `validate_rank81_lorentz.py:27–46` selects first saved cell, builds rational-parameter rotation and boost, reevaluates values. | E/I; analytic invariance follows from definition, not finite tests. |
| 178–187 | Bibliographic entries | Primary arXiv metadata and APS publisher metadata retrieved in phase02. | Primary-source bibliographic checks; no priority inference. |
| 192–193 | Repeated Einstein index corresponds to edge and one raised endpoint | `latex.py:7–19` generates unique edge labels with one upper and one lower occurrence. | P/C; ordering must agree with evaluator. |
| 194–195 | Companion includes edges, adjacency, formula hashes and costs | `graph_to_latex.export_basis`, manifest and validator. | I/source-inspected schema. Costs are implementation metadata, not proof. |
| 197 | Included appendix displays all fixed formulas | `paper/tables/rank81_formulas.tex`, generated from fixed manifest. | C/I. No independent visual transcription of all81 by this reviewer; root owns compile/render checks. |

## Older manuscripts: every explicit theorem/proposition inspected

The primary whole-manuscript sentence ledger is above. Older drafts were searched for material conflicts and all their explicit theorem/proposition/proof environments were inspected in the requested main sources. This is not a claim that every sentence of every legacy appendix, table, archived review package or release document has been rewritten.

The six older main files now have qualified titles/abstracts and a visible statement that their numerical claims remain **archived coordinate-model claims**. Scientific numerical tables/macros and identities were retained. The full PRD main file derives from JHEP; matching prose fixes are present in both, and the generator now preserves the status statement and qualified title.

| Location / proof | Argument and precise evidence | Verdict / repair |
|---|---|---|
| `manuscript/main.tex` and `submission_candidate/main.tex`, proposition `prop:cardinality` | For D+span(S)=A, the quotient map sends S to a spanning set of A/D; dimension≤cardinality. No computation is needed for this lemma. | P as abstract linear algebra. Substituting the numerical quotient dimension depends on the archived flow model and polynomial identity hypotheses. |
| JHEP/PRD `prop:bridge`; PRD-letter `prop:bridge` | Full-column-rank map, gamma-trace kernel, left inverse and projection are finite matrix identities. Gamma matrices and bridge code are in `spinor_trace_bridge/`; appendices C/F describe the certificate inputs. | E/I at the stated tested primes. A full matrix identity is stronger than checking sample vectors. Arbitrary-Lorentz equivariance requires a symbolic/generator argument beyond selected transformations; the paper’s finite-prime statement is not automatically a characteristic-zero proof of every property. |
| JHEP/PRD `thm:reach`; PRD-letter `thm:main` | Reconstructed target coordinates feed an exact rational fixed point. Artifacts `results/stress_flow/D10_characteristic_zero.json`, `Q10_characteristic_zero.json`; exact minor and covectors concern the resulting coordinate matrices. | O → C. Added hypotheses that coordinate maps are polynomial identities, target set is complete, and activation rules represent the stated flow. Exact arithmetic alone cannot establish those hypotheses. |
| JHEP/PRD `prop:cardinality`; PRD-letter `prop:card` | Same quotient-map proof as above. | P; applying dimension3 remains conditional on the closure interpretation. No new cardinality theorem claimed. |
| JHEP/PRD `thm:gten`; PRD-letter `thm:gten`; paired appendix I | F∧F=0 for odd form; self-duality implies metric norm0; the displayed algebraic stress tensor has trace proportional to that norm for each value of its metric-norm coefficient. | P for quadratic trace vanishing. O → fix: “first contributes at degree4” became first **possible** contribution in an even-degree expansion; proving a nonzero quartic interacting term requires another input. |
| JHEP/PRD `thm:bp`; paired appendix J | Rational-matrix ranks and inclusion–exclusion from `B10_coordinates_per_prime.json`, `B10_P10_intersection_exact.json`, `B10_P10_intersection_generator.json`. | E/I/F. The theorem now explicitly concerns archived reconstructed matrices, not corrected published expressions. Proposed integer relation is finite-sample validated, not a proved polynomial identity from those checks alone. |
| PRL main/end matter/supplemental | No formal proof environment in main; quotient cardinality argument, bridge, closure, candidate comparison and Jacobian claims inherit the same dependencies. | Qualified abstract/title/status; removed “science complete and certified.” The old model’s numerical content remains archived, not a new global result. |

## Specific older-draft repairs and exact derivations

1. **Trace normalization.** The displayed tensor has first term F_{μα…}F_ν^{α…}/(p−1)! while the pairing is defined without a factorial. Contracting with η^{μν} therefore gives [1/(p−1)!−cd]〈F,F〉, not [1−cd]〈F,F〉. Corrected in JHEP, PRD, PRD-letter and paired trace appendices. For p=5,d=10 the coefficient is 1/24−10c; since 〈F,F〉=0 on the stated module, the vanishing conclusion is unchanged. This is an algebraic consistency correction, not a new scientific numerical result.
2. **Polynomial versus differential relations.** An 83-candidate family of generic Jacobian rank81 has two excess differential directions; the rank does not output “exactly two” explicit polynomial relations or prove the ideal is generated by two relations.
3. **Homogeneous Hilbert count.** Corrected the legacy description from “a count of generators” to dimension of the homogeneous polynomial space including products.
4. **Closure upper bound.** Replaced unconditional “no separate upper bound needed” reasoning with an exact statement about the reconstructed coordinate model and explicit polynomial-map/activation/completeness hypotheses.
5. **Sample-span equality.** Common-sample two-way containment and union rank prove equality of evaluation spans. Polynomial span equality needs identities. Restricted universal “any single-graph contraction” statements to the enumerated family unless exhaustiveness is proved.
6. **Rational reconstruction.** Removed the incorrect assertion that rational reconstruction always returns a value. Removed the inference that a large rational numerator necessarily makes a modular rank wrong: coefficient recovery and exceptional-prime rank loss are different questions.
7. **Source transfer.** All older B10 references to the “published span” are explicitly defined as archived implemented-source readings, with J10–J12 mismatch prominently stated. The fresh corrected source registry cannot inherit those results by relabeling.
8. **Jacobian criterion.** Corrected the legacy appendix assertion that generic functional independence and algebraic independence are different for a polynomial subfamily in characteristic zero. A nonzero minor proves algebraic independence of that subfamily; it does not make every member of the larger dependent candidate family independent.

## Exact execution and modification evidence

All source reads, metadata computations and edit scripts in this phase were run through sibling `run_command.py` with an explicit working directory. Plain reads of newly generated logs were permitted by the coordinator and were not recursively wrapped. Phase01’s initial unwrapped bootstrap inventory remains disclosed in its authored report; it was not repeated in this phase.

- `literature_01_inventory`: fresh repair file inventory.
- `literature_02_prose_read`: target manuscript, map routines and certificate implementation.
- `literature_03_variant_claims`, `04_claim_context`, `05_proof_locations`: legacy source claims and explicit proof locations.
- `literature_06_qualify_prose`, `08_legacy_detail_edits`: reviewable edit scripts with before/after hashes.
- `literature_07_secondary_sources`: exact legacy definitions, appendices and builder/closure source.
- `literature_09_diff_review`: saved substantive diff.
- `literature_10_ledger_artifacts`, `14_final_evidence_read`: line-numbered repaired target, source entrypoints and fresh raw-file identities.
- `literature_11_prior_authored_report_read`: reading the earlier authored claim report, explicitly authorized as guidance. No computation cache was read or reused.
- `literature_12_preserve_generated_scope`, `13_conversion_scope_check`: builder prose fix and successful in-memory conversion checks. This is a generation check, not a PDF compilation.

The scientific input hashes printed by command14 still match the frozen values: order8 e780f097…, order10 92b02433…, order12 9a784dc5…, rank81 manifest 59848eb1…, rank81 certificate c329edc4…, octic map30140fa0…, degree10 map429dbf74…. Full SHA-256 values are retained in the command stdout.

The coordinator reported successful fresh graph, independent directional-derivative, graph-parity and Lorentz-transform checks, and a separate packaging failure/repair. Those reports do not erase the frozen source mismatch or establish the unproved polynomial identities. The orbit-tangent result and a preliminary PDF compilation subsequently passed, as reported by the coordinator. The complete corrected degree-ten map outcome and final PDF compilation after the orbit addition remain separate integration items.

## Orbit-tangent addendum

The coordinator supplied `../root-review/orbit_tangent_certificate.json`, SHA-256 `94813eeb36ed9d07fea0a95f41490d31bba2cf268f56ee68761eaba15fdf3557`. Command `literature_15_orbit_evidence_read` freshly read and hashed it; command `literature_16_add_orbit_witness` added its argument and path to the graph manuscript. The implementation is reported as pure Python signed alternating components, infinitesimal matrix action and modular elimination, with no repository imports. This reviewer inspected the artifact metadata, not a second implementation of that calculation.

| Prime | Seed | Action rank | 45×45 minor residue | All81 Jacobian rows annihilate all45 action rows |
|---|---|---|---|---|
| 50021 | 16999642918068834541 | 45 | 5222 | true |
| 32749 | 9932584768098142723 | 45 | 10852 | true |

**Argument:** the action matrix has45 rows, with entries integral linear polynomials in the independent126 components. A verified nonzero minor modulo either prime proves generic characteristic-zero action rank at least45. It cannot exceed45, so it equals45. Differentials of all invariant polynomials annihilate those orbit directions, hence their generic rank is at most126−45=81. Combined with the verified graph Jacobian minor, this substantiates the previously cited maximal generic independence claim. The additional J·action-transpose zero checks are finite implementation validations; the analytic contraction-invariance argument is what applies to every invariant. No conclusion about a global or rational generating family is added.

## Degree-twelve addendum

The mathematics reviewer supplied `../math-review/degree12_polynomial_gradient_certificate.json`, SHA-256 `b4d9de0dfe9966969897924848c08eb445dbce7746b89ec920f340da25945e85`. Command `literature_26_degree12_evidence_read` freshly read and hashed the artifact. It independently evaluates the 10 product monomials and62 graph polynomials, concatenating gradients at two recorded points into a72×252 matrix for each prime. The reported ranks are72 at both50021 and32749; the72×72 minor residues are43334 and12699 respectively. The artifact preserves coordinates, seeds, full matrices, pivots and exact integer determinants of the residue matrices.

A nonzero stacked-gradient minor certifies linear independence of the homogeneous degree-twelve polynomials, provided those entries are the stated gradients: a constant linear relation of the polynomials would differentiate to a relation in the stacked matrix. Lifting the nonzero modular minor gives the characteristic-zero lower bound72. This does not claim72 functionally independent invariants at one point. Equality with the entire degree-twelve invariant space still uses the external Hilbert coefficient72; no independent character/Hilbert computation was performed here.

## Remaining proof obligations, not silent passes

- Correct source transcription and fresh evaluation/map evidence for the repaired degree-ten registry.
- Proof, or explicitly conditional scope, for every reconstructed polynomial identity and flow target map.
- The fresh degree-twelve homogeneous72-direction lower-bound certificate is now supplied above. The Hilbert upper bound remains a cited representation-theoretic input rather than a separately recomputed character calculation.
- Generic orbit dimension is supported by the separately executed action certificate above; its definition-to-implementation correspondence remains the ordinary computational trust boundary, not an unproved subtraction assumption.
- Root’s compilation/render inspection of the repaired paper and packaging validation; this reviewer has not claimed those checks.
- Exhaustive literature priority is neither completed nor claimed. The bounded search report supplies 47 recorded query strings and primary-source coverage limits.

The repaired prose preserves the graph certificate’s valid mathematical implication while keeping these other claims at their actual evidentiary strength.

## Subsequent exact source-map evidence

The source reviewer subsequently supplied an exact bounded-CRT evaluation certificate and corrected maps. Commands `literature_55_exact_source_evidence` and `literature_56_exact_source_scope` read their hashes, premises, ranks and fresh-crosscheck statuses. This is new evidence after the earlier pending-status snapshot; it does not validate the frozen J10–J12 readings.

| Artifact in `../source-review/` | SHA-256 |
|---|---|
| `exact-source-evaluation-certificate.json` | `01f9ab8d8f966827f820541a6e0bfec8e8bf64f710ec5b9f3be6dc825c61ed12` |
| `order8_change_of_basis_exact.json` | `1a98b3c2c5073662ee9a93adcfb3184d2e03611072afb4b184e9dce472917372` |
| `order10_change_of_basis_exact.json` | `9a672693ee237a98406595a1b7540ceaa686853148b8a0d142b06f544964424d` |

The source reviewer reports 14 binary points evaluated over seven primes, with rigorous numerator bounds allowing unique exact integer recovery by CRT. Exact graph evaluation ranks are7 and14. **Conditional proof:** if the published Hilbert coefficients are valid upper bounds7 and14 and the literal source contractions are invariant polynomials, those graph families are bases and evaluation on these points is injective on the relevant invariant spaces. The exact solved coordinate maps then imply polynomial identities. This injectivity argument is stronger than holdout agreement, but its Hilbert and invariance premises must remain explicit.

The corrected source degree-ten span has rank12, its primitive quotient rank11, its union with the two-dimensional product space rank13, and product intersection rank1. The source reviewer reports unchanged octic maps and unchanged first nine decic rows; the final three decic rows change, with difference rank3 even after omitting product columns. The dense modular checks agree at83 fresh points. The displayed hatted octic six-element list has rank5, and rank6 after adjoining the product, so it must not be called a seven-dimensional basis by itself. An independent verifier of the CRT proof is separately owned by the mathematics reviewer and is not silently assumed here.

The six older manuscript variants retain explicit archived-model qualifications. Their regeneration does not promote their old tables to the corrected-source interpretation. Root integrates the new exact-map evidence into the graph paper and final audit package.
