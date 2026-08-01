# Priority and overlap

## Overlap with the source papers, stated without hedging

This work is downstream of arXiv:2509.14350 and arXiv:2509.14351. It uses their
problem, their twelve degree-ten expressions, their stress-flow construction and
their count of 81. It does not re-derive any of those and does not claim them.

What it adds is structural and computational: the dimension of the degree-ten
space, a certified basis, the complete incidence of its natural subspaces, the
quotient by the reachable subspace with explicit representatives, and an exact
machine-checked bridge to the spinor description.

## The one result that is a correction rather than an addition

The degree-ten published span was widely expected --- including by us, in an
earlier draft of our own notes --- to be a complement to the products. It is
not. We record this prominently because a reader who assumes otherwise will
mis-assign the primitive content of the published structures by one dimension.

## Independence of implementation

The tensor and spinor implementations were written separately and neither
imports the other; this was verified by grep in both directions. That is
**implementation independence**, not clean-room independence: no protocol
prevented shared assumptions, and the same person had access to both. The
manuscript says so.

## Priority posture

No priority claim is made anywhere in the manuscript. If a coauthor's literature
knowledge shows that any result here has an earlier appearance, the affected
statement is a citation, not a retraction, because none of the claims is phrased
as a priority claim.
