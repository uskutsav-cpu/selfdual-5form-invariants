# The complexified representation bridge

## Statement

Let `g = so(10,C)` and let `V` be the irreducible `126`-dimensional module of
self-dual five-forms. The two implementations in this project realise `V` in two
different real frames of the same complex module:

    trace side    V_L  = self-dual five-forms of the Lorentzian frame  (1,9)
    spinor side   V_S  = gamma-traceless Sym^2 of the chiral spinor,
                         built in the null frame, real form (5,5)

The bridge is the explicit isomorphism `V_L -> V_S` given by

    S_{ab} = (1/5!) F_{mu1...mu5} (Gamma^{mu1...mu5})_{ab}

composed with the frame transition. Over `C` and over `F_p` this is an
isomorphism of `g`-modules. Over `R` it is not defined, because the two real
frames are inequivalent real forms.

## 1. The complexified algebra

`so(10,C)` is simple of rank 5, dimension 45, type `D_5`. Its real forms include

    so(10)     compact          signature (10,0)
    so(1,9)    Lorentzian
    so(5,5)    split
    so*(10)                     (not used here)

All are Zariski-dense in `SO(10,C)`.

## 2. Chiral spinors and the 126

For `D_5` the two half-spin modules `S_+`, `S_-` are 16-dimensional. In signature
`(1,9)` and in signature `(5,5)` — both satisfying `s - t = 0 mod 8` — they carry
a real structure, so the chiral spinor is Majorana–Weyl and 16-dimensional over
`R`. In each case

    Sym^2(S_+) = V_10 (+) V_126,

where the `10` is the image of the gamma-trace `sigmabar^{mu,ab} S_{ab}` and the
`126` is its kernel. Independently, `Lambda^5(V_10) = 252` splits under the Hodge
star into self-dual and anti-self-dual `126`s. As `so(10,C)`-modules,

    V_126 = Lambda^5_+ ,

the highest weight being `2 omega_5` (equivalently `omega_5 + omega_5`), which is
the standard identification of the self-dual five-form with the symmetric
gamma-traceless square of a chiral spinor.

The implementation does not import this. `NullFrameClifford.gamma_trace_constraints`
has rank exactly 10 over `F_p`, so the gamma-traceless space is exactly 126, and
`BridgeMap.verify()` shows the image of the self-dual five-forms *equals* that
space as a subspace, not merely in dimension.

## 3. Where the real forms differ, and where they do not

**Dimensions of invariants agree exactly.** For a connected reductive `G_C` with
real form `G_R`, and a real module `V_R` with `V_R (x) C = V_C`,

    R[V_R]^{G_R} (x) C  =  C[V_C]^{G_C}

in every degree, because `G_R` is Zariski-dense in `G_C` so a polynomial
invariant under `G_R` is invariant under `G_C`. Hence the graded dimensions of
the invariant ring do not depend on which real form is used. This is what makes
the degree-4, 6, 8 and 10 counts directly comparable between a Lorentzian
implementation and a split one, with no complexification caveat and no appeal to
the bridge at all.

**Component values do not agree without transport.** A real self-dual five-form
of `(1,9)` is not a real self-dual five-form of `(5,5)`. The transition
multiplies four directions by `i`. Comparing *values* of invariants at a given
tensor therefore requires a field in which the transition exists.

**`F_p` supplies such a field.** Over `F_p` signature is undefined and a
nondegenerate quadratic form is classified by its discriminant alone. Both
metrics have discriminant `-1` up to squares, so they are congruent, and the
transition matrix is exact. This is why the common-sample comparison in `WS-I`
can be an exact modular statement rather than a numerical one.

## 4. What the bridge is verified to do

At each of `p = 32749` and `p = 32719`:

| property | result |
|---|---|
| `*^2` on five-forms | `+1` |
| `dim` self-dual / anti-self-dual | `126` / `126` |
| rank of the forward map | `126` (not 136) |
| kernel | **equals** the anti-self-dual subspace (span equality) |
| image | **equals** the gamma-traceless subspace (span equality) |
| left inverse | `inverse . forward = P_selfdual`, exactly |
| scaling `F -> cF` | exact |
| `GL(5)` equivariance | exact, character `chi(A) = det(A)` |
| frame congruence `L^T eta_null L = eta_Lor` | exact |
| tolerance used anywhere | none |

`GL(5)` is a 25-dimensional subgroup of the 45-dimensional `so(10)`, chosen
because the oscillator realisation makes its action integral: for `A in GL(5)`,
`e_i -> A e_i` and `e^i -> A^{-T} e^i` preserves the null metric, and the induced
map on `Lambda^even W` has minors of `A` as entries. So the equivariance check is
a genuine continuous-group statement carried out in exact arithmetic, not a
discrete spot check.

The remaining 20 directions of `so(10)` are not covered by this test. They are
covered indirectly: a map that is `GL(5)`-equivariant and sends the irreducible
`126` onto the irreducible `126` is unique up to scale by Schur's lemma once
`so(10)`-equivariance is granted, but `GL(5)`-equivariance alone does not grant
it. This is logged as review item **G-4**.

## 5. What is still convention-dependent

The spinor index placement in the archive's `sigma^mu_{ab}` is undocumented. The
bridge fixed it by requiring exact `GL(5)` equivariance; of eight candidate
placements exactly one works, on every component, with a single scalar. That is
strong evidence the placement is the intended one, but it is a *reconstruction*
of the archive author's convention, not a citation of it. Logged as **G-1**.

## 6. Consequences for the manuscript

Permitted:

- "The two implementations realise the same complex module in inequivalent real
  frames; invariant dimensions are therefore directly comparable."
- "The bridge is an exact isomorphism over `F_p` from self-dual five-forms onto
  the gamma-traceless symmetric chiral squares, with a verified left inverse."
- "Component-level comparison is carried out over `F_p`, where the frame
  transition exists exactly."

Not permitted:

- Any claim that the two implementations use the same signature.
- Any claim of a real component-level identification between a Lorentzian and a
  split realisation.
- Any claim that `so(10)`-equivariance of the bridge has been verified in full;
  what is verified is `GL(5)` equivariance.
