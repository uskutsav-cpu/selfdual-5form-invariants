# Claim ledger

Science entry gate: **PASS**. Tests: 466 passed, 0 failed.

| claim | strength | evidence | scope |
|---|---|---|---|
| Generic functional rank is 81 | **certified (lower bound) + analytic (upper)** | 15 cells all rank 81; 81x81 minor nonzero at 6 primes | count is the source literature's; 126-45=81 is analytic |
| Exact equivariant bridge with left inverse | **certified** | bridge_validation.json at two primes; span equalities, not dimensions | - |
| Orientation is pinned by construction | **certified** | 11 primes, all 4 residue classes, independent verifier | - |
| Degree 4,6,10 span equality | **certified** | common-sample comparison, holdout validated | - |
| Degree 8 span equality | **certified** | rank 7 both sides; tensor-word family load-bearing | property of the family |
| dim_Q A10 = 14 | **proved** | structural: basis vectors are the coordinate system | - |
| dim_Q D10 = 11 | **proved** | exact rational closure; 11x11 minor below, 3 annihilators above | seed closure |
| dim_Q Q10 = 3 | **proved** | constructed: representatives independent, spanning, each needed | - |
| dim B10 = 12 | **certified at the tested primes only** | solved mod p; no rational solve exists | 12 <= dim_Q B10 <= 14 |
| dim(B10 cap P10) = 1 | **certified at the tested primes only** | inherits B10's gap | - |
| Degree-12 equivalence | **NOT CLAIMED** | no spinor-side enumeration exists | excluded |
| Any physical / type IIB consequence | **NOT CLAIMED** | PO-07 open: field redefinitions untested | withheld |

## Words that are not licensed anywhere in the paper

`first`, `unique`, `canonical`, `exhaustive`, `previously unknown`, `all orders`, `syzygy`

## Prior art

The enumerate-evaluate-relate workflow is Elamaran, Ferko and Scarlett, PRD 114 (2026) 026016. The paper claims only its exact and certified realisation for the ten-dimensional self-dual five-form.
