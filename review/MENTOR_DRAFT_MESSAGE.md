# Draft message to the mentor

**Not sent.** This is a draft for the user to review, edit and send themselves.
Placeholders in ANGLE BRACKETS need filling in before it goes anywhere.

---

Subject: Draft paper on degree-ten invariants of the self-dual five-form — request for review

Dear <MENTOR NAME>,

I've attached a complete draft of the work on Lorentz invariants of the
ten-dimensional self-dual five-form, and I would be grateful for your review
before it goes any further.

The short version of what it establishes: the degree-ten invariant space has
dimension 14 over the rationals, the subspace reachable by the stress-tensor
flow has dimension 11, and the quotient therefore has dimension 3 — three
independent degree-ten directions that flow does not reach. Separately, the span
of the published degree-ten structures turns out to meet the product sector in
exactly one dimension, and that intersection is written out as an explicit
integer identity. All of these are exact over Q rather than modulo a prime.

There is also an exact lower bound of 81 on the generic functional rank, with an
explicit 81×81 minor. I want to be clear that the number 81 itself is not mine —
it is analytic and it is in the literature. What I claim is the certified lower
bound reproducing it.

I would particularly value your view on four things:

1. **The stress-tensor trace argument (§10).** I prove the free stress tensor of
   a self-dual five-form is traceless for any improvement coefficient, which
   fixes `Tr(τ)` as beginning at field degree four. Everything at degree ten
   depends on this — if it began at degree two the quotient would be zero
   instead of three. The mathematics is short and I am fairly confident in it.
   What I could not settle from the published text is whether the `τ` appearing
   in the flow is an object of the shape my theorem assumes. If you can tell me,
   that closes the last load-bearing gap.

2. **Whether `D10` is correctly named.** The result turns on distinguishing the
   raw span of generated targets (dimension 14) from what the flow actually
   activates (dimension 11). Conflating them gives zero, which is the answer I
   had before catching the error.

3. **Credit and novelty framing.** Every novelty claim in my ledger is marked
   provisional, because a literature search can only show absence of evidence.
   I would rather understate than overstate, and I would value your judgement on
   whether I have the balance right — particularly around rank 81 and around the
   relationship to the published degree-ten structures.

4. **Whether the physical discussion (§13) is too cautious.** I decline to draw
   any Type IIB conclusion or to interpret the three missed directions. That may
   be the right call or it may be leaving the most interesting question
   unasked.

Two things I should flag directly rather than let you discover them.

The draft was prepared with substantial AI assistance — code, debugging,
drafting, and the running of the verification scripts. So the computations were
not checked by a human independently of the system that produced them. The
manuscript says so in its disclosure section. I did not want that buried.

And the paper openly describes several errors found in my own earlier work,
including two that had produced wrong numbers. I decided that reporting them
makes the rest more trustworthy rather than less, but if you think that is the
wrong call for a journal submission, tell me.

Nothing has been submitted anywhere. Authorship, affiliations, licence and DOI
are all deliberately unresolved and marked in red in the draft — I did not want
to presume anything about authorship before speaking with you.

Attached:

- `paper.pdf` — the full draft (41 pages, including 12 appendices)
- `mentor_review_guide.pdf` — a short orientation, including where to look first
- `claim_ledger.pdf` — every claim with its proof type and supporting artifact
- `figure_book.pdf` — the figures on their own
- `reproduction_quickstart.pdf` — how to re-run the results

The code and all certificates are at
`github.com/uskutsav-cpu/selfdual-5form-invariants`, branch
`publication/jhep-mentor-draft`.

Thank you for taking the time.

Best regards,
<YOUR NAME>
