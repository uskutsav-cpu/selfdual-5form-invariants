# JHEP novelty matrix --- final

Generated 2026-08-01T21:37:20+00:00 by `scripts/emit_jhep_novelty_final.py`.

| id | claim | classification |
|---|---|---|
| N-01 | A ten-dimensional self-dual five-form admits 81 functionally independent Lorentz invariants. | **known** |
| N-02 | 126 - dim so(1,9) = 81 bounds the generic functional rank above. | **known** |
| N-03 | Enumerate contraction graphs, evaluate on generated tensor data, find linear relations to expose functional dependencies. | **known** |
| N-04 | The tensor and spinor descriptions of the self-dual five-form correspond. | **known in another representation** |
| N-05 | An exact equivariant bridge Phi: Lambda^5_+ V -> Sym^2_{gamma-tr} S_+ with forward rank 126, kernel exactly the anti-self-dual 126, image exactly the gamma-traceless 126, and a left inverse composing to the self-dual projector. | **apparently new after search** |
| N-06 | The oscillator frame's real form is split (5,5), not Euclidean SO(10); (5,5) and (1,9) are inequivalent real forms, congruent over C and over F_p. | **made explicit here** |
| N-07 | Degree-8 tensor and spinor spans are equal, and the structured tensor-word family is what supplies the missing direction. | **exactly certified here** |
| N-08 | Degree-10 tensor and spinor spans are equal. | **exactly certified here** |
| N-09 | An explicit 81x81 minor of the integral Jacobian has nonzero determinant, giving rank_Q >= 81 unconditionally. | **exactly certified here** |
| N-10 | The complete degree-10 atlas and its incidence table. | **strengthened here** |
| N-11 | dim_Q A10 = 14, dim_Q D10 = 11, dim_Q Q10 = 3, over the rationals. | **exactly certified here** |
| N-12 | The pure-N^(4125) compact basis for Q10. | **made explicit here** |
| N-13 | Formula-independent reverse recovery of the degree-10 quotient. | **independently reproduced** |
| N-14 | A reproducible computational proof architecture: frozen executions, immutable per-cell artifacts, read-only aggregation with adversarial tests, clean-clone reproduction. | **apparently new after search** |
| N-15 | A degree-10 stress-flow obstruction with physical consequences. | **unresolved** |

## Detail

### N-01 --- known

**Claim.** A ten-dimensional self-dual five-form admits 81 functionally independent Lorentz invariants.

**Prior work.** Hutomo, Lechner and Sorokin, JHEP 02 (2026) 147 [2509.14351]; Cederwall et al., J.Phys.A 59 (2026) 065203 [2509.14350].

**What this paper adds.** A machine-checkable lower bound of 81 matching the published count, from an exact modular Jacobian over a 15-cell sample-by-prime matrix.

**Permitted wording.** The count is attributed to the sources. This paper supplies a certificate for it, and says so.

### N-02 --- known

**Claim.** 126 - dim so(1,9) = 81 bounds the generic functional rank above.

**Prior work.** Cederwall et al. [2509.14350], generic-orbit counting.

**What this paper adds.** Cited, not reproved. It is the upper half of the rank statement and no computation here supplies it.

**Permitted wording.** Stated as analytic and attributed.

### N-03 --- known

**Claim.** Enumerate contraction graphs, evaluate on generated tensor data, find linear relations to expose functional dependencies.

**Prior work.** Elamaran, Ferko and Scarlett, Phys.Rev.D 114 (2026) 026016 [2512.23750], for a 3-form in six dimensions.

**What this paper adds.** An exact and certified realization of that workflow for the ten-dimensional self-dual five-form: integral coordinate basis, modular arithmetic throughout, holdout primes, and a characteristic-zero lower bound rather than a numerical rank.

**Permitted wording.** MANDATORY. The general workflow is prior art and must be credited as such. The manuscript may claim only the exact and certified realization, never the approach.

### N-04 --- known in another representation

**Claim.** The tensor and spinor descriptions of the self-dual five-form correspond.

**Prior work.** Standard Clifford algebra; the correspondence is classical and is used in [2509.14350].

**What this paper adds.** An explicit executable map with an exact left inverse, verified at two primes.

**Permitted wording.** The correspondence is classical. The executable exact map is the contribution.

### N-05 --- apparently new after search

**Claim.** An exact equivariant bridge Phi: Lambda^5_+ V -> Sym^2_{gamma-tr} S_+ with forward rank 126, kernel exactly the anti-self-dual 126, image exactly the gamma-traceless 126, and a left inverse composing to the self-dual projector.

**Prior work.** No source found giving the map with certificates. Searched: both core papers and their 98 combined references, all 18 citing papers, and the spinor-conventions literature.

**What this paper adds.** Span equalities rather than dimension coincidences; equivariance under GL(5) with the det character and under Clifford reflections, which generate the full group by Cartan-Dieudonne.

**Permitted wording.** May be described as, to our knowledge, not previously given with certificates. Not 'first'.

### N-06 --- made explicit here

**Claim.** The oscillator frame's real form is split (5,5), not Euclidean SO(10); (5,5) and (1,9) are inequivalent real forms, congruent over C and over F_p.

**Prior work.** Real forms of Spin(10,C) are standard. The specific correction and its consequence for this construction are not in the literature because the construction is not either.

**What this paper adds.** The metric is extracted from the anticommutators rather than assumed, and the frame transition is constructed and checked.

**Permitted wording.** A correction to this project's own earlier record. The manuscript states the mathematics, not the history, and must not claim a real orthogonal transformation between inequivalent signatures.

### N-07 --- exactly certified here

**Claim.** Degree-8 tensor and spinor spans are equal, and the structured tensor-word family is what supplies the missing direction.

**Prior work.** None found.

**What this paper adds.** Rank 7 on both sides, union rank 7, containment both ways, two fitting and two holdout primes, and a family ablation showing the port-graph family alone reaches only 6.

**Permitted wording.** May be stated as certified. The ablation is reported because it is the informative part.

### N-08 --- exactly certified here

**Claim.** Degree-10 tensor and spinor spans are equal.

**Prior work.** None found.

**What this paper adds.** Rank 14 on both sides on a common sample, holdout validated. Both spans equal A10, whose dimension 14 is structural.

**Permitted wording.** May be stated as certified. Does not depend on exhausting either grammar; see docs/DEGREE10_NO_STOP_SCIENTIFIC_CLAIM.md.

### N-09 --- exactly certified here

**Claim.** An explicit 81x81 minor of the integral Jacobian has nonzero determinant, giving rank_Q >= 81 unconditionally.

**Prior work.** None found. The count 81 is prior; a certificate for it is not.

**What this paper adds.** Two independent determinant routines agreeing, over a matrix of sample points and primes, with the integer-lift argument stated.

**Permitted wording.** 'Certified', not 'proved'. The matching upper bound is analytic and belongs to N-02.

### N-10 --- strengthened here

**Claim.** The complete degree-10 atlas and its incidence table.

**Prior work.** Twelve degree-10 candidate structures appear in [2509.14350], as expressions rather than a basis, with relations undetermined.

**What this paper adds.** Dimensions and containments for A10, B10, G10, P10, D10, with the correction that the published span is not a product complement.

**Permitted wording.** 'Complete' is permitted for the atlas only in the sense certified, and B10 carries 'at the tested primes'.

### N-11 --- exactly certified here

**Claim.** dim_Q A10 = 14, dim_Q D10 = 11, dim_Q Q10 = 3, over the rationals.

**Prior work.** None. Earlier statements of these numbers, including this project's own, were modular.

**What this paper adds.** A10's upper bound is structural; D10 is an exact rational fixed-point closure, agreeing with the modular record and with the same free columns.

**Permitted wording.** May be stated as exact over Q. The seed-closure scope caveat travels with it.

### N-12 --- made explicit here

**Claim.** The pure-N^(4125) compact basis for Q10.

**Prior work.** None found.

**What this paper adds.** Constructed with certificates; described as preferred ambiguity-minimal, since PO-11 leaves one member source-reading-dependent.

**Permitted wording.** Never 'canonical', never 'unique', never 'ambiguity-robust'.

### N-13 --- independently reproduced

**Claim.** Formula-independent reverse recovery of the degree-10 quotient.

**Prior work.** Reproduces the published Level-B span from an independent search.

**What this paper adds.** Recovery, on fit and holdout primes.

**Permitted wording.** 'Recovery', never 'exhaustive enumeration'; PO-12 is open.

### N-14 --- apparently new after search

**Claim.** A reproducible computational proof architecture: frozen executions, immutable per-cell artifacts, read-only aggregation with adversarial tests, clean-clone reproduction.

**Prior work.** No comparable apparatus found in this literature. Finite-field linear algebra itself is standard and is cited.

**What this paper adds.** 32 aggregator tests, each breaking one thing and asserting the named refusal; source-critical hashing; provenance binding.

**Permitted wording.** May be described as, to our knowledge, going beyond the reproducibility of the source literature. Not 'first'.

### N-15 --- unresolved

**Claim.** A degree-10 stress-flow obstruction with physical consequences.

**Prior work.** Qualitative non-universality in D=10 is in [2509.14351].

**What this paper adds.** The exact codimension is established; the physical reading is not, because PO-07 is open.

**Permitted wording.** REMOVED as a physical claim. Appears as a mathematical application with the physical reading explicitly withheld.

## Tally

| classification | count |
|---|---|
| apparently new after search | 2 |
| exactly certified here | 4 |
| independently reproduced | 1 |
| known | 3 |
| known in another representation | 1 |
| made explicit here | 2 |
| strengthened here | 1 |
| unresolved | 1 |

