#!/usr/bin/env python3
"""Stage 9 --- close the proof-obligation ledger for the JHEP manuscript.

Each obligation gets a final status and, more importantly, a *manuscript
consequence*: the sentence the paper is and is not allowed to write. The
statuses are deliberately few, so that "we looked into it" cannot masquerade
as a resolution.

Allowed statuses:
    PROVED, EXACTLY CERTIFIED, DISPROVED, COUNTEREXAMPLE FOUND,
    REMOVED FROM CLAIMS, OPEN AND EXPLICITLY DELIMITED, NOT APPLICABLE

Writes:
    audit/JHEP_PROOF_OBLIGATIONS_FINAL.md
    audit/JHEP_PROOF_OBLIGATIONS_FINAL.json

Usage:
    python scripts/emit_jhep_proof_obligations_final.py [--repo .]
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

STATUSES = {
    "PROVED", "EXACTLY CERTIFIED", "DISPROVED", "COUNTEREXAMPLE FOUND",
    "REMOVED FROM CLAIMS", "OPEN AND EXPLICITLY DELIMITED", "NOT APPLICABLE",
}

LEDGER: list[dict] = [
    dict(
        id="PO-01",
        statement="Canonicalisation is exact at every degree actually used.",
        role="Underwrites every graph-basis identification on the tensor side.",
        evidence="The WL heuristic was removed; canonicalisation is exact via "
                 "pynauty or raises rather than guessing.",
        missing="Nothing.",
        attempt="Discharged in Phase 0, before this manuscript.",
        result="Exact canonicalisation throughout.",
        status="PROVED",
        consequence="The manuscript may describe canonicalisation as exact.",
        source="docs/PROOF_OBLIGATIONS.md; scripts/generate_graph_catalog.py",
    ),
    dict(
        id="PO-02",
        statement="`leading_field_degree` is correct, not merely self-consistent.",
        role="Supports the exhaustiveness of the degree-6 argument behind the "
             "flow claims.",
        evidence="18 expected generator multisets = 18 present, none missing, "
                 "none extra; leading degrees additive across products.",
        missing="A hand derivation, independently checked: Tr(tau) has leading "
                "degree 4 because the free stress tensor is traceless, and "
                "Tr(tau^k) has leading degree 2k for k >= 2. The values are "
                "currently computed by the same code they validate.",
        attempt="Not attempted in this manuscript; it is a clean-room writing "
                "task, not a computation.",
        result="Internal completeness established; external derivation absent.",
        status="OPEN AND EXPLICITLY DELIMITED",
        consequence="No claim in this manuscript rests on it. The flow material "
                    "appears as an application with its scope stated, and the "
                    "generator inventory is described as internally complete "
                    "rather than independently derived.",
        source="docs/PROOF_OBLIGATIONS.md",
    ),
    dict(
        id="PO-03",
        statement="I12_61 and I12_62 are polynomial syzygies.",
        role="Would upgrade a Jacobian dependence at degree 12 to a polynomial "
             "identity.",
        evidence="A Jacobian dependence at a generic point, which gives "
                 "functional dependence only.",
        missing="An exhibited polynomial identity: bound the relation degree, "
                "enumerate candidate monomials, exact evaluation matrix, "
                "modular nullspace, rational reconstruction, fresh-sample "
                "verification.",
        attempt="Not attempted. Degree 12 is outside this manuscript's claim "
                "scope, so the obligation does not gate anything here.",
        result="Unchanged.",
        status="NOT APPLICABLE",
        consequence="The word 'syzygy' does not appear for these objects. "
                    "Degree 12 enters only as the certified Jacobian block and "
                    "as labelled partial evidence.",
        source="docs/PROOF_OBLIGATIONS.md",
    ),
    dict(
        id="PO-04",
        statement="The K6 <-> Sigma_2 identification is the authors' own.",
        role="Wording of the sextic basis claims.",
        evidence="arXiv:2509.14350v2 proves (Sigma_1, Sigma_2) is a sextic "
                 "basis in the spinor formalism but does not publish the change "
                 "of basis to (Tr(M^3), K6). The identification here is inferred.",
        missing="The explicit map, from the authors or derived independently.",
        attempt="External. It may need a person rather than a computation, and "
                "no contact has been made.",
        result="Still inferred.",
        status="OPEN AND EXPLICITLY DELIMITED",
        consequence="The manuscript describes the identification as inferred and "
                    "cites the source for what it actually proves. It does not "
                    "attribute the change of basis to the source.",
        source="docs/PROOF_OBLIGATIONS.md",
    ),
    dict(
        id="PO-05",
        statement="Tr(M^6) has certified rational coordinates, or every "
                  "downstream theorem can be stated without them.",
        role="Any characteristic-zero statement that routes through Tr(M^6) "
             "graph coordinates.",
        evidence="29 of 72 columns exceed the CRT uniqueness bound at 15 primes "
                 "(modulus about 5.2e67). The flow coefficients lifted cleanly "
                 "at five primes, so this is a height problem specific to "
                 "Tr(M^6), not a shortage of effort.",
        missing="Either an analytic identity, or a reformulation making graph "
                "coordinates unnecessary.",
        attempt="Route (B) is taken here by construction rather than by proof: "
                "no claim in this manuscript uses Tr(M^6) graph coordinates. "
                "The exact D10 result routes through the rational flow targets, "
                "which do lift, not through Tr(M^6).",
        result="Avoided rather than solved.",
        status="NOT APPLICABLE",
        consequence="Tr(M^6) coefficients are never quoted. The manuscript says "
                    "so explicitly rather than leaving the omission unexplained.",
        source="docs/PROOF_OBLIGATIONS.md; results/stress_flow/trace_sector.json",
    ),
    dict(
        id="PO-06",
        statement="A second independent holdout prime validates the "
                  "reconstructions.",
        role="Every modular certificate.",
        evidence="Two independent holdout primes, 192/192 identical "
                 "reconstructions across two fit sets.",
        missing="Nothing.",
        attempt="Discharged in Phase 0.",
        result="Holdout validation is real, not nominal.",
        status="EXACTLY CERTIFIED",
        consequence="The manuscript may describe holdout validation as "
                    "independent, and should name the primes.",
        source="docs/PROOF_OBLIGATIONS.md",
    ),
    dict(
        id="PO-07",
        statement="The K6 transport statement survives field redefinitions and "
                  "the equations of motion.",
        role="Gates every physical and Type IIB reading of the flow result.",
        evidence="The transport equation is an off-shell statement in fixed "
                 "conventions.",
        missing="Classify the allowed local field redefinitions at each degree, "
                "compute their action on q6, determine whether q6 = 0 is "
                "preserved, then repeat modulo the leading equations of motion.",
        attempt="Not attempted.",
        result="Unchanged.",
        status="OPEN AND EXPLICITLY DELIMITED",
        consequence="No physical consequence and no Type IIB consequence is "
                    "drawn from the flow result anywhere in the manuscript. The "
                    "limitations section says why, naming this obligation.",
        source="docs/PROOF_OBLIGATIONS.md",
    ),
    dict(
        id="PO-08",
        statement="The three-element completion of D10 is minimal under change "
                  "of basis.",
        role="Any minimality claim about the quotient representatives.",
        evidence="Two separable halves. Cardinality: if D + span(S) = A then "
                 "applying the quotient map gives span(pi(S)) = Q, and a span of "
                 "|S| vectors has dimension at most |S|, so |S| >= dim Q. Since "
                 "dim Q10 = 3 and the exhibited completion has exactly 3 "
                 "elements, it is of minimum cardinality in any basis. "
                 "Permutation subgroup: four trials per degree, invariant.",
        missing="Removal minimality under general GL. Requires regenerating the "
                "certificates in the new basis and re-expressing the monomial "
                "index consistently; the obvious test of multiplying coordinate "
                "rows by a random matrix is invalid, because the resulting rows "
                "correspond to no actual flow problem.",
        attempt="The cardinality half was proved analytically. The general-GL "
                "half was not attempted; its cost and its invalid shortcut are "
                "both recorded.",
        result="Cardinality minimality holds in any basis. Removal minimality "
               "holds only for the permutation subgroup.",
        status="OPEN AND EXPLICITLY DELIMITED",
        consequence="The manuscript may say the completion has minimum "
                    "cardinality in any basis, and that removal minimality is "
                    "verified under relabelling. It may not say the "
                    "representatives are minimal, unique or canonical.",
        source="docs/PROOF_OBLIGATIONS.md; "
               "results/generalized_flow/minimality_certificates/basis_permutation.json",
    ),
    dict(
        id="PO-09",
        statement="Exceptional primes do not corrupt the modular certificates.",
        role="Every MOD-CERT row.",
        evidence="rank_{F_p} <= rank_Q always, so a modular rank is an "
                 "unconditional LOWER bound. Agreement across primes is "
                 "corroboration, not proof, but the direction of any possible "
                 "failure is determined.",
        missing="For any claim needing an upper bound, a characteristic-zero "
                "computation or a Hadamard-type bound on the relevant minors.",
        attempt="The two places where an upper bound was actually needed were "
                "closed directly rather than by counting primes. Rank 81: the "
                "upper bound 126 - 45 = 81 is analytic. D10: the closure was "
                "recomputed over Q with exact rational arithmetic.",
        result="No surviving claim depends on a modular upper bound.",
        status="EXACTLY CERTIFIED",
        consequence="Modular results are stated as lower bounds and labelled "
                    "'at the tested primes' where that is all they are. B10 and "
                    "B10 ∩ P10 carry that label; A10, G10, P10, D10 and Q10 do not.",
        source="docs/PROOF_OBLIGATIONS.md; "
               "results/stress_flow/D10_characteristic_zero_final.json",
    ),
    dict(
        id="PO-10",
        statement="An induction on degree supports an all-orders claim.",
        role="Any all-orders theorem.",
        evidence="None. No induction exists.",
        missing="Base cases, a recursion step, preservation of hypotheses, and "
                "an argument that no exceptional degree exists.",
        attempt="Not attempted.",
        result="Unchanged.",
        status="REMOVED FROM CLAIMS",
        consequence="'All orders' appears nowhere in the manuscript. Every "
                    "statement is degree-resolved and names its degrees.",
        source="docs/PROOF_OBLIGATIONS.md",
    ),
    dict(
        id="PO-11",
        statement="Bracket colour in the published equation (4.24) is resolved.",
        role="Which Q10 Level-B representatives are unconditional.",
        evidence="Colour does not survive PDF text extraction, and colour fixes "
                 "operation order. Both readings of every ambiguous candidate "
                 "are implemented and projected. P10_10 and P10_12 give "
                 "identical Q10 images under both readings; P10_09 and P10_11 "
                 "differ. No ambiguity-robust triple exists among the twelve "
                 "published candidates.",
        missing="A colour render of the journal page, or a statement from the "
                "authors.",
        attempt="Not attempted here; it needs a person or a colour source.",
        result="The selected basis attains the minimum of one "
               "source-reading-dependent member.",
        status="OPEN AND EXPLICITLY DELIMITED",
        consequence="The basis is called 'preferred ambiguity-minimal', never "
                    "'ambiguity-robust'. Only P10_10 and P10_12 are described as "
                    "unconditional, and the measurement showing no robust triple "
                    "exists is reported rather than hidden.",
        source="docs/PROOF_OBLIGATIONS.md",
    ),
    dict(
        id="PO-12",
        statement="The degree-10 block class is exhaustively enumerated.",
        role="Any claim of complete enumeration over M/N contractions.",
        evidence="The reverse benchmark met its recovery goal -- Q10 rank 3 "
                 "independently, span equal to the published Level-B span on fit "
                 "and holdout primes. It did not meet the exhaustion goal: 5 of "
                 "21 sectors are capped at 30 000 raw topologies and even the "
                 "exhausted sectors were sampled at 40 candidates.",
        missing="A sweep of every canonical candidate in the declared class; "
                "roughly 15 hours on one worker as a lower bound, plus an "
                "unknown multiple for the capped sectors.",
        attempt="Not attempted; the machine is committed to the certificate "
                "matrix and no claim here needs it.",
        result="Unchanged.",
        status="OPEN AND EXPLICITLY DELIMITED",
        consequence="The manuscript never claims complete enumeration of every "
                    "M/N contraction, and never says the reverse search "
                    "establishes minimality of anything. It reports recovery, "
                    "which is what was achieved.",
        source="docs/PROOF_OBLIGATIONS.md",
    ),
    dict(
        id="PO-13",
        statement="The Q10 change-of-basis matrices have certified rational "
                  "entries.",
        role="Any characteristic-zero statement about the Level-A/Level-B map.",
        evidence="Both directions certified modularly at two primes and verified "
                 "mutually inverse. Rational reconstruction attempted and not "
                 "certified: two primes give a CRT modulus of about 1.07e9, so a "
                 "lift is unique only when numerator and denominator are both "
                 "below about 2.3e4, and the entries are generic residues of "
                 "that magnitude.",
        missing="More primes. The projection is checkpointed, so the remaining "
                "four are incremental rather than a rerun.",
        attempt="Not attempted here. Note this is independent of the D10 result: "
                "that used the rational flow targets, not these maps.",
        result="Unchanged.",
        status="OPEN AND EXPLICITLY DELIMITED",
        consequence="The Level-A/Level-B maps are described as modular "
                    "certificates, never as rational identities. dim_Q Q10 = 3 "
                    "does not depend on them.",
        source="docs/PROOF_OBLIGATIONS.md",
    ),
]

# Distinctions that get conflated if they are not written down separately.
MINIMALITY_DISTINCTIONS = [
    dict(notion="cardinality lower bound",
         status="PROVED, in any basis",
         statement="|S| >= dim Q for any completing set S, because the quotient "
                   "map sends S to a spanning set of Q.",
         source="PO-08 cardinality half"),
    dict(notion="removal minimality of the selected set",
         status="VERIFIED under the permutation subgroup only",
         statement="No element of the exhibited triple can be dropped without "
                   "losing closure -- checked under basis relabelling, not under "
                   "general GL.",
         source="PO-08 permutation half"),
    dict(notion="minimality under arbitrary basis change",
         status="OPEN",
         statement="Not established. The obvious test is invalid; see PO-08.",
         source="PO-08"),
    dict(notion="uniqueness",
         status="NOT CLAIMED",
         statement="No claim that the triple is the only minimum-cardinality "
                   "completion.",
         source="--"),
    dict(notion="canonicality",
         status="NOT CLAIMED",
         statement="No basis-independent canonical choice is established. "
                   "'Canonical' is a forbidden word for this object.",
         source="docs/Q10_CANONICALITY_SCOPE.md"),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".", type=Path)
    args = ap.parse_args()
    repo = args.repo.resolve()
    when = datetime.now(timezone.utc).isoformat(timespec="seconds")

    bad = [o["id"] for o in LEDGER if o["status"] not in STATUSES]
    counts: dict[str, int] = {}
    for o in LEDGER:
        counts[o["status"]] = counts.get(o["status"], 0) + 1

    record = {
        "generated_utc": when,
        "n_obligations": len(LEDGER),
        "status_counts": counts,
        "invalid_statuses": bad,
        "obligations": LEDGER,
        "minimality_distinctions": MINIMALITY_DISTINCTIONS,
        "blocking_for_this_manuscript": [
            o["id"] for o in LEDGER
            if o["status"] == "OPEN AND EXPLICITLY DELIMITED"
            and "No claim in this manuscript rests on it" not in o["consequence"]
            and "does not gate" not in o["consequence"]
        ],
        "none_blocking_note": (
            "Every OPEN obligation is delimited by removing or narrowing the "
            "claim it would have supported, not by leaving the claim standing "
            "with a caveat attached."),
    }

    (repo / "audit" / "JHEP_PROOF_OBLIGATIONS_FINAL.json").write_text(
        json.dumps(record, indent=1) + "\n", encoding="utf-8")

    L: list[str] = []
    A = L.append
    A("# Proof obligations --- final status for the JHEP manuscript")
    A("")
    A(f"Generated {when} by `scripts/emit_jhep_proof_obligations_final.py`.")
    A("")
    A("Read the **manuscript consequence** column. An obligation that stays open")
    A("is not a caveat bolted onto a surviving claim; it is a claim that was")
    A("narrowed or removed.")
    A("")
    A("## Tally")
    A("")
    A("| status | count |")
    A("|---|---|")
    for k in sorted(counts):
        A(f"| {k} | {counts[k]} |")
    A("")
    A("## Obligations")
    A("")
    for o in LEDGER:
        A(f"### {o['id']} --- {o['status']}")
        A("")
        A(f"**Statement.** {o['statement']}")
        A("")
        A(f"**Scientific role.** {o['role']}")
        A("")
        A(f"**Present evidence.** {o['evidence']}")
        A("")
        A(f"**Missing argument.** {o['missing']}")
        A("")
        A(f"**Attempt performed.** {o['attempt']}")
        A("")
        A(f"**Result.** {o['result']}")
        A("")
        A(f"**Manuscript consequence.** {o['consequence']}")
        A("")
        A(f"**Source.** `{o['source']}`")
        A("")
    A("## Minimality, split into the things it is usually confused with")
    A("")
    A("| notion | status | statement |")
    A("|---|---|---|")
    for m in MINIMALITY_DISTINCTIONS:
        A(f"| {m['notion']} | **{m['status']}** | {m['statement']} |")
    A("")
    A("The first of these does not imply any of the others. The manuscript uses")
    A("only the first two, in those words.")
    A("")
    (repo / "audit" / "JHEP_PROOF_OBLIGATIONS_FINAL.md").write_text(
        "\n".join(L) + "\n", encoding="utf-8")

    for o in LEDGER:
        print(f"{o['id']:6s} {o['status']}")
    print()
    for k in sorted(counts):
        print(f"{counts[k]:2d}  {k}")
    if bad:
        print("INVALID STATUSES: " + ", ".join(bad))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
