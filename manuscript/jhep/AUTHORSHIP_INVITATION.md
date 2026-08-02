# Authorship invitation — draft for the author to send

This is a draft. Read it, change it to sound like you, and send it yourself.
Do not send it as though it came from anyone else.

Nothing in this repository may list a co-author until a reply agreeing to it
exists in writing and is recorded in `audit/AUTHOR_APPROVAL_CHECKLIST.md`.

---

**Subject:** Invitation to co-author — self-dual five-form invariants in D=10

Dear Dr. Ferko,

I am a high-school student in Frisco, Texas, working on the ring of Lorentz
invariants of a self-dual five-form in ten dimensions. I am writing to ask
whether you would be willing to be a co-author on a manuscript I have prepared,
and if so whether you would be willing to act as corresponding author.

I want to be direct about three things up front.

**The method is yours, and the paper says so.** The workflow of enumerating
candidate contractions, evaluating them at sample points and detecting
relations from the Jacobian is the one in Elamaran, Ferko and Scarlett,
*Machine Learning Invariants of Tensors*, Phys. Rev. D 114 (2026) 026016. The
paper cites it as the source of the method and does not claim it. What I have
done is execute it in exact arithmetic for this particular problem and produce
a certificate: an explicit 81×81 minor with nonzero determinant, confirmed by
two independent determinant routines, over a matrix of primes and sample seeds.

**There is one result I believe is new to this problem, and one negative
result.** The free stress tensor of a self-dual five-form in D=10 is traceless
identically and off shell — it follows in three lines from the fact that a
five-form has odd degree, so F∧F = −F∧F. Consequently
Tr(τ)[V_d] = 10(d−2)V_d has no quadratic part. Using this, the degree-ten seed
closure of the Hutomo–Lechner–Sorokin stress flow computes exactly over the
rationals as dim D10 = 11 inside dim A10 = 14, leaving a three-dimensional
quotient the seeded flow does not reach. The negative result is that Tr(M⁶) has
no certified rational lift at fifteen primes; I report that rather than
guessing the coefficients.

**The work used substantial AI assistance and the paper discloses it.** Most of
the code, all of the test suites and much of the audit apparatus were
machine-written, as was the analysis behind the degree-ten result. The
disclosure is in the manuscript's acknowledgments and in a separate document.
It also states plainly that this does not constitute independent human
verification — which is part of why I am writing to you.

If any of this is wrong, or already known, or not worth a paper, I would rather
hear that than publish it. If you would prefer to be acknowledged rather than
listed as an author, or not mentioned at all, that is entirely fine and I will
remove the reference.

The manuscript and the full computational record are available; I can send
either.

Thank you for your time.

Utsav Sunil Kumar
Heritage High School, Frisco, TX

---

## Notes for the sender

- Verify Dr. Ferko's current affiliation before sending. The request that
  prompted this draft said "MIT IAIFI lab"; that has **not** been checked
  against a current source, and getting an affiliation wrong in print is its
  own problem.
- If he agrees to corresponding author, he — not you — files the submission.
  That is what the role means.
- Keep the reply. It is the record `audit/AUTHOR_APPROVAL_CHECKLIST.md` needs.
