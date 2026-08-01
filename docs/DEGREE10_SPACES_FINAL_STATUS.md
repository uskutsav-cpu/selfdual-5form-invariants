# Degree-10 subspaces --- final status

Generated 2026-08-01T21:31:07+00:00 by `scripts/emit_degree10_space_status.py`.

## Summary

| space | modular | exact over Q | status |
|---|---|---|---|
| A10 | 14 | 14 | PROVED |
| G10 | 12 | 12 | PROVED |
| P10 | 2 | 2 | PROVED |
| D10 | 11 | 11 | PROVED |
| B10 | 12 | **not established** | CERTIFIED AT THE TESTED PRIMES; NOT PROVED OVER Q |
| B10 ∩ P10 | 1 | **not established** | CERTIFIED AT THE TESTED PRIMES; NOT PROVED OVER Q |

## Why three of these need no computation

A10, G10 and P10 are spans of *distinct standard basis vectors* in atlas
coordinates --- all fourteen, the twelve graph generators, and the two lower
products respectively. A set of k distinct unit vectors has rank k over any
field. Their dimensions are therefore structural: no prime enters, and no
prime can be exceptional. Reporting them with a modular caveat would have
been a caveat about nothing.

## Why B10 is different

B10 is the span of the published equation-(4.24) candidates, and each
candidate's coordinate vector is *recovered* by solving a linear system
against a design matrix mod p. The coefficients are modular objects. There
is no rational solve, because the atlas evaluators are modular, so:

- `dim_Q B10 >= 12`, since rank over F_p bounds rank over Q from below
- `dim_Q B10 <= 14`, since B10 is a subspace of A10

and nothing between them is established. Closing it needs a rational
evaluator for the atlas elements, which does not exist in this package.

## The intersection

`dim(B ∩ P) = dim B + dim P - dim(B + P)` needs all three dimensions over Q.
`dim_Q P10 = 2` exactly, but `dim_Q B10` is only bounded, so the
intersection inherits the gap. Its modular value is 1, consistent
across 2 primes, and that is what may be stated.

## Consequence for the manuscript

> A10, G10, P10 and D10 may be stated as exact characteristic-zero dimensions. B10 and B10 ∩ P10 must carry 'at the tested primes' wherever they appear.

