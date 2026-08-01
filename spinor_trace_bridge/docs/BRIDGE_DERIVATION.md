# Bridge derivation

How the map is built, in the order the code builds it. Every claim here is
checked by a test; the test name is given.

## Step 0 — what is being bridged

| | trace side | spinor side |
|---|---|---|
| package | `sdinv` (frozen) | `sd5_invariants` (frozen, third-party) |
| object | self-dual five-form `F`, 252 sorted components | gamma-traceless symmetric `S_{ab}`, 136 coordinates |
| frame | orthonormal, `diag(-1,+1,...,+1)` | null oscillator, real signature `(5,5)` |
| arithmetic | exact over `F_p` | float64 |

The bridge (`sdbridge`) is a third package. It imports both by public interface
and rewrites neither.

## Step 1 — redo the Clifford construction exactly

`clifford.py` rebuilds the oscillator realisation over `F_p`:

- `wedge_operator(i)`, `contraction_operator(i)` — integral `32 x 32`.
- `chevalley_pairing()` — integral `16 x 16`, carrying `(-1)^{p(p-1)/2}`.
- `sigma[mu] = B g_mu`, symmetric — *tested*, not assumed
  (`test_clifford_relation_exact`).
- `sigma_bar[mu] = h_mu B^{-1}`, satisfying
  `sigma^mu sigmabar^nu + sigma^nu sigmabar^mu = 2 eta^{mu nu}` — *tested*.

Why redo it: the archive is integral right up to a single float SVD, the one
that extracts the 126-dimensional gamma-traceless nullspace. That SVD is the
only place a rank tolerance ever has to be chosen. Done over `F_p` the step is
exact, and the bridge ends up with no tolerance at all.

Result: `gamma_trace_constraints` has rank exactly `10`
(`test_gamma_trace_constraints_have_rank_ten`), so the gamma-traceless space is
exactly `126` (`test_gamma_traceless_module_is_126`).

## Step 2 — identify the frame, and correct the record

The metric induced by the archive's own operators is

    eta = (1/2) [[0, I_5], [I_5, 0]],   real signature (5,5) — SPLIT.

`test_null_frame_signature_is_split` computes all one hundred anticommutators and
diagonalises. This corrects an earlier record that called the frame Euclidean and
treated `*^2 = -1` as an obstruction; see `REAL_FORM_DICTIONARY.md`. In split
signature, as in Lorentzian, `*^2 = +1` on five-forms and real self-dual
five-forms exist.

## Step 3 — build the frame transition, don't assume it

Over `R` the two frames are inequivalent real forms. Over `F_p` signature does
not exist and only the discriminant survives; both metrics have discriminant `-1`
up to squares, so they are congruent.

`signature.py::congruence` constructs `L` explicitly:

1. congruence-diagonalise each form (`diagonalise`), handling the totally
   isotropic diagonal that the null metric actually has;
2. canonicalise each diagonal to `diag(1,...,1,disc)` using
   `diag(a,b) ~ diag(1,ab)`, solving `a x^2 + b y^2 = 1` over `F_p`;
3. match the two discriminants with a square root.

`TransitionFrame.verify()` then checks `L^T eta_null L = eta_Lorentzian`
exactly (`test_transition_is_an_exact_congruence`), at both primes.

## Step 4 — the forward map

    S_{ab} = (1/5!) F_{mu1...mu5} (Gamma^{mu1...mu5})_{ab}

with

    (Gamma^{mu1...mu5})_{ab}
      = (1/5!) sum_perm sign (sigma sigmabar sigma sigmabar sigma)_{ab}.

Because both objects are totally antisymmetric the outer `1/5!` cancels against
the sum over orderings, so the implementation sums over *sorted* index tuples
with unit weight. `forward_matrix` is the explicit `252 x 136` matrix obtained by
pushing each basis five-form through the frame transition and contracting.

## Step 5 — what the map does, verified rather than asserted

At `p = 32749` and `p = 32719`:

| statement | how it is checked | test |
|---|---|---|
| `*^2 = +1` on five-forms | frozen `sdinv.forms.check_star_squared` | `test_star_squares_to_plus_one_on_five_forms` |
| self-dual and anti-self-dual are each `126` | rank of the projectors | `test_selfdual_and_antiselfdual_each_have_dimension_126` |
| forward has rank `126`, not `136` | modular rank | `test_forward_rank_is_126_not_136` |
| kernel **equals** the anti-self-dual subspace | two-way span containment | `test_forward_kernel_is_exactly_antiselfdual` |
| image **equals** the gamma-traceless subspace | two-way span containment | `test_image_is_exactly_the_gamma_traceless_126` |
| every image is gamma-traceless | direct contraction | `test_gamma_trace_of_every_image_vanishes` |

The span-equality checks matter. A dimension match alone would leave open that
the kernel is some *other* 126-dimensional subspace; two-way containment closes
that.

## Step 6 — the left inverse

No closed form is claimed. `left_inverse` picks 126 pivot columns of the image,
inverts the resulting `126 x 126` block exactly, and pushes back through the
self-dual basis. Defining property, checked exactly:

    inverse(forward(F)) = P_selfdual F      for arbitrary F

so the composite is the self-dual projector, not the identity
(`test_inverse_recovers_only_the_selfdual_part`). That is the correct statement:
the anti-self-dual part is genuinely destroyed and cannot be recovered.

## Step 7 — equivariance

Two independent certificates, both exact, both with the scalar *solved for*
rather than assumed.

**`GL(5)`** (`covariance.py`). The oscillator realisation makes this subgroup
integral: `e_i -> A e_i`, `e^i -> A^{-T} e^i` preserves the null metric, and the
induced map on `Lambda^even W` has minors of `A` as entries. Verified law:

    forward(V(A) . F) = det(A) * Lambda(A)^{-1} forward(F) Lambda(A)^{-T}

with `chi(A) = det(A)` exactly at every tested element
(`test_gl5_equivariance_with_determinant_character`).

**Full rotation group** (`rotations.py`). `GL(5)` is only 25 of the 45
directions. Clifford reflections close the rest: `Gamma(u) Gamma(x) Gamma(u)^{-1}
= -Gamma(R_u x)`, and by Cartan–Dieudonné reflections generate the whole
orthogonal group. Verified law:

    forward(R . F) = (prod_i Q(u_i))^{-1} * rho^T forward(F) rho

where `rho` is the unnormalised Clifford lift. The observed scalar equals the
predicted Clifford normalisation exactly, for products of two and of four
reflections (`test_equivariant_under_the_full_rotation_group`).

Reflections were chosen deliberately: they are polynomial in the group element,
so unlike exponentials of Lie-algebra elements they survive modular arithmetic
intact.

**Index placement was determined, not chosen.** The archive does not document
whether `sigma^mu_{ab}` carries upper or lower spinor indices. All eight
candidate placements were scanned; exactly one satisfies the equivariance on
every component with a single scalar. Recorded as review item G-1.

## Step 8 — limits of the certificate

- Everything is modular at two primes. This is not a characteristic-zero proof.
- Equivariance is verified at sampled group elements, exactly, not proved as a
  symbolic identity for all elements.
- The `GL(5)` and reflection lifts use different normalisation conventions
  (exterior-power lift versus Clifford product), which is why their characters
  differ in form. Both are congruence transformations of a symmetric bilinear
  form, which is the invariant content.

## Artifacts

- `spinor_trace_bridge/results/bridge_validation.json` — full certificate at both
  primes, including the solved characters.
- `spinor_trace_bridge/tests/` — 72 tests (`test_bridge.py` and `test_adversarial.py`).
