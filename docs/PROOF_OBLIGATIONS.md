# Proof obligations

Open mathematical debts. Each has an ID, the claim it supports, what would
discharge it, and its current state. Nothing in `docs/CLAIM_LEDGER.md` may be
strengthened while its supporting obligation is open.

Baseline: `3ed32805b38ce34216b34888f6539e3538e90fb9`

| ID | supports | state |
|---|---|---|
| PO-01 | C-ATLAS-05 | **DISCHARGED** (Phase 0) |
| PO-02 | C-GEN-01 | PARTIAL |
| PO-03 | C-ATLAS-04 | OPEN |
| PO-04 | C-SEXTIC-* | OPEN (external) |
| PO-05 | C-TRM6-01 | OPEN |
| PO-06 | C-FLOW-01 | **DISCHARGED** (Phase 0) |
| PO-07 | C-FLOW-03 | OPEN |
| PO-08 | C-MIN-01 | **PARTIAL** (permutation subgroup done) |
| PO-09 | all `MOD-CERT` | OPEN |
| PO-10 | Phase 5 | NOT STARTED |

---

## PO-01 — canonicalisation is exact at every degree actually used — **DISCHARGED**

**Supports** C-ATLAS-01, C-ATLAS-05.

**Original concern.** An earlier Weisfeiler–Leman fallback was measured to
collide on precisely the graphs in play: at order 6, 49 true isomorphism
classes collapse to 39 WL keys. Because the enumerator keeps the first graph
per key, a collision **drops a genuine candidate**, and a dropped candidate can
only lower a rank — a confident undercount.

**Discharged, Phase 0.** Verified at `3ed3280`:

- `_canonical_wl` **no longer exists** in `src/sdinv/graphs.py`
  (`hasattr(sdinv.graphs, "_canonical_wl") == False`);
- `canonical()` dispatches to `_canonical_nauty` whenever pynauty is present,
  falls back to the exact n! form only for n ≤ 6, and otherwise **raises**
  `RuntimeError` rather than degrading silently;
- pynauty is importable at runtime (`pynauty is not None == True`) and pinned
  at `2.8.8.1` in `requirements-lock.txt`;
- order 8 is generated directly by nauty's `geng | multig` toolchain, so
  labelled duplicates never arise.

The failure mode is now loud rather than silent, which is the property that
matters. No residual undercount risk.

## PO-02 — `leading_field_degree` is correct, not merely self-consistent

**Supports** C-GEN-01, and through it the exhaustiveness of the degree-6
argument behind C-FLOW-02/03.

Phase 0 verified: 18 expected multisets = 18 present, none missing, none extra,
and leading degrees are additive across products for every generator. That
establishes *internal* completeness given the per-generator
`leading_field_degree` values.

**Still open**: those values are computed by the same code they validate. A
derivation — Tr(τ) has leading degree 4 because the free stress tensor is
traceless, Tr(τ^k) has leading degree 2k for k ≥ 2 — should be written out and
independently checked, ideally clean-room.

## PO-03 — are I12_61 and I12_62 polynomial syzygies?

**Supports** C-ATLAS-04.

Currently only a Jacobian dependence is established. A Jacobian dependence at a
generic point means functional dependence; it does **not** exhibit a polynomial
identity, and the manuscript may not say "syzygy" until one is constructed.

**Discharged by**: bounding the relation degree, enumerating candidate
monomials, computing the exact evaluation matrix, taking a modular nullspace,
reconstructing rationals, and verifying on fresh samples at independent primes
— or by proving no such identity exists in the searched range, with the range
stated.

**Target**: Phase 3.

## PO-04 — the K6 ↔ Σ₂ identification (EXTERNAL)

**Supports** C-SEXTIC-01/02/03 wording.

arXiv:2509.14350v2 proves (Σ₁, Σ₂) is a sextic basis in the spinor formalism
but does **not** publish the change of basis to (Tr(M³), K6). Our
identification is inferred.

**Discharged by**: obtaining the spinor implementation or the explicit map from
the authors, or deriving it independently and verifying numerically. Marked
external because it may need a person, not a computation.

## PO-05 — Tr(M⁶): analytic reduction or basis-independent formulation

**Supports** C-TRM6-01.

29 of 72 columns exceed the CRT uniqueness bound at 15 primes (modulus ≈
5.2e67). Informative contrast: the *flow* coefficients lifted cleanly at five
primes, so this is a height problem specific to Tr(M⁶), not a shortage of
effort. More primes is the wrong instrument.

**Discharged by** either
(A) an analytic identity via Cayley–Hamilton / trace identities / self-duality
    / Schouten identities, verified exactly; or
(B) a proof that every downstream theorem can be stated with Tr(M⁶) as a
    primitive stress-adapted element, making graph coordinates unnecessary.

**Target**: Phase 2. (B) is the more likely route and is sufficient.

## PO-06 — second independent holdout prime — **DISCHARGED**

**Supports** C-FLOW-01.

The committed artifact used five fit primes and **one** holdout (32717); the
standard requires at least two.

**Discharged, Phase 0.** Two assemblies were run over the six available
interacting certificates, each excluding a different prime:

| fit primes | holdout | result |
|---|---|---|
| 32749, 32719, 32693, 32771, 32717 | **32713** | passed |
| 32749, 32719, 32693, 32771, 32713 | **32717** | passed |

Both report `all_modular_and_rational_holdouts_passed: true`. The stronger
check also holds: the two fits agree on the new-forcing dimensions
`{4:1, 6:1, 8:3, 10:5, 12:21}` and produce **192/192 identical** reconstructed
coordinate vectors. Two different fit sets converging on byte-identical
rationals, each validated on the prime it excluded, is materially stronger
than a single holdout.

Reproduce: `scripts/assemble_interacting_stress_adapted.py` with
`--certificates` omitting one prime and `--validation-certificate` set to it.

## PO-07 — does the K6 statement survive field redefinitions and EOM?

**Supports** C-FLOW-03, and gates any physical reading.

The transport equation is an off-shell statement in fixed conventions. A
field-redefinition-dependent obstruction is not a physical obstruction.

**Discharged by**: classifying allowed local field redefinitions at each
degree, computing their action on q6, and determining whether q6 = 0 is
preserved; then repeating modulo the leading equations of motion.

**Until discharged**, no physical or Type IIB consequence may be drawn from
C-FLOW-03.

## PO-08 — minimality under basis change — **PARTIAL**

**Supports** C-MIN-01, C-MIN-02.

**Done (Phase 1): the permutation subgroup.** Random relabellings of the basis
at a degree, applied consistently to `basis`, `coordinates` **and**
`coefficient_monomial`, with the missing set tracked back through the inverse
relabelling. Four trials per degree, all invariant:

| degree | closure dim | missing count | recovered set |
|---|---|---|---|
| 10 | 11 | 3 | I10_6, I10_7, I10_12 |
| 12 | 68 | 4 | I12_59, I12_60, I12_61, I12_62 |

Certificate: `results/generalized_flow/minimality_certificates/basis_permutation.json`

**Why this is not the whole obligation, and why the obvious test is invalid.**
Each certificate target row is indexed by a `coefficient_monomial` that is
itself expressed in the *same* basis as the output `coordinates`. A general
invertible change of basis therefore re-expresses **both**. Multiplying the
coordinate rows by a random matrix `B` and re-running would *look* like a
basis-change test and would not be one: the resulting rows correspond to no
actual flow problem, and would very likely still return 3 and 4 while meaning
nothing.

**Still open: general GL.** Requires regenerating the certificates in the new
basis (~530 s/prime, plus changes to the generator machinery so the monomial
index is re-expressed consistently). Not attempted; scope recorded rather than
claimed.

**Also owed**: an argument that the intrinsic quotient dimension bounds the
minimal cardinality from below, which would make cardinality minimality
basis-independent by construction rather than by testing.

## PO-09 — exceptional primes

**Supports** every `MOD-CERT` row.

Rank mod p is a lower bound for the characteristic-zero rank, with equality
unless p divides a relevant minor. Agreement across 15 primes makes a
coincidence unlikely but does not prove it.

**Discharged by**: a Hadamard-type bound on the relevant minors giving a prime
count beyond which agreement forces equality, or one exact
characteristic-zero computation at a decisive rank.

## PO-10 — the induction for any all-orders claim

**Supports** Phase 5.

No induction on degree currently exists. Degree-12 data cannot imply an
all-orders theorem. Required: base cases, a recursion step, preservation of
hypotheses, and an argument that no exceptional degree exists.

**Until discharged**, "all orders" is forbidden in every document (ledger F-5).
