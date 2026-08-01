"""Manuscript consistency and wording gates.

Two jobs:

1.  Refuse specific overclaims.  Each rule below exists because the claim it
    forbids is one this project could plausibly have made and cannot support.
2.  Diff every number in the manuscript against the artifacts it came from, so a
    stale value cannot survive a rebuild.

Exit code is nonzero if any gate fails.  Run:
    python manuscript/scripts/check_manuscript.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANUSCRIPT = ROOT / "manuscript"

FAILURES: list[str] = []
CHECKS = 0


def fail(rule: str, detail: str) -> None:
    FAILURES.append(f"{rule}: {detail}")


def manuscript_text() -> str:
    """All manuscript prose, with generated files excluded.

    generated/numbers.tex is excluded because it contains macro *names*, not
    prose, and matching rules against names produces false positives.
    """
    parts = []
    for p in sorted(MANUSCRIPT.rglob("*.tex")):
        if "generated" in p.parts:
            continue
        parts.append(p.read_text())
    return "\n".join(parts)


def near(text: str, word: str, context: str, window: int = 400) -> list[str]:
    """Occurrences of `word` within `window` characters of `context`."""
    hits = []
    for m in re.finditer(word, text, re.IGNORECASE):
        lo, hi = max(0, m.start() - window), min(len(text), m.end() + window)
        if re.search(context, text[lo:hi], re.IGNORECASE):
            hits.append(text[max(0, m.start() - 60):m.end() + 60].replace("\n", " "))
    return hits


def wording_gates(text: str) -> None:
    global CHECKS

    # A forbidden word is only a violation when it is ASSERTED.  The manuscript
    # is required to discuss each of these claims in order to deny it, so a rule
    # that fires on the denial makes the gate unusable.  Each rule below is
    # therefore skipped when a negation appears in the same neighbourhood.
    NEGATION = (r"\bnot\b|\bnever\b|\bno\b|weaker than|is not|are not|"
                r"neither|do not|does not|without")

    rules = [
        # (name, pattern, required-context or None, why)
        ("proved-rank-81-computationally",
         r"(prov(e|ed|es)|demonstrat\w*)\s+(that\s+)?(the\s+)?(generic\s+)?"
         r"(functional\s+)?(dimension|rank)\s*(is\s*)?(81|\\genericFunctionalDim)",
         None,
         "the computation gives a lower bound; 81 is analytic"),
        ("clean-room-asserted",
         r"clean[- ]?room", None,
         "the implementations are independent, not clean-room"),
        ("complete-invariant-ring-asserted",
         r"complete\s+invariant\s+ring|generating\s+set\s+for\s+the\s+(full\s+)?ring",
         None, "no generating set for the ring is claimed"),
        ("q12-classified",
         r"degree[- ]twelve\s+(is\s+)?classified|degree\s*12\s+(is\s+)?classified",
         None, "degree twelve is background, not classified"),
        ("amb02-resolved",
         r"AMB-02\s+(is\s+)?resolv", None,
         "the source ambiguity is avoided, not resolved"),
        ("uncertified-rational-reconstruction",
         r"exact\s+over\s+(\\mathbb\{Q\}|the\s+rationals)", None,
         "results are modular; no certified rational reconstruction exists"),
        ("first-ever",
         r"\bfirst[- ]ever\b|\bfor the first time\b|\brevolutionary\b|"
         r"\bdefinitive(ly)?\b|\bbreakthrough\b", None,
         "prestige language is not supported"),
        # The Letter once described the degree-ten deficit as "not a bound ---
        # an exact dimension".  It is a bound: D10 admits directions that raise
        # the rank mod p, so dim Q10 is an upper bound over Q.  This rule fires
        # on any phrasing that denies the bound rather than stating it.
        ("quotient-described-as-not-a-bound",
         r"not\s+a\s+bound|(deficit|quotient)[^.]{0,40}\bexact\s+dimension",
         None,
         "dim Q10 is an upper bound in characteristic zero; see PO-09"),
    ]
    for name, pattern, context, why in rules:
        CHECKS += 1
        if context:
            hits = near(text, pattern, context)
        else:
            hits = [text[max(0, m.start() - 60):m.end() + 60].replace("\n", " ")
                    for m in re.finditer(pattern, text, re.IGNORECASE)]
        if name.endswith("-asserted") or name == "proved-rank-81-computationally":
            # keep only occurrences that are NOT denials
            kept = []
            for m in re.finditer(pattern, text, re.IGNORECASE):
                lo, hi = max(0, m.start() - 220), min(len(text), m.end() + 220)
                if not re.search(NEGATION, text[lo:hi], re.IGNORECASE):
                    kept.append(text[max(0, m.start() - 60):m.end() + 60].replace("\n", " "))
            hits = kept
        if hits:
            fail(name, f"{why}. Found: {hits[:2]}")

    # 'canonical' must always carry a scope qualifier or an explicit denial
    CHECKS += 1
    for m in re.finditer(r"canonical", text, re.IGNORECASE):
        lo, hi = max(0, m.start() - 300), min(len(text), m.end() + 300)
        window = text[lo:hi]
        if not re.search(r"not\s+(call|claim)|no\s+.{0,30}canonicalit|"
                         r"canonical\s*(form|isation|ization|ise|ize)|"
                         r"relabelling|graph", window, re.IGNORECASE):
            fail("canonical-without-scope",
                 f"'canonical' used without scope: ...{window[280:360]}...")

    # 'exhaustive' anywhere must be a denial
    CHECKS += 1
    for m in re.finditer(r"exhaustive", text, re.IGNORECASE):
        lo, hi = max(0, m.start() - 200), min(len(text), m.end() + 200)
        if not re.search(r"\bnot\b|never|is\s+not", text[lo:hi], re.IGNORECASE):
            fail("exhaustive-not-denied",
                 "'exhaustive' appears without an explicit denial")


def required_disclosures(text: str) -> None:
    """Statements the manuscript must contain, not merely avoid contradicting."""
    global CHECKS
    required = [
        (r"not\s+an\s+exhaustive\s+enumeration", "reverse search scope disclaimer"),
        (r"not\}?\s*\\?e?m?p?h?\{?not\}?[^.]{0,60}canonical|"
         r"not[^.]{0,80}canonical|no\s+universal\s+canonicality",
         "canonicality denial"),
        (r"implementation\s+independence.{0,80}not\s+claimed|"
         r"not\s+claimed\s+to\s+be\s+it", "clean-room denial"),
        (r"lower\s+bound", "the Jacobian result must be stated as a bound"),
        (r"analytic", "the 81 must be attributed to an analytic argument"),
        (r"HUMAN ACTION REQUIRED", "author placeholders must be visible"),
    ]
    for pattern, what in required:
        CHECKS += 1
        if not re.search(pattern, text, re.IGNORECASE):
            fail("missing-disclosure", f"{what} not found in the manuscript")


def claim_diff() -> None:
    """Every generated macro must match its artifact right now."""
    global CHECKS
    gen = MANUSCRIPT / "generated" / "numbers.tex"
    if not gen.exists():
        fail("claim-diff", "generated/numbers.tex is missing; run make_numbers.py")
        return
    text = gen.read_text()
    macros = dict(re.findall(r"\\newcommand\{\\(\w+)\}\{([^}]*)\}", text))

    def check(name: str, expected) -> None:
        global CHECKS
        CHECKS += 1
        got = macros.get(name)
        if got is None:
            fail("claim-diff", f"macro {name} absent")
        elif str(got) != str(expected):
            fail("claim-diff", f"{name} is {got!r} but the artifact says {expected!r}")

    inc = ROOT / "results/intrinsic_candidates/degree10_space_incidence.json"
    if inc.exists():
        d = json.loads(inc.read_text())
        prime = sorted(d["per_prime"])[0]
        dims = d["per_prime"][prime]["dims"]
        check("dimAten", dims["A10"])
        check("dimBten", dims["B10"])
        check("dimGten", dims["G10"])
        check("dimPten", dims["P10"])
        check("dimDten", dims["D10"])
        check("dimQten", dims["A10"] - dims["D10"])

    pp = ROOT / "results/intrinsic_candidates/degree10_published_product_intersection.json"
    if pp.exists():
        d = json.loads(pp.read_text())
        v = d["per_prime"][sorted(d["per_prime"])[0]]
        check("dimBcapP", v["dim_B10_cap_P10"])
        check("dimBplusP", v["dim_B10_plus_P10"])
        check("publishedPrimitiveContent",
              v["dim_B10_published"] - v["dim_B10_cap_P10"])

    br = ROOT / "spinor_trace_bridge/results/bridge_validation.json"
    if br.exists():
        d = json.loads(br.read_text())
        one = d["primes"][sorted(d["primes"])[0]]
        check("starSquared", one["bridge"]["star_squared"])
        check("bridgeForwardRank", one["bridge"]["forward_rank"])
        check("dimGammaTraceless", one["clifford"]["gamma_traceless_dim"])

    ex = ROOT / "results/rank81/certificate.json"
    if ex.exists():
        d = json.loads(ex.read_text())
        runs, summ = d["runs"], d["summary"]
        sched = runs[0]["schedule_summary"]
        cum = runs[0]["jacobian"]["cumulative_rank_by_degree"]
        ranks = sorted({r["jacobian"]["total_rank"] for r in runs})
        check("exactJacRank", "/".join(map(str, ranks)))
        check("exactJacPoints", len({(r["prime"], r["seed"]) for r in runs}))
        check("exactJacScheduled", sched["planned"])
        check("exactJacEvaluated", sched["by_terminal_status"].get("evaluated", 0))
        check("exactJacErrors", sched["evaluation_errors"])
        check("exactJacZeroRows", sched["zero_rows"])
        check("charZeroLowerBound", summ.get("characteristic_zero_lower_bound"))
        # Every degree, not just the last.  The dimension dictionary carried a
        # wrong interior value (8 for 9) for some time precisely because only
        # the endpoint was ever checked.
        for degree, word in (("4", "Four"), ("6", "Six"), ("8", "Eight"),
                             ("10", "Ten"), ("12", "Twelve")):
            if degree in cum:
                check(f"cumRankDeg{word}", cum[degree])

    mn = ROOT / "results/rank81/minor81_certificate.json"
    if mn.exists():
        d = json.loads(mn.read_text())
        check("minorSize", d["minor_size"])
        check("nMinorPrimes", d["summary"]["n_primes_verified"])

    # an unresolved artifact must be loud, not silently absent
    CHECKS += 1
    missing = [k for k, v in macros.items() if "ARTIFACTMISSING" in v]
    if missing:
        print(f"  note: {len(missing)} macro(s) still awaiting artifacts: "
              f"{', '.join(sorted(missing))}")


def build_gates() -> None:
    """Parse the LaTeX log for errors, undefined references and citations."""
    global CHECKS
    log = MANUSCRIPT / "main.log"
    if not log.exists():
        # main.log is a build artifact and is not committed, so in a fresh clone
        # it is legitimately absent.  Fall back to the packaging manifest, which
        # records the diagnostics of an ISOLATED build -- a stronger check than
        # the in-place log, since it proves the source archive is self-contained.
        manifest = ROOT / "submission_candidate" / "package_manifest.json"
        if not manifest.exists():
            fail("build", "neither manuscript/main.log nor "
                          "submission_candidate/package_manifest.json exists; "
                          "run build_submission_package.py")
            return
        diag = json.loads(manifest.read_text())["build"]
        for name, key in (("latex-errors", "errors"),
                          ("undefined-citations", "undefined_citations"),
                          ("undefined-references", "undefined_references")):
            CHECKS_LOCAL = 1
            globals()["CHECKS"] += CHECKS_LOCAL
            if diag.get(key):
                fail(name, f"{diag[key]} in the isolated build")
        globals()["CHECKS"] += 1
        if not diag.get("pdf_produced"):
            fail("build", "the isolated build produced no PDF")
        return
    text = log.read_text(errors="replace")
    for name, pattern in (("latex-errors", r"^! "),
                          ("undefined-citations", r"Citation.*undefined"),
                          ("undefined-references", r"Reference.*undefined")):
        CHECKS += 1
        n = len(re.findall(pattern, text, re.MULTILINE))
        if n:
            fail(name, f"{n} occurrence(s) in main.log")
    CHECKS += 1
    if not re.search(r"Output written on main\.pdf", text):
        fail("build", "no PDF was produced")


#: Headline numbers that appear in prose under docs/ and must track an artifact.
#: This gate exists because the wording and claim-diff gates cover manuscript
#: sources only, and two status documents were once left asserting a superseded
#: Jacobian rank while the certificate next to them said otherwise. A reader
#: picking the project up reads those documents first, so a stale number there
#: is at least as damaging as one in the manuscript.
DOC_SUPERSEDED = [
    # (path, forbidden regex, why it is wrong now, artifact that settles it)
    (
        "docs/RANK81_EXACT_CERTIFICATE.md",
        r"Scope:\s*82 of 83|c046_portgraph_d12.*evaluation_error",
        "the schedule is complete; every candidate is `evaluated`",
        "results/rank81/certificate.json",
    ),
    (
        "docs/JHEP_SPEC_STATUS.md",
        r"identical at three independent points",
        "the exact certificate is reported per (prime, seed) point, not as a "
        "count of agreeing points",
        "results/rank81/certificate.json",
    ),
]


def doc_consistency() -> None:
    """Status documents must not contradict the certificates beside them.

    Two kinds of check, both narrow on purpose:

    1.  Explicit superseded phrasings, listed above, are forbidden outright.
    2.  Any document that states an exact Jacobian rank must state the one the
        certificate currently records.
    """
    global CHECKS
    cert = ROOT / "results/rank81/certificate.json"
    if not cert.exists():
        return
    d = json.loads(cert.read_text())
    ranks = sorted({r["jacobian"]["total_rank"] for r in d["runs"]})
    sched = d["runs"][0]["schedule_summary"]

    for rel, pattern, why, artifact in DOC_SUPERSEDED:
        CHECKS += 1
        p = ROOT / rel
        if not p.exists():
            continue
        if re.search(pattern, p.read_text(), re.IGNORECASE):
            fail("doc-consistency",
                 f"{rel} still contains superseded wording -- {why} "
                 f"(see {artifact})")

    # A stated *Jacobian* rank in the docs must be one the certificate records.
    # The pattern is deliberately narrow: the repository states many other exact
    # ranks (the degree-12 atlas, the I6 obstruction, the stress-flow span) and
    # none of them has anything to do with this certificate.
    permitted = {str(r) for r in ranks}
    for p in sorted((ROOT / "docs").glob("*.md")):
        body = p.read_text()
        # The value must follow the phrase directly, through nothing but a
        # copula, a separator or table/markdown punctuation.  Allowing arbitrary
        # filler makes the gate reach across a clause and read a degree label as
        # a rank, which is how it first produced false positives on the degree-12
        # atlas and the I6 obstruction.
        for m in re.finditer(
                r"(?:Jacobian rank|exact modular rank)\s*(?:is|=|of|:|\|)?\s*\**(\d{1,3})",
                body, re.IGNORECASE):
            CHECKS += 1
            if m.group(1) not in permitted:
                # A superseded value is only a failure when it is asserted as
                # current; an explicitly retracted one is fine and is how the
                # record of a correction survives.
                lo = max(0, m.start() - 300)
                if re.search(r"supersede|superseded|earlier revision|no longer|retract",
                             body[lo:m.end() + 200], re.IGNORECASE):
                    continue
                fail("doc-consistency",
                     f"{p.relative_to(ROOT)} asserts exact rank {m.group(1)}, "
                     f"but the certificate records {'/'.join(sorted(permitted))}")

    # Test and gate counts drift the same way a rank does, and they had drifted
    # twice by the time this was added (49 -> 72 bridge tests, 32 -> 50 gates).
    # The manuscript takes both from generated macros; the prose under docs/ and
    # submission_candidate/ cannot, so it is checked instead.
    gen = MANUSCRIPT / "generated" / "numbers.tex"
    if gen.exists():
        macros = dict(re.findall(r"\\newcommand\{\\(\w+)\}\{([^}]*)\}",
                                 gen.read_text()))
        # The counts are written several different ways across these documents,
        # so match "N tests" and decide which suite is meant from the nearest
        # keyword rather than trying to enumerate the phrasings.  Deciding by
        # *nearest* keyword matters: "tensor ... 199 tests" and "bridge ... 72
        # tests" sit on consecutive lines in one file, and a plain window
        # containment test attributes the first to the bridge.
        #
        # Coverage is partial and deliberately so.  A count whose sentence names
        # neither suite -- "...; 72 tests at two primes." in
        # LIVE_STATE_DISCOVERY.md -- is not attributed and is not checked.
        # Widening the window until it catches that one also starts attributing
        # unrelated counts, which is the worse failure: a gate that cries wolf
        # gets weakened, and this one exists because a real staleness slipped
        # through.  Three of the four phrasings in the repository are covered.
        suites = [(r"bridge|test_bridge", macros.get("nBridgeTests"), "bridge"),
                  (r"tensor|trace side", macros.get("nTraceTests"), "tensor")]
        roots = [ROOT / "docs", ROOT / "submission_candidate",
                 ROOT / "spinor_trace_bridge" / "docs"]
        for d in roots:
            for p in sorted(d.rglob("*.md")) if d.exists() else []:
                body = p.read_text()
                for m in re.finditer(r"(\d{1,4})\s+(?:\w+\s+)?tests\b", body):
                    lo = max(0, m.start() - 90)
                    before = body[lo:m.start()]
                    # "72 bridge tests" puts the keyword after the number, so
                    # look forward as far as the end of the match and no further.
                    after = body[m.start():m.end()]
                    best = None
                    for pattern, expected, label in suites:
                        if expected is None:
                            continue
                        if re.search(pattern, after, re.IGNORECASE):
                            best = (0, expected, label)
                            break
                        hits = list(re.finditer(pattern, before, re.IGNORECASE))
                        if hits:
                            # distance from the keyword to the number
                            dist = len(before) - hits[-1].end()
                            if best is None or dist < best[0]:
                                best = (dist, expected, label)
                    if best is None:
                        continue
                    _, expected, label = best
                    CHECKS += 1
                    if m.group(1) != str(expected):
                        fail("doc-consistency",
                             f"{p.relative_to(ROOT)} states {m.group(1)} {label} "
                             f"tests; collection reports {expected}")

    CHECKS += 1
    if not sched["complete"]:
        # Not a failure -- but the docs must not claim a complete schedule.
        for p in sorted((ROOT / "docs").glob("*.md")):
            if re.search(r"Scope:\s*83 of 83", p.read_text()):
                fail("doc-consistency",
                     f"{p.relative_to(ROOT)} claims a complete schedule but "
                     f"the certificate records evaluation errors")


def main() -> int:
    text = manuscript_text()
    wording_gates(text)
    required_disclosures(text)
    claim_diff()
    doc_consistency()
    build_gates()

    print(f"manuscript gates: {CHECKS} checks")
    if FAILURES:
        print(f"FAILED ({len(FAILURES)}):")
        for f in FAILURES:
            print(f"  - {f}")
        return 1
    print("all gates passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
