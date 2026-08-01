"""Generate every scientific number in the manuscript from result artifacts.

The manuscript must not contain a hard-coded scientific value.  This script
reads the JSON certificates and emits `manuscript/generated/numbers.tex`, a file
of `\\newcommand`s.  If an artifact is missing, the macro is emitted as
`\\ARTIFACTMISSING{name}`, which is defined in the preamble to typeset a loud
marker -- so a missing input is visible in the PDF instead of silently becoming
a stale number.

Run:
    python manuscript/scripts/make_numbers.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "manuscript" / "generated" / "numbers.tex"

MISSING: list[str] = []

#: TeX control-sequence names may contain letters only, so degrees are spelled.
DEGREE_WORDS = {4: "Four", 6: "Six", 8: "Eight", 10: "Ten"}


def load(rel: str):
    p = ROOT / rel
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except json.JSONDecodeError:
        return None


def macro(name: str, value) -> str:
    if value is None:
        MISSING.append(name)
        return f"\\newcommand{{\\{name}}}{{\\ARTIFACTMISSING{{{name}}}}}"
    return f"\\newcommand{{\\{name}}}{{{value}}}"


def main() -> int:
    lines = [
        "% GENERATED FILE -- do not edit.",
        "% Produced by manuscript/scripts/make_numbers.py from result artifacts.",
        "",
    ]

    # --- degree-10 spaces, from the incidence certificate --------------------
    inc = load("results/intrinsic_candidates/degree10_space_incidence.json")
    if inc:
        prime = sorted(inc["per_prime"])[0]
        dims = inc["per_prime"][prime]["dims"]
        pair = inc["per_prime"][prime]["incidence"]
        lines += [
            macro("dimAten", dims["A10"]),
            macro("dimBten", dims["B10"]),
            macro("dimGten", dims["G10"]),
            macro("dimPten", dims["P10"]),
            macro("dimDten", dims["D10"]),
            macro("dimQten", dims["A10"] - dims["D10"]),
            macro("capBG", pair["B10|G10"]["intersection"]),
            macro("capPB", pair["P10|B10"]["intersection"]),
            macro("capPG", pair["P10|G10"]["intersection"]),
            macro("capDB", pair["D10|B10"]["intersection"]),
            macro("sumPB", pair["P10|B10"]["sum"]),
            macro("nIncidencePrimes", len(inc["per_prime"])),
        ]
    else:
        for n in ("dimAten dimBten dimGten dimPten dimDten dimQten capBG capPB "
                  "capPG capDB sumPB nIncidencePrimes").split():
            lines.append(macro(n, None))

    # --- published / product intersection ------------------------------------
    pp = load("results/intrinsic_candidates/degree10_published_product_intersection.json")
    if pp:
        first = sorted(pp["per_prime"])[0]
        v = pp["per_prime"][first]
        lines += [
            macro("dimBcapP", v["dim_B10_cap_P10"]),
            macro("dimBplusP", v["dim_B10_plus_P10"]),
            macro("publishedPrimitiveContent",
                  v["dim_B10_published"] - v["dim_B10_cap_P10"]),
        ]
    else:
        for n in ("dimBcapP", "dimBplusP", "publishedPrimitiveContent"):
            lines.append(macro(n, None))

    # --- bridge certificate ---------------------------------------------------
    br = load("spinor_trace_bridge/results/bridge_validation.json")
    if br:
        primes = sorted(br["primes"])
        one = br["primes"][primes[0]]
        lines += [
            macro("bridgePrimes", ", ".join(primes)),
            macro("nBridgePrimes", len(primes)),
            macro("starSquared", one["bridge"]["star_squared"]),
            macro("dimSelfdual", one["bridge"]["selfdual_dim"]),
            macro("dimAntiSelfdual", one["bridge"]["antiselfdual_dim"]),
            macro("bridgeForwardRank", one["bridge"]["forward_rank"]),
            macro("dimGammaTraceless", one["clifford"]["gamma_traceless_dim"]),
            macro("gammaTraceRank", one["clifford"]["gamma_trace_rank"]),
        ]
    else:
        for n in ("bridgePrimes nBridgePrimes starSquared dimSelfdual "
                  "dimAntiSelfdual bridgeForwardRank dimGammaTraceless "
                  "gammaTraceRank").split():
            lines.append(macro(n, None))

    # --- common-sample comparison --------------------------------------------
    cmp_ = load("verification/spinor_trace_comparison.json")
    if cmp_ and cmp_.get("primes"):
        # choose the prime with the most completed degrees: picking the first
        # key alphabetically would silently report a partially finished run
        pk = max(cmp_["primes"], key=lambda k: len(cmp_["primes"][k].get("degrees", {})))
        slot = cmp_["primes"][pk]
        lines.append(macro("comparisonPrime", pk))
        lines.append(macro("nCommonSamples", slot.get("n_samples")))
        fam = slot.get("sample_families", {})
        for f in ("sparse", "structured", "generic", "holdout"):
            lines.append(macro(f"nSample{f.capitalize()}", fam.get(f)))
        for d, word in DEGREE_WORDS.items():
            e = slot.get("degrees", {}).get(str(d))
            lines.append(macro(f"traceRankDeg{word}",
                               e["trace_evaluation_rank"] if e else None))
            lines.append(macro(f"spinorRankDeg{word}",
                               e["spinor_evaluation_rank"] if e else None))
            lines.append(macro(f"spansEqualDeg{word}",
                               ("yes" if e["spans_equal_all_samples"] else "no")
                               if e else None))
            lines.append(macro(f"holdoutDeg{word}",
                               ("yes" if e["holdout_validated"] else "no")
                               if e else None))
    else:
        lines.append(macro("nCommonSamples", None))
        for f in ("Sparse", "Structured", "Generic", "Holdout"):
            lines.append(macro(f"nSample{f}", None))
        for word in DEGREE_WORDS.values():
            for k in ("traceRank", "spinorRank", "spansEqual", "holdout"):
                lines.append(macro(f"{k}Deg{word}", None))

    # --- exact archive Jacobian ----------------------------------------------
    aj = load("verification/spinor_archive_jacobian_exact.json")
    if aj and aj.get("runs"):
        ranks = sorted({r["exact_modular_rank_of_port_graph_subset"] for r in aj["runs"]})
        lines += [
            macro("archiveJacobianRank", ranks[0] if len(ranks) == 1 else "/".join(map(str, ranks))),
            macro("archiveJacobianRunsAgree", "yes" if len(ranks) == 1 else "no"),
            macro("nArchiveCandidates", aj["n_candidates_total"]),
            macro("nArchivePortGraphs", aj["n_port_graphs_used"]),
            macro("nArchiveStructured", aj["n_structured_not_reimplemented"]),
            macro("nArchiveJacobianRuns", len(aj["runs"])),
        ]
    else:
        for n in ("archiveJacobianRank archiveJacobianRunsAgree nArchiveCandidates "
                  "nArchivePortGraphs nArchiveStructured nArchiveJacobianRuns").split():
            lines.append(macro(n, None))

    # --- float64 Jacobian matrix ---------------------------------------------
    fj = load("verification/SPINOR_JACOBIAN_RUNS.json")
    if fj and fj.get("runs"):
        by = {}
        for r in fj["runs"]:
            by[r["classification"]] = by.get(r["classification"], 0) + 1
        nd = sorted({r["observed_rank"] for r in fj["runs"]
                     if r["classification"] == "nondegenerate generic"
                     and r["observed_rank"] is not None})
        lines += [
            macro("nFloatRuns", len(fj["runs"])),
            macro("nFloatNondegenerate", by.get("nondegenerate generic", 0)),
            macro("nFloatDegenerate", by.get("degenerate sample", 0)),
            macro("nFloatInconclusive", by.get("numerically inconclusive", 0)),
            macro("floatNondegenerateRanks",
                  "/".join(map(str, nd)) if nd else "none"),
        ]
    else:
        for n in ("nFloatRuns nFloatNondegenerate nFloatDegenerate "
                  "nFloatInconclusive floatNondegenerateRanks").split():
            lines.append(macro(n, None))

    # --- fixed analytic constants (not computed, so stated with provenance) ---
    lines += [
        "% analytic constants -- literature or elementary, not computed here",
        macro("dimFiveFormComponents", 252),
        macro("dimSelfDualModule", 126),
        macro("dimLorentzAlgebra", 45),
        macro("genericFunctionalDim", 81),
        macro("dimSymSpinor", 136),
        macro("spinorDim", 16),
    ]

    # one extra macro the Letter needs and the long form does not
    inc2 = load("results/intrinsic_candidates/degree10_space_incidence.json")
    if inc2:
        pr = sorted(inc2["per_prime"])[0]
        dd = inc2["per_prime"][pr]["dims"]
        lines.append(macro("dimQtenMinusOne", dd["A10"] - dd["D10"] - 1))
    else:
        lines.append(macro("dimQtenMinusOne", None))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n")
    prl = ROOT / "manuscript" / "prl" / "generated" / "numbers.tex"
    prl.parent.mkdir(parents=True, exist_ok=True)
    prl.write_text("\n".join(lines) + "\n")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(lines)} lines)")
    if MISSING:
        print(f"WARNING: {len(MISSING)} macros have no artifact yet:")
        for m in MISSING:
            print(f"  - {m}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
