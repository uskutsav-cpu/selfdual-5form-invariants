# Literature coverage and manuscript qualification report — phase 02

Date of research: 2026-09-07. Frozen reference commit: `2b7663bbf5a06d1340973434f195a84ae2773e8f`. Prose repairs are in the separate `repair-checkout`; the frozen checkout is not edited.

## Finding and limits

The inspected primary sources do not furnish an explicit maximal 81-invariant family for a general real self-dual five-form in signature (1,9). This is a statement about the documented coverage, **not a novelty or priority finding**. Searches by equivalent representation names did not produce a primary source establishing an equivalent explicit family. They do not exclude one under other terminology, in unindexed material, or in an uninspected citation.

A relevant methodological precedent missing from the first search was found: Elamaran, Ferko and Scarlett use contraction graphs/tensor networks with numerical linear algebra for tensor invariants. Their main example is the general three-form in six dimensions; their conclusion specifically leaves chiral five-forms in ten dimensions as future work. The repaired graph manuscript cites that work and makes no priority claim. [Primary article](https://doi.org/10.1103/ny3m-drnj), [arXiv full text, section 5](https://arxiv.org/html/2512.23750).

The frozen literature-map audit remains failed because its implemented degree-ten J10–J12 antisymmetrizers differ from the primary PDF and TeX. This finding was supplied by the separate source reviewer through the coordinator. This reviewer does not claim to have independently retranscribed those indices. Corrected source maps require separate formula and execution evidence; none of the archived B10 claims is silently transferred to a corrected interpretation. This failure is distinct from the graph-only Jacobian argument.

## Primary-source coverage

| Primary work and date | Passage inspected and relevance | Explicit 81-family status in inspected material |
|---|---|---|
| M. Cederwall, J. Hutomo, S. M. Kuzenko, K. Lechner, D. P. Sorokin, *Some remarks on invariants*, arXiv:2509.14350v2 (29 January 2026), J. Phys. A 59 (2026) 065203 | Section 4, Eq. (4.2), low-degree constructions and section 4.1.4; generic count and Hilbert input, incomplete high-degree construction. | Does not provide the full explicit family. [Primary text](https://arxiv.org/html/2509.14350v2), [publisher DOI](https://doi.org/10.1088/1751-8121/ae3bb8). |
| J. Hutomo, K. Lechner, D. P. Sorokin, *On non-linear chiral 4-form theories in D=10*, arXiv:2509.14351v2, JHEP 02 (2026) 147 | Section 2.1 explicitly distinguishes the dimension count from finding all explicit invariants; conclusions discuss restrictions of stress-tensor deformations. | Explicit construction remains open in this source. [Primary text](https://arxiv.org/html/2509.14351v2). |
| A. Elamaran, C. Ferko, S. Scarlett, *Machine Learning Invariants of Tensors*, arXiv:2512.23750v1 (26 December 2025), Phys. Rev. D 114 (13 July 2026) 026016 | Abstract, graph algorithm, six-dimensional three-form examples and section 5; prior graph/numerical methodology. | Ten-dimensional chiral five-form application is future work. [Primary text](https://arxiv.org/html/2512.23750), [journal article](https://doi.org/10.1103/ny3m-drnj). |
| Z. Avetisyan, O. Evnin, K. Mkrtchyan, *Nonlinear (chiral) p-form electrodynamics*, arXiv:2205.02522v2 (4 June 2022), JHEP 08 (2022) 112 | Section 4.4 and relevant appendix; dimension estimate and contrast with six dimensions. | Gives an expected count and low-degree discussion, not an explicit 81-family. [Primary text](https://arxiv.org/html/2205.02522v2). |
| G. Buratti, K. Lechner, L. Melotti, *Self-interacting chiral p-forms in higher dimensions*, arXiv:1909.10404 (2019), Phys. Lett. B 798 (2019) 135018 | Sections 4–6; quartic ten-dimensional interaction and higher-order outlook. This phase retrieved the full HTML rather than relying on an abstract. | Quartic result, with higher orders outside that result. [Primary text](https://arxiv.org/html/1909.10404). |
| S. M. Kuzenko, *Manifestly duality-invariant interactions in diverse dimensions*, arXiv:1908.04120v2 (3 September 2019) | Seven-page primary PDF; sections 1–2 reformulate U(1) duality-invariant interactions in dimensions 4p. | Related formalism with a different dimensional/self-duality setting; no explicit 81-family found. [Primary PDF](https://arxiv.org/pdf/1908.04120). |
| C. Ferko, S. M. Kuzenko, K. Lechner, D. P. Sorokin, G. Tartaglino-Mazzucchelli, *Interacting Chiral Form Field Theories and T-T-like Flows in Six and Higher Dimensions*, arXiv:2402.06947v2 (3 March 2024), JHEP 05 (2024) 320 | Introduction, section 6 and discussion, with searches for ten-dimensional references; general auxiliary-field/formalism extension. | No explicit 81-family located in those passages. This was targeted reading, not a line-by-line audit of all 1,598 HTML lines. [Primary text](https://arxiv.org/html/2402.06947v2). |
| M. F. Paulos, *Higher derivative terms including the Ramond-Ramond five-form*, arXiv:0804.0763v2 (20 April 2010), JHEP 10 (2008) 047 | Sections 3.8–4 and scope of the higher-derivative expansion; finite tensor structures in a specific string correction. | Different fixed-order problem, no full arbitrary-degree 81-family. [Primary text](https://arxiv.org/html/0804.0763v2). |
| J. F. Melo and J. E. Santos, *Stringy corrections to the entropy of electrically charged supersymmetric black holes with AdS5 × S5 asymptotics*, arXiv:2007.06582v3 (3 March 2022; first submitted 13 July 2020), Phys. Rev. D 103 (2021) 066008 | Six-page PDF, Eq. (12)–(14), Table I, fixed higher-derivative corrections and correction of Paulos table typographical errors. Full PDF retrieved in phase 02. | Twenty correction monomials are not a maximal invariant family of the general five-form. [Primary PDF](https://arxiv.org/pdf/2007.06582), [version metadata](https://arxiv.org/abs/2007.06582). |

Source inconsistency retained explicitly: Cederwall section 4.1.4 says 64 new degree-twelve directions while Eq. (4.2) has exponent 62; the accompanying total 83 is consistent with 62 plus 21 lower-degree directions. The frozen inventory uses 62. We did not alter that numerical result from the inconsistent prose. [Primary source](https://arxiv.org/html/2509.14350v2).

## Search method and closure

Phase 01 recorded 32 exact query strings in its authored `literature-review/search-queries.md`. Phase 02 added 15 exact queries below, giving 47 recorded query strings across the two phases, with possible conceptual overlap. The phase-01 report is an authored research record, not fresh phase-02 computational evidence. No old computational cache or checkpoint was reused.

Queries used tensor names, selfdual/self-dual spellings, chiral four-form potential versus five-form field strength, 81, functional basis, graph methods, Spin(10), SO(1,9), the 126 representation and Dynkin label (00002). The new graph-method paper supplied an additional backward-reference route. Technical conclusions use primary papers rather than search snippets, third-party summaries or discussion-board answers.

The current pass resolves the earlier abstract-only/PDF-access gaps for Buratti, Kuzenko, Melo/Santos and the recent graph-method paper. The CERN Indico “Invariant Quotient Sub-Rings” slide link still returns an access error through the available retrieval tool; its search-indexed excerpt concerns an amplitude ring, and is not relied on for a mathematical conclusion. The related HHH amplitude paper was already excluded on primary scope in phase 01.

This is a bounded, broad literature search, **not exhaustive database coverage**. There was no complete MathSciNet/zbMATH review, no exhaustive forward-citation graph, no bulk scan of all arXiv preprints, no full search in every language, and no assertion about unpublished/private work. Current search-index snippets also mix crawl dates with publication dates; the dates above use primary metadata where available. No absence-of-hits argument is used as a theorem or submission priority claim.

## Exact new queries

1. `"self-dual" "five-form" "81" invariants basis 2026`
2. `"self-dual" "5-form" "basis" "invariants" -site:researchgate.net -site:emergentmind.com -site:themoonlight.io`
3. `"Spin(10)" "126" "polynomial invariants"`
4. `"selfdual" "five-form" "invariants"`
5. `"Machine learning invariants of tensors"`
6. `"self-dual" "81" "basis" invariants -site:emergentmind.com -site:researchgate.net -site:themoonlight.io`
7. `"2509.14350" citations "invariants" -site:emergentmind.com -site:researchgate.net -site:themoonlight.io`
8. `"self-dual" "five-form" "functional basis"`
9. `"self-dual" "5-form" "81" invariants -site:emergentmind.com -site:themoonlight.io -site:researchgate.net`
10. `"Spin(10)" "126" invariant ring`
11. `"D5" "00002" invariants`
12. `"Some remarks on invariants" "basis" -site:researchgate.net -site:emergentmind.com -site:themoonlight.io`
13. `"chiral" "five-form" "invariants" "2026" -site:researchgate.net -site:emergentmind.com`
14. `"selfdual" "5-forms" invariants basis`
15. `"SO(1,9)" "invariants" "basis"`

## Provenance and deliverables

- `fresh-web-retrieval-log.json`: phase-02 batches 01–07, dated queries and raw retrieval results.
- `fresh-web-retrieval-log-supplement.json`: batch 08.
- `primary-metadata-log.json`: batch 09, including exact version/publication dates.
- `manuscript-claim-ledger.md`: central graph claim chain and sentence/claim ledger, plus older-draft theorem audit.
- `manuscript-changes.json`, `legacy-detail-changes.json`: edit before/after hashes.
- `qualify_manuscripts.py`, `qualify_legacy_details.py`, `qualify_generation.py`: recorded, reviewable prose transformations; scripts run through the phase-02 command logger.
- Numerical execution and source-transcription evidence belong to the coordinator and other reviewers. Their component checks do not convert this report into an overall PASS.
