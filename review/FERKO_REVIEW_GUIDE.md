# Review guide

Short, and ordered by how much your judgement is needed rather than by how the
paper is organised.

## The four things most worth your scepticism

### 1. The frame orientation (section on the frame orientation)

The congruence between the split $(5,5)$ oscillator metric and the Lorentzian
$(1,9)$ metric is solved modulo $p$ via a square root, which has two values
differing by an orientation reversal. Orientation flips the Hodge star, which
exchanges the eigenspace the gamma map annihilates.

This was found by a holdout prime failing, misdiagnosed as a $p \equiv 3
\pmod 8$ rule on two examples, and then refuted when $32633$ --- which is
$1 \bmod 8$ --- turned out to need the same branch. **If the pinning
convention is not the one you would choose, the bridge section changes.**

### 2. $\dim_{\mathbb{Q}} D_{10} = 11$

$D_{10}$ is the activated flow closure. The first attempt at this computation
took the raw span of all degree-ten flow targets, got $14$, and would have
reported a quotient of $0$ --- no obstruction at all. The distinction between
the raw span and the activated closure is the whole result.

**The question for you is whether $D_{10}$ as defined is the physically right
object**, not whether the arithmetic is right; the arithmetic is checked two
ways.

### 3. Rank $81$

The count is yours and your coauthors'. What is contributed here is a
certificate: an explicit $81 \times 81$ minor, nonzero at six primes by two
independent determinant routines. **Is that a contribution worth the space the
paper gives it?**

### 4. Degree-eight ablation

Span equality at degree eight holds only with the structured tensor-word
family; the port-graph family alone reaches rank six of seven. Reported as a
property of the candidate family, not of the bridge. **Is that the right
reading?**

## What the paper deliberately does not claim

- degree-twelve tensor--spinor equivalence
- any all-order result
- a complete invariant-ring presentation
- canonicality or uniqueness of any basis
- any physical or type IIB consequence of the flow result
- invention of the enumerate--evaluate--relate method

## Where the numbers come from

Every number in the paper is generated from a JSON certificate at build time.
There are no hand-typed values; the build fails if an artifact is missing. The
reproduction quickstart shows how to regenerate any of them.

## What would change your mind is worth telling us

If a convention is wrong, the affected section is named in the claim ledger
along with what else depends on it.
