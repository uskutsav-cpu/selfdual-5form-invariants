# Referee B — spinors and real forms

Adversarial internal review.

---

## B1. The orientation story is reported, but is the fix complete?

You found that a square-root branch left the self-dual/anti-self-dual choice
unpinned, and you now select the branch under which the self-dual space survives.
Fine. But your selection criterion is *itself* the property you are trying to
establish: you pick the branch that makes the composite have rank 126, and then
report that the composite has rank 126. That is circular as a *verification*
even though it is sound as a *construction*.

You need an independent check that the branch you selected is the one matching
the stated orientation convention — not merely the one that produces a non-zero
answer.

**Severity: serious.** This is the sharpest objection in this report.

## B2. `star^2 = +1` is asserted for Lorentzian signature; where is Euclidean?

The paper says `star^2 = +1` on middle forms in ten Lorentzian dimensions. In
Euclidean signature the sign is the other one, and your own appendix I records an
incident where a Euclidean projector was mistaken for an anti-self-dual one. Given
that history, the signature dependence deserves to be stated where the convention
is fixed, not only in the appendix that records the error.

**Severity: minor.**

## B3. Majorana–Weyl, and which real form the spinors live in

You cite Kugo–Townsend for the Clifford facts and you note that the oscillator
frame is adapted to split signature. But `Sym^2 S_+` has different reality
properties in `(1,9)` and `(5,5)`. The paper says dimension counts descend from
the complexification, which is true, but the *symmetry* of `C Γ^(5)` — which is
what makes the bridge land in the symmetric square — is a statement that should
be checked in the real form you actually compute in.

**Severity: moderate.**

## B4. The equivariance check solves for a character

Solving for `χ(Λ)` rather than asserting it is good practice. But if `χ` comes
out identically 1, the check has less discriminating power than it appears: an
implementation error that commuted with the group action would pass. What is the
test that would fail?

**Severity: moderate.**

## B5. Gamma normalisation

The `1/5!` is described as a choice that cancels. It does cancel in ranks. Does
it cancel in the *integer* identity of section 11? An identity with specific
integer coefficients is not obviously invariant under rescaling one of the
objects entering it.

**Severity: moderate.** Possibly a genuine issue with how the identity is stated.

## B6. Left inverse versus inverse

You are careful that `Φ Φ⁻` is a projector, not the identity. Good. But the
abstract says "with an exact left inverse" and a hurried reader will read
"invertible". Consider being explicit in the abstract.

**Severity: minor.**
