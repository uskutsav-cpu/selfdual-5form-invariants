# Priority ledger --- final

Generated 2026-08-01T21:37:20+00:00.

The question this file answers is not 'is it new' but 'who may this paper say did it'.

## Belongs to the literature

- **N-01** A ten-dimensional self-dual five-form admits 81 functionally independent Lorentz invariants.
  - prior: Hutomo, Lechner and Sorokin, JHEP 02 (2026) 147 [2509.14351]; Cederwall et al., J.Phys.A 59 (2026) 065203 [2509.14350].
  - this paper: A machine-checkable lower bound of 81 matching the published count, from an exact modular Jacobian over a 15-cell sample-by-prime matrix.

- **N-02** 126 - dim so(1,9) = 81 bounds the generic functional rank above.
  - prior: Cederwall et al. [2509.14350], generic-orbit counting.
  - this paper: Cited, not reproved. It is the upper half of the rank statement and no computation here supplies it.

- **N-03** Enumerate contraction graphs, evaluate on generated tensor data, find linear relations to expose functional dependencies.
  - prior: Elamaran, Ferko and Scarlett, Phys.Rev.D 114 (2026) 026016 [2512.23750], for a 3-form in six dimensions.
  - this paper: An exact and certified realization of that workflow for the ten-dimensional self-dual five-form: integral coordinate basis, modular arithmetic throughout, holdout primes, and a characteristic-zero lower bound rather than a numerical rank.

- **N-04** The tensor and spinor descriptions of the self-dual five-form correspond.
  - prior: Standard Clifford algebra; the correspondence is classical and is used in [2509.14350].
  - this paper: An explicit executable map with an exact left inverse, verified at two primes.

## Belongs to this paper, at the stated strength

- **N-05** An exact equivariant bridge Phi: Lambda^5_+ V -> Sym^2_{gamma-tr} S_+ with forward rank 126, kernel exactly the anti-self-dual 126, image exactly the gamma-traceless 126, and a left inverse composing to the self-dual projector.
  - strength: apparently new after search
  - wording: May be described as, to our knowledge, not previously given with certificates. Not 'first'.

- **N-06** The oscillator frame's real form is split (5,5), not Euclidean SO(10); (5,5) and (1,9) are inequivalent real forms, congruent over C and over F_p.
  - strength: made explicit here
  - wording: A correction to this project's own earlier record. The manuscript states the mathematics, not the history, and must not claim a real orthogonal transformation between inequivalent signatures.

- **N-07** Degree-8 tensor and spinor spans are equal, and the structured tensor-word family is what supplies the missing direction.
  - strength: exactly certified here
  - wording: May be stated as certified. The ablation is reported because it is the informative part.

- **N-08** Degree-10 tensor and spinor spans are equal.
  - strength: exactly certified here
  - wording: May be stated as certified. Does not depend on exhausting either grammar; see docs/DEGREE10_NO_STOP_SCIENTIFIC_CLAIM.md.

- **N-09** An explicit 81x81 minor of the integral Jacobian has nonzero determinant, giving rank_Q >= 81 unconditionally.
  - strength: exactly certified here
  - wording: 'Certified', not 'proved'. The matching upper bound is analytic and belongs to N-02.

- **N-10** The complete degree-10 atlas and its incidence table.
  - strength: strengthened here
  - wording: 'Complete' is permitted for the atlas only in the sense certified, and B10 carries 'at the tested primes'.

- **N-11** dim_Q A10 = 14, dim_Q D10 = 11, dim_Q Q10 = 3, over the rationals.
  - strength: exactly certified here
  - wording: May be stated as exact over Q. The seed-closure scope caveat travels with it.

- **N-12** The pure-N^(4125) compact basis for Q10.
  - strength: made explicit here
  - wording: Never 'canonical', never 'unique', never 'ambiguity-robust'.

- **N-13** Formula-independent reverse recovery of the degree-10 quotient.
  - strength: independently reproduced
  - wording: 'Recovery', never 'exhaustive enumeration'; PO-12 is open.

- **N-14** A reproducible computational proof architecture: frozen executions, immutable per-cell artifacts, read-only aggregation with adversarial tests, clean-clone reproduction.
  - strength: apparently new after search
  - wording: May be described as, to our knowledge, going beyond the reproducibility of the source literature. Not 'first'.

## Withheld

- **N-15** A degree-10 stress-flow obstruction with physical consequences.
  - REMOVED as a physical claim. Appears as a mathematical application with the physical reading explicitly withheld.

## The sentence that must appear

> Previous work developed graph enumeration, evaluation on generated
> tensor data and relation finding for tensor-invariant discovery. The
> present work gives an exact and certified realization for the
> ten-dimensional self-dual five-form, constructs a real-form-aware
> tensor-spinor bridge with an exact inverse, and supplies holdout and
> characteristic-zero certificates.

