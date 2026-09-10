# Referee A — invariant theory

## A1. "Functional rank 81 is not algebraic independence of 83 candidates."

Correct, and the paper says so in the same breath as the number: 83 candidates
of rank 81 means the selection carries functional **dependencies**. A wording
gate fails the build on any phrasing asserting independence of all 83.

**Resolved.** No change needed; the statement was already the narrow one.

## A2. "A modular rank is not a characteristic-zero rank."

Accepted, and it is why the paper separates four things that a reader could
otherwise conflate: rank at one modular sample, the characteristic-zero lower
bound, the generic characteristic-zero rank, and algebraic independence.

The lower bound is unconditional because the coordinate basis is integral, so the
Jacobian is an integer reduction and `rank_{F_p} <= rank_Q`. The matching upper
bound `126 - 45 = 81` is **analytic and from the literature**, cited, and not
claimed here. Both are documented, which is the condition under which the generic
value may be stated.

**Resolved.**

## A3. "The quotient construction could be an artefact of the basis."

The dimensions of `A10`, `B10`, `G10`, `P10` are pinned over `Q` by counting
spanning sets — a modular rank equal to the size of an explicit spanning set
forces the dimension with no prime excluded. `D10` is not of that form and was
the one exposed number; it is now settled by an exact rational closure with a
CRT lift validated at a held-out prime and an explicit non-vanishing `11 x 11`
integer minor.

**Resolved**, and it was not resolved when this objection would first have been
raised — the referee is right that it needed doing.

## A4. "Minimality and completeness language."

Four properties are separated and only one is claimed:

| property | status |
|---|---|
| cardinality minimality, any basis | **proved** — a span of `k` vectors has dimension at most `k` |
| removal minimality | open, shown in the fixed basis and under relabellings only |
| minimality under arbitrary `GL` | open, not attempted |
| uniqueness / canonicality | **not claimed**; a gate blocks unscoped "canonical" |

**Resolved by delimitation**, which is the honest outcome rather than a proof.

## A5. "Is the degree-ten enumeration exhaustive?"

No, and the paper never says it is. Degrees 4, 6 and 8 terminate on candidate
exhaustion **within a declared candidate grammar**; degree ten has no terminal
status and the paper says "saturation", never "exhaustion". A gate requires the
word "exhaustive" to appear only adjacent to an explicit denial.

**Resolved by delimitation.**

## Verdict

No fatal objection. A3 was a genuine gap and is closed; the rest were already
scoped correctly, which is what the wording gates are for.
