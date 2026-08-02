# Cover message to the mentor — draft, not sent

Subject: ten confirmations on the degree-10 self-dual five-form paper

The degree-10 classification is finished and verified. Before anything is posted
I need your confirmation on ten points, attached as
`MENTOR_REVIEW_PACKAGE_FINAL.pdf` with a one-page decision form.

**Nine are wording or convention. One is not.**

**G-10** is the one that matters. The closure's leading-degree bookkeeping rests
on the free stress tensor of a self-dual five-form being traceless, so that
`Tr(τ)` first contributes at field degree four rather than two. I have derived
this rather than assumed it:

- the trace is `(1 − cd)⟨F,F⟩` for *any* improvement coefficient `c`, so only
  `⟨F,F⟩` matters;
- `F ∧ F` is a top form built from two copies of an odd-degree form, hence zero,
  and `⟨F,⋆F⟩` is proportional to it;
- so `⟨F,F⟩ = 0` on either eigenspace of the star.

Verified computationally with a control at four primes, by code that imports none
of the flow machinery. And it is load-bearing: forcing `Tr(τ)` to contribute from
degree two gives `dim Q10 = 0` instead of `3`.

**What I need from you** is confirmation that the free theory and stress
convention used are the ones you intend, and that no formulation in use — PST,
auxiliary-field, clone, Hamiltonian — changes the quadratic trace. The
independence from `c` narrows this: a differing formulation would have to change
the quadratic scalar *available*, not merely the trace convention.

**G-2** is second in priority and is a correction to something I may have told
you earlier. I previously recorded the oscillator frame as Euclidean, which would
have blocked the bridge entirely. That was wrong: the real signature is `(5,5)`,
split, computed from all one hundred anticommutators of your own operators. Real
self-dual five-forms exist there. If the earlier claim reached you, please
disregard it.

**G-8** concerns credit for the number 81. It is analytic, it is in the
literature, and the paper attributes it there; the earlier float64 evidence is
from your archive. What is claimed here is only the exact lower bound. Please
confirm that division.

Two administrative points: your archive is **not** redistributed — only a
manifest of hashes — and whether that stays the arrangement is G-7. And
authorship is a separate conversation, not part of this package.
