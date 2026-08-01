# Data and code package

Compact certificates for every claim, plus the manuscripts. Everything here is
project-authored.

## Not included

The third-party spinor enumeration archive. Redistribution permission is
unresolved; see `docs/THIRD_PARTY_ARCHIVE_BOUNDARY.md`. A manifest of per-file
hashes and adapter instructions ships instead, so a reader holding their own copy
can reproduce the archive-dependent results. Everything else reproduces without
it.

## Verify

    shasum -a 256 -c release/SHA256SUMS

## Reproduce

    python -m pytest                                  # 199 tensor tests
    cd spinor_trace_bridge && python -m pytest        # 72 bridge tests
    python spinor_trace_bridge/scripts/run_degree8_span.py
    python spinor_trace_bridge/scripts/run_stress_trace_sector.py
    python spinor_trace_bridge/scripts/run_rank81_certificate.py --archive PATH
    python spinor_trace_bridge/scripts/run_minor81_certificate.py --archive PATH
    ./manuscript/prl/build.sh

Long runs checkpoint per candidate and resume by re-issuing the same command.

## Licence

**Not chosen.** Without one this code is not reusable regardless of hosting. It
is a human decision; see `submission_candidate/AUTHORSHIP_DECISION_REQUIRED.md`.
