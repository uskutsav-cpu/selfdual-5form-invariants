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
import re
import sys
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


def collect_tests(root: Path):
    """Number of tests pytest collects under `root`, or None if it cannot.

    Returns None rather than a guess: an unavailable count must show as a loud
    marker in the PDF, not as a plausible stale integer.
    """
    import subprocess
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "--collect-only", "-q",
             "-p", "no:cacheprovider"],
            cwd=root, capture_output=True, text=True, timeout=300)
    except (OSError, subprocess.SubprocessError):
        return None
    m = re.search(r"(\d+)\s+tests?\s+collected", proc.stdout)
    if m:
        return int(m.group(1))
    # `-q` prints one "path: N" line per file and no total when it succeeds.
    counts = re.findall(r"^\S+\.py:\s*(\d+)$", proc.stdout, re.MULTILINE)
    return sum(int(c) for c in counts) if counts else None


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

    # --- exact analytic Jacobian certificate ---------------------------------
    # This is the strongest computational statement in the package, so every
    # number it contributes is read from the certificate and never spelled out
    # in the manuscript source.
    ex = load("results/rank81/certificate.json")
    if ex and ex.get("runs"):
        runs = ex["runs"]
        summ = ex["summary"]
        ranks = sorted({r["jacobian"]["total_rank"] for r in runs})
        primes = sorted({r["prime"] for r in runs})
        points = sorted({(r["prime"], r["seed"]) for r in runs})
        cum = runs[0]["jacobian"]["cumulative_rank_by_degree"]
        sched = runs[0]["schedule_summary"]
        lines += [
            macro("exactJacRank", "/".join(map(str, ranks))),
            macro("exactJacRunsAgree", "yes" if summ.get("all_runs_agree") else "no"),
            macro("exactJacPoints", len(points)),
            # Emitted so the prose stays grammatical whatever the artifact says,
            # rather than being written as "point(s)".
            macro("exactJacPointWord", "point" if len(points) == 1 else "points"),
            macro("exactJacPrimeWord", "prime" if len(primes) == 1 else "primes"),
            macro("exactJacPrimes", ", ".join(map(str, primes))),
            macro("nExactJacPrimes", len(primes)),
            macro("exactJacRows", runs[0]["jacobian"]["n_rows"]),
            macro("exactJacCols", runs[0]["jacobian"]["n_columns"]),
            macro("exactJacScheduled", sched["planned"]),
            macro("exactJacEvaluated", sched["by_terminal_status"].get("evaluated", 0)),
            macro("exactJacErrors", sched["evaluation_errors"]),
            macro("exactJacZeroRows", sched["zero_rows"]),
            macro("exactJacScheduleComplete", "yes" if sched["complete"] else "no"),
            macro("exactJacEulerPass", "yes" if summ.get("all_euler_checks_pass") else "no"),
            macro("charZeroLowerBound", summ.get("characteristic_zero_lower_bound")),
            macro("cumRankDegFour", cum.get("4")),
            macro("cumRankDegSix", cum.get("6")),
            macro("cumRankDegEight", cum.get("8")),
            macro("cumRankDegTen", cum.get("10")),
            macro("cumRankDegTwelve", cum.get("12")),
        ]
    else:
        for n in ("exactJacRank exactJacRunsAgree exactJacPoints exactJacPrimes "
                  "nExactJacPrimes exactJacRows exactJacCols exactJacScheduled "
                  "exactJacEvaluated exactJacErrors exactJacZeroRows "
                  "exactJacScheduleComplete exactJacEulerPass charZeroLowerBound "
                  "cumRankDegFour cumRankDegSix cumRankDegEight cumRankDegTen "
                  "cumRankDegTwelve").split():
            lines.append(macro(n, None))

    # --- explicit non-vanishing minor ----------------------------------------
    mn = load("results/rank81/minor81_certificate.json")
    if mn:
        ms = mn.get("summary", {})
        lines += [
            macro("minorSize", mn.get("minor_size")),
            macro("minorPrimes", ", ".join(sorted(mn.get("per_prime", {})))),
            macro("nMinorPrimes", ms.get("n_primes_verified")),
            macro("minorDetNonzero", "yes" if ms.get("integer_minor_nonzero") else "no"),
        ]
    else:
        for n in ("minorSize minorPrimes nMinorPrimes minorDetNonzero").split():
            lines.append(macro(n, None))

    # --- exact characteristic-zero D10 / Q10 ---------------------------------
    cz = load("results/stress_flow/D10_characteristic_zero.json")
    czq = load("results/stress_flow/Q10_characteristic_zero.json")
    if cz and czq:
        mn = cz.get("lower_bound_certificate") or {}
        lift = cz.get("lift", {})
        lines += [
            macro("dimDtenQ", cz["D10_dim_over_Q"]),
            macro("dimQtenQ", czq["Q10_dim_over_Q"]),
            macro("dimAtenQ", czq["A10_dim_over_Q"]),
            macro("czSettled", "yes" if cz.get("settled") else "no"),
            macro("czMinorSize", mn.get("size")),
            macro("czFitPrimes", len(lift.get("fitting_primes", []))),
            macro("czHoldoutPrime", lift.get("holdout_prime")),
            macro("czIntegerRows", lift.get("integer_rows")),
            macro("czLiftedRows", lift.get("reconstructed_rows")),
            macro("czSweeps", cz.get("closure_sweeps")),
            # The relation symbol itself is generated, so the manuscript cannot
            # assert equality while the certificate records only a bound.
            macro("czQtenRelation", "=" if cz.get("settled") else "\\le"),
        ]
    else:
        for n in ("dimDtenQ dimQtenQ dimAtenQ czSettled czMinorSize czFitPrimes "
                  "czHoldoutPrime czIntegerRows czLiftedRows czSweeps "
                  "czQtenRelation").split():
            lines.append(macro(n, None))

    # --- exact characteristic-zero B10 cap P10 --------------------------------
    bp = load("results/degree10/B10_P10_intersection_exact.json")
    if bp:
        g = bp.get("generator", {})
        lines += [
            macro("bpSettled", "yes" if bp.get("settled") else "no"),
            macro("bpCapQ", bp.get("dim_B10_cap_P10_over_Q")),
            macro("bpSumQ", bp.get("dim_B10_plus_P10_over_Q")),
            macro("bpFitPrimes", len(bp.get("fitting_primes", []))),
            macro("bpHoldoutPrime", bp.get("holdout_prime")),
            macro("bpFreshPrime", g.get("verified_at_fresh_prime")),
            macro("bpFreshSamples", g.get("fresh_samples")),
            macro("bpCapRelation", "=" if bp.get("settled") else "\\le"),
        ]
    else:
        for n in ("bpSettled bpCapQ bpSumQ bpFitPrimes bpHoldoutPrime "
                  "bpFreshPrime bpFreshSamples bpCapRelation").split():
            lines.append(macro(n, None))

    # --- degree-8 span equality with the full spinor family ------------------
    # Distinct from the comparison table, which uses the port-graph stream only.
    d8 = load("verification/degree8_span_equality.json")
    if d8 and d8.get("primes"):
        pk = sorted(d8["primes"])[0]
        r = d8["primes"][pk]
        fam = r.get("family_contribution", {})
        indispensable = sorted(k for k, v in fam.items()
                               if v.get("rank_without_this_family", 0) < r["trace_rank"])
        lines += [
            macro("dEightTraceRank", r["trace_rank"]),
            macro("dEightSpinorRank", r["spinor_rank"]),
            macro("dEightUnionRank", r["union_rank"]),
            # The row count is prime-dependent: a randomly drawn port graph
            # whose evaluation vector vanishes identically mod p is dropped, and
            # two more vanish at the holdout primes. Ranks and conclusions do
            # not vary, so a range is reported rather than one prime's value.
            macro("dEightSpinorRowsMin",
                  min(v["n_spinor_rows"] for v in d8["primes"].values())),
            macro("dEightSpinorRowsMax",
                  max(v["n_spinor_rows"] for v in d8["primes"].values())),
            macro("dEightPrimes", d8["summary"]["primes_tested"]),
            macro("dEightPrimesEqual", d8["summary"]["primes_with_span_equality"]),
            macro("dEightIndispensable",
                  ", ".join(k.replace("_", " ") for k in indispensable) or "none"),
            macro("dEightRankWithoutWords",
                  fam.get("tensor_word", {}).get("rank_without_this_family")),
        ]
    else:
        for n in ("dEightTraceRank dEightSpinorRank dEightUnionRank "
                  "dEightSpinorRowsMin dEightSpinorRowsMax dEightPrimes dEightPrimesEqual "
                  "dEightIndispensable dEightRankWithoutWords").split():
            lines.append(macro(n, None))

    # --- test counts, collected rather than typed --------------------------
    # These went stale twice (49 -> 72 bridge tests) while sitting in the
    # manuscript as literals.  Collection is a static import pass, costs about
    # two seconds, and cannot disagree with the suite it describes.
    lines += [macro("nTraceTests", collect_tests(ROOT)),
              macro("nBridgeTests", collect_tests(ROOT / "spinor_trace_bridge"))]

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
