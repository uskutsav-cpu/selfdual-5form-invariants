# Independent review of the exact source-map certificate method

This review covers the new literal-source programs and the bounded-CRT proof
method. It does not approve the frozen phase01 transcription. Certificate
execution status is recorded separately in
`source_crt_independent_verification.json` when available; the existence of a
verifier or this method review is not itself evidence that it has run.

## Denominators, component bounds and summed indices

All 126 coordinates are binary integers in the integral self-dual
parametrization. Each dense five-form component is therefore 0, 1 or −1;
there is no sum of two independent coordinates in one dense component.

For a fixed component of M, at most `4! C(9,4)=3024` ordered internal tuples
can contribute. For a nonzero fixed triple in N, at most `7*6=42` ordered
internal pairs can contribute. Normalized antisymmetrization is a signed
average, so it cannot increase the maximum absolute component. Hence
`|M|≤3024`, `|N|,|Q|,|T|,|B|≤42`. The raw metric-metric-M trace tensor has
absolute components at most 3024, and its two normalized projectors preserve
that bound. Consequently

`|P| ≤ 42 + 5·42 + (9/28)·3024 = 1224`.

N and M are integral. Q is the ten-shuffle first-five projector, so 10 clears
its denominators. Because Q is already alternating in the first two slots of
its last triple, the six-term normalized last-three projector reduces to a
three-term normalized sum. Thus T has denominator dividing 30. B has denominator
dividing 20. In P, the `5T` term has denominator dividing 6, and the trace term
has coefficient `9/(28·36)=1/112` before its integer numerator sum. Therefore
`lcm(6,112)=336` clears P. No additional trace symmetry is required for this
safe denominator.

Expanding M² and the two-Q intermediate, a closed source contraction containing
m M factors and s six-index factors has `m+3s` summed metric indices. This
gives degree-ten counts

`5,7,9,9,9,9,11,11,13,15,15,15`.

The respective denominator multipliers are

`1,336,100,2400,400,3360,1000,2000,60000,200000,2700000,2700000`.

These include every normalized two-, three- and four-slot operation in the
independently transcribed programs. Their LCM is 37,800,000. The primary
degree-eight denominators are `1,336,100,240000,400,3360`; H1–H5 have denominator
`30^4=810000`, while H6 shares the denominator 336 of the second primary scalar.

Each index sum has ten choices and diagonal metric coefficients have absolute
value one. Multiplying the block bounds and the number of index assignments
therefore gives rigorous bounds. The largest cleared source numerator bound is

`2700000 · 42^5 · 10^15 = 352866326400000000000000000000`.

A degree-ten graph has 25 metric edges and coefficients ±1 before summation,
so its absolute value is at most `10^25`. Degree-eight graphs are bounded by
`10^20`. Products satisfy the same total-edge bounds. Every per-candidate
bound, factor count and denominator is recorded independently in
`source_bound_review.json`.

All seven proposed moduli are independently verified prime by trial division:
32749, 32719, 32693, 32713, 32717, 32771 and 32779. Their product is

`40274678413255193510345405666987`,

which is strictly larger than twice the largest cleared bound,

`705732652800000000000000000000`.

Thus the centered CRT reconstruction of each cleared source value and each
integer graph value is unique within its rigorously known interval. This
recovers integer **evaluation entries** before rational linear algebra; it
does not depend on a heuristic height bound for reconstructed map coefficients.

## Why exact finite evaluations imply identities here

Let V10 be the full rational invariant space of homogeneous degree ten on the
stated self-dual representation. The necessary external mathematical premise
is `dim(V10)≤14`, not merely a plethystic exponent counting twelve proposed
new directions. Fourteen invariant graph/product polynomials with an invertible
14-point evaluation matrix are linearly independent. With that upper bound,
they form a basis of V10, and evaluation at those points is injective.

Each literal source contraction is a polynomial in that same space: M and N
are covariant contractions, normalized slot projectors commute with the group
action, P is a covariant linear combination, and every scalar dummy index is
contracted with exactly one metric. Its degree is fixed by its factors. Hence
the difference between a source contraction and its exact solved graph
combination lies in V10. Zero evaluations imply zero polynomial by injectivity.

The same argument applies to degree eight with the premise `dim(V8)≤7` and
a rank-seven graph/product evaluation matrix. With fourteen sampled points,
degree-eight evaluation is an isomorphism **onto its seven-dimensional image**
in Q^14, not onto all Q^14. A nonzero selected 7×7 minor establishes the needed
injectivity. No independence assumption about the printed source candidates
is needed before their actual coordinate ranks are computed.

Once the graph/product functions form a basis, rational coordinate row-space
ranks describe polynomial subspaces exactly. If W is the degree-ten source
span and P the two-dimensional lower-product span, then

`dim(W∩P)=rank(W)+2−rank(W+P)`.

The first twelve atlas columns are the chosen complement to P, so their rank
is the quotient-image rank. An intersection witness must have zero first
twelve coordinates and a nonzero final product pair. The verifier checks the
full witness span, not just a numerical relation at one point. In degree eight
it checks both inverse matrices and preserves the product correction.

## Independent verification boundary

`verify_source_crt.py` uses a direct-product CRT implementation, independently
authored integer Bareiss determinants, and a separate Fraction row-echelon
implementation. It imports no source fitting helper or repository module and
does not repeat tensor evaluations. It checks point coverage, common binary
coordinates, file and evaluator hashes, all cleared bounds, every exact
evaluation entry, both maps, rational residuals, inverses, ranks and witness
spans. It also compares the graph definitions against the frozen ordered basis.

The polynomial conclusion remains conditional on the specified invariant-space
upper bounds and analytic invariance, and on correct execution of the fixed
residue programs. The first two are mathematical premises that must be cited
and explained independently; they are not consequences of finite sampling.
The source-reading scope remains the literal displayed formulas and their
explicit colored brackets. An exact map for those definitions does not erase
separate interpretive qualifications concerning prose-only irrep projections.
