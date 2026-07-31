# A compact Level-B basis for Q10

## 1. The basis

    Q10 Level-B basis  =  { P10_09, P10_10, P10_12 }

Preferred under the simplicity criterion in
`scripts/build_Q10_levelB_basis.py`, and minimal among the twelve published
equation-(4.24) candidates. Artifacts:
`intrinsic_Q10_levelB_basis.json`, `Q10_basis_search.json`.

This closes Level B for degree 10. Level A was an explicit ten-F-index
contraction graph per class; Level B expresses the same three quotient
directions in the `M / N^(1050) / N^(4125)` block language.

## 2. The search, in full

Four of the twelve candidates have nonzero image in Q10: P10_09, P10_10,
P10_11, P10_12. Of the four possible three-element subsets, **three** are
independent, and both primes agree on which:

    { P10_09, P10_10, P10_11 }
    { P10_09, P10_10, P10_12 }
    { P10_10, P10_11, P10_12 }

The fourth subset, `{P10_09, P10_11, P10_12}`, is dependent.

**Removal minimality.** `P10_10` appears in every independent triple, so it
cannot be dropped from any basis. The reason is visible in the vectors: at
32749 the images of P10_09, P10_11 and P10_12 all have third component 0, so
those three span at most a two-dimensional subspace. `P10_10` is the only
candidate reaching the third quotient direction. The same holds at 32717.

Any two of `{P10_09, P10_11, P10_12}` are pairwise independent in the first two
coordinates — the three pairwise determinants at 32749 are 19461, 1674 and
9775, all nonzero — so the choice of the other two members is genuinely free
and must be settled by the simplicity criterion rather than by necessity.

## 3. Why P10_12 is preferred over P10_11

This is the one place where the criterion does real work, and it turns on
source robustness rather than on size.

All three of P10_10, P10_11, P10_12 carry the unresolved bracket ambiguity
**AMB-02**. Both readings of each were implemented and projected separately.
Measured:

| candidate | quotient image under the two AMB-02 readings |
|---|---|
| P10_10 | **identical** at both primes |
| P10_12 | **identical** at both primes |
| P10_11 | **different** at both primes |

So a basis containing `P10_11` is a basis whose value would change once the
ambiguity is resolved, while `{P10_09, P10_10, P10_12}` is stable against the
part of the ambiguity that has been measured. The scoring function encodes this
as a fixed penalty, and it is what separates the top two candidates:

    183.1   P10_09, P10_10, P10_12      <- preferred
    222.2   P10_10, P10_11*, P10_12
    233.7   P10_09, P10_10, P10_11*

(`*` marks a member whose quotient image moves under its source ambiguity.)

`P10_09` carries **AMB-01**, whose alternative reading has *not* been
implemented, so its robustness is **unmeasured** rather than established. That
is a known gap, not a silent assumption — see §5.

## 4. Scoring criterion

Lower is simpler. Weights are stated, not tuned:

    10 x (number of M + N1050 + N4125 blocks)
     5 x (explicit BLACK bracket operations)
     8 x (RED bracket operations)
     1 x (expanded permutation terms; a RED sym over k slots gives k!)
     1 x (measured single-evaluation seconds)
    50   if the quotient image is NOT invariant under an unresolved
         source ambiguity

Per-member figures, measured at prime 32749, seed 5:

| candidate | M | N1050 | N4125 | black | red | perm terms | seconds | robust |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| P10_09 | 1 | 4 | 0 | 0 | 1 | 6 | 5.1 | unmeasured |
| P10_10 | 0 | 5 | 0 | 0 | 0 | 1 | 5.4 | **yes** |
| P10_11 | 0 | 5 | 0 | 0 | 0 | 1 | 7.2 | **no** |
| P10_12 | 0 | 5 | 0 | 0 | 0 | 1 | 6.6 | **yes** |

Peak RSS for the whole two-prime projection was 531 MB.

## 5. What is and is not claimed

**Permitted**: "`{P10_09, P10_10, P10_12}` is a three-element Level-B basis for
Q10, preferred under the documented simplicity criterion and minimal among the
twelve published equation-(4.24) candidates, verified at one fit and one
holdout prime."

**Forbidden**:

1. **Not** canonical. No class larger than the twelve published candidates has
   been enumerated, so "simplest structure reaching Q10" is unsupported.
2. **Not** independent of AMB-01. `P10_09`'s alternative red-bracket reading is
   unimplemented; if it turns out to change the quotient image, `P10_09` loses
   its robustness advantage over `P10_11` and the preferred basis should be
   re-selected. **This is the first thing to check next.**
3. **Not** a statement about Q12, which remains at rank 0 from the three
   published degree-12 structures.
4. **Not** rationally reconstructed. The basis is certified modularly at two
   primes; the coefficients relating it to Q10_A/B/C are modular, and no CRT
   reconstruction to rationals has been performed.

## 6. Open

- Implement the AMB-01 alternative reading of `P10_09` and re-measure (§5.2).
- Extend from two primes to the full six-prime set. The projection is
  checkpointed, so the four remaining primes are incremental.
- Express Q10_A, Q10_B, Q10_C explicitly in this basis, and the basis in the
  full 14-element atlas, with the change-of-basis matrices reconstructed to
  rationals rather than left modular.
