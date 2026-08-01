# AI-assistance disclosure --- JHEP manuscript

Factual, and deliberately unflattering where that is accurate. No AI system is
listed as an author, and none can be.

This extends `submission_candidate/ai_use_disclosure.md`, which covers the work
predating this manuscript. Everything there still holds. What follows is what
was added for the JHEP article.

## What AI assistance did, for this manuscript

| activity | extent |
|---|---|
| code generation | Substantial. The per-cell certificate driver, the read-only matrix aggregator, the execution-freeze and provenance tooling, the exact rational D10/Q10 closure, the source-corpus builder and the pytest counter were all AI-written. |
| test generation | All of them. 32 aggregator tests, 19 test-counter tests. Each was written by the same system that wrote the code they test. |
| debugging | Three defects were found and fixed. A flop-budget mismatch that presented as a scientific evaluation error; a cache key that collided two bibliographic records and served one paper's metadata under another's key; a test-counter fallback that would have miscounted a killed run as a clean one. |
| literature search | 39 sources resolved against INSPIRE-HEP and Crossref, 98 references imported from the two core papers, 18 citing papers enumerated and assessed. This is a search with authoritative metadata, not a survey by someone who knows the field. |
| analysis | The exact rational D10 closure, the structural A10/G10/P10 argument, and the classification of which degree-10 statements are exposed to an exceptional prime. |
| manuscript drafting | Not yet begun at the time of writing. When it happens it will be AI-drafted and will require author rewriting. |
| claim narrowing | The prohibited-claims list, the novelty classifications, and the decision to exclude degree 12 were AI-proposed. They restrict what the paper says rather than extending it. |

## What AI assistance did not do

- **It did not verify anything independently.** Every check was written by the
  same system, in the same session, under the same assumptions. Agreement
  between an implementation and its own tests is not independent verification.
  The four adversarial referee simulations are subject to exactly this
  limitation and say so in their own text.
- **It did not establish novelty.** The prior-art finding that matters most in
  this manuscript --- that Elamaran, Ferko and Scarlett already published the
  enumerate-evaluate-relate workflow --- came from a citation sweep, and it
  narrowed the claim. But absence from a search is not evidence of absence, and
  recognising a prior formulation of the same statement requires knowing the
  field. Every novelty row remains provisional pending author judgement.
- **It did not decide authorship, and cannot.**
- **It did not obtain any approval.** No approval recorded anywhere in this
  repository was given by a human at the time of writing. The checklist in
  `audit/AUTHOR_APPROVAL_CHECKLIST.md` is empty by design.

## One thing worth stating plainly

A referee is entitled to know how much of this was machine-written. The honest
answer is: most of the code, all of the tests, all of the audit apparatus, and
the analysis that produced the exact D10 result. What a human supplied is the
research question, the mathematical design predating this work, the tensor-side
implementation, and --- when it happens --- the judgement about whether any of
it is worth publishing.

## Human verification status

**None has occurred.** This is not a formality: three of the defects listed
above were found only because the same system re-examined its own output under
a different framing, and there is no reason to believe that process is
exhaustive. Independent human review of the bridge derivation, the exact
rational closure and the claim ledger is a prerequisite for submission, not a
courtesy.

## Final responsibility

Rests entirely with the human authors, who must be satisfied that every claim
is one they would defend in front of a referee without reference to how it was
produced.
