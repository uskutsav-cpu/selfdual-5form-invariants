# Referee C — non-linear chiral fields

## C1. "The whole activation scheme rests on an unstated assumption about Tr(tau)."

It rested on one, and the referee has found the load-bearing item. It is now
derived rather than asserted:

- the free stress tensor of a `p`-form is quadratic in `F`, so its trace is a
  degree-2 scalar;
- for `T_{mn} ~ F_{m...}F_n^{...} - c eta_{mn} <F,F>` the trace is
  `(1 - cd) <F,F>` for **any** improvement coefficient, so only `<F,F>` matters;
- `F ^ F` is a top form built from two copies of an odd-degree form in even
  dimension, hence identically zero, and `<F, *F>` is proportional to it;
- so on either eigenspace `F = ±*F` gives `<F,F> = ±<F,*F> = 0`.

Verified computationally with a control (unprojected five-forms give non-zero
`<F,F>`), at four primes, by a test that imports no flow code.

**What remains for the mentor**, and it is narrow: confirmation that the free
theory and stress convention used are the intended ones. The independence from
`c` means a differing formulation would have to change the quadratic scalar
*available*, not merely the trace convention.

## C2. "Show that it matters."

Re-running the closure with `Tr(tau)` contributing from degree two gives
`dim Q10 = 0` instead of `3`. The paper's central number collapses. C1 is not a
technicality, and the counterfactual is recorded rather than described.

It also reproduces exactly an earlier error of this project's, in which the
unconditional span gave rank 14 and quotient 0, and is retained as a negative
regression fixture.

## C3. "What is D10 physically? A closure is not a physical statement."

`D10` is the degree-ten image of the stress-flow construction of the source
literature — a statement about what that construction reaches, not about nature.
The paper says exactly this and draws no physical consequence from it.

## C4. "What does Q10 = 3 mean for a theorist?"

That there are three independent directions of degree-ten local structure the
flow cannot generate, with explicit representatives, and that `P10 ⊂ D10` — so
the missing directions are not products of anything simpler. A candidate
degree-ten term can now be expanded in a certified basis and its class in `Q10`
read off. Before, it could only be compared against twelve published expressions
not known to be complete or independent.

## C5. "Type IIB."

Nothing is claimed. No coefficient, no supersymmetric completion, no causality,
no amplitude, no all-orders statement. The single occurrence of "Type IIB" in the
manuscript is inside the sentence disclaiming all of them.

## Verdict

C1 was the correct place to attack and it is now closed analytically, with the
counterfactual establishing that it mattered. The physics claims are narrow and
match what is proved.
