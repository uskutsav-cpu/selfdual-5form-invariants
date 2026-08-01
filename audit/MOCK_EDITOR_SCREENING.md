# Mock editorial screening

The six questions, answered from evidence.

### 1. Is there significant new material?

**Qualified yes, pending literature confirmation.** The degree-ten graded
dimension, the complete incidence of its natural subspaces, the quotient with
explicit representatives, the exact bridge with certified kernel and image, and
the exact modular Jacobian are all absent from the two source papers consulted.
No systematic sweep beyond those two has been done, so every novelty row remains
PROVISIONAL. An editor would be right to ask for that sweep before accepting the
framing.

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
ten-item limitations section, and 32 automated gates fail the build on specific
overclaims --- and, symmetrically, on the *absence* of specific required
disclosures. The gates are negation-aware, because the first version flagged the
manuscript's own disclaimers and would have created pressure to delete them.

---

## Screening decision (simulated)

**Send for review, with a note to the referee** that the novelty framing rests on
a literature search the authors describe as incomplete, and that the physics
significance is the point most in need of expert judgement.
