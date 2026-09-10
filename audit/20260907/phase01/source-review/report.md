# Independent source-formula audit: stop on transcription discrepancy

Frozen commit: `2b7663bbf5a06d1340973434f195a84ae2773e8f`.

**Finding:** the degree-10 source transcription/program in `src/sdinv/published_degree10_invariants.py` disagrees with the original arXiv v2 colored brackets for candidates 10, 11 and 12. The independent audit stopped at this source conflict. No tensor evaluation or repair followed.

## Original-source evidence and independence

The original [arXiv v2 PDF](https://arxiv.org/pdf/2509.14350v2), [TeX source](https://arxiv.org/src/2509.14350v2), and [HTML section 4.1.4](https://arxiv.org/html/2509.14350v2#S4.SS1.SSS4) were retrieved afresh. PDF printed/page number 25 was rendered and visually read; colored brackets were also checked in the original TeX. The entire degree-10 list is conventionally referred to as equation (4.24), although that number appears on a blank eqnarray row below candidate 1 and individual remaining candidates have no printed equation number. Exact TeX labels are `I1010`, `I1011`, `I1012`.

The manually authored source transcription `manual-transcription.md` was frozen by wrapped command `source_012_freeze_manual_transcription` **before** the first frozen implementation/result-file read, `source_013_read_frozen`. The transcription includes all six degree-8 primary expressions, all five hatted expressions plus their sixth entry, and all twelve degree-10 expressions, along with contraction and bracket conventions. It is not copied from repository implementation or previous audit notes. Original source, PDF, rendered pages, and exact line-numbered source/code excerpts are retained.

## Exact discrepancy

Let `Q[a,b,c,d,e;f]` be the covariant 1050 tensor, with its first five slots already normalized-antisymmetric. Thus the source's black bracket operation is already present in Q. Define, in zero-based array axes,

- `B = Alt_(4,5) Q`, a normalized trailing-pair operation, factor `1/2!`;
- `T = Alt_(3,4,5) Q`, a normalized trailing-triple operation, factor `1/3!`.

All red operations act **after** the first-five black operation. In the all-covariant presentation, each repeated dummy edge has one inverse metric; this retains source upper/lower contractions while making the bracket programs unambiguous. No conjugation or additional trace subtraction is introduced.

| Candidate | Original TeX lines / source operation | Frozen primary implementation |
|---|---|---|
| `I10^(10)` | label line 1641, formula lines 1642–1643: red pair over `mu1,mu2` on the first Q, i.e. `B,Q,Q,Q,Q` | function line 406 defaults `reading="outer"`; `_nested_pair` lines 395–398 returns Q unchanged for that reading. Registry lines 529–535 chooses this evaluator. |
| `I10^(11)` | label line 1645, formula lines 1646–1648: three red triples on the final three Q factors, over `(nu1,nu2,nu3)`, `(lambda2,lambda3,nu1)`, `(lambda1,lambda3,nu3)`, i.e. `Q,Q,T,T,T` | function line 429 defaults `reading="outer"`; lines 442–446 leave the last three Q factors without the three red projections. Registry lines 536–542 chooses this evaluator. |
| `I10^(12)` | label line 1650, formula line 1651: three red triples on the final three Q factors, over `(nu1,nu2,nu3)`, `(rho2,lambda2,lambda3)`, `(nu3,lambda1,lambda3)`, i.e. `Q,Q,T,T,T` | function line 451 defaults `reading="outer"`; lines 463–467 leave the last three Q factors without the three red projections. Registry lines 543–549 chooses this evaluator. |

Original TeX line 1653 explicitly specifies the order of the red and black operations. `BRACKET_STAGES`, frozen code lines 578–586, instead calls candidates 10–12 `black only (nested)`. That classification is directly contradicted by the original colored TeX and rendered PDF.

The optional `nested` branch at frozen lines 399–402 applies **only** a pair antisymmetrizer on axes `(4,5)`. It supplies the displayed trailing-pair operation for candidate 10, but it does not transcribe the three trailing-triple operations for candidates 11 or 12: only their first affected factor goes through `_nested_pair`, and their other two factors receive no red operation. Candidate 10's optional numeric reading and its incorrect black-only metadata must therefore be distinguished from the primary default reading.

Normalized formula differences, using the contraction topologies already written independently in `manual-transcription.md`:

```
                    Original source       Frozen primary       Frozen nested variant
I10^(10) factors    B,Q,Q,Q,Q              Q,Q,Q,Q,Q            B,Q,Q,Q,Q
I10^(11) factors    Q,Q,T,T,T              Q,Q,Q,Q,Q            Q,Q,B,Q,Q
I10^(12) factors    Q,Q,T,T,T              Q,Q,Q,Q,Q            Q,Q,B,Q,Q
```

The table concerns bracket operations before index raising. It is a source/program discrepancy, not a claim that all these different-looking contractions are necessarily different polynomials. No unproved tensor identity has been used to repair or reinterpret the discrepancy.

## Qualifications and stopped work

The source expressly presents the twelve degree-10 expressions as possible basis candidates. The present finding does not prove or disprove the rank of either the literal source list or the frozen implementation. In particular, **the mathematical effect on the 12×14 atlas and its claimed one-dimensional product intersection remains unevaluated**. The independently certified rank-81 graph minors, if otherwise valid, are **not disproved by this source-transcription finding**.

`results/order8_change_of_basis.json` and `results/order10_change_of_basis.json` were captured alongside implementation files in the fresh `source_013_read_frozen` log; their scientific contents were not inspected before the stop trigger. No modular samples, symbolic identity checks, basis-map checks, or atlas/intersection verification were executed by this subaudit.

The degree-8 manual transcription matches the visible contraction topologies during the initial source/code review, but no numerical basis-map certification was completed. Degree-8 source prose about trace-subtracted 660/770 irreps is less explicit than the displayed formulas; the frozen degree-8 implementation explicitly chooses literal formulas without silently adding trace subtractions. The hatted second definition is printed as (4.19), with its second equality printed as (4.20), a numbering distinction suppressed by the HTML rendering.

Separately, the original PDF p25 prints degree-12 count 64 while giving cumulative count 83. Equation (4.2) prints degree-12 primitive exponent 62, and 1+2+6+12+62=83. This is an internal source inconsistency consistent with a prose typo; it is not evidence against a frozen numerical value of 62.

## Provenance and procedural record

All downloaded sources and audit deliverables are siblings outside the immutable checkout, under `source-review/`. No frozen file was edited. No old checkout, earlier agent analysis, checkpoint, cache, or previous result was reused. One bootstrap read-only `pwd && ls -la` inspected the newly created audit directory before wrapper use; root was immediately informed. Root then authorized plain reading of fresh audit command logs so that wrapper output did not have to be recursively wrapped.

Relevant wrapped command names:

- `source_005_curl_pdf`, `source_006_curl_source`: successful original-source downloads using system TLS; earlier wrapped urllib attempts failed DNS/trust validation and are preserved.
- `source_007_pdf_skill_and_extract`, `source_008_tex_and_pdf_tools`: original TeX extraction and source reading.
- `source_009_pdf_text`, `source_010_pdf_pages`, `source_011_pdf_render`: text indexing and visual render preparation.
- `source_012_freeze_manual_transcription`: independent manual transcription frozen.
- `source_013_read_frozen`: first frozen-file reading; discrepancy encountered here.
- `source_014_package_discrepancy_only`: exact excerpts, line numbers, and hashes packaged after stop, without tensor evaluation.
- `source_015_write_final_discrepancy_report`: this report and unexecuted reproduction script written after stop.

`source-conflict-evidence.json` contains exact line-numbered excerpts from both the original TeX and the frozen implementation. `verify_source_evidence.py` is a standalone **unexecuted** provenance-check script; it imports no repository modules and performs no tensor or scientific calculation. It is supplied for later reproduction, not run after the audit's stop instruction.

SHA256:

| Artifact | SHA256 |
|---|---|
| manual-transcription.md | `39695b36bc78a70e80c38a7981b40976dd08bc31fb98fccccbe7157a9ff9620c` |
| original-InvariantsV2.tex | `a4e9f50e0047400e383820c9ba35c6cd2447faddcea627f890a5f9a6826957f2` |
| arxiv-v2.pdf | `ec51d9e22c4d75651e2024d09b17562bc5c4d89c191c3ab11cf86697a9c7880e` |
| arxiv-v2-source.tar | `f3f1f2fed99595545a972aa788bf70212a134f65b16882466939d22840dcb540` |
| frozen published_degree10_invariants.py | `f3a5ce94b4f9066e58e9aa893e33c95079bf6fc5b069644756847ec3dc5ad6ef` |
| source-conflict-evidence.json | `c6416921df07c451275a3c27961e56bdafe5713909128cd6be32d923deaac2c7` |
