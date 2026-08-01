# Authorship and credit --- final position

Authorship is not decided here and cannot be. What this file does is record the
contribution facts accurately enough that the decision can be made from them.

It supersedes nothing in `submission_candidate/CONTRIBUTION_LEDGER.csv`; it
adds the JHEP-specific work and states the credit questions that are still open.

## Principles applied

- Mentorship, code access, discussion and institutional position are not, by
  themselves, authorship.
- An AI system is not an author.
- Credit for a result goes to whoever produced it, including when that is
  awkward.

## Contribution record for this manuscript

| contribution | who | evidence |
|---|---|---|
| research question and mathematical design | HUMAN --- NAME REQUIRED | repository history predating this work |
| tensor-side implementation (`sdinv`) | HUMAN --- NAME REQUIRED, with AI assistance | git history of `src/sdinv` |
| spinor-variable enumeration archive | THIRD PARTY --- NAME AND PERMISSION REQUIRED | archive outside this tree; Windows paths under another person's home directory |
| the count of 81 functionally independent invariants | THE SOURCE LITERATURE | JHEP 02 (2026) 147; J.Phys.A 59 (2026) 065203 |
| the enumerate-evaluate-relate method | PRIOR ART | Phys.Rev.D 114 (2026) 026016 |
| split-signature correction | AI-derived; requires confirmation | `spinor_trace_bridge/docs/REAL_FORM_DICTIONARY.md` |
| exact bridge, inverse, equivariance certificates | AI-written; requires confirmation | `spinor_trace_bridge/` |
| exact analytic Jacobian and integral basis | AI-written | `spinor_trace_bridge/src/sdbridge/` |
| 15-cell rank certificate matrix and its provenance apparatus | AI-written | `results/rank81/`, `audit/RANK_MATRIX_*` |
| exact rational D10/Q10 closure | AI-derived | `scripts/exact_D10_Q10_characteristic_zero.py` |
| cardinality bound for minimality | AI-derived; elementary, not claimed as novel | manuscript proposition; PO-08 |
| source corpus and citation graph | AI-assembled from INSPIRE-HEP and Crossref | `audit/JHEP_SOURCE_*` |
| prior-art identification that narrowed the method claim | AI-found in the citation sweep | `audit/JHEP_CURRENT_CITING_PAPERS.md` |
| manuscript text | AI-drafted; requires author rewriting | `manuscript/jhep/` |
| supervision | HUMAN --- NAME REQUIRED | |
| funding | UNKNOWN --- MUST NOT BE INFERRED | |

## Credit questions that are open

1. **The numerical rank 81.** The count is the source literature's. This work
   contributes a certificate. The manuscript must not read as though it
   discovered the number, and the introduction is where that goes wrong most
   easily.
2. **The exact characteristic-zero certification.** New here as far as the
   search goes, and produced by AI. Whether a human author is willing to stand
   behind it is a question for them, not a formality.
3. **The bridge.** Same position.
4. **The third-party archive.** Its author contributed the candidate selection
   that several results depend on. That is a real scientific contribution and
   the manuscript names its role in the data availability statement. Whether it
   warrants authorship, acknowledgement, or neither, is not an AI's call, and
   the person has not been contacted.
5. **The cardinality proposition.** Elementary and explicitly not claimed as
   novel. Included because it discharges half of PO-08.

## What is recorded as fact, not judgement

- No human has verified any result in this manuscript.
- No approval has been given.
- The archive owner has not been contacted.
- No licence has been chosen.

These are the four things a reader of this file most needs to know, and none of
them improves by being phrased more gently.
