# Status against the JHEP execution specification

Specification: `JHEP_Full_Completion_Execution_Prompt.pdf`
(sha256 `18963027c30967799a807a7097296d0c…`, 30 pages, prepared 2026-07-31).

## Workstream status

| WS | subject | status |
|---|---|---|
| **A** | exact trace-side degree-10 result | **COMPLETE** |
| **B** | product / primitive / reachable decomposition with incidence certificates | **COMPLETE** |
| C | trace reproducibility, clean clones, additional primes, rational reconstruction | partial — 199 tests + clean clone done at an earlier commit; additional primes and reconstruction NOT done |
| D | spinor baseline audit | **COMPLETE** (commit `b70bf33`) |
| E | rank-81 numerical certification | partial — two archived Jacobians analysed and the degenerate one diagnosed; the 5-seed x 3-scale x 3-step matrix NOT run |
| F | degree-10 spinor no-stop | NOT started |
| G | signature / complexification argument | NOT started |
| H | gamma bridge | NOT started (depends on G) |
| I | spinor-trace common-sample comparison | NOT started (depends on H) |
| J | physics interpretation | NOT started |
| K | manuscript, figures, tables, bibliography, private package, mock review | NOT started |

## Workstream A — complete

Atlas `A10` dim 14; published span `B10` dim 12; reachable closure `D10` dim 11;
quotient `Q10` dim 3; pure-`N4125` basis certified with explicit round-tripped
formulas; reverse recovery rank 3/3 with span equality against Level-A and
published bases; 199 tests passing.

## Workstream B — complete, and it overturned a tempting claim

    P10 = span(I4_1*I6_1, I4_1*I6_2)          dim 2, the only degree-10 products
    dim(B10 cap P10) = 1,  dim(B10 + P10) = 13

So the published span carries one product direction: its primitive content is
**11, not 12**, and the `12 = 12` match with the spinor primitive count is
dimensional coincidence.

The correspondence that IS structural:

    P10 cap G10 = 0,  P10 + G10 = 14   ->   A10 = G10 (+) P10   (12 + 2)

with `G10` the span of the twelve graph generators. Also verified:
`P10 subset D10`, so products contribute nothing to `Q10`.

Certificates: `degree10_published_product_intersection.json`,
`degree10_space_incidence.json`. Regression test:
`test_published_span_is_not_a_primitive_complement`.

## Exact resumption order

The specification's dependency chain makes **G** the critical path: H depends on
G, I depends on H, and the manuscript's cross-validation sections depend on I.
**E** and **F** are independent of that chain and can proceed in parallel.

1. **G** — complexification/real-form argument. The mathematical content is
   fixed and known: `so(10,C)` has both `Spin(10)` and `Spin(1,9)` real forms;
   the 126 is the gamma-traceless symmetric chiral square in both; `*^2 = +1`
   in Lorentzian signature admits a real self-dual 5-form while `*^2 = -1` in
   Euclidean does not, so the spinor implementation must be read as
   complexified or as carrying imaginary self-duality. Dimensions are
   comparable over `C`; component comparisons need a chosen real form.
2. **E** — Jacobian matrix over seeds/scales/steps, never normalising a row
   below the declared noise floor.
3. **F** — degree-10 spinor no-stop, streamed, with terminal status per
   candidate.
4. **H**, **I**, then **J**, **K**.
