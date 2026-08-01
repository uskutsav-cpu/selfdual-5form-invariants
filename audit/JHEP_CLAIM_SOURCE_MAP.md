# Claim to source map

Built 2026-08-01T19:46:32+00:00 by `scripts/build_jhep_source_corpus.py`.

Read the third column first. It says whether the statement is the
literature's or this paper's, which is the only thing that governs how the
manuscript is allowed to phrase it.

| statement | sources | provenance |
|---|---|---|
| A ten-dimensional self-dual five-form has 81 functionally independent Lorentz invariants. | `Hutomo:2025chiral` (2509.14351), `Cederwall:2025invariants` (2509.14350) | FROM THE LITERATURE. The count is theirs. This paper supplies a machine-checkable lower bound matching it, not the count. |
| 126 - dim so(1,9) = 126 - 45 = 81 bounds the generic functional rank from above. | `Cederwall:2025invariants` (2509.14350) | FROM THE LITERATURE, analytic. No computation here supplies it. |
| The problem of an explicit invariant basis in D = 10 is open and hard. | `Cederwall:2025invariants` (2509.14350) | FROM THE LITERATURE. Stated by the source as an open problem; must not be presented as this paper's observation. |
| Stress-flow universality of D = 4 and D = 6 does not carry over to D = 10. | `Hutomo:2025chiral` (2509.14351), `Ferko:2024interacting` (2402.06947) | FROM THE LITERATURE, qualitatively. The exact codimension is not in the source. |
| Enumerate contraction graphs, evaluate on sample points, and read off functional dependencies from a rank. | `Elamaran:2025machine` (2512.23750) | METHOD PRIOR ART. This paper's contribution is the exact and certified form -- integral basis, modular arithmetic, holdout primes, characteristic-zero lower bound -- not the approach. |
| A nonzero value at one sample point certifies a polynomial is not identically zero. | `Schwartz:1980` (10.1145/322217.322225), `Zippel:1979` (10.1007/3-540-09519-5_73) | STANDARD. Cited for the argument, not claimed. |
| Exact canonical forms for the invariant graphs. | `McKay:2014nauty` (1301.1493) | STANDARD TOOL, used through pynauty; cited as the algorithm. |
| An independent fraction-free determinant confirms the 81x81 minor. | `Bareiss:1968` (10.1090/S0025-5718-1968-0226829-0) | STANDARD ALGORITHM. Cited for the second routine. |
| Majorana-Weyl spinors exist in signatures (1,9) and (5,5). | `Kugo:1982bn` (10.1016/0550-3213(83)90584-9), `VanProeyen:1999ni` (hep-th/9910030) | STANDARD. Cited for the conventions used in appendix A. |
| A ten-dimensional self-dual five-form is a field of Type IIB supergravity. | `Sen:2015covariant` (1511.08220), `Paulos:2008tn` (0804.0763), `Liu:2022eight` (2205.11530), `Adhikari:2026typeiib` (2603.18248) | CONTEXT ONLY. This paper computes no Type IIB correction. |
| Causality and hyperbolicity constrain nonlinear self-dual theories. | `Russo:2024causal` (2401.06707), `Russo:2025chiral2form` (2504.01467), `BabaeiAghbolagh:2026classifying` (2602.03426) | CONTEXT AND LIMITATION. All in D = 4 or D = 6; no D = 10 causality theorem is proved here. |
| The exact equivariant tensor-spinor bridge, its left inverse, and degree-resolved span equality. | -- | NO SOURCE FOUND. Candidate contribution of this paper; the analytic correspondence is classical, the exact executable map and its certificates appear to be new. See audit/JHEP_NOVELTY_MATRIX.md. |
