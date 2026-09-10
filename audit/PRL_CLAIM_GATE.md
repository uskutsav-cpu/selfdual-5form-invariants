# PRL claim gate

Scored against the seven criteria, from final evidence. The decision rule is
that the Letter is finalised for submission **only if all seven pass**.

| criterion | verdict | evidence |
|---|---|---|
| Validity | **PASS** | Every central dimension is an exact rank over `F_p` with recorded pivot rows and columns. Degree-8 span equality holds at four primes with holdout validation. Exact Jacobian rank 81 with Euler homogeneity passing for every evaluated candidate. No unresolved defect changes any central claim. |
| Compression | **PASS** | The central logic is the exact dimensions and the quotient; it fits the Letter core with specialists' material in End Matter and Supplemental. |
| Independence | **PASS** | The quotient is obtained in graph, block-tensor and spinor descriptions, connected by a map whose kernel and image are identified by span equality and which is equivariant under the full rotation group. The spinor-to-five-form map agrees with an independent third-party implementation exactly, entry by entry. |
| Innovation | **CONDITIONAL** | The result goes materially beyond the known count 81 and the known non-universality of stress-only flows: it gives the exact codimension, explicit representatives, and minimality. But every novelty row in `NOVELTY_MATRIX.md` is still marked PROVISIONAL because the systematic literature sweep has not been done. Innovation cannot be scored PASS on evidence that does not yet exist. |
| Impact | **FAIL, as currently supported** | The theorem constrains formulation at **one order**. "Any scheme must add at least three generators at degree ten" is a real constraint, but it is not shown to persist, grow, or stabilise at higher order, and degree twelve is explicitly not classified. A referee asking "what happens at the next order?" has no answer here. |
| Broad interest | **FAIL, as currently supported** | The narrative --- a standard construction does not reach everything, and here is exactly what it misses --- is accessible. But the object is a specific graded piece of a specific invariant ring, and nothing in the result reaches a reader who does not already care about ten-dimensional chiral form dynamics. |
| Physical content | **BORDERLINE** | There is a field-theory consequence (a requirement on the generator set of any deformation scheme at this order) and an explicit inaccessible interaction. There is no prediction, no amplitude, no symmetry consequence, and no selection principle among the three directions. |

## Decision

**The gate does not pass.** Three criteria are not met on current evidence:
Impact, Broad interest, and (conditionally) Innovation.

Per the stated decision rule, the outcome is therefore:

1. The PRL manuscript is completed as a **polished draft labelled
   NOT YET SUBMISSION-READY**, with the failing criteria named in the file
   itself so the label cannot drift loose from its reason.
2. The longer-form manuscript is the vehicle for the result as it stands. It is
   complete, compiles clean, and does not overclaim.

## What would change the verdict

These are concrete, not aspirational.

**For Impact.** Establish the behaviour at degree twelve. If the codimension
grows, the result becomes a statement about a systematic failure rather than an
isolated one. If it stabilises, that is a structural theorem. Either outcome is
a Letter; the present order-ten-only statement is not. Degree twelve is
explicitly out of scope for this execution.

**For Broad interest.** Connect one of the three directions to something with
independent standing --- a supersymmetry obstruction, a causality or
hyperbolicity condition, or a known effective-action structure. A selection
principle among the three would do it. None is currently derived, and inventing
one is forbidden.

**For Innovation.** Complete the literature sweep described in
`RELATED_WORK_SEARCH.md`. This is bounded work, not research: walk the citation
graph of the two source papers for any earlier explicit degree-ten construction.
If none exists, Innovation upgrades to PASS on evidence.

## Note on how this was scored

The temptation is to argue the borderline criteria upward, because the underlying
computation is solid and it would be satisfying to call it a Letter. That is
exactly the failure mode the specification's own integrity rule names: *never
manufacture a PRL-level claim*. The computation being difficult and correct is
not the criterion. Impact and broad interest are separate tests, and they are not
currently met.
