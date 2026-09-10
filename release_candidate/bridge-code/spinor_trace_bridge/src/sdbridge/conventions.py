"""Frozen conventions for the spinor/tensor bridge.

Every sign in this package is pinned here.  Nothing downstream may re-derive a
convention; it must import the constant.  Changing a value in this file is a
scientific change and must be accompanied by a re-run of the whole test suite.

The two implementations being bridged do NOT use the same frame:

  trace side   `sdinv`   : orthonormal frame, metric diag(-1,+1,...,+1),
                           i.e. Lorentzian signature (1,9), exact over F_p.
  spinor side  `sd5_invariants`
                         : null (oscillator) frame, metric (1/2) [[0,I],[I,0]],
                           whose real form is SPLIT, signature (5,5).

Both frames are frames for the same complex form so(10,C).  Over F_p (and over
C) the two metrics are congruent -- see `signature.py`, which constructs the
transition matrix explicitly rather than assuming it.  Over R they are
inequivalent real forms; see docs/REAL_FORM_DICTIONARY.md.
"""

from __future__ import annotations

# --- dimensions -------------------------------------------------------------

SPACETIME_DIM = 10
FORM_DEGREE = 5
SPINOR_DIM = 16          # chiral (Weyl) spinor, one chirality
FULL_SPINOR_DIM = 32     # Dirac
OSCILLATORS = 5          # W = C^5, Lambda^* W = 32

N_FIVE_FORM_COMPONENTS = 252   # C(10,5)
N_SELFDUAL_COMPONENTS = 126    # (1/2) C(10,5)
N_SYMMETRIC_SPINOR = 136       # C(17,2) = dim Sym^2(16)
N_GAMMA_TRACELESS = 126        # 136 - 10

# --- metric -----------------------------------------------------------------

#: Trace-side orthonormal frame.  `sdinv.forms.metric_signs(10, lorentzian=True)`
#: returns exactly this.  Mostly-plus: the 0 direction is timelike.
LORENTZIAN_SIGNS = (-1,) + (1,) * 9

#: Real signature of the spinor side's null frame, established by
#: `tests/test_clifford.py::test_null_frame_signature_is_split`.
NULL_FRAME_REAL_SIGNATURE = (5, 5)

#: eta_null = NULL_METRIC_SCALE * [[0, I_5], [I_5, 0]].  The 1/2 is forced by
#: {e_i ^ , iota_i} = 1 together with the Clifford normalisation below.
NULL_METRIC_SCALE_NUMERATOR = 1
NULL_METRIC_SCALE_DENOMINATOR = 2

# --- Clifford ---------------------------------------------------------------

#: Clifford relation.  {Gamma^mu, Gamma^nu} = CLIFFORD_NORMALISATION * eta^{mu nu}.
CLIFFORD_NORMALISATION = 2

#: Chirality: Lambda^even W is the positive-chirality module S_+.
POSITIVE_CHIRALITY_IS_EVEN = True

#: The Chevalley pairing carries the reversal sign (-1)^{p(p-1)/2} on p-forms.
#: This is what makes sigma^mu_{ab} symmetric; see `sd5_invariants.gamma10`.
CHEVALLEY_REVERSAL_SIGN = True

# --- form conventions -------------------------------------------------------

#: epsilon_{0 1 2 ... 9} = +1 in the Lorentzian orthonormal frame.  This is the
#: trace side's convention, fixed by `sdinv.forms.hodge_matrix`, which orders the
#: permutation as (complement, index-set).
EPSILON_0_THROUGH_9 = +1

#: (*F)_I = (1/(d-p)!) eps_I^J F_J, with indices raised by LORENTZIAN_SIGNS.
#: For p=5, d=10, Lorentzian: *^2 = (-1)^{p(d-p)} sign(det eta) = (-1)^25 * (-1)
#: = +1, so real self-dual five-forms exist.  Verified at runtime by
#: `sdinv.forms.check_star_squared`.
STAR_SQUARED_ON_FIVE_FORMS = +1

#: Self-dual means *F = +F.  The projector is (1 + *)/2.
SELF_DUALITY_SIGN = +1

# --- the bridge map ---------------------------------------------------------

#: S_{ab} = FORWARD_NORMALISATION * F_{mu1...mu5} (Gamma^{mu1...mu5})_{ab},
#: with FORWARD_NORMALISATION = 1/5! and a sum over ALL index tuples.  Working
#: with sorted tuples instead cancels the 1/5!; `bridge.py` uses the sorted-tuple
#: form and this constant records the unsorted normalisation it is equal to.
FORWARD_NORMALISATION_DENOMINATOR = 120  # 5!

#: The forward map annihilates anti-self-dual five-forms and is injective on the
#: self-dual 126.  Both are asserted, not assumed: see
#: `tests/test_bridge.py::test_forward_kernel_is_exactly_antiselfdual`.
FORWARD_KERNEL_IS_ANTISELFDUAL = True

# --- arithmetic -------------------------------------------------------------

#: The bridge is exact over F_p.  Both primes are the trace side's own
#: (`sdinv.modp.P` and `sdinv.modp.ALT_P`), so bridge results and trace results
#: live in literally the same field.
DEFAULT_PRIME = 32749
ALT_PRIME = 32719

#: Everything in the construction is integral before inversion, so no float
#: tolerance enters the bridge at all.  There is no `rtol` in this package.
BRIDGE_IS_EXACT = True
