# Referee C — non-linear chiral field theory

Adversarial internal review.

---

## C1. G-10: whose stress tensor?

Theorem 10.1 proves that *a* stress tensor of the form written in equation
(I.1) is traceless. The theorem is stated for "the free stress tensor". But the
theories in question are formulated in several inequivalent ways — PST,
Sen's decoupled auxiliary field, Mkrtchyan's covariant actions — and the stress
tensor of the *free* theory is not the only object that could be meant when the
flow is defined. If the flow's `τ` is not the object your theorem is about, the
theorem is true and irrelevant.

**Severity: serious.** This is the crux of the paper's dependence on physics
input.

## C2. The flow is defined by reference, not reproduced

Section 9 says the flow is "as formulated in [Hutomo–Lechner–Sorokin]". A reader
cannot check your reachability result without going to that paper and
reconstructing the flow themselves. For a result whose entire content is *what
this flow reaches*, the flow should be written down.

**Severity: serious for readability, moderate for correctness.**

## C3. "The flow does not reach three directions" — of what?

The claim is about a specific generator set at a specific degree. A reader will
hear "the stress flow cannot produce these interactions", which is much stronger.
The limitations section admits the generator-extension problem, but the abstract
and conclusions do not carry the qualifier.

**Severity: moderate.**

## C4. Comparison with six dimensions is asserted, not demonstrated

Section 13 says the six-dimensional case shows universality and the
ten-dimensional degree-ten sector is "the first place in this programme where the
flow provably fails to be exhaustive". That is a strong comparative claim resting
on a reading of other people's results. Either substantiate it or soften it.

**Severity: moderate.**

## C5. Type IIB is raised and then dropped

You cite Paulos, Green–Gutperle–Vanhove and Liu et al., say the five-form is the
IIB RR field strength, and then decline to draw any conclusion. That is honest,
but a referee will ask why the section exists. Either the invariants constrain
those corrections in some way you can state, or the discussion is motivational
and should say so plainly in its first sentence rather than its last.

**Severity: minor.**

## C6. Conformal interpretation

The trace result is a conformal statement in the free theory. You use it purely
as grading bookkeeping. Is there a physical reading of the fact that the flow's
reach is controlled by where the trace starts? If so it is the most interesting
sentence you could write and it is missing.

**Severity: minor — an opportunity, not a defect.**

## C7. No statement about the deformed stress tensor's trace

You prove the *free* trace vanishes. The flow involves the *deformed* `τ`.
Nothing is said about whether the deformed trace vanishes, or why that does not
matter for the grading argument.

**Severity: moderate.**
