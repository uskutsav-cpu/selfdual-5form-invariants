# Live authoritative state

Verified at the start of the final claim-closure pass, from the repository
and the remote — not from the goal's reported values. Machine-readable:
`audit/JHEP_FINAL_AUTHORITATIVE_STATE.json`.

## Reconciliation

| | |
|---|---|
| branch | `research/maximal-chiral-four-form-program` |
| local commit | `69d8d0d8b0af` |
| remote commit | `69d8d0d8b0af` |
| diverged | no |
| ahead/behind | `0	0` |
| untracked files | 0 |
| tags | 7 |

The goal reported HEAD as `035b772`. That was **not** current: the branch
had advanced. The reported value was not assumed and the live one is used
throughout.

## Single authoritative writer

Active writers: **1** (pid 79189)

Counted with `pgrep -f` on the script names. A first attempt reported 8 and
was wrong: it ran `ps aux | grep` inside `bash -lc`, where the shell's own
command line matched the pattern. The bracketed-grep idiom protects against
self-matching only when the pattern is not passed through another shell.
This is recorded because an inflated writer count would have triggered a
pointless kill of the one legitimate job.

No two processes share a row cache, a result JSON, a test log, a checkpoint
directory or the generated macro file. Earlier in this project two did —
two rank-81 runs against one row cache, and two test runs against one log —
and the second was discarded rather than trusted.

One `pytest` process belonging to a **different repository**
(`mp5d-symmetry-exceptional-topology`) and a different session was observed
running concurrently. It shares no artifact with this repository, so it does not
violate the single-writer requirement, and it was **not killed** — it is not this
session's to terminate. It does compete for CPU, which is the reason the
clean-clone suite ran slowly rather than any fault in the suite.

## Artifact hashes at this state

| artifact | sha256 |
|---|---|
| `manuscript/generated/numbers.tex` | `367bdbdd17d0c9e8...` |
| `results/rank81/certificate.json` | `6acecda746fd9490...` |
| `results/rank81/minor81_certificate.json` | `745f36b55427656e...` |
| `results/stress_flow/D10_characteristic_zero.json` | `aebf38967d08f9b1...` |
| `results/stress_flow/Q10_characteristic_zero.json` | `17b7e6c6f5313d4e...` |
| `spinor_trace_bridge/results/bridge_validation.json` | `93db9f8af7c6f25d...` |
| `submission_candidate/arxiv_source.tar.gz` | `27023fc0cf91267e...` |
| `submission_candidate/compiled_manuscript.pdf` | `890b3ca366d8f592...` |
| `submission_candidate/jhep_source.zip` | `7d22e8836d70f176...` |
| `verification/degree8_span_equality.json` | `9100d557a4189185...` |
| `verification/spinor_trace_comparison.json` | `a3ea0bf9448e65f9...` |

## Releases already public

Seven tags exist and five GitHub releases are already published, on
explicit instruction earlier in the project. This constrains what
"approval before release" can still mean: the code and certificates are
already visible. What remains genuinely unreleased is the arXiv posting,
the journal submission and the DOI.
