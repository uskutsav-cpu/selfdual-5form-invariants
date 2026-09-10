# Equation (4.24): index audit of all twelve degree-10 candidates

Source of record: Cederwall, Hutomo, Kuzenko, Lechner, Sorokin, *Some remarks
on invariants*, J. Phys. A 59 (2026) 065203, eq (4.24) — arXiv:2509.14350v2
PDF page 25 (sha256 `ec51d9e22c4d75651e2024d09b17562b…`, identical to the file
recorded in `primary_source_manifest.json`). The PDF is **not** committed.

## 0. How index placement is decided

PDF text extraction returns stacked super/subscripts in an order that depends
on glyph position, so it does **not** reliably say which index of `M` is up and
which is down. Placement is therefore *not* read off the extraction. It is
fixed by a rule that has a unique answer:

> **Every contracted edge carries exactly one raised end.**

An edge joining two equally-placed slots contracts with `delta` instead of
`eta`. That is not a Lorentz scalar, and it is invisible under rotations —
`delta` and `eta` agree on the spatial block — so only a **boost** exposes it.

This is not a precaution. `P10_07` originally raised all six axes on both inner
`N` factors, making its three alpha edges delta-contractions. It passed
homogeneity and rotation invariance, produced plausible values, and was only
caught because the degree-10 projection reported `not_in_atlas_span` on all six
primes. See §3.

The building blocks and their intrinsic placement:

| block | routine | placement |
|---|---|---|
| `mixed` | `five_form_moment` | `M_{a}{}^{b}` — slot 0 DOWN, slot 1 UP |
| `mm` | `mixed @ mixed` | `(MM)_{a}{}^{b}` — slot 0 DOWN, slot 1 UP |
| `N^(1050)` | `composite_n1050` | all six axes DOWN; axes (0,1,2,3,4) already antisymmetrised |
| `N^(4125)` | `composite_n4125` | all six axes DOWN |

`mm` being `(MM)_{a}{}^{b}` rather than `(MM)^{a}{}_{b}` is the detail that
fixes `P10_07` and `P10_08`: the matrix product contracts the UP index of the
first factor with the DOWN index of the second, so the surviving slots are DOWN
then UP.

## 1. Verbatim structure, all twelve

Transcribed from the extracted text stream; bracket **delimiters** are reliable
even though bracket **colour** is not. Square `[...]` are the black
antisymmetrisations; round `(...)` are the red operations, which the paper
states act *upon* the black ones.

| # | structure | blocks | brackets |
|---|---|---|---|
| 1 | `tr M^5` | M×5 | none |
| 2 | `(MM)^{m1}_{n1} M^{m2}_{n2} M^{m3}_{n3} N^(4125)_{n1n2n3}{}^{m1m2m3}` | M×4, N4125 | none |
| 3 | `M^{m1}_{n1} M^{m2}_{n2} M^{m3}_{n3} (N^{[m1m2m3,a1a2]a3} N_{[n1n2n3,a1a2]a3})` | M×3, N1050×2 | black only, supplied by `composite_n1050` |
| 4 | `(MM)^{mn} M^{rl} (N_{[a1a2a3a4(m]n} N^{[a1a2a3a4}{}_{r]l)})` | M×3, N1050×2 | black + **RED** `( m … r]l )` |
| 5 | `(MM)_{[n1}{}^{[m1} M_{n2]}{}^{m2]} N_{[r1r2r3,r4 m1]m2} N^{[r1r2r3,r4 n1]n2}` | M×3, N1050×2 | black ×2, explicit |
| 6 | `(MM)^{n1}_{m1} M^{n2}_{m2} N_{[m1m2r1,r2r3]r4} N^{r1r2r3,r4n1n2}_(4125)` | M×3, N1050, N4125 | black only, supplied |
| 7 | `N_{[r1r2r3,r4r5]}{}^{m} (MM)_{m}{}^{k} (N^{[r1r2r3,}{}_{a1a2]a3} N^{[r4r5k,a1a3]a2})` | M×2, N1050×3 | black only, supplied |
| 8 | `N_{[r1r2r3,r4 n]m} M^{[n}{}_{r5} M^{m]}{}_{k} (N^{[r1r2r3,}{}_{a1a2]a3} N^{[r4r5k,a1a3]a2})` | M×2, N1050×3 | black ×1, explicit |
| 9 | `N_{[a1a2a3a4k](n} M^{km} N^{[a1a2a3a4}{}_{r]l)} N^{[b1b2b3b4m]n} N_{[b1b2b3b4}{}_{r]l}` | M×1, N1050×4 | black + **RED** `( n … r]l )` |
| 10 | `(N_{[r1r2r3,r4[m1]m2]} N^{[r1r2r3,}{}_{a1a2]a3} N^{[r4n1n2,a1a3]a2}) (N_{[b1b2b3,b4n1]n2} N^{[b1b2b3,b4m1]m2})` | N1050×5 | black, **nested** |
| 11 | `(N_{[r1r2r3,}{}^{a1a2]a3} N_{[m1m2m3,a1a2]a3}) (N^{[m1m2m3[n1n2]n3]} N^{[r1r2l1[l2l3]}{}_{n1]} N^{[r3}{}_{n2 l2[l1l3]n3]})` | N1050×5 | black, **nested** |
| 12 | `(N_{[r1r2r3,}{}^{a1a2]a3} N_{[m1m2m3,a1a2]a3}) (N^{[m1m2m3[n1n2]n3]} N_{[n1}{}^{r1l1[r2l2]l3]} N^{[r3}{}_{n2l2[n3l1]l3]})` | N1050×5 | black, **nested** |

Field degree is 10 for every entry: `M` and `N` are each degree 2 in `F`, and
every row carries five blocks.

## 2. Implemented candidates

| # | evaluator | raise pattern | validation |
|---|---|---|---|
| 1 | `p10_01_trM5` | — | homogeneity, boost, 6 primes |
| 2 | `p10_02_mm_m_m_n4125` | `N4125` axes (3,4,5) | homogeneity, boost, 6 primes |
| 3 | `p10_03_m3_n1050_n1050` | `N` all six on one copy | homogeneity, boost, 6 primes |
| 5 | `p10_05_mm_m_antisym_n1050_n1050` | `N` all six on one copy | homogeneity, boost, mutation |
| 6 | `p10_06_mm_m_n1050_n4125` | `N4125` all six | homogeneity, boost, 6 primes |
| 7 | `p10_07_n1050_mm_n1050_n1050` | outer (5); inner (0,1,2) / (0,1,3,4,5) | homogeneity, boost, edge-freedom, mutation |
| 8 | `p10_08_n1050_mm_antisym_n1050_n1050` | outer (4,5); inner (0,1,2) / (0,3,4,5) | homogeneity, boost, mutation |

## 3. The `P10_07` metric-placement defect — recorded in full

**Symptom.** `not_in_atlas_span` on all six primes. A consistent failure across
independent moduli is structural, not modular bad luck.

**Cause.** The evaluator raised axes `(0,1,2,3,4,5)` on *both* inner `N`
factors, so the three alpha edges `a1,a2,a3` each joined two raised slots.

**Evidence.**

| candidate | base | boosted | rotated |
|---|---|---|---|
| P10_01/02/03/06 | — | equal | equal |
| P10_07 (as shipped) | 22769 | 19807 | 22769 |

Rotation-invariant, boost-violating: the signature of a metric misplacement.

**Fix.** `mm` is `(MM)_{a}{}^{b}`, so the outer `N` carries `mu` UP — axis 5
raised — and the second inner `N` carries `kappa` DOWN — axis 2 *not* raised.
Raise `(5,)` / `(0,1,2)` / `(0,1,3,4,5)`.

**Confirmation beyond the boost test.** Moving the metric to the other end of
each alpha edge — raising `(0,1,2,3,4,5)` and `(0,1)` instead — gives
bit-identical values (10384 at 32749, 25537 at 32719). A true tensor
contraction cannot care which end carries the metric, so this rules out being
boost-invariant by accident.

**Why it survived.** No boost test existed for any degree-10 candidate. The
suite checked homogeneity, which catches int64 overflow, and nothing else about
index placement. `test_every_published_candidate_is_boost_invariant` now covers
all of them, and `test_the_original_p10_07_placement_really_was_broken` pins the
diagnosis so a reversion cannot pass silently.

## 4. Open source ambiguities

These are recorded rather than guessed, per the program's evidence rules.

**AMB-01 — extent of the red bracket in I^(4) and I^(9).** The red parenthesis
opens before `mu` (resp. `nu`) and closes after `lambda`, enclosing four slots.
Two readings are consistent with the glyph stream:

- (a) symmetrise all four enclosed indices;
- (b) symmetrise the two *pairs*, `(mu nu)` against `(rho lambda)`.

Both reduce to the same tensor only if the pair blocks are already symmetric,
which is not established here. Colour is what disambiguates and colour does not
survive extraction.

**AMB-02 — nested bracket association in I^(10), I^(11), I^(12).** Structures
such as `[r1r2r3,r4[m1]m2]` and `[r1r2l1[l2l3]{}_{n1]}` contain a black bracket
opening inside another black bracket, with the inner closing before the outer.
Whether the inner is a genuine nested antisymmetrisation or a red-stage
operation printed in square glyphs cannot be settled from the text stream.

Resolving either requires a colour render of journal page 17 / arXiv page 25.

## 5. Measured properties of the implemented brackets

**P10_05** — both black antisymmetrisations are non-vacuous: removing them
changes the value.

**P10_08** — its black antisymmetrisation `[nu ... mu]` is **redundant**, and
this is a property of the contraction, not a defect. Measured at 32749 and
32719:

| variant | 32749 | 32719 |
|---|---:|---:|
| no bracket | 10763 | 25675 |
| antisym (nu, mu) | 10763 | 25675 |
| **sym (nu, mu)** | **0** | **0** |
| antisym (nu, rho5) — control | 11222 | 2674 |
| antisym (mu, kappa) — control | 3880 | 27191 |

The symmetric part of the pair contracts to exactly zero, so the rest of the
contraction already projects onto the antisymmetric part and the explicit
bracket adds nothing. The two controls show the bracket engine is genuinely
acting on this tensor, so the redundancy is a fact about I^(8) rather than a
silently disabled operation.

**Consequence for testing.** A non-vacuity test of the form "removing the
bracket must change the value" is the wrong guard here: it fails on a correct
implementation. The test instead asserts the vanishing of the symmetric part,
which is the *reason* for the redundancy, plus a live-engine control.

## 6. AMB-02 measured

Both readings were implemented and projected. The quotient image is what
matters, and it is not always sensitive to the ambiguity:

| candidate | raw values differ? | Q10 image differs? |
|---|---|---|
| I^(10) | yes | **no** — identical at both primes |
| I^(11) | yes | **yes** — differs at both primes |
| I^(12) | no — readings agree exactly | no |

So AMB-02 is harmless for I^(10) and I^(12) at the level of the quotient, and
live for I^(11). This is what makes `{P10_09, P10_10, P10_12}` preferable to a
basis containing P10_11; see `intrinsic_degree10_levelB.md` §3.
