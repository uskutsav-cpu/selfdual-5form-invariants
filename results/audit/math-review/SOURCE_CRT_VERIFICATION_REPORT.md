# Independent exact source certificate and portable verifier

The completed exact source certificate passes an independently written verifier. Its SHA256 is `01f9ab8d8f966827f820541a6e0bfec8e8bf64f710ec5b9f3be6dc825c61ed12`.

`verify_source_crt.py` uses a direct-product CRT formula, independently authored integer Bareiss elimination, and an independently authored rational row-echelon algorithm. It does not import the source fitting helpers or production repository modules, and does not recompute tensor contractions. It verifies the hashes of 98 recorded point files and their recorded program inputs, all 14 common binary coordinate vectors, all seven primes, all 630 reconstructed integer entries, their rational evaluations, exact graph minors, exact maps and inverse, degree-8 product correction, and source-space ranks and intersection witnesses.

The bounds were reviewed from the stated tensor formulas, normalized antisymmetrizations, clearing denominators, and explicit summed-index counts. The CRT modulus is `40274678413255193510345405666987`; twice the largest absolute cleared-integer bound is `705732652800000000000000000000`. The strict inequality proves uniqueness of each reconstructed signed integer evaluation. These are bounded integer reconstructions, not heuristic rational reconstruction of map coefficients. Details are in `SOURCE_CRT_METHOD_REVIEW.md` and the reproducible `source_bound_review.py`.

The exact ranks are: graph atlas degree 8: 7; graph atlas degree 10: 14; selected degree-8 source family: 7; primary degree-8 family: 6; hatted family: 5; primary plus product: 6; hatted plus product: 6; degree-10 source family: 12; degree-10 primitive quotient: 11; and product intersection: 1. The source family together with the two products has rank 13. The graph/source map and one-dimensional intersection witness were checked rather than assumed.

The passage from these exact evaluations to exact polynomial identities is conditional on the published upper bounds of 7 and 14 for the full rational invariant spaces and on analytic invariance of the specified source formulas. Those upper bounds were not independently derived in this audit. The degree-8 evaluation map into the 14 sample coordinates is injective onto its seven-dimensional image; the degree-10 evaluation map is an isomorphism onto the 14-dimensional sample space. This interpretation also assumes that the recorded modular executions implement their hashed fixed programs. Source-reading scope remains the literal displayed formulas. These checks do not retract the frozen transcription failure or silently recertify its old maps.

The new `repair-checkout/scripts/verify_independent_audit.py` is a separate portable wrapper; previously executed audit sources were preserved. It resolves the saved checker through explicit relocated paths. The default invocation, tested against packaged paths, passes in about six seconds and verifies:

- Four frozen 81-by-81 graph minors using full integer determinants.
- Two fresh independent graph minors, agreement of saved full Jacobian rows and values, and directional derivatives.
- Two saved 45-by-45 orbit minors and Jacobian annihilation of the saved orbit directions.
- Two degree-12 72-by-72 minors, including reconstruction of the product-rule rows and stacked gradients.
- The exact source CRT certificate and exact equality of both canonical maps to the embedded certificate maps.

The `--source-only` invocation also passes, in under one second. Both modes validate saved arithmetic evidence and hashes without production imports, tensor recomputation, or rederivation of the Hilbert upper bounds. Both reject Python optimization mode so verification assertions cannot silently disappear.

Two isolated-copy negative tests passed by rejecting corrupted evidence. Incrementing `exact_integer_numerator_evaluations.atlas10[0][0]` by one produced exit 1 at the independent reconstruction comparison. Incrementing the canonical degree-8 `literature_to_graph[0][0]` by one produced exit 1 with `canonical degree8 map differs from exact certificate`. All authoritative certificate and map hashes remained unchanged. The original evidence was never mutated.

Exact commands, stdout, stderr, exits and hashes are recorded under `commands/math_verify_exact_source_certificate`, `math_source_exact_bounds`, `math_install_portable_wrapper`, `math_portable_all_saved_evidence`, `math_portable_source_only`, `math_prepare_negative_evidence`, `math_negative_source_integer`, `math_negative_canonical_map`, and `math_summarize_portable_verification`. Machine-readable results are `source_crt_independent_verification.json` and `portable_verification_results.json`.
