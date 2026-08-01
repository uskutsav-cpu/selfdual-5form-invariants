# Mock editorial screening

The six questions, answered from evidence.

### 1. Is there significant new material?

**Qualified yes, pending literature confirmation.** The degree-ten graded
dimension, the complete incidence of its natural subspaces, the quotient with
explicit representatives, the exact bridge with certified kernel and image, and
the exact modular Jacobian are all absent from the six papers audited directly in
`audit/RELATED_WORK_COMPLETE.md`. Every novelty row nonetheless remains
PROVISIONAL, and the reason is no longer an outstanding search: a search
establishes absence of evidence, not evidence of absence, and an editor would be
right to want an expert in the field to say so rather than a bibliography.

### 2. Is the result of interest to the journal's audience?

**Uncertain, and the honest answer is "depends on the reader".** For someone
constructing non-linear chiral four-form theories, being able to decide whether a
degree-ten term is reachable is directly useful. For a reader wanting a physical
prediction, there is none here. The manuscript does not pretend otherwise.

### 3. Is there a clear physics point?

**Yes, and it is narrow.** The stress-flow construction misses exactly three
degree-ten directions, they are exhibited, and they are not products of anything
simpler. That is a statement about what a construction can and cannot generate,
not a statement about nature.

### 4. Are the principal claims understandable without running the code?

**Yes.** Every dimension is stated in the text and in tables, the incidence table
is complete, and the reasoning is in the main text rather than deferred to the
supplement. A reader who never opens the repository can follow every claim; they
would have to take the arithmetic on trust, which is what the certificates are
for.

### 5. Are all computational claims reproducible?

**Yes, with one documented exception.** Every number in the manuscript is
generated from a JSON certificate by a versioned script; a missing artifact
produces a red marker in the PDF rather than a stale number. The exception is the
archive-dependent results, which need a private copy of third-party code;
a manifest with hashes and adapter instructions is provided.

### 6. Is the manuscript honest about limitations?

**Yes, and the mechanism is enforced rather than promised.** There is a
limitations section, and 50 automated gates fail the build on specific
overclaims --- and, symmetrically, on the *absence* of specific required
disclosures. The gates are negation-aware, because the first version flagged the
manuscript's own disclaimers and would have created pressure to delete them.

The gates now also cover `docs/`, not just the manuscript sources. That was
added after two status documents were found asserting a superseded Jacobian rank
while the certificate beside them said otherwise --- the manuscript was correct
throughout, but a reader picking the project up reads those documents first.

---

## Screening decision (simulated)

**Send for review, with a note to the referee** that the novelty framing rests
on a literature search the authors do not treat as conclusive, and that the
physics significance is the point most in need of expert judgement.

One caveat on this screening: it is simulated by the same process that wrote the
manuscript, so it is a checklist, not an independent opinion. It cannot supply
the judgement question 2 actually turns on.
