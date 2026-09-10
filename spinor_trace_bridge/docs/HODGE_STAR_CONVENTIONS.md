# Hodge star, epsilon and self-duality conventions

Every convention below is pinned as a constant in
`spinor_trace_bridge/src/sdbridge/conventions.py`. Downstream code imports the
constant; it may not re-derive a sign locally. A change to this file is a
scientific change.

## 1. Metric

| side | frame | metric | field |
|---|---|---|---|
| trace (`sdinv`) | orthonormal | `diag(-1,+1,...,+1)`, signature `(1,9)` | `F_p` |
| spinor (`sd5_invariants`) | null / oscillator | `(1/2)[[0,I_5],[I_5,0]]`, real signature `(5,5)` | float64 |
| bridge (`sdbridge`) | both, related by `TransitionFrame.L` | as above | `F_p`, exact |

Mostly-plus. Index `0` is the timelike direction on the trace side.
`sdinv.forms.metric_signs(10, lorentzian=True)` returns exactly
`conventions.LORENTZIAN_SIGNS`, and a test asserts the equality rather than
trusting it.

## 2. Epsilon

    epsilon_{0 1 2 ... 9} = +1

in the Lorentzian orthonormal frame. This is the trace side's convention,
implicit in `sdinv.forms.hodge_matrix`, which orders the permutation as
`(complement, index-set)` relative to `(0,1,...,9)`. The bridge does not define
its own epsilon; it uses the frozen one.

## 3. Hodge star

    (*F)_I = (1/(d-p)!) epsilon_I{}^J F_J

with indices raised by the metric. On sorted multi-indices this is `+/-` the
component on the complementary index set, times the raising signs — which is how
`hodge_matrix` implements it, without ever building a `10^10` epsilon tensor.

## 4. Star squared

    ** = (-1)^{p(d-p)} sign(det eta)

For `d = 10`, `p = 5`, Lorentzian: `(-1)^25 * (-1) = +1`.

This is **verified at runtime**, not assumed: `sdinv.forms.check_star_squared`
returns the scalar `c` with `*^2 = c * 1` and the bridge tests assert `c == +1`
at both primes.

In the split frame `(5,5)` the same formula gives `(-1)^25 * (-1) = +1` as well;
in Euclidean `(10,0)` it would give `-1`. See `REAL_FORM_DICTIONARY.md`.

## 5. Self-duality

    F is self-dual  <=>  *F = +F,        projector P = (1 + *)/2

The sign is `conventions.SELF_DUALITY_SIGN = +1`. The anti-self-dual projector is
`1 - P`. Over `F_p` the factor `1/2` is `inv(2, p)`, exact.

Dimensions, checked rather than quoted:

    dim Lambda^5(R^10) = 252,   dim (self-dual) = dim (anti-self-dual) = 126.

## 6. Gamma normalisation

    {Gamma^mu, Gamma^nu} = 2 eta^{mu nu}          (CLIFFORD_NORMALISATION = 2)

Chirality: `Lambda^even W` is `S_+`. The Chevalley pairing carries the reversal
sign `(-1)^{p(p-1)/2}` on `p`-forms, which is what makes `sigma^mu_{ab}`
symmetric; the bridge tests assert the symmetry rather than assuming it.

The antisymmetrised five-gamma is

    (Gamma^{mu1...mu5})_{ab}
        = (1/5!) sum_{perms} sign(perm) (sigma^{mu1} sigmabar^{mu2} sigma^{mu3}
                                         sigmabar^{mu4} sigma^{mu5})_{ab}

i.e. unit weight on the identity permutation.

## 7. Spinor index placement — fixed by experiment, not by assumption

The archive does not document whether its symmetric `sigma^mu_{ab}` carries upper
or lower spinor indices, and the two choices give different covariance laws. The
bridge therefore **determined** the placement instead of guessing it: all eight
candidate placements were tested against the exact `GL(5)` action, and exactly
one reproduces the transformed image on every component with a single scalar:

    forward(V(A) . F) = det(A) * Lambda(A)^{-1} forward(F) Lambda(A)^{-T}

with `V(A) = blockdiag(A, A^{-T})` on the null directions and `Lambda(A)` the
induced map on `Lambda^even W`. The character is `det(A)` exactly, at every
tested group element, at both primes. This is recorded because it is a
convention *result*, not a convention *choice*, and a reader reproducing the
work should know it was pinned this way.

## 8. Forward map normalisation

    S_{ab} = (1/5!) F_{mu1...mu5} (Gamma^{mu1...mu5})_{ab}

summed over all index tuples. Because both objects are totally antisymmetric,
this equals the sum over *sorted* tuples with unit weight, which is what
`bridge.py` implements. `FORWARD_NORMALISATION_DENOMINATOR = 120` records the
unsorted normalisation the implementation is equal to.

## 9. Inverse

No closed-form inverse is claimed. The bridge constructs a **left inverse on the
self-dual subspace** by inverting the `126 x 126` restriction of the forward map
in an explicitly chosen pivot basis. Its defining property is checked exactly:

    inverse(forward(F)) = P F      for every F, self-dual part or not,

so `inverse . forward` is the self-dual projector, not the identity — which is
the correct statement, since the anti-self-dual part is genuinely destroyed.

## 10. Arithmetic

The bridge is exact over `F_p` and contains **no floating-point step and no
tolerance**. This is possible because the spinor construction is integral up to
its single float SVD (the `126`-dimensional gamma-traceless nullspace), and that
step is redone modularly here. There is no `rtol` in the package. The one
floating-point computation in the test suite is the signature diagnostic of
section 1, which is a real-form statement and has no modular analogue.
