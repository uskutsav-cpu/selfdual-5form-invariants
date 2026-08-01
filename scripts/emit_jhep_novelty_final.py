#!/usr/bin/env python3
"""Stage 12 --- the final novelty ledger and the words it licenses.

Two things live here. The novelty matrix classifies every claim the manuscript
intends to make. The prohibited-claims list turns that into a mechanical rule:
each of the words `first`, `complete`, `exact`, `unique`, `canonical`,
`minimal`, `exhaustive`, `previously unknown` may appear only where a ledger
entry supports it, and the manuscript gate reads this file to enforce that.

Writes:
    audit/JHEP_NOVELTY_MATRIX_FINAL.md
    audit/JHEP_PRIORITY_LEDGER_FINAL.md
    audit/JHEP_PROHIBITED_CLAIMS_FINAL.md
    audit/JHEP_NOVELTY_FINAL.json

Usage:
    python scripts/emit_jhep_novelty_final.py [--repo .]
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

CLASSES = {
    "known", "known in another representation", "suggested previously",
    "independently reproduced", "made explicit here", "strengthened here",
    "exactly certified here", "apparently new after search", "unresolved",
}

CLAIMS: list[dict] = [
    dict(
        id="N-01", claim="A ten-dimensional self-dual five-form admits 81 "
                         "functionally independent Lorentz invariants.",
        classification="known",
        prior="Hutomo, Lechner and Sorokin, JHEP 02 (2026) 147 [2509.14351]; "
              "Cederwall et al., J.Phys.A 59 (2026) 065203 [2509.14350].",
        here="A machine-checkable lower bound of 81 matching the published "
             "count, from an exact modular Jacobian over a 15-cell "
             "sample-by-prime matrix.",
        wording="The count is attributed to the sources. This paper supplies a "
                "certificate for it, and says so.",
    ),
    dict(
        id="N-02", claim="126 - dim so(1,9) = 81 bounds the generic functional "
                         "rank above.",
        classification="known",
        prior="Cederwall et al. [2509.14350], generic-orbit counting.",
        here="Cited, not reproved. It is the upper half of the rank statement "
             "and no computation here supplies it.",
        wording="Stated as analytic and attributed.",
    ),
    dict(
        id="N-03", claim="Enumerate contraction graphs, evaluate on generated "
                         "tensor data, find linear relations to expose "
                         "functional dependencies.",
        classification="known",
        prior="Elamaran, Ferko and Scarlett, Phys.Rev.D 114 (2026) 026016 "
              "[2512.23750], for a 3-form in six dimensions.",
        here="An exact and certified realization of that workflow for the "
             "ten-dimensional self-dual five-form: integral coordinate basis, "
             "modular arithmetic throughout, holdout primes, and a "
             "characteristic-zero lower bound rather than a numerical rank.",
        wording="MANDATORY. The general workflow is prior art and must be "
                "credited as such. The manuscript may claim only the exact and "
                "certified realization, never the approach.",
    ),
    dict(
        id="N-04", claim="The tensor and spinor descriptions of the self-dual "
                         "five-form correspond.",
        classification="known in another representation",
        prior="Standard Clifford algebra; the correspondence is classical and "
              "is used in [2509.14350].",
        here="An explicit executable map with an exact left inverse, verified "
             "at two primes.",
        wording="The correspondence is classical. The executable exact map is "
                "the contribution.",
    ),
    dict(
        id="N-05", claim="An exact equivariant bridge Phi: Lambda^5_+ V -> "
                         "Sym^2_{gamma-tr} S_+ with forward rank 126, kernel "
                         "exactly the anti-self-dual 126, image exactly the "
                         "gamma-traceless 126, and a left inverse composing to "
                         "the self-dual projector.",
        classification="apparently new after search",
        prior="No source found giving the map with certificates. Searched: both "
              "core papers and their 98 combined references, all 18 citing "
              "papers, and the spinor-conventions literature.",
        here="Span equalities rather than dimension coincidences; equivariance "
             "under GL(5) with the det character and under Clifford reflections, "
             "which generate the full group by Cartan-Dieudonne.",
        wording="May be described as, to our knowledge, not previously given "
                "with certificates. Not 'first'.",
    ),
    dict(
        id="N-06", claim="The oscillator frame's real form is split (5,5), not "
                         "Euclidean SO(10); (5,5) and (1,9) are inequivalent "
                         "real forms, congruent over C and over F_p.",
        classification="made explicit here",
        prior="Real forms of Spin(10,C) are standard. The specific correction "
              "and its consequence for this construction are not in the "
              "literature because the construction is not either.",
        here="The metric is extracted from the anticommutators rather than "
             "assumed, and the frame transition is constructed and checked.",
        wording="A correction to this project's own earlier record. The "
                "manuscript states the mathematics, not the history, and must "
                "not claim a real orthogonal transformation between "
                "inequivalent signatures.",
    ),
    dict(
        id="N-07", claim="Degree-8 tensor and spinor spans are equal, and the "
                         "structured tensor-word family is what supplies the "
                         "missing direction.",
        classification="exactly certified here",
        prior="None found.",
        here="Rank 7 on both sides, union rank 7, containment both ways, two "
             "fitting and two holdout primes, and a family ablation showing the "
             "port-graph family alone reaches only 6.",
        wording="May be stated as certified. The ablation is reported because "
                "it is the informative part.",
    ),
    dict(
        id="N-08", claim="Degree-10 tensor and spinor spans are equal.",
        classification="exactly certified here",
        prior="None found.",
        here="Rank 14 on both sides on a common sample, holdout validated. Both "
             "spans equal A10, whose dimension 14 is structural.",
        wording="May be stated as certified. Does not depend on exhausting "
                "either grammar; see docs/DEGREE10_NO_STOP_SCIENTIFIC_CLAIM.md.",
    ),
    dict(
        id="N-09", claim="An explicit 81x81 minor of the integral Jacobian has "
                         "nonzero determinant, giving rank_Q >= 81 "
                         "unconditionally.",
        classification="exactly certified here",
        prior="None found. The count 81 is prior; a certificate for it is not.",
        here="Two independent determinant routines agreeing, over a matrix of "
             "sample points and primes, with the integer-lift argument stated.",
        wording="'Certified', not 'proved'. The matching upper bound is "
                "analytic and belongs to N-02.",
    ),
    dict(
        id="N-10", claim="The complete degree-10 atlas and its incidence table.",
        classification="strengthened here",
        prior="Twelve degree-10 candidate structures appear in [2509.14350], as "
              "expressions rather than a basis, with relations undetermined.",
        here="Dimensions and containments for A10, B10, G10, P10, D10, with the "
             "correction that the published span is not a product complement.",
        wording="'Complete' is permitted for the atlas only in the sense "
                "certified, and B10 carries 'at the tested primes'.",
    ),
    dict(
        id="N-11", claim="dim_Q A10 = 14, dim_Q D10 = 11, dim_Q Q10 = 3, over "
                         "the rationals.",
        classification="exactly certified here",
        prior="None. Earlier statements of these numbers, including this "
              "project's own, were modular.",
        here="A10's upper bound is structural; D10 is an exact rational "
             "fixed-point closure, agreeing with the modular record and with "
             "the same free columns.",
        wording="May be stated as exact over Q. The seed-closure scope caveat "
                "travels with it.",
    ),
    dict(
        id="N-12", claim="The pure-N^(4125) compact basis for Q10.",
        classification="made explicit here",
        prior="None found.",
        here="Constructed with certificates; described as preferred "
             "ambiguity-minimal, since PO-11 leaves one member "
             "source-reading-dependent.",
        wording="Never 'canonical', never 'unique', never 'ambiguity-robust'.",
    ),
    dict(
        id="N-13", claim="Formula-independent reverse recovery of the "
                         "degree-10 quotient.",
        classification="independently reproduced",
        prior="Reproduces the published Level-B span from an independent search.",
        here="Recovery, on fit and holdout primes.",
        wording="'Recovery', never 'exhaustive enumeration'; PO-12 is open.",
    ),
    dict(
        id="N-14", claim="A reproducible computational proof architecture: "
                         "frozen executions, immutable per-cell artifacts, "
                         "read-only aggregation with adversarial tests, "
                         "clean-clone reproduction.",
        classification="apparently new after search",
        prior="No comparable apparatus found in this literature. Finite-field "
              "linear algebra itself is standard and is cited.",
        here="32 aggregator tests, each breaking one thing and asserting the "
             "named refusal; source-critical hashing; provenance binding.",
        wording="May be described as, to our knowledge, going beyond the "
                "reproducibility of the source literature. Not 'first'.",
    ),
    dict(
        id="N-15", claim="A degree-10 stress-flow obstruction with physical "
                         "consequences.",
        classification="unresolved",
        prior="Qualitative non-universality in D=10 is in [2509.14351].",
        here="The exact codimension is established; the physical reading is not, "
             "because PO-07 is open.",
        wording="REMOVED as a physical claim. Appears as a mathematical "
                "application with the physical reading explicitly withheld.",
    ),
]

# Word -> the only entries that license it.
WORD_LICENCES: dict[str, dict] = {
    "first": dict(licensed_by=[], rule="Not licensed anywhere. The priority "
                  "ledger supports 'to our knowledge, not previously given' at "
                  "most. Do not use."),
    "complete": dict(licensed_by=["N-10"], rule="Permitted only for the degree-10 "
                     "atlas in the certified sense, and never for enumeration "
                     "(PO-12) or for the invariant ring."),
    "exact": dict(licensed_by=["N-05", "N-07", "N-08", "N-09", "N-11", "N-14"],
                  rule="Permitted for arithmetic that is exact -- modular or "
                       "rational -- never for a claim whose bound is one-sided."),
    "unique": dict(licensed_by=[], rule="Not licensed. No uniqueness is "
                   "established for any basis or representative."),
    "canonical": dict(licensed_by=[], rule="Not licensed. Forbidden for Q10 "
                      "representatives; see docs/Q10_CANONICALITY_SCOPE.md."),
    "minimal": dict(licensed_by=["N-12"], rule="Permitted only as 'minimum "
                    "cardinality in any basis' (PO-08 cardinality half) or "
                    "'preferred ambiguity-minimal'. Never bare."),
    "exhaustive": dict(licensed_by=[], rule="Not licensed at degree 10 (PO-12) "
                       "or for any grammar. Degrees 4, 6, 8 reached "
                       "candidate_exhaustion and that specific word may be "
                       "quoted as a terminal state."),
    "previously unknown": dict(licensed_by=[], rule="Not licensed. Use 'we have "
                               "not found it in the literature searched', with "
                               "the search scope stated."),
    "all orders": dict(licensed_by=[], rule="Not licensed (PO-10). No induction "
                       "exists."),
    "syzygy": dict(licensed_by=[], rule="Not licensed for I12_61/I12_62 (PO-03); "
                   "only a Jacobian dependence is established."),
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".", type=Path)
    args = ap.parse_args()
    repo = args.repo.resolve()
    when = datetime.now(timezone.utc).isoformat(timespec="seconds")
    audit = repo / "audit"

    bad = [c["id"] for c in CLAIMS if c["classification"] not in CLASSES]
    counts: dict[str, int] = {}
    for c in CLAIMS:
        counts[c["classification"]] = counts.get(c["classification"], 0) + 1

    record = {"generated_utc": when, "claims": CLAIMS,
              "classification_counts": counts, "invalid_classifications": bad,
              "word_licences": WORD_LICENCES}
    (audit / "JHEP_NOVELTY_FINAL.json").write_text(
        json.dumps(record, indent=1) + "\n", encoding="utf-8")

    L = ["# JHEP novelty matrix --- final", "",
         f"Generated {when} by `scripts/emit_jhep_novelty_final.py`.", "",
         "| id | claim | classification |", "|---|---|---|"]
    for c in CLAIMS:
        L.append(f"| {c['id']} | {c['claim']} | **{c['classification']}** |")
    L += ["", "## Detail", ""]
    for c in CLAIMS:
        L += [f"### {c['id']} --- {c['classification']}", "",
              f"**Claim.** {c['claim']}", "",
              f"**Prior work.** {c['prior']}", "",
              f"**What this paper adds.** {c['here']}", "",
              f"**Permitted wording.** {c['wording']}", ""]
    L += ["## Tally", "", "| classification | count |", "|---|---|"]
    for k in sorted(counts):
        L.append(f"| {k} | {counts[k]} |")
    L.append("")
    (audit / "JHEP_NOVELTY_MATRIX_FINAL.md").write_text("\n".join(L) + "\n",
                                                        encoding="utf-8")

    P = ["# Priority ledger --- final", "",
         f"Generated {when}.", "",
         "The question this file answers is not 'is it new' but 'who may this "
         "paper say did it'.", "",
         "## Belongs to the literature", ""]
    for c in CLAIMS:
        if c["classification"] in ("known", "known in another representation",
                                   "suggested previously"):
            P += [f"- **{c['id']}** {c['claim']}", f"  - prior: {c['prior']}",
                  f"  - this paper: {c['here']}", ""]
    P += ["## Belongs to this paper, at the stated strength", ""]
    for c in CLAIMS:
        if c["classification"] in ("exactly certified here", "made explicit here",
                                   "strengthened here", "apparently new after search",
                                   "independently reproduced"):
            P += [f"- **{c['id']}** {c['claim']}",
                  f"  - strength: {c['classification']}",
                  f"  - wording: {c['wording']}", ""]
    P += ["## Withheld", ""]
    for c in CLAIMS:
        if c["classification"] == "unresolved":
            P += [f"- **{c['id']}** {c['claim']}", f"  - {c['wording']}", ""]
    P += ["## The sentence that must appear", "",
          "> Previous work developed graph enumeration, evaluation on generated",
          "> tensor data and relation finding for tensor-invariant discovery. The",
          "> present work gives an exact and certified realization for the",
          "> ten-dimensional self-dual five-form, constructs a real-form-aware",
          "> tensor-spinor bridge with an exact inverse, and supplies holdout and",
          "> characteristic-zero certificates.", ""]
    (audit / "JHEP_PRIORITY_LEDGER_FINAL.md").write_text("\n".join(P) + "\n",
                                                         encoding="utf-8")

    Q = ["# Prohibited claims --- final", "",
         f"Generated {when}.", "",
         "Each word below may appear only where a novelty entry licenses it.",
         "The manuscript gate reads `audit/JHEP_NOVELTY_FINAL.json`.", "",
         "| word | licensed by | rule |", "|---|---|---|"]
    for word, spec in WORD_LICENCES.items():
        lic = ", ".join(spec["licensed_by"]) or "**nothing**"
        Q.append(f"| `{word}` | {lic} | {spec['rule']} |")
    Q += ["", "## Claims that must not appear at all", "",
          "- degree-12 tensor-spinor equivalence",
          "- a complete degree-12 spinor atlas",
          "- a degree-12 basis map",
          "- complete equivalence through degree 12",
          "- all-order classification",
          "- a complete invariant-ring presentation",
          "- universal canonicality or basis uniqueness",
          "- invention of graph enumeration, random evaluation or relation finding",
          "- any physical or Type IIB consequence of the flow result (PO-07)",
          "- enumeration completeness beyond the certified grammar (PO-12)", ""]
    (audit / "JHEP_PROHIBITED_CLAIMS_FINAL.md").write_text("\n".join(Q) + "\n",
                                                           encoding="utf-8")

    for k in sorted(counts):
        print(f"{counts[k]:2d}  {k}")
    print(f"\nwords with no licence: "
          f"{[w for w, s in WORD_LICENCES.items() if not s['licensed_by']]}")
    if bad:
        print("INVALID: " + ", ".join(bad))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
