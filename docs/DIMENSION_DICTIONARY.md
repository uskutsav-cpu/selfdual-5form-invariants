# Degree-10 dimension dictionary

Every number below dimensions a *different* object. Several are numerically
equal, and at least one apparent agreement is **unverified**.

## 1. The numbers

| n | dimensions what | grading | arithmetic | source |
|---:|---|---|---|---|
| **126** | components of a self-dual 5-form in D=10 | — | exact | analytic |
| **45** | dim SO(1,9) | — | exact | analytic |
| **81** | generic **functional** dimension = 126 − 45 | cumulative, all degrees | analytic; float64 numerically | **literature** (analytic); spinor Jacobian is a *check* |
| **14** | degree-10 **atlas**: polynomial invariants of F-degree 10 | graded, degree 10 | exact modular | trace repo |
| **12** | **published-candidate span** inside that 14 | graded, degree 10 | exact modular | trace repo |
| **12** | **primitive** (non-product) generators at degree 10 | graded, degree 10 | float64 | spinor `m_10` / `selected_new` |
| **2** | **product** directions at degree 10 | graded, degree 10 | float64 | spinor `product_rank` |
| **11** | **reachable closure** D10 (stress-flow generated) | graded, degree 10 | exact modular | trace repo |
| **3** | **Q10 = atlas / D10** | graded, degree 10 | exact modular | trace repo |

## 2. Two different splittings of the same 14

    14 = 12 + 2      published-candidate span    +  complement      (trace)
    14 = 12 + 2      primitive generators        +  products        (spinor)
    14 = 11 + 3      reachable closure D10       +  quotient Q10    (trace)

The third line is **unrelated** to the first two. `Q10 = 3` is a quotient by the
*stress-flow reachable* subspace, not by products. Nothing about `Q10` follows
from the primitive/product decomposition, and the word "independent" must never
be used for both.

## 3. An UNVERIFIED agreement — do not assert it

Lines 1 and 2 both read `12 + 2`, and it is tempting to say the published
candidates span exactly the primitive part. **That has not been computed.**

The trace side has never computed its product subspace at degree 10
separately; the earlier report recorded `PRODUCT RANK / PRIMITIVE RANK: not
computed`. So it is not known whether the 12-dimensional published span
coincides with a 12-dimensional primitive complement, or merely has the same
dimension. If the published span contained even one product direction, its
primitive content would be 11, not 12, and the agreement would be coincidental.

**Required before any manuscript claim of correspondence**: compute the
degree-10 product subspace on the trace side (products of the degree-4 and
degree-6 invariants) and test containment against the published span. Until
then the permitted statement is:

> The trace-side published-candidate span and the spinor-side primitive count
> are both 12-dimensional at degree 10. Whether they are the same subspace has
> not been determined.

## 4. Words that are banned without a qualifier

| word | must be qualified as |
|---|---|
| rank | atlas rank / published rank / quotient rank / Jacobian rank |
| independent | linearly independent / functionally (algebraically) independent |
| primitive | non-product generator (spinor grading) — **not** "published candidate" |
| dimension | of which space, at which degree, cumulative or graded |
