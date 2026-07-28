# Lorentz invariants of a self-dual 5-form in 10D

Extension of Elamaran–Ferko–Scarlett, *Machine Learning Invariants of Tensors*
([arXiv:2512.23750](https://arxiv.org/abs/2512.23750), Phys. Rev. D).

## The question

How many functionally independent Lorentz scalars can be built from a
self-dual 5-form $F^+_{\mu_1\ldots\mu_5}$ in ten dimensions, and what are they
explicitly?

The **count is known: 81** (Hutomo–Lechner–Sorokin,
[arXiv:2509.14351](https://arxiv.org/abs/2509.14351), JHEP 02 (2026) 147;
structural analysis in Cederwall–Hutomo–Kuzenko–Lechner–Sorokin,
[arXiv:2509.14350](https://arxiv.org/abs/2509.14350)).

The **explicit generators are not known.** The literature has only partial
results at orders 4 and 8. That gap is what this repo attacks.

Physics payoff: the most general Lagrangian depending on $F_5$ but not its
derivatives is an arbitrary function of those scalars, which controls
ModMax-type and $T\bar{T}$-like flows for chiral 4-form theories (type IIB).

## Status

| Case | Result |
|---|---|
| 6D generic 3-form (reproduction) | **PASS** — 5 invariants, pattern 1,2,1,1 at orders 2,4,6,8, confirmed under two primes |
| 10D self-dual 5-form, order 4 | **1** independent invariant (all 4 candidate graphs enumerated — complete) |
| 10D, order 6 | not yet run (49 candidate graphs) |
| 10D, order 8+ | not yet run |

## Method

**Candidate generation is a graph enumeration, not a search.** A fully
contracted scalar from $n$ copies of a $p$-form is a perfect matching on the
$np$ index slots, and the induced multigraph has every vertex of valence $p$.
So the complete candidate list at order $n$ is:

> symmetric $n\times n$ non-negative integer matrices, zero diagonal, every row sum $= p$

Two exact pruning rules: no self-loops (a self-contraction of an antisymmetric
form vanishes), and $m_{ij} \le p-1$ for the self-dual case (multiplicity $p$
forces a factor $F\cdot F = 0$). Disconnected graphs are products of lower
invariants and can never raise the rank, so they are dropped.

**Independence is a Jacobian rank, not a search over samples.** Given
candidates $I_a$, the rank of $\partial I_a/\partial A^k$ at one random point
*is* the number of functionally independent invariants. Adding more random
samples cannot raise it; only better candidates can.

$I$ is multilinear in its $n$ vertices, so
$\partial I/\partial A^k = \sum_v [\text{graph with } F \text{ at } v \to P(e_k)]$.
We contract everything except $v$ once (the *amputated tensor*) and take inner
products, costing $n$ einsums per graph rather than $252n$.

**Arithmetic is exact over $\mathbb{F}_p$.** Invariant values span an enormous
dynamic range, so a float SVD forces you to guess a rank tolerance — and that
guess *is* the answer. Over $\mathbb{F}_p$, zero means zero. Every result is
confirmed under a second prime.

## Read this before changing the core

`np.einsum` multiplies **all** operands before summing. At order $n$ the
products reach $p^n$, int64 wraps past $2^{63}$, and **numpy raises nothing** —
you get plausible, confident, wrong numbers. Asking for an optimised path does
not save you: for a symmetric contraction numpy will return a single step
contracting all $n$ operands at once.

This bug appeared three times during development. It produced rank 9 and then
rank 7 for a quantity whose mathematical ceiling is 5. It was only ever caught
by comparing against exact bigint arithmetic.

`mod_einsum` therefore contracts **strictly two operands at a time** with
reduction after every step, plus an explicit overflow guard. Do not replace it
with a bare `np.einsum` call. `tests/test_core.py::test_mod_einsum_matches_exact_bigint`
exists to catch exactly this.

## Run it

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

pytest tests/ -v              # gates. must pass before trusting anything.
python3 scripts/run_6d.py     # reproduction. must print PASS.
python3 scripts/run_10d.py --orders 4 6
```

`run_6d.py` is the gate. If it does not print PASS, every 10D number is
meaningless — fix that first.

## Scope

**Do not expect to reach 81 by enumeration.** Candidate counts at order $n$
grow superexponentially (order 6: 49; order 8: thousands; order 12: ~$10^7$),
and with 81 independent invariants in a 126-dimensional representation the
required orders run well past 20. Five authors published the count rather than
the list; the method does not reach.

Achievable target: complete bases at orders 4 and 6, a serious attempt at
order 8 including reproduction of the five known 8th-order invariants that
appear in $\alpha'^3$ corrections to the type IIB effective action. That
reproduction is the strongest available external validation.

## Layout

```
src/sdinv/modp.py      exact F_p linear algebra, overflow-safe pairwise einsum
src/sdinv/forms.py     p-forms, Hodge dual via index complement, self-dual projector
src/sdinv/graphs.py    valence-regular multigraph enumeration
src/sdinv/contract.py  contraction evaluation, amputated-tensor Jacobian
scripts/run_6d.py      reproduction gate
scripts/run_10d.py     the extension
tests/test_core.py     correctness gates
```

## Open questions for Prof. Ferko

1. Is the per-order breakdown of the 81 written down anywhere? A Hilbert
   series giving the number of primaries at each degree would convert an
   unbounded search into a checklist with a stopping criterion.
2. Order 4 gives exactly 1 independent invariant here. Does that match
   expectations?
3. Is the target a functionally independent set, or a full generating set
   with syzygies? Those differ enormously in difficulty.
