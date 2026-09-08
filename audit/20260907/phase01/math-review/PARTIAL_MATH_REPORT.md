# Partial independent mathematics audit — stopped on cross-audit discrepancy

Frozen commit: `2b7663bbf5a06d1340973434f195a84ae2773e8f`.

All input files came from the newly created immutable `../checkout`. No
previous workspace, previous audit material, old environment, checkpoints,
or cached computational results were used. All scripts and results in this
directory were created for this audit. Scientific executions used the new
`../environment/bin/python` and the parent audit command recorder.

**Status: PARTIAL / STOPPED.** The parent instructed this branch to stop when
the source-transcription reviewer reported discrepancies in frozen degree-ten
literature formulas. No scientific process was running in this branch at the
stop message, and no scientific computations were started thereafter. The
reported source discrepancy was not investigated by this branch. The completed
checks below do not constitute a completed release audit or approval.

## Completed independent integer determinant calculation

`bareiss_minors.py` imports only Python standard-library modules. It imports
neither `RankSieve`, `determinant_mod`, any certificate verifier, nor any other
repository module. It selects the advertised 81 columns from each stored
81-by-126 Jacobian, lifts every residue to a Python integer, computes the
full integer determinant by fraction-free Bareiss elimination, checks the
remainder of every exact division, and reduces only the final determinant.
Small independent determinant cases check a required row swap, a singular
matrix, and a 3-by-3 determinant before examining the certificate.

| Prime | Seed | Integer determinant digits | Row swaps | Computed residue | Expected residue | Result |
|---:|---:|---:|---:|---:|---:|---|
| 32749 | 20260907 | 384 | 0 | 20345 | 20345 | PASS |
| 32749 | 20260908 | 382 | 0 | 30761 | 30761 | PASS |
| 32719 | 20260907 | 383 | 0 | 1653 | 1653 | PASS |
| 32719 | 20260908 | 383 | 0 | 2167 | 2167 | PASS |

Every advertised pivot list was exactly the first 81 columns, with no duplicate
columns; every Jacobian had the expected shape and reduced integer entries.
`bareiss_results.json` retains each complete integer determinant, the input
certificate SHA-256, the selected columns, and elapsed times. This is an
independent check of the **stored matrices**. It does not by itself establish
that those stored entries are derivatives of the graph polynomials.

Execution evidence: `../commands/math_bareiss_minors/command.json`,
`stdout.log`, and `stderr.log`. Exit 0; recorded runtime approximately 2.331 s.
The command recorder gives stdout SHA-256
`63c20c31e82cd89144c2f71a50b050f0d0a86808a873ebdc97798377f143a711`;
stderr is empty.

## Completed convention and ordered-graph audit

`independent_conventions.py` imports no repository modules. It implements
permutation parity by counting inversions, builds Hodge-complement directions
directly, reconstructs adjacency and Einstein formulas independently from the
ordered edge lists, and compares those reconstructions with the frozen data.

The metric is `diag(-1,+1,...,+1)`, so signature `(1,9)` counts one negative
and nine positive directions. For increasing input index set `I`, its sorted
complement `J`, and lower-index epsilon with `epsilon[0,...,9]=+1`, the code's
explicit output-first Hodge convention is

\[
\star e_I = \operatorname{sgn}(J,I)\left(\prod_{i\in I}\eta^{ii}\right)e_J.
\]

Applying it twice gives the product of two block-parity signs and the ten
metric signs. Interchanging the two blocks of length five gives
`(-1)^(5*5)=-1`, while the metric product is `-1`; hence
`star^2=(-1)^(25+1)=+1`. This conclusion is tied to that explicit Hodge and
epsilon convention; the abstract words “self-dual” alone do not specify the
epsilon ordering. The script verifies all 252 complementary index pairs
directly over the integers.

There are `C(10,5)=252` compact alternating components. Complementation has
no fixed five-element index set, so it partitions them into 126 pairs. Each
pair supplies one eigenvector for each eigenvalue `+1` and `-1` in
characteristic unequal to two. The time-containing representatives number
`C(9,4)=126`. For each such `I`, `e_I + star(e_I)` has component 1 at `I`, one
component `+1` or `-1` at its complement, and zero elsewhere. Thus the upper
126-by-126 block of the 252-by-126 direction matrix is the identity. The
matrix has only `0,1,-1` entries, is self-dual column by column, and gives
the exact coordinates `A_I=F_I` without a projector factor of `1/2`.

The independently generated direction-matrix digest matches the certificate:
`e1a48f2071670fce31d7694eeddf091caffec94dec1056aba52468c39f930bb8`.
`independent_integral_directions.json` contains that newly generated matrix.
All four independently reconstructed 252-component forms equal their frozen
`selfdual_components` arrays. Their fully contracted quadratic norms vanish
modulo the corresponding prime. Their 81 saved Jacobian rows each satisfy
Euler's homogeneous-polynomial identity, checked with Python integers.

All 81 selected graphs pass the following checks:

- Exactly the ordered degree inventory `4:1, 6:2, 8:6, 10:12, 12:60`.
- Ordered, nonrepeated edge records with `0 <= i < j < n` and multiplicity
  from 1 through 4, hence no loops.
- Adjacency reconstructed from those records exactly equals the stored
  matrix; every row sum is five and each graph is connected.
- Exactly `5*n/2` contracted edges, each represented by one upper and one
  lower occurrence in the reconstructed formula.
- The independently reconstructed ordered Einstein formula equals the
  frozen formula byte for byte, and the ordered edge-record digest equals
  the stored formula digest.

An all-covariant representation of such a graph is

\[
\sum_{\{a_e\}}\prod_v F_{a_{e(v,1)}\ldots a_{e(v,5)}}
                  \prod_e\eta^{a_e a_e}
\]

for this diagonal metric. There is precisely one inverse metric per edge.
Equivalently, one endpoint index is raised and the other remains lowered.
The frozen printed formulas raise incoming indices at the larger-numbered
endpoint; the production contraction implementation attaches signs to the
opposite endpoint. These yield the same scalar because the diagonal metric
sign is multiplied exactly once on the same shared dummy index. Attaching a
metric to both ends would square its sign and change the contraction. Assigning
uniform variance to entire vertices would not implement mixed-variance
vertices in general. Under a metric-preserving change of frame, contracted
transformation matrices cancel pairwise; this is the algebraic Lorentz-scalar
argument. This branch did **not** perform a fresh numerical boost test before
the stop instruction.

The script explicitly counts all 120 permutations of five slots: 60 even and
60 odd. A slot permutation multiplies the alternating tensor by its parity.
Swapping blocks of respectively `r` and `s` slots contributes `(-1)^(r*s)`;
swapping two complete five-slot blocks gives `-1`. Reordering whole scalar
tensor factors in a product is commutative and introduces no separate sign;
the potential sign in a graph relabeling comes from the induced slot
permutations, whose parities must be multiplied over vertices. Consequently
an unsigned graph-isomorphism class does not alone identify the signed ordered
formula. This branch checked the supplied ordered formulas, but did not finish
an independent numerical test of graph-relabeling signs or enumerate graph
automorphism sign characters before the stop.

Self-loops vanish because a symmetric metric contracted against two slots of
one alternating tensor is zero. In a five-valent graph, an edge of multiplicity
five isolates its two vertices as a full quadratic contraction. On the chosen
self-dual odd-degree space the complementary pair terms in that norm cancel;
the four direct norm evaluations are consistent with this elementary argument.

Execution evidence: `../commands/math_conventions/command.json`, stdout and
stderr. Exit 0; runtime approximately 0.456 s; stdout SHA-256
`0e515184c6789578d85ec6fa8c9de3bc2c337fcce27b1444bef37679c8700e7f`.
Detailed newly computed results are in `conventions_results.json`.

## Independent value/derivative oracle — written and profiled, NOT executed

`independent_oracle.py` is a newly written candidate oracle with no `sdinv`
imports. It independently expands the form and a direction using the
inversion-count Hodge construction. It places metric signs at the incoming
endpoint, matching the printed formulas and independently of the production
tail-sign choice. It asks `opt_einsum` only to select a contraction path;
the tensor arithmetic is its own reshaping and binary matrix contractions.
It propagates `F + epsilon*dF`, `epsilon^2=0`, forwards, so its derivative
method is structurally different from the production reverse-mode Jacobian.

The intended arithmetic argument is that every input is a nonnegative integer
residue, every binary dot has at most `K` terms, and the maximum unreduced sum
`K*(p-1)^2` stays below `2^53`. Such integer products and partial sums are
exactly representable by float64. Reduction is performed after every product
and every derivative addition. The candidate includes explicit bounds and
planned Python-bigint comparisons, but those arithmetic self-tests are in
the evaluation branch and **were not run**.

Only `--profile` ran. Its estimates over all 81 graphs at one cell were:

- 503,449,599,000 forward-dual scalar multiplication terms.
- Largest three-output-array allocation estimate: 240,000,000 bytes.
- Largest bounded unreduced integer dot: 107,243,150,400,000, below `2^53`.

The three-array figure is not an RSS bound; operands, reshaped copies,
intermediates, Python, and library memory require additional space. The parent
was coordinating one heavy evaluator process alongside other tests. No oracle
graph values, directional derivatives, full gradients, fresh-point rank, or
permutation checks were evaluated before stop. Therefore the candidate oracle
must not be described as validated or as an independent pass of the stored
Jacobian.

Profile evidence: `../commands/math_oracle_profile/`, exit 0; stdout SHA-256
`dfe1ffd3471cc083c55b96c442f7c88192541d467a74763b1513a7946b7c4de5`.
`oracle_profile.json` preserves newly generated paths and per-graph estimates.

A genuinely fresh coordinate seed was generated after the freeze immediately
before the stop: prime 32749, seed `9726505986870736088`, generated by
`secrets.randbits(64)` and used with Python `random.Random(seed)` to draw
126 `randrange(prime)` coordinates. `fresh_point.json` records all coordinates,
the generator description, and creation timestamp. This point has **not** been
evaluated. Its generation command is captured in
`../commands/math_fresh_point/`, exit 0, stdout SHA-256
`e8392596b184e24b75b28dbc7bee3eeb236ff9a52aa9cfa2c401129e89b444fa`.

## Reproduction and provenance notes

To rerun either completed computation in a separately authorized continuation,
choose a new unique command name, because the recorder prevents overwriting:

```sh
python3 ../run_command.py --name math_bareiss_rerun_UNIQUE --cwd "$PWD" -- ../environment/bin/python bareiss_minors.py
python3 ../run_command.py --name math_conventions_rerun_UNIQUE --cwd "$PWD" -- ../environment/bin/python independent_conventions.py
```

These examples assume the working directory is this `math-review` directory.
They are documentation only and were not executed after the stop.

The initial bootstrap inventory was a plain `ls -la` of the newly created audit
root before using the recorder. It read no checkout file contents. This was
immediately disclosed to the parent. The parent clarified that plain inventory
and fresh-log reads are permitted; recursive wrapping of log reads is not
required. Scientific computations and the fresh-point generation were all
recorded. Fresh source-inspection commands are captured under
`math_initial_inspect`, `math_schema_inspect`, `math_read_conventions`, and
`math_convention_source_details`. No frozen file was edited.

Remaining work, requiring a resumed audit after the discrepancy is resolved:
execute and validate the independent oracle; compare all 81 values and
directional derivatives with independently obtained production derivatives at
the fresh point; perform fresh graph-relabeling sign checks and numerical
Lorentz transforms; and complete any parent-assigned remaining certificate
recomputation. No statement here upgrades those unperformed checks to PASS.
