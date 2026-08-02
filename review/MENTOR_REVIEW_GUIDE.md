# Mentor review guide

A short orientation to the draft, written to save you time rather than to
persuade you. If you read only one section of this file, read
"Where to look first".

---

## What the paper claims

The degree-ten Lorentz-invariant structure of a self-dual five-form in ten
dimensions, determined exactly:

- the full degree-ten invariant space has dimension **14** over `Q`;
- the subspace reachable by the stress-tensor flow has dimension **11**;
- the quotient therefore has dimension **3** — three directions the flow misses;
- the span of the published degree-ten structures meets the product sector in
  exactly **1** dimension, written out as an explicit integer identity;
- the generic functional rank of the candidate family is **at least 81**,
  certified by an explicit 81×81 minor.

All four dimensions are exact over the rationals, not modulo a prime.

## What is new, and what is not

**Not new, and the paper says so in the introduction and again in §6:** the
enumerate–evaluate–relate workflow (Elamaran–Ferko–Scarlett), the stress-flow
construction (Hutomo–Lechner–Sorokin), the gamma-matrix map, the number 81, and
the elementary cardinality bound of proposition 9.4.

**What we claim:** the exact dimensions, the exact intersection with its
generator, the certified bridge implementation, the exact lower bound with its
minor, and the certification layer generally.

**Every novelty row is PROVISIONAL** (`audit/MENTOR_DRAFT_NOVELTY_LEDGER.md`).
A literature search shows absence of evidence, not evidence of absence. Nothing
is described as new on the strength of that file alone, and no row may be
upgraded without you.

## Which calculations are exact, and in what sense

| result | strength |
|---|---|
| `dim_Q D10 = 11`, `dim_Q Q10 = 3` | exact over `Q` — CRT lift, held-out prime, fixed point in exact rational arithmetic |
| `dim_Q(B10 ∩ P10) = 1` | exact over `Q` — CRT lift, held-out prime, fresh-sample re-verification |
| `dim_Q A10 = 14` | exact over `Q` via the spanning-set argument (§6) |
| generic rank ≥ 81 | exact mod `p`, carried to characteristic zero by an integer minor |
| generic rank = 81 | **analytic and cited** — the upper bound is not ours |
| bridge properties | exact mod `p` at each prime used |
| degree-8 indispensability | ablation within our own families — **qualified, not universal** |

## What remains open

Ten items, listed in §14 and in the claim ledger. The ones most likely to matter
to you: removal minimality outside a fixed basis; the generator-extension
question; no Hilbert-series cross-check; 13 of 15 rank-matrix cells not
independently recomputed; and the source ambiguity AMB-01/02, which we avoid
rather than resolve.

---

## Where to look first

In this order. The first item is the one that carries the most weight.

1. **G-10 — §10 and appendix I.** The theorem: the free stress tensor of a
   self-dual five-form is traceless, for *any* improvement coefficient, so
   `Tr(τ)` begins at field degree four. Everything at degree ten depends on it —
   the counterfactual gives `Q10 = 0`. The mathematics is short and we believe
   it is right. **The question for you is whether the flow's `τ` is an object of
   the shape the theorem assumes, in the formulation the source intends.** We
   could not settle that from the published text and have flagged it rather than
   assumed the favourable reading.

2. **The orientation-fixed bridge — §5.3 and appendix B.** A square-root branch
   in the frame congruence was silently selecting the anti-self-dual projector at
   some primes. Found because three rank-matrix cells failed at `p = 32707`;
   diagnosed as a branch, not an exceptional prime, by flipping it at both a
   failing and a working prime. No published number changed. Please confirm the
   branch we pin is the one you would intend.

3. **The exact definition of `D10` — §9.1 and appendix H.** The distinction
   between the *raw target span* (dimension 14) and the *activated closure*
   (dimension 11) is the whole result. Conflating them gives `Q10 = 0`, which is
   the answer this project had before catching the error. Is "reachable by the
   stress flow" the right name for what we compute?

4. **The quotient `Q10` — §9.2–9.4.** Three exact annihilating covectors, an
   explicit 11×11 minor, and a basis-free cardinality bound.

5. **Rank 81 — §8 and appendix G.** Specifically the credit split: we claim the
   lower bound and the certificate, and cite the analytic upper bound. Is that
   apportionment right?

6. **The published-basis result — §11.** That the published span contains one
   product direction. We have tried to frame this as a structural observation
   rather than a criticism; please check it reads that way.

7. **Physical significance — §13.** We decline to interpret. Too cautious?

8. **Title and novelty positioning.** *Exact degree-ten invariants of a self-dual
   five-form in ten dimensions.*

---

## Where the code and certificates are

Repository: `github.com/uskutsav-cpu/selfdual-5form-invariants`
Branch: `publication/jhep-mentor-draft`

| what | where |
|---|---|
| headline certificates | `results/stress_flow/`, `results/degree10/`, `results/rank81/` |
| input manifest with hashes | `results/mentor_draft/scientific_input_manifest.json` |
| claim → certificate map | `audit/MENTOR_DRAFT_CLAIM_CERTIFICATE_MATRIX.md` |
| adversarial reviews and our replies | `audit/MENTOR_DRAFT_REFEREE_{A,B,C,D}.md`, `..._INTERNAL_RESPONSE.md` |
| manuscript source | `manuscript/jhep/` |

## How to reproduce the main results

```
git clone https://github.com/uskutsav-cpu/selfdual-5form-invariants
cd selfdual-5form-invariants
git switch publication/jhep-mentor-draft
python3 -m venv .venv
.venv/bin/python3 -m pip install -r requirements.txt
.venv/bin/python3 -m pytest tests spinor_trace_bridge/tests -q
.venv/bin/python3 scripts/d10_characteristic_zero.py
.venv/bin/python3 scripts/b10_p10_characteristic_zero.py
```

Expected: 254 + 86 tests passing; `dim_Q D10 = 11`, `dim_Q Q10 = 3`;
`dim_Q(B10 ∩ P10) = 1`.

Note: `opt_einsum` is imported by the code but is optional, absent from
`requirements.txt`, and was **not** installed for the certified runs.

---

## Two things you should know before you start

**On AI assistance.** This work was prepared with substantial AI assistance,
including code generation, debugging, drafting, and — importantly — the
*execution* of the verification scripts. The computations were therefore not
verified by a human independently of the system that produced them. The
manuscript says this plainly in its disclosure section rather than leaving it to
be inferred. No AI system is an author.

**On the errors reported in the paper.** The draft describes six defects found
in this project's own earlier work, including two that produced wrong published
numbers before being caught. That is deliberate. A computational result's
credibility rests as much on the errors that were found as on the checks that
passed, and burying them would make the remaining claims harder, not easier, to
trust.
