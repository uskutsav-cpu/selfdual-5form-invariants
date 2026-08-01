# Mentor review package

Short on purpose. The detail is in the repository; this is what to look at and
what is being asked.

## What the paper claims

An exact tensor-spinor invariant theory for the ten-dimensional self-dual
five-form: an equivariant bridge with an exact left inverse, degree-resolved
span equality through degree 10, and a characteristic-zero certificate for
generic functional rank 81.

## What it does not claim

The count 81 (yours), the general enumerate-evaluate-relate method (Elamaran,
Ferko and Scarlett), degree-12 equivalence, all-order results, a complete
invariant ring, canonicality, or any physical or Type IIB consequence.

## The four things most worth your scepticism

1. **The split-signature correction.** The oscillator frame is (5,5), not
   Euclidean SO(10). This overturned a recorded blocker in this project's own
   notes. If it is wrong, the bridge section is wrong.
   → `spinor_trace_bridge/docs/REAL_FORM_DICTIONARY.md`

2. **dim_Q D10 = 11 by exact rational closure.** Previously this was modular
   only, and modular is the wrong direction for a subtracted subspace. The
   claim is now that the closure was recomputed over Q. The first attempt at
   this returned 14 and a quotient of 0; the difference was which space was
   being computed.
   → `docs/D10_Q10_FINAL_STATUS.md`

3. **The rank-81 certificate.** 15 cells over three seeds, three fitting primes
   and two holdout primes, all agreeing. The lower bound is certified; the
   matching upper bound is your analytic 126 − 45.
   → `docs/RANK81_MULTI_SAMPLE_CERTIFICATE.md`

4. **The degree-8 ablation.** Span equality holds at rank 7 only with the
   structured tensor-word family; the port-graph family alone reaches 6.
   → `verification/DEGREE8_SPAN_EQUALITY.md`

## What this package is asking you for

The decisions in `review/MENTOR_DECISION_FORM.md`. Four are scientific
confirmations, four are credit questions, five are wording, and four can only
be closed by a person.

## What you should know before reading

- No human has verified any of this. Every check was written by the same system
  that wrote the code it checks.
- The AI-assistance disclosure is deliberately unflattering and should be read:
  `manuscript/jhep/ai_assistance_disclosure.md`.
- No licence has been chosen, so the code is not currently reusable by anyone.
- The third-party archive is excluded from every release and its owner has not
  been contacted.

## What happens if you do nothing

Nothing is submitted. There is no automatic path from this package to arXiv or
to JHEP, and the submission tag is not created while approvals are outstanding.
