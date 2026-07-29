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

The degree-by-degree partition function is also known through order 22. In
particular,

> $P(t)=1+t^4+2t^6+7t^8+\cdots
> =(1-t^4)^{-1}(1-t^6)^{-2}(1-t^8)^{-6}\cdots$.

Thus there is one quartic generator, two sextic generators, and six octic
generators; the seventh degree-8 scalar is the product $I_4^2$. The literature
gives a tensor basis for the octic generators. This repo supplies an explicit
contraction-graph basis and independently checks its Jacobian rank.

Physics payoff: the most general Lagrangian depending on $F_5$ but not its
derivatives is an arbitrary function of those scalars, which controls
ModMax-type and $T\bar{T}$-like flows for chiral 4-form theories (type IIB).

## Status

| Case | Result |
|---|---|
| 6D generic 3-form (reproduction) | **PASS** — 5 invariants, pattern 1,2,1,1 at orders 2,4,6,8, confirmed under two primes |
| 10D self-dual 5-form, order 4 | **1** independent invariant (all 4 candidate graphs enumerated — complete) |
| 10D, order 6 | **2** new independent invariants, running rank **3 / 81** (49 exact graph classes) |
| 10D, order 8 | **6** new independent invariants, running rank **9 / 81** (1,689 exact graph classes; complete under two primes) |

Artifacts:

- [`results/10d_order8.json`](results/10d_order8.json) — the nine graph
  generators, two-prime rank logs, and completeness claim.
- [`results/10d_graph_catalog.json`](results/10d_graph_catalog.json) — all
  4, 49, and 1,689 exact isomorphism classes at orders 4, 6, and 8.
- [`results/10d_baseline.json`](results/10d_baseline.json) — the original
  order-4/order-6 baseline.

### The six order-8 graph generators

`nij^m` means that tensor copies `i` and `j` share `m` contracted indices.
Every omitted pair has multiplicity zero.

| ID | Exact contraction graph |
|---|---|
| $I_{8,1}$ | `n8[04^4,05^1,14^1,16^4,25^4,27^1,36^1,37^4]` |
| $I_{8,2}$ | `n8[03^4,06^1,14^4,16^1,25^4,26^1,37^1,47^1,57^1,67^2]` |
| $I_{8,3}$ | `n8[03^4,04^1,14^1,15^1,16^2,17^1,25^4,26^1,37^1,46^1,47^2,67^1]` |
| $I_{8,4}$ | `n8[03^2,06^2,07^1,14^4,16^1,25^4,26^1,36^1,37^2,47^1,57^1]` |
| $I_{8,5}$ | `n8[03^2,04^1,06^2,14^2,15^1,17^2,25^4,26^1,36^2,37^1,47^2]` |
| $I_{8,6}$ | `n8[03^2,06^2,07^1,14^2,15^1,16^2,24^1,25^2,27^2,36^1,37^2,45^2]` |

These six Jacobian rows add six directions to the quartic/sextic basis under
both primes 32749 and 32719. This meets the published upper bound of six new
octic generators, so the list is complete. The remaining degree-8 scalar is
the disconnected product $I_4^2$.

### Exact order-8 enumeration

The catalog is generated with nauty 2.9.3:

```bash
geng -cq 8 | multig -q -T -m4 -r5
```

`geng` emits each connected underlying simple graph once. `multig` assigns
edge multiplicities, enforces degree 5 and maximum multiplicity 4, and
suppresses isomorphic weighted outputs. The result is exactly **1,689**
connected candidates. `pynauty` supplies an independent exact certificate in
the tests; no Weisfeiler-Lehman hash is used for correctness.

### Why the tests use a boost, not just a rotation

`test_10d_contractions_survive_a_lorentz_boost` applies a genuine SO(1,9) element.
This is deliberate: if raised/lowered indices are assigned **per tensor copy**
rather than **per contracted edge**, an edge joining two same-placement vertices
contracts with $\delta$ instead of $\eta$. A pure rotation cannot see that error —
$\delta$ and $\eta$ agree on the spatial block — so the quantity looks invariant
and is not. A boost mixes the timelike direction and exposes it immediately.
Any candidate that changes value under a boost is not an invariant, whatever a
rank count says.

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

**Independence is a Jacobian rank.** Given candidates $I_a$, the generic rank
of $\partial I_a/\partial A^k$ is the number of functionally independent
invariants. A uniformly random point over a large finite field attains that
generic rank with high probability. The complete order-8 basis is recomputed
under a second prime to guard against an unlucky specialization.

$I$ is multilinear in its $n$ vertices, so
$\partial I/\partial A^k = \sum_v [\text{graph with } F \text{ at } v \to P(e_k)]$.
The production code contracts the tensor network once and reverse-
differentiates its globally optimized contraction tree, reusing intermediates
for all vertices. A separate amputated-tensor implementation remains as a
correctness oracle in the tests.

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
reduction after every step, plus an explicit overflow guard. Large pairwise
contractions use float64/BLAS only when every unreduced integer sum is proven
to stay below $2^{53}$, so the result remains exact. Do not replace this with a
bare multi-operand `np.einsum` call.

## Run it

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

pytest tests/ -v              # gates. must pass before trusting anything.
python3 scripts/run_6d.py     # reproduction. must print PASS.
python3 scripts/run_10d.py    # orders 4, 6, 8 under both primes
```

`run_6d.py` is the gate. If it does not print PASS, every 10D number is
meaningless — fix that first.

The exact catalog is committed. To regenerate it, install
[nauty](https://pallini.di.uniroma1.it/) so `geng` and `multig` are on `PATH`,
then run:

```bash
python3 scripts/generate_graph_catalog.py
```

## Scope

The repository is now complete through order 8. It does **not** claim to have
all 81 functionally independent invariants: the partition function has 12 new
generators at order 10 and 62 at order 12, and candidate graph counts grow
superexponentially. Extending this explicit graph basis beyond order 8 remains
open.

## Layout

```
src/sdinv/modp.py      exact F_p linear algebra, overflow-safe pairwise einsum
src/sdinv/forms.py     p-forms, Hodge dual via index complement, self-dual projector
src/sdinv/graphs.py    exact multigraph certificates, nauty generation, catalogs
src/sdinv/contract.py  contraction evaluation, optimized reverse-mode Jacobian
scripts/run_6d.py      reproduction gate
scripts/run_10d.py     two-prime complete computation through order 8
scripts/generate_graph_catalog.py  exact nauty catalog generation
tests/test_core.py     correctness gates
```

## Next questions

1. What is the explicit change of basis between these six graph contractions
   and the six tensor expressions in arXiv:2509.14350v2?
2. Which graph topologies give the most efficient order-10 basis?
3. At what degree do the first nonlinear relations among the published
   generator counts appear?
