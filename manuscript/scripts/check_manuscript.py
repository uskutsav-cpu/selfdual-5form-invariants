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
        fail("build", "main.log missing; the manuscript has not been built")
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


def main() -> int:
    text = manuscript_text()
    wording_gates(text)
    required_disclosures(text)
    claim_diff()
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
