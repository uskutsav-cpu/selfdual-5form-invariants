# Objection–response matrix

| id | objection | grade | resolution | evidence | manuscript location | status |
|---|---|---|---|---|---|---|
| M1 | not physics | major | reframed around the stress-flow deficit; four concrete enabled calculations | `docs/WHAT_THE_CLASSIFICATION_ENABLES.md` | sec. 12 | addressed; residual risk acknowledged |
| M2 | modular ≠ char 0 | major | lower/upper directions separated; integral basis makes the lower bound unconditional | `sdbridge/integral.py`; gate `uncertified-rational-reconstruction` | sec. 4.2, 13 | disclosed |
| M3 | 81 is not yours | major | attributed to the analytic argument with citation; gate blocks the overclaim | gate `proved-rank-81-computationally` | sec. 1, 11 | resolved |
| M4 | reverse search not exhaustive | major | demoted to corroboration; word gated to appear only with a denial | gate `exhaustive-not-denied` | sec. 8, 13 | resolved |
| M5 | degree-eight disagreement | major | strict containment explained as an ansatz property; bridge separately certified | `verification/spinor_trace_comparison.json` | sec. 10 | resolved by added text |
| M6 | wrong signature | major | premise refuted: frame is split (5,5), not Euclidean | `test_null_frame_signature_is_split` | sec. 7.1 | refuted |
| M7 | a convention was guessed | major | disclosed as a reconstruction determined by equivariance | `covariance.py`, `rotations.py` | sec. 9, 13 | disclosed; review item G-1 |
| m1 | equivariance at sampled elements | minor | stated | `bridge_validation.json` | sec. 13 | disclosed |
| m2 | no seed/scale/step matrix | minor | stated with the reason; archived pair analysed instead | `SPINOR_JACOBIAN_RUNS.json` | sec. 11, app. E | disclosed |
| m3 | exact Jacobian reaches 59 | minor | reported as the port-graph subset only | `spinor_archive_jacobian_exact.json` | sec. 11, 13 | disclosed |
| m4 | only two primes | minor | stated | — | sec. 13 | disclosed |
| m5 | "canonical" | minor | gated | gate `canonical-without-scope` | sec. 6 | resolved |
| m6 | novelty unestablished | minor | all rows PROVISIONAL; no priority language | `audit/NOVELTY_MATRIX.md` | — | disclosed |
| m7 | third-party dependency | minor | manifest + adapter instructions | `release_candidate/` | app. F | disclosed |

## Second pass

The review was re-run after the M1 and M5 manuscript changes. No new objection
appeared; M1 remains the objection most likely to survive contact with a real
referee, and that is recorded rather than argued away.
