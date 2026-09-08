# Legacy PDF regeneration and bounded visual review

All six qualified legacy sources compiled successfully with bundled Tectonic0.17.0. They passed the bounded review-draft checks described below. These PDFs are not a scientific audit-pass statement or submission-ready artifacts.

| Source under repair-checkout | New PDF under literature-review | Pages | Final build command |
|---|---|---:|---|
| `manuscript/main.tex` | `compiled/main/main.pdf` | 26 | `literature_29_compile_network_main` |
| `manuscript/jhep/main.tex` | `compiled/jhep/main.pdf` | 49 | `literature_29_compile_network_jhep` |
| `manuscript/prd/main.tex` | `compiled/prd/main.pdf` | 26 | `literature_35_recompile_prd` |
| `manuscript/prd_letter/main.tex` | `compiled/prd_letter/main.pdf` | 6 | `literature_47_recompile_prd_letter` |
| `manuscript/prl/main.tex` | `compiled/prl/main.pdf` | 4 | `literature_59_final_compile_prl` |
| `submission_candidate/main.tex` | `compiled/submission/main.pdf` | 26 | `literature_29_compile_network_submission` |

The total is137 pages. Source and PDF SHA-256 values, checked against the current files, are in `pdf-delivery-manifest.json` and each `compiled/<variant>/qa/qa-manifest.json`. Main tracked legacy PDFs were not replaced. The two repaired PRL figure PDFs were installed in repair-checkout only after their individual visual checks. Root owns the graph-paper PDF.

## What was inspected

All137 pages were rendered at62dpi and assembled into11 complete contact sheets. Every contact sheet was viewed to check page flow, margins, figures and tables. All six opening pages were viewed at125dpi. The audit-scope paragraphs are visible; PDF text checks confirm the source mismatch, conditional identity interpretation and absence of priority claims. All PDFs have no extracted unresolved-reference marker `??` and no replacement-character markers. Source/PDF hashes match the rendered versions.

The PRL page containing the two diagrams was also examined in detail. The initial diagram assets had colliding labels; the repaired figures were inspected separately at170dpi, then again on the final PDF page. No missing float, obvious content clipping or page-level overlap was observed in the final rendered set. Contact sheets are not a full-resolution proofread of every character or equation.

## Repairs needed to complete the builds

- Main and submission sources now select the XeTeX hyperref driver conditionally, enabling Tectonic while retaining other-engine compatibility.
- PRD had a duplicate audit paragraph caused by matching a commented maketitle as well as the real command. It now has one audit paragraph and the restored comment. In-memory generator conversion also verifies exactly one audit paragraph.
- PRD-letter's APS bibliography style raised errors for article entries without journal fields. Verified current Hutomo and Elamaran publication metadata were added; remaining entries lacking a journal field were changed to misc while preserving their citation fields. These entry-type changes do not assert new publication status.
- PRL uses the compiler-recommended floatfix class option. Its two figure generators now wrap and reposition labels, reduce hatch density and enlarge vertical spacing. They render the same archived numerical labels and captions. This was presentation regeneration of explicitly inherited results, not fresh scientific verification.

Exact commands and failed attempts remain in the sibling `commands/` directories. Initial package downloads failed under restricted network access; permitted network access supplied missing Tectonic packages. The first main build then exposed the real hyperref driver mismatch, which was corrected. The initial plotting runtime lacked Matplotlib; an isolated `literature-review/plotting-runtime/` installation supplied it without changing the scientific environment.

## Residual warnings and limitations

Underfull-box warnings remain in some justified text, tables and bibliography entries; no corresponding obvious clipping was found. JHEP reports its obsolete pagecolor option and the expected missing-author-email draft placeholder. Main/submission retain hyperref bookmark math-token warnings. APS bibliography warnings about missing issue-number fields remain; these do not leave unresolved citations in the extracted final PDFs.

REVTeX still emits stuck/deferred-float warnings for PRL and a stuck-float warning in the last PRD helper log. The final renders visibly contain both PRL figures and all five PRD figures. Those warnings are recorded, not silently called absent. Helper JSON preserves the tail of compiler output and can omit earlier messages in long builds; the PRD-letter raw Tectonic rerun retained a full diagnostic log to identify all missing-journal errors. Final PRD-letter helper output no longer reports BibTeX errors.

The draft authorship, affiliation and submission-status placeholders are intentionally visible. The legacy PDFs retain old tables under their explicit archived-model qualifications. The new corrected source-map certificate belongs to the separate scientific integration and does not retroactively validate the frozen formulas.
