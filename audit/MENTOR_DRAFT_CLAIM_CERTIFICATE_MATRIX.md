# Claim → certificate matrix

Every central statement in the mentor draft maps to an artifact, a proof in the
text, or a primary source. A claim with no entry here should not be in the paper.

Machine-checked companion: `results/mentor_draft/scientific_input_manifest.json`
records the SHA-256 of every artifact read and fails if any is missing. It
reported **27 of 27 inputs verified, no problems**.

| claim | where in the draft | type | source |
|---|---|---|---|
| `star^2 = +1` on middle forms | §2, app. A | exact finite-field certificate | test suite; macro `\starSquared` |
| `dim Λ⁵₊ = 126` | §2 | analytic, standard | representation theory |
| Bridge lands in the gamma-traceless subspace | §5, app. C | exact finite-field certificate | bridge suite |
| Bridge rank 126, kernel zero | §5, prop. 5.1 | exact finite-field certificate | bridge suite; `\bridgeForwardRank` |
| Exact left inverse, round trip | §5, app. C | exact finite-field certificate | bridge suite |
| Equivariance with character solved for | §5, app. C | exact finite-field certificate | bridge suite |
| Lorentzian and split are different real forms, not a frame change | §5.2 | analytic, standard | corrected from an earlier error in this project |
| Orientation branch swaps the eigenspaces | §5.3, app. B | analytic + regression | `docs/FRAME_ORIENTATION_FINDING.md` |
| `p = 32707` is not exceptional | §5.3, app. B | counterfactual test | branch flip at a failing and a working prime |
| Tensor and spinor spans equal at d = 4, 6, 10 | §7 | multi-prime validation + holdout | comparison artifact; `\spansEqualDeg*` |
| Degree-eight ranks all equal 7 | §7.2 | exact finite-field, 4 primes | `\dEightUnionRank` |
| Tensor words indispensable (qualified) | §7.2 | ablation | `\dEightRankWithoutWords` |
| Generic functional rank ≥ 81 | §8, app. G | exact finite-field certificate → char 0 | `results/rank81/minor81_certificate.json` |
| Generic functional rank = 81 | §8.4 | analytic, **cited** | arXiv:2509.14351 |
| Schedule complete: 83/83, 0 errors, 0 zero rows | §8.1, app. G | artifact | `full_rank_matrix_publication_final.json` |
| 15 cells, identical rank and pivots | §8.3 | artifact | same |
| Only 2 of 15 cells independently recomputed | §8.4, §14 | **limitation** | `provenance.not_verified` field in the artifact |
| `dim_Q A10 = 14` | §9, thm 9.2 | spanning-set + exact modular | `Q10_characteristic_zero.json` |
| `dim_Q D10 = 11` | §9, thm 9.2 | exact rational certificate | `D10_characteristic_zero.json`, 11×11 minor |
| `dim_Q Q10 = 3` | §9, thm 9.2 | exact rational certificate | same |
| No upper-bound argument needed for D10 | §9.2 | analytic | fixed point over Q is an equality |
| Raw target span ≠ D10 | §9.1, app. H | negative fixture | `G10_counterfactual.json` |
| Cardinality minimality | §9.4, prop. 9.4 | analytic theorem | proved in the text; **not novel** |
| Removal minimality | §14 | **open** | checked only in the fixed graph basis |
| Free stress trace vanishes, any improvement | §10, thm 10.1, app. I | analytic theorem | proved in text; `tests/test_G10_trace_activation.py` |
| Control: ⟨F,F⟩ ≠ 0 generically | app. I | exact finite-field certificate | same test file |
| G-10 counterfactual gives Q10 = 0 | §10 | counterfactual | `\gTenCounterfactualQten` |
| `dim_Q(B10 ∩ P10) = 1` | §11, thm 11.1 | exact rational certificate | `B10_P10_intersection_exact.json` |
| The explicit integer identity | §11, eq. (11.2) | exact, fresh-prime verified | `B10_P10_intersection_generator.json` |
| The identity check failed first | §11 remark, app. J | disclosed | recorded, with the adjustment stated |
| Degree 12 is partial input only | §14 | **scope limitation** | stated verbatim |
| No Type IIB claim | §13 | **explicit non-claim** | gated |
| No all-order theorem | §14 | **explicit non-claim** | gated |
| AMB-01/02 avoided, not resolved | §14, app. E | **open** | compact basis avoids the ambiguous candidates |

## Claims deliberately absent

Checked for and confirmed absent by `check_draft.py`:

- a complete invariant-ring presentation;
- an all-order classification;
- a unique or canonical basis;
- a complete degree-twelve equivalence;
- algebraic independence of all 83 candidates;
- a Type IIB effective-action prediction;
- causality, hyperbolicity or supersymmetry statements;
- any licence, DOI, arXiv identifier, author list or approval.
