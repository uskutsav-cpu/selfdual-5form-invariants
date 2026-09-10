# Related work: complete audit

Searched through 2026-08-01. Primary sources consulted directly at their arXiv or
publisher landing pages, not through summaries.

## Papers audited

| id | title | authors | date | relevance | does it pre-empt any claim here? |
|---|---|---|---|---|---|
| arXiv:2509.14350 / J. Phys. A **59** (2026) 065203 | Some remarks on invariants | Cederwall, Hutomo, Kuzenko, Lechner, Sorokin | v2 29 Jan 2026 | source of the twelve degree-10 candidate structures | **No.** Gives expressions, not a basis; relations undetermined |
| arXiv:2509.14351 / JHEP **02** (2026) 147 | On non-linear chiral 4-form theories in D=10 | Hutomo, Lechner, Sorokin | v2 6 Jan 2026 | source of the count 81 and of the stress-flow construction; states D=10 differs from D=4,6 | **Partly.** The *qualitative* non-universality is theirs and is cited as such. The exact codimension is not there |
| arXiv:2601.13022 | On nonlinear self-duality in 4p dimensions | Kuzenko | v3 11 Jun 2026 | cites 2509.14351; extends 4D self-dual models to `D = 4p` with the stress-tensor trace driving the flow | **No.** `D = 10` is not of the form `4p`; no five-form invariant classification |
| arXiv:2602.24058 | More on TTbar-like deformations in higher dimensions | Brizio, Kade, Sfondrini, Sorokin | v1 27 Feb 2026 | higher-dimensional stress-tensor flows for Nambu–Goto, Born–Infeld, DBI | **No.** No self-dual five-form invariants, no obstruction theorem |
| arXiv:2606.13064 | Exact Relevant Stress-Tensor Flows and a Causality No-Go in Self-Dual Electrodynamics | Babaei-Aghbolagh, Chen, He, Hou | v1 11 Jun 2026 | a genuine no-go for stress-tensor flows, but in **four** dimensions and about causality | **No.** Different dimension, different obstruction. Relevant as a *method* precedent for selection principles |
| arXiv:2402.06947 | Interacting Chiral Form Field Theories and TTbar-like Flows in Six and Higher Dimensions | — | 2024 | the `D = 6` universality baseline | **No.** Establishes the case our `D = 10` result contrasts with |
| Kugo & Townsend, Nucl. Phys. B **221** (1983) 357 | Supersymmetry and the division algebras | Kugo, Townsend | 1983 | Majorana–Weyl existence by signature | cited only for that |

## The decisive quotation

The source paper itself states that finding an explicit form of the invariants
"turns out to be an open and highly non-trivial group-theoretical problem, with
detailed treatment to be found in separate publications."

That is the strongest available evidence that the explicit degree-10
classification was open at the time of writing, and it comes from the authors of
the very paper that defines the problem — not from an absence of search results.

## What the source paper already contains, which we must not re-claim

- the count 81, and its derivation from the trivial generic stabiliser;
- the identification `M_mu{}^nu = F_{mu rho1..rho4} F^{nu rho1..rho4}`, symmetric
  and traceless, in the **54** of `SO(1,9)`;
- the invariants `I_{2n} = Tr M^n`, `n = 2, ..., 10`, i.e. exactly `D − 1 = 9` of
  them;
- the single independent fourth-order invariant `I_4 = Tr M^2`;
- the statement that `D = 10` requires structures beyond stress-tensor invariants.

Every one of these is cited, and none is presented as new.

## Claims classified

| claim | classification |
|---|---|
| count 81 | **known** — cited |
| `M` symmetric traceless, `Tr M^n` for `n = 2..10` | **known** — cited |
| `D = 10` needs more than stress-tensor invariants | **known, qualitative** — cited |
| explicit degree-10 basis, `dim A10 = 14` | **apparently new** — source calls the problem open |
| `dim D10 = 11`, `dim Q10 = 3` | **apparently new** |
| published span is *not* a product complement | **apparently new**; a correction |
| `M`-trace sector codimension 12 at degree 10 | **apparently new**, and an easy corollary of known ingredients |
| trace-sector deficiency proposition | **apparently new**, but elementary; a counting corollary, not a deep theorem |
| exact rank-81 certificate with an explicit minor | **apparently new** as a certificate; the number is not |
| tensor–spinor bridge as an exact certified map | **apparently new** as an implementation; the gamma map itself is standard |
| cross-dimensional flow theorem | **not proven** — see the theorem attempt |

## Limits of this audit

Searched: the two source papers, their citing papers found via search, and
targeted queries on the specific objects. **Not** searched: the full citation
graph of the classical invariant-theory literature on `Spin(10)` modules, or
theses. A result in that literature under different terminology would not have
been found. Every "apparently new" above therefore remains **PROVISIONAL** and is
so marked in the claim matrix.
