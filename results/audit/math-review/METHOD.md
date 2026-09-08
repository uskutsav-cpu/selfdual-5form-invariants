# Independent mathematical audit — continuation methods

Target: frozen commit `2b7663bbf5a06d1340973434f195a84ae2773e8f` in
`../frozen-checkout`. The prior stopped audit remains separate and unchanged.
This continuation does not certify any repaired literature transcription.

Only independently authored audit script source was copied from the previous
audit, with explicit user authorization. `SCRIPT_PROVENANCE.json` records the
copied source paths and hashes. Old results, intermediates, caches, checkpoints
and environments were not imported. All numerical results here were rerun in
the new environment. `bareiss_minors.py`, `independent_conventions.py`, and
`independent_oracle.py` were adapted to the new frozen-checkout path; the other
scripts were written during this continuation.

## Determinants and conventions

The standard-library-only Bareiss implementation computes each complete
integer determinant of the stored 81-by-81 minor before reducing modulo the
prime. It imports no repository code, Gaussian determinant implementation,
rank sieve or verifier. Every Bareiss division is checked for zero remainder.
Full integer determinants are retained in `bareiss_results.json`.

The separate conventions script derives Hodge signs by inversion counting.
For sorted five-tuple `I` and sorted complement `J`, it uses the frozen
output-first epsilon convention
`star(e_I) = sign(J,I) * product(metric[I]) * e_J`. The two block parities
contribute `(-1)^25`, the signature `(1,9)` contributes `-1`, and star squared
is `+1`. Direct integer checks cover all 252 index sets. Complementary pairs
give 126 self-dual directions. Choosing the time-containing tuple in each
pair gives integral directions `e_I + star(e_I)`, with entries `0,+1,-1` and
an identity 126-by-126 coordinate block. Their digest and all four reconstructed
frozen component vectors are compared with the frozen certificate.

Ordered edge lists are inputs, not independently discovered graphs. The script
validates their ordering, multiplicities and valences, independently rebuilds
adjacency matrices, and reconstructs all printed Einstein formulas. Each edge
has one upper and one lower index occurrence. The custom evaluator places the
metric at the incoming endpoint; production places it at the outgoing endpoint.
Both place exactly one inverse metric on the shared dummy index.

## Independent forward-dual evaluator

`efficient_oracle.py` and its supporting independent modules import no
production code. They independently expand compact forms, assign slots from
ordered edge records, and apply metric signs. `opt_einsum` is used only to plan
a binary contraction order. Actual contractions are independently implemented
as explicit transposes, reshapes and guarded matrix products.

For nonnegative residues less than `p`, a dot product with `K` summands is
bounded by `K*(p-1)^2`. Every call checks this bound is below `2^53`; all integer
products and partial sums are then exactly representable by float64. Every
dot is reduced modulo `p` before the next operation. The derivative addition
is also reduced. The float64 operations therefore have an integer exactness
argument, rather than a tolerance-based acceptance rule. Small matrix products
and a 100,000-term scalar dot are checked against Python integer arithmetic.
This method still shares NumPy and machine BLAS primitives with production;
independence concerns the constructed tensors, contraction program, derivative
method and checks, not an independently implemented hardware arithmetic unit.

Forward differentiation propagates `F + epsilon*dF`, with `epsilon^2=0`.
Each binary operation propagates `d(A B)=dA B+A dB`; it never constructs a
production gradient or invokes production reverse differentiation.

Each new PointEngine has a bounded 256 MiB LRU cache keyed by complete
contraction structure and initial metric/slot placement. It can reuse exact
subexpressions across graphs at the same point. Different points get distinct
engines and do not share numerical caches. Multiple engine objects may coexist
during validation, so 256 MiB is a per-engine cache bound, not a process RSS
bound. Dense inputs, active arrays and matrix-product workspace are additional.

The root generated two post-freeze points and directions at primes 50021 and
32749, recorded in `../root-review/fresh_cells.json`. The new-prime absence scan
and its scope are documented by the root. The oracle first wrote values and
directional derivatives without consulting production numerical outputs.
`compare_fresh.py` subsequently compares them with separate recorded production
results, forming `J*h` using Python integers. All coordinates, directions and
raw comparisons are retained.

## Independent reverse validation and degree-twelve linear independence

`independent_reverse.py` is an independently written reverse-adjoint tape and
direct coordinate pullback. It shares the custom oracle's forward binary
kernel but does not import the production evaluator, planner, Hodge code,
projection or rank code. Distinct tensor copies remain separate leaves.
Adjoints are summed only when pulling back to the common input form. Each
coordinate pullback explicitly sums its 240 signed dense entries: 120 from
the time-containing component and 120 from its Hodge complement.

The reverse result is checked against the independent forward-dual derivative
and every one of the production row's 126 entries at both root points for all
81 selected invariants. The two additional degree-twelve graphs, I12_61 and
I12_62, also receive independent forward-dual checks. Euler homogeneity is
checked for every independently computed row.

The degree-twelve homogeneous inventory is fixed as the ten products
`I4^3`, the three sextic products, the six `I4*I8_j` products, and all 62
connected degree-twelve graphs. Product gradients use the product rule on
independently evaluated low-degree values and gradients.

For each prime, the root point is supplemented by a newly generated random
point at the **same** prime, with its own recorded 128-bit seed. Gradients are
concatenated horizontally to a 72-by-252 matrix. Different primes are never
combined into one rank calculation. Independent Python modular elimination
selects 72 pivot columns if possible; the corresponding integer minor is
then evaluated by Bareiss and reduced. Up to four same-field points are
allowed if two do not suffice. Full matrices, coordinates, seeds, selected
columns and complete integer determinants are preserved.

A nonzero minor of this stacked gradient matrix proves linear independence
of the 72 homogeneous polynomials. It is distinct from functional independence
at one point and does not claim 72 algebraically independent degree-twelve
functions or an invariant-ring presentation. The upper bound of 72 still
requires its stated mathematical/literature justification; this calculation
provides the independent lower bound. No 72-point value matrix is claimed:
the faster independently validated stacked-gradient method replaced that plan.

## Permutation signs

`automorphism_signs.py` enumerates all weighted-graph automorphisms of every
selected graph using independent constraint backtracking. Vertex candidates
must have the same sorted incident multiplicities; partial assignments must
preserve every assigned adjacency entry. It computes the induced sign from
the product of the alternating-slot permutation signs at vertices.

The numerical sign campaign checks one explicit nontrivial vertex relabeling
for each of the 81 graphs and an odd permutation of two slots at one tensor
copy in each graph. It also checks every adjacent vertex swap structurally,
its inverse, and a composed permutation sign relation. Scalar factors commute;
signs arise from reordered alternating slots, not from swapping whole scalar
factors. The complete five-slot permutation parity count is 60 even and 60 odd.

Finally, selected degrees 4, 6, 8, 10 and 12 receive exact interpolation of
`I(A+t*h)` at `t=0,...,degree`. Finite-field Lagrange derivative weights recover
the derivative at zero from values alone, furnishing another check of the
forward-dual derivative that does not use reverse propagation.

## Evidence boundary

Execution records are under `../commands/math_*/`, with exact command arguments,
working directories, exit status, timing and stdout/stderr hashes. Numerical
status is supplied separately in the generated continuation results/report.
The methods described here must not be treated as completed merely because
their scripts exist. None of these checks repairs or recertifies the frozen
degree-ten source-paper mapping that blocked the first audit.
