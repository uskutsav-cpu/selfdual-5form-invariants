# Referee A — invariant theory

Adversarial internal review. The brief is to attack, not to be fair.

---

## A1. "Generic functional rank 81" is doing more work than it can bear

You compute a Jacobian at one or two sample points and find rank 81. You then
call this the *generic* functional rank. A single point gives you a lower bound
on the generic rank and nothing more. If your sample happened to be
non-generic in the other direction — which sampling cannot rule out — you would
be under-reporting, not over-reporting, so the direction is safe; but the word
"generic" in a claim certified at specific points needs to be justified in the
text, not assumed.

**Severity: moderate.** The mathematics is fine; the wording invites a stronger
reading than the evidence supports.

## A2. Functional independence is not algebraic independence

Section 8 computes the rank of a Jacobian. That establishes functional
independence at a point. Nothing in the paper establishes that the 83 candidates
are algebraically independent, and a reader in this field will slide between the
two notions unless stopped. If a syzygy exists among your candidates, the
Jacobian rank is blind to it.

**Severity: serious if unaddressed.**

## A3. The quotient construction assumes D10 is a subspace

`Q10 = A10/D10` is only meaningful if `D10` is a linear subspace of `A10`. The
closure is an iterative construction; you should state explicitly that its output
is a span, and that the flow's action is linear on the relevant graded piece.
Otherwise the quotient is not defined and the number 3 has no meaning.

**Severity: moderate.** Probably a gap in exposition rather than in the work.

## A4. "Basis" is used where "spanning set" would be honest

You exhibit sets and call them bases. A basis is minimal by definition; you prove
cardinality minimality (fine) but explicitly leave removal minimality open. Then
calling the exhibited set a basis is at best loose.

**Severity: minor but pervasive.**

## A5. Minimality language

Proposition 9.4 is a two-line argument from rank-nullity. Presenting it as a
numbered proposition risks a reader taking it for a contribution. If it is
standard, say so at the point of statement, not only in an audit file they will
never see.

**Severity: minor.**

## A6. The spanning-set argument is stated but not applied carefully

You say a space spanned by exactly `k` explicit elements has `dim_Q ≤ k`, so a
modular rank of `k` pins the rational dimension. True. But this requires that the
`k` elements are genuinely explicit *over Q* — i.e. that you have rational
coordinate vectors for them, not merely modular ones. For `B10` you did the CRT
lift, so that is fine. For `A10` and `G10`, is it? If the atlas elements are only
ever represented modulo `p`, the argument does not apply to them.

**Severity: serious.** This one could invalidate a headline number if the answer
is wrong.

## A7. Where is the Hilbert series?

For a question of this shape the natural cross-check is the Hilbert series of the
invariant ring. You do not compute one, and you do not say why not. A reader will
wonder whether the graded dimensions you report are consistent with one.

**Severity: moderate.** A missing check, not an error.
