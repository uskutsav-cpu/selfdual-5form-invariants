# G-10 — the free stress tensor is traceless, and Tr(τ) begins at degree four

**Status: PROVED.** Not "exactly certified", not "verified over the tested
fields" — the argument below is analytic, holds off shell, and does not
depend on the sign convention for ε, on the duality channel, or on the real
form. The computations quoted are cross-checks on a proof, not the proof.

This closes the item the handoff identified as the highest-risk unresolved
physics question. Mentor review is still wanted, but for *conventions and
physical interpretation* — it is no longer standing in for a missing
derivation.

## What had to be shown

The activated flow closure assumes that `Tr(τ)` has no quadratic part, so
that its targets first switch on at field degree four. If instead `Tr(τ)`
began at degree two, extra directions would be reachable from the start, the
closure would grow, and `dim Q10 = 3` could collapse. The obstruction stands
or falls on this.

## Conventions, quoted from the project rather than assumed

From `docs/stress_flow_definition_audit.md` and `src/sdinv/stress.py`:

```
η_{μν} = diag(−1, +1, …, +1)      ε^{01…9} = −1      *Λ = Λ
```

`Λ` is the auxiliary self-dual five-form of the INZ formulation, identified
on the physical gauge-field equation with `Λ₅ = −F₅⁺`. **Degree** means
homogeneous polynomial degree in the components of `Λ`; `Λ` has degree 1,
`M` and the free stress tensor have degree 2. Coupling order is a different
filtration and is not used here.

The moment tensor and the free stress tensor are

```
M_{μν} = Λ_{μ ρ₁ρ₂ρ₃ρ₄} Λ_ν^{ρ₁ρ₂ρ₃ρ₄}          T⁽⁰⁾_{μν} = M_{μν} / (2·4!) = M_{μν}/48
```

(`free_stress`, `src/sdinv/stress.py:515`). The fully interacting Hilbert
tensor from the INZ action is

```
T_{μν}[V] = (1/(2·4!)) ( Λ_μ^{ρ(4)} Λ_{ν ρ(4)} − 25 V_{Λ μ}^{ρ(4)} V_{Λ ν ρ(4)} )
            − (1/4!) g_{μν} ( V − ½ Λ·V_Λ )
```

with `V_{Λ μ(5)} = ∂V/∂Λ^{μ(5)}` **anti**-self-dual.

## Step 1 — a (anti-)self-dual five-form has vanishing full square

Let `F` be a real 5-form in `D = 10` with `*F = σF`, `σ = ±1`. For any
p-form, `α ∧ *β = ⟨α, β⟩ vol`. Take `α = β = F`:

```
⟨F, F⟩ vol = F ∧ *F = σ (F ∧ F)
```

But `F` has odd degree 5, and for a p-form `F ∧ F = (−1)^{p²} F ∧ F`, so
with `p = 5`, `F ∧ F = −F ∧ F`, hence

```
F ∧ F = 0      ⟹      ⟨F, F⟩ = F_{μ₁…μ₅} F^{μ₁…μ₅} = 0.
```

**This is off shell, algebraic, and independent of σ.** It uses only
antisymmetry and self-duality — no equation of motion, no Bianchi identity,
no improvement term, no choice of action formulation.

Note where it does *not* hold: real self-duality requires `** = +1` on
5-forms, i.e. `(−1)^{p(D−p)}(−1)^t = (−1)^{25}(−1)^t = +1`, so `t` must be
odd. Lorentzian `(1,9)` and split `(5,5)` qualify; Euclidean `(10,0)` does
not, and there the statement is only about complex self-dual forms. The
verifier tests all three and reports exactly this.

## Step 2 — the free stress tensor is traceless

```
η^{μν} M_{μν} = Λ^{ν ρ(4)} Λ_{ν ρ(4)} = ⟨Λ, Λ⟩ · 4!  = 0
```

by Step 1 with `σ = +1`. Therefore `Tr T⁽⁰⁾ = 0` **identically**. Not on
shell; not up to an improvement; not for a special `V`. The trace of the
free tensor vanishes for every algebraically self-dual `Λ`.

## Step 3 — both bilinear terms of the interacting trace drop out

Tracing the interacting tensor with `g^{μν}` in `D = 10`:

```
Tr T[V] = (1/48)( ⟨Λ,Λ⟩·4! − 25 ⟨V_Λ, V_Λ⟩·4! ) − (10/4!)( V − ½ Λ·V_Λ )
```

`⟨Λ,Λ⟩ = 0` by Step 1 with `σ = +1`. And `V_Λ` is **anti**-self-dual, so
`⟨V_Λ, V_Λ⟩ = 0` by Step 1 with `σ = −1` — the argument never used the sign.
Both bilinear terms vanish, leaving

```
Tr T[V] = − (10/4!) ( V − ½ Λ·V_Λ ).
```

## Step 4 — the Euler factor, and why degree two is empty

Let `V_d` be the part of `V` homogeneous of degree `d` in `Λ`. Euler's
theorem gives `Λ·V_{d,Λ} = d·V_d`, so

```
Tr T[V_d] = − (10/4!) (1 − d/2) V_d = (10/48) (d − 2) V_d.
```

In the project's `τ` normalisation (`τ = 48·T`, the `M`-normalised tensor):

```
Tr(τ)[V_d] = 10 (d − 2) V_d.
```

The factor `(d − 2)` vanishes identically at `d = 2`. **A quadratic
interaction contributes nothing to the trace, for any coefficient.** The
next degree present in the flow's grading is `d = 4`, where the coefficient
is `10·2 = 20 ≠ 0`.

Two independent facts are doing the work and both are needed: `⟨Λ,Λ⟩ = 0`
removes the bilinear terms (Steps 1–3), and the Euler factor `(d−2)` removes
degree two (Step 4). Neither alone suffices.

## Step 5 — the activation consequence, spelled out

```
free stress tensor traceless                      (Step 2)
  ⇒ Tr(τ) has no term bilinear in Λ alone         (Step 3)
  ⇒ Tr(τ)[V_d] = 10(d−2)V_d, zero at d = 2        (Step 4)
  ⇒ Tr(τ) has no quadratic contribution
  ⇒ no degree-2 tr_tau target exists
  ⇒ the tr_tau family first activates at degree 4
```

The last step is the one the closure consumes: with no degree-2 target,
nothing in the `tr_tau` family is reachable until a degree-4 direction is
already in the span, which is exactly the activation condition implemented in
`activated_closure` (`scripts/verify_D10_independent.py:203`).

## Independent verification (Phase 3.4)

`scripts/verify_g10_trace_independent.py` rebuilds the Hodge star, the
duality projector, `M` and the trace from the definitions in exact integer
arithmetic. It imports nothing from `src/sdinv` and nothing from the
stress-flow production code.

| what | result |
|---|---|
| `**` on 5-forms, Lorentzian (1,9) | `+1` — real self-duality exists |
| `**` on 5-forms, split (5,5) | `+1` — real self-duality exists |
| `**` on 5-forms, Euclidean (10,0) | `−1` — no real self-dual 5-form |
| samples tested (2 signatures × 2 ε signs × 2 channels) | 192 |
| samples with `Tr M ≠ 0` | **0** |
| samples with `M` non-symmetric | 0 |

Result: `results/stress_flow/g10_trace_verification.json`.

## Cross-check against the production artifact

`results/stress_flow/interacting_flow_equations.json` carries 192 targets.
Every one of the `tr_tau` generator's targets has coefficient exactly
`10(d−2)`, derived here analytically and independently:

| field degree | artifact coefficient | `10(d−2)` |
|---:|---:|---:|
| 4 | 20 | 20 |
| 6 | 40 | 40 |
| 8 | 60 | 60 |

and `min(field_degree) = 4` over the whole `tr_tau` family, with **no
degree-2 target present**. The artifact's own `derivation` field reads
`Tr(tau)[V_d]=10*(d-2)*V_d`, matching the formula obtained above from the
action. The derivation and the data agree coefficient by coefficient.

## Formulation independence (Phase 3.3)

Step 1 is a statement about an algebraically self-dual 5-form and nothing
else, so it survives any reformulation that keeps `*Λ = Λ`. Steps 3–4 use
the INZ Hilbert tensor with `V_Λ` anti-self-dual. PST, clone and Hamiltonian
formulations differ by terms proportional to the auxiliary/PST-scalar
equations and by field redefinitions; at the perturbative order used here
they change `T_{μν}` by such terms and do not introduce a `Λ`-bilinear trace,
because any candidate bilinear is again `⟨Λ,Λ⟩` or `⟨V_Λ,V_Λ⟩` and both
vanish identically. **What is convention-dependent is the overall
normalisation of `τ` (the 48), not the vanishing.** The trace-order
statement the closure relies on — "no quadratic part" — is therefore
formulation-independent at the order used.

The one place this would fail is a formulation whose stress tensor contains a
term bilinear in `Λ` that is *not* a full contraction — e.g. contracted
through a background structure other than `η`. No formulation in scope does
this.

## Counterfactual (Phase 3.6)

`tests/test_g10_trace_activation.py` inserts the degree-2 trace contribution
that G-10 rules out. A quadratic trace is unconditional, so its coefficient
monomial is empty and the `tr_tau` family activates immediately rather than
waiting for a degree-4 direction. The recorded effect:

| quantity | G-10 holds | quadratic trace inserted |
|---|---:|---:|
| `dim D10` | **11** | 14 |
| `dim Q10` | **3** | **0** |

This is not a perturbation of the answer — it is the difference between an
obstruction and no obstruction, and it reproduces the historical error
exactly: taking the unconditional span of all raw targets gave rank 14 and
quotient 0, and nothing objected at the time. G-10 is what stands between
those two numbers, so it is load-bearing in the strongest sense: **if the
free stress tensor were not traceless, this paper would have no degree-10
result to report.**

Nine tests cover the family: the Euler coefficient against every shipped
`tr_tau` target, the absence of a degree-2 target, the baseline closure, the
raw-span negative fixture, the counterfactual and its reported effect, a live
rerun of the independent verifier, and the real-form table. All pass.

## Verdict

| question | answer |
|---|---|
| Free stress tensor traceless? | **Yes, identically and off shell** |
| Depends on self-duality? | **Yes — this is the only input** |
| Depends on an equation of motion? | No |
| Depends on an improvement term? | No |
| Depends on the action formulation? | No (normalisation only) |
| Lowest degree of `Tr(τ)` | **4** |
| G-10 status | **PROVED** |
