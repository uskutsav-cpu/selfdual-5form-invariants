# Internal response to the terminal referee round

Four hostile reviews, twenty objections. Grading them by what they actually cost:

## Objections that identified real defects — all fixed

| # | objection | what it was | resolution |
|---|---|---|---|
| **B3** | Hodge/orientation conventions unpinned | the null-frame congruence was fixed only up to a square-root branch, which flipped the annihilated eigenspace; the construction was silently the anti-self-dual projector at `p = 32707` | orientation normalised by construction; 3 regression tests, one asserting the wrong branch breaks it |
| **C1** | the `Tr(tau)` degree assumption was unproved | load-bearing and circular — validated by the code that used it | derived analytically, independent of the improvement coefficient; verified with a control; counterfactual shows `Q10` would be 0 |
| **A3** | `D10` could be a modular artefact | it was: `dim D10 = 11` was a lower bound over `Q` | exact rational closure, held-out-prime-validated lift, explicit non-vanishing minor |
| **D4** | builds not reproducible | archive hashes differed on every rebuild, solely from an embedded timestamp | `SOURCE_DATE_EPOCH` plus normalised tar/zip metadata; byte-identical from an independent clone |
| **D5** | CRT without a height bound | the first `B10 cap P10` lift silently failed on 3 of 12 | reported as unsettled until seven primes sufficed; validated at a held-out prime and re-verified at a further one |
| **D6** | source cleanliness | one stray file from a shell-quoting accident was tracked | removed; 0 unknown-provenance files remain |

## Objections that were already correctly scoped

A1 (functional vs algebraic independence), A2 (modular vs characteristic zero),
A4 (four kinds of minimality), A5 (enumeration not exhaustive), B4 (equivariance
at sampled elements), B5 (left inverse, not inverse), C3 (`D10` is a statement
about a construction), C4 (what `Q10` enables), C5 (no Type IIB claim).

Each of these is enforced by a wording gate rather than by intention, which is
why they survived a hostile reading unchanged.

## Objections answered by delimitation, not proof

- removal minimality and arbitrary-`GL` minimality: open, stated as open;
- degree-ten enumeration completeness: no such claim is made;
- degree twelve: partial certified input to the rank calculation, excluded from
  the equivalence and classification claims.

## What a real referee could still legitimately press

1. **G-10's conventions.** The derivation is formulation-independent in the sense
   that it does not depend on the improvement coefficient. It does depend on the
   free theory being the one intended. Only a coauthor can confirm that.
2. **Novelty.** Every row of the novelty matrix is `PROVISIONAL`. A literature
   search shows absence of evidence, not evidence of absence.
3. **Thirteen unverified matrix cells.** Internal consistency plus agreement on
   the two overlapping cells is what is established; independent recomputation of
   the rest is not.
4. **Physical significance.** The result is structural. Whether that is
   interesting enough for the venue is a judgement this process cannot make about
   itself.

## Note on this exercise

These reviews are written by the same process that wrote the manuscript. They are
a checklist, not an independent opinion, and three of the six defects above were
found by following the reviews' own lines of attack rather than by the reviews
being right in the abstract. That is the useful thing they did; it is not the
same as peer review.
