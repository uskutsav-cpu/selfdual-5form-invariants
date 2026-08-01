# Proof obligations --- final status for the JHEP manuscript

Generated 2026-08-01T21:35:11+00:00 by `scripts/emit_jhep_proof_obligations_final.py`.

Read the **manuscript consequence** column. An obligation that stays open
is not a caveat bolted onto a surviving claim; it is a claim that was
narrowed or removed.

## Tally

| status | count |
|---|---|
| EXACTLY CERTIFIED | 2 |
| NOT APPLICABLE | 2 |
| OPEN AND EXPLICITLY DELIMITED | 7 |
| PROVED | 1 |
| REMOVED FROM CLAIMS | 1 |

## Obligations

### PO-01 --- PROVED

**Statement.** Canonicalisation is exact at every degree actually used.

**Scientific role.** Underwrites every graph-basis identification on the tensor side.

**Present evidence.** The WL heuristic was removed; canonicalisation is exact via pynauty or raises rather than guessing.

**Missing argument.** Nothing.

**Attempt performed.** Discharged in Phase 0, before this manuscript.

**Result.** Exact canonicalisation throughout.

**Manuscript consequence.** The manuscript may describe canonicalisation as exact.

**Source.** `docs/PROOF_OBLIGATIONS.md; scripts/generate_graph_catalog.py`

### PO-02 --- OPEN AND EXPLICITLY DELIMITED

**Statement.** `leading_field_degree` is correct, not merely self-consistent.

**Scientific role.** Supports the exhaustiveness of the degree-6 argument behind the flow claims.

**Present evidence.** 18 expected generator multisets = 18 present, none missing, none extra; leading degrees additive across products.

**Missing argument.** A hand derivation, independently checked: Tr(tau) has leading degree 4 because the free stress tensor is traceless, and Tr(tau^k) has leading degree 2k for k >= 2. The values are currently computed by the same code they validate.

**Attempt performed.** Not attempted in this manuscript; it is a clean-room writing task, not a computation.

**Result.** Internal completeness established; external derivation absent.

**Manuscript consequence.** No claim in this manuscript rests on it. The flow material appears as an application with its scope stated, and the generator inventory is described as internally complete rather than independently derived.

**Source.** `docs/PROOF_OBLIGATIONS.md`

### PO-03 --- NOT APPLICABLE

**Statement.** I12_61 and I12_62 are polynomial syzygies.

**Scientific role.** Would upgrade a Jacobian dependence at degree 12 to a polynomial identity.

**Present evidence.** A Jacobian dependence at a generic point, which gives functional dependence only.

**Missing argument.** An exhibited polynomial identity: bound the relation degree, enumerate candidate monomials, exact evaluation matrix, modular nullspace, rational reconstruction, fresh-sample verification.

**Attempt performed.** Not attempted. Degree 12 is outside this manuscript's claim scope, so the obligation does not gate anything here.

**Result.** Unchanged.

**Manuscript consequence.** The word 'syzygy' does not appear for these objects. Degree 12 enters only as the certified Jacobian block and as labelled partial evidence.

**Source.** `docs/PROOF_OBLIGATIONS.md`

### PO-04 --- OPEN AND EXPLICITLY DELIMITED

**Statement.** The K6 <-> Sigma_2 identification is the authors' own.

**Scientific role.** Wording of the sextic basis claims.

**Present evidence.** arXiv:2509.14350v2 proves (Sigma_1, Sigma_2) is a sextic basis in the spinor formalism but does not publish the change of basis to (Tr(M^3), K6). The identification here is inferred.

**Missing argument.** The explicit map, from the authors or derived independently.

**Attempt performed.** External. It may need a person rather than a computation, and no contact has been made.

**Result.** Still inferred.

**Manuscript consequence.** The manuscript describes the identification as inferred and cites the source for what it actually proves. It does not attribute the change of basis to the source.

**Source.** `docs/PROOF_OBLIGATIONS.md`

### PO-05 --- NOT APPLICABLE

**Statement.** Tr(M^6) has certified rational coordinates, or every downstream theorem can be stated without them.

**Scientific role.** Any characteristic-zero statement that routes through Tr(M^6) graph coordinates.

**Present evidence.** 29 of 72 columns exceed the CRT uniqueness bound at 15 primes (modulus about 5.2e67). The flow coefficients lifted cleanly at five primes, so this is a height problem specific to Tr(M^6), not a shortage of effort.

**Missing argument.** Either an analytic identity, or a reformulation making graph coordinates unnecessary.

**Attempt performed.** Route (B) is taken here by construction rather than by proof: no claim in this manuscript uses Tr(M^6) graph coordinates. The exact D10 result routes through the rational flow targets, which do lift, not through Tr(M^6).

**Result.** Avoided rather than solved.

**Manuscript consequence.** Tr(M^6) coefficients are never quoted. The manuscript says so explicitly rather than leaving the omission unexplained.

**Source.** `docs/PROOF_OBLIGATIONS.md; results/stress_flow/trace_sector.json`

### PO-06 --- EXACTLY CERTIFIED

**Statement.** A second independent holdout prime validates the reconstructions.

**Scientific role.** Every modular certificate.

**Present evidence.** Two independent holdout primes, 192/192 identical reconstructions across two fit sets.

**Missing argument.** Nothing.

**Attempt performed.** Discharged in Phase 0.

**Result.** Holdout validation is real, not nominal.

**Manuscript consequence.** The manuscript may describe holdout validation as independent, and should name the primes.

**Source.** `docs/PROOF_OBLIGATIONS.md`

### PO-07 --- OPEN AND EXPLICITLY DELIMITED

**Statement.** The K6 transport statement survives field redefinitions and the equations of motion.

**Scientific role.** Gates every physical and Type IIB reading of the flow result.

**Present evidence.** The transport equation is an off-shell statement in fixed conventions.

**Missing argument.** Classify the allowed local field redefinitions at each degree, compute their action on q6, determine whether q6 = 0 is preserved, then repeat modulo the leading equations of motion.

**Attempt performed.** Not attempted.

**Result.** Unchanged.

**Manuscript consequence.** No physical consequence and no Type IIB consequence is drawn from the flow result anywhere in the manuscript. The limitations section says why, naming this obligation.

**Source.** `docs/PROOF_OBLIGATIONS.md`

### PO-08 --- OPEN AND EXPLICITLY DELIMITED

**Statement.** The three-element completion of D10 is minimal under change of basis.

**Scientific role.** Any minimality claim about the quotient representatives.

**Present evidence.** Two separable halves. Cardinality: if D + span(S) = A then applying the quotient map gives span(pi(S)) = Q, and a span of |S| vectors has dimension at most |S|, so |S| >= dim Q. Since dim Q10 = 3 and the exhibited completion has exactly 3 elements, it is of minimum cardinality in any basis. Permutation subgroup: four trials per degree, invariant.

**Missing argument.** Removal minimality under general GL. Requires regenerating the certificates in the new basis and re-expressing the monomial index consistently; the obvious test of multiplying coordinate rows by a random matrix is invalid, because the resulting rows correspond to no actual flow problem.

**Attempt performed.** The cardinality half was proved analytically. The general-GL half was not attempted; its cost and its invalid shortcut are both recorded.

**Result.** Cardinality minimality holds in any basis. Removal minimality holds only for the permutation subgroup.

**Manuscript consequence.** The manuscript may say the completion has minimum cardinality in any basis, and that removal minimality is verified under relabelling. It may not say the representatives are minimal, unique or canonical.

**Source.** `docs/PROOF_OBLIGATIONS.md; results/generalized_flow/minimality_certificates/basis_permutation.json`

### PO-09 --- EXACTLY CERTIFIED

**Statement.** Exceptional primes do not corrupt the modular certificates.

**Scientific role.** Every MOD-CERT row.

**Present evidence.** rank_{F_p} <= rank_Q always, so a modular rank is an unconditional LOWER bound. Agreement across primes is corroboration, not proof, but the direction of any possible failure is determined.

**Missing argument.** For any claim needing an upper bound, a characteristic-zero computation or a Hadamard-type bound on the relevant minors.

**Attempt performed.** The two places where an upper bound was actually needed were closed directly rather than by counting primes. Rank 81: the upper bound 126 - 45 = 81 is analytic. D10: the closure was recomputed over Q with exact rational arithmetic.

**Result.** No surviving claim depends on a modular upper bound.

**Manuscript consequence.** Modular results are stated as lower bounds and labelled 'at the tested primes' where that is all they are. B10 and B10 ∩ P10 carry that label; A10, G10, P10, D10 and Q10 do not.

**Source.** `docs/PROOF_OBLIGATIONS.md; results/stress_flow/D10_characteristic_zero_final.json`

### PO-10 --- REMOVED FROM CLAIMS

**Statement.** An induction on degree supports an all-orders claim.

**Scientific role.** Any all-orders theorem.

**Present evidence.** None. No induction exists.

**Missing argument.** Base cases, a recursion step, preservation of hypotheses, and an argument that no exceptional degree exists.

**Attempt performed.** Not attempted.

**Result.** Unchanged.

**Manuscript consequence.** 'All orders' appears nowhere in the manuscript. Every statement is degree-resolved and names its degrees.

**Source.** `docs/PROOF_OBLIGATIONS.md`

### PO-11 --- OPEN AND EXPLICITLY DELIMITED

**Statement.** Bracket colour in the published equation (4.24) is resolved.

**Scientific role.** Which Q10 Level-B representatives are unconditional.

**Present evidence.** Colour does not survive PDF text extraction, and colour fixes operation order. Both readings of every ambiguous candidate are implemented and projected. P10_10 and P10_12 give identical Q10 images under both readings; P10_09 and P10_11 differ. No ambiguity-robust triple exists among the twelve published candidates.

**Missing argument.** A colour render of the journal page, or a statement from the authors.

**Attempt performed.** Not attempted here; it needs a person or a colour source.

**Result.** The selected basis attains the minimum of one source-reading-dependent member.

**Manuscript consequence.** The basis is called 'preferred ambiguity-minimal', never 'ambiguity-robust'. Only P10_10 and P10_12 are described as unconditional, and the measurement showing no robust triple exists is reported rather than hidden.

**Source.** `docs/PROOF_OBLIGATIONS.md`

### PO-12 --- OPEN AND EXPLICITLY DELIMITED

**Statement.** The degree-10 block class is exhaustively enumerated.

**Scientific role.** Any claim of complete enumeration over M/N contractions.

**Present evidence.** The reverse benchmark met its recovery goal -- Q10 rank 3 independently, span equal to the published Level-B span on fit and holdout primes. It did not meet the exhaustion goal: 5 of 21 sectors are capped at 30 000 raw topologies and even the exhausted sectors were sampled at 40 candidates.

**Missing argument.** A sweep of every canonical candidate in the declared class; roughly 15 hours on one worker as a lower bound, plus an unknown multiple for the capped sectors.

**Attempt performed.** Not attempted; the machine is committed to the certificate matrix and no claim here needs it.

**Result.** Unchanged.

**Manuscript consequence.** The manuscript never claims complete enumeration of every M/N contraction, and never says the reverse search establishes minimality of anything. It reports recovery, which is what was achieved.

**Source.** `docs/PROOF_OBLIGATIONS.md`

### PO-13 --- OPEN AND EXPLICITLY DELIMITED

**Statement.** The Q10 change-of-basis matrices have certified rational entries.

**Scientific role.** Any characteristic-zero statement about the Level-A/Level-B map.

**Present evidence.** Both directions certified modularly at two primes and verified mutually inverse. Rational reconstruction attempted and not certified: two primes give a CRT modulus of about 1.07e9, so a lift is unique only when numerator and denominator are both below about 2.3e4, and the entries are generic residues of that magnitude.

**Missing argument.** More primes. The projection is checkpointed, so the remaining four are incremental rather than a rerun.

**Attempt performed.** Not attempted here. Note this is independent of the D10 result: that used the rational flow targets, not these maps.

**Result.** Unchanged.

**Manuscript consequence.** The Level-A/Level-B maps are described as modular certificates, never as rational identities. dim_Q Q10 = 3 does not depend on them.

**Source.** `docs/PROOF_OBLIGATIONS.md`

## Minimality, split into the things it is usually confused with

| notion | status | statement |
|---|---|---|
| cardinality lower bound | **PROVED, in any basis** | |S| >= dim Q for any completing set S, because the quotient map sends S to a spanning set of Q. |
| removal minimality of the selected set | **VERIFIED under the permutation subgroup only** | No element of the exhibited triple can be dropped without losing closure -- checked under basis relabelling, not under general GL. |
| minimality under arbitrary basis change | **OPEN** | Not established. The obvious test is invalid; see PO-08. |
| uniqueness | **NOT CLAIMED** | No claim that the triple is the only minimum-cardinality completion. |
| canonicality | **NOT CLAIMED** | No basis-independent canonical choice is established. 'Canonical' is a forbidden word for this object. |

The first of these does not imply any of the others. The manuscript uses
only the first two, in those words.

