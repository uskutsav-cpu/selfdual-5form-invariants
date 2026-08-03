#!/usr/bin/env python3
"""Validation gates for the mentor-review draft.

These are the checks the completion criteria name, expressed so that each one can
fail on its own and say why. A gate that cannot fail is not a gate, so several of
these were negative-tested during development by deliberately introducing the
condition they detect.

    python3 manuscript/jhep/scripts/check_draft.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
JHEP = ROOT / "manuscript" / "jhep"

failures: list[str] = []
passes: list[str] = []


def gate(name: str, ok: bool, detail: str = "") -> None:
    (passes if ok else failures).append(f"{name}{': ' + detail if detail else ''}")


def body_text() -> str:
    """main.tex plus every appendix, as one string."""
    parts = [(JHEP / "main.tex").read_text()]
    for p in sorted((JHEP / "appendices").glob("*.tex")):
        parts.append(p.read_text())
    return "\n".join(parts)


def main() -> int:
    text = body_text()
    # Prose gates must match across source line breaks, so compare against a
    # whitespace-collapsed copy. Without this a gate silently passes or fails
    # depending on where the paragraph happened to wrap.
    flat = re.sub(r"\s+", " ", text).lower()
    log = (JHEP / "main.log").read_text() if (JHEP / "main.log").exists() else ""

    # --- LaTeX health -----------------------------------------------------
    for label, needle in [("no overfull boxes", "Overfull"),
                          ("no underfull boxes", "Underfull"),
                          ("no undefined citations", "Undefined citation"),
                          ("no undefined references", "Undefined reference")]:
        gate(label, needle.lower() not in log.lower())

    # --- bibliography -----------------------------------------------------
    bib = (JHEP / "references.bib").read_text()
    defined = set(re.findall(r"@\w+\{([^,]+),", bib))
    cited: set[str] = set()
    for m in re.finditer(r"\\cite\{([^}]*)\}", text):
        cited.update(k.strip() for k in m.group(1).split(","))
    gate("every bib entry is cited", defined == cited or not (defined - cited),
         f"uncited: {sorted(defined - cited)}")
    gate("every citation exists in the bib", not (cited - defined),
         f"missing: {sorted(cited - defined)}")

    # --- placeholders -----------------------------------------------------
    gate("no TODO markers",
         not re.search(r"\b(TODO|FIXME|XXX|TBD)\b", text))

    # Every \pending{...} must be one of the permitted human decisions.
    permitted = ("author", "affiliation", "corresponding", "orcid", "licence",
                 "license", "doi", "arxiv", "acknowledg", "pending")
    bad = [m for m in re.findall(r"\\pending\{([^}]*)\}", text)
           if not any(w in m.lower() for w in permitted)]
    gate("placeholders are only the permitted human decisions", not bad,
         f"unexpected: {bad}")

    # --- generated-value discipline ---------------------------------------
    # The body must not hard-code the headline dimensions as bare digits in
    # prose. They must arrive through macros. We check the specific sentences
    # where a typed value would be most tempting.
    for pattern, why in [
        (r"\\dim_\\Q\s*\\Ften\s*=\s*14", "dim A10 typed rather than \\dimAtenQ"),
        (r"\\dim_\\Q\s*\\Dten\s*=\s*11", "dim D10 typed rather than \\dimDtenQ"),
        (r"\\dim_\\Q\s*\\Qten\s*=\s*3", "dim Q10 typed rather than \\dimQtenQ"),
    ]:
        gate(f"no typed scientific value ({why})", not re.search(pattern, text))

    # --- wording gates ----------------------------------------------------
    lowered = text.lower()
    for label, pattern in [
        ("no unscoped completeness claim",
         r"complete invariant ring|all-order classification|complete through degree 12"),
        ("no canonical-basis claim",
         r"\bcanonical basis\b|\bunique basis\b"),
        ("no degree-12 equivalence claim",
         r"complete degree-twelve equivalence|complete degree-12 equivalence"),
    ]:
        hits = re.findall(pattern, lowered)
        gate(label, not hits, f"found: {hits}")

    # The rank-81 statement must be scoped to the selected family.
    gate("rank 81 is scoped to the selected family",
         "selected family has generic functional rank" in lowered)
    gate("algebraic independence is explicitly disclaimed",
         "algebraically independent" in lowered and "not" in lowered)

    # Degree-eight indispensability must carry its qualifier.
    gate("degree-eight claim is qualified",
         "within the tested candidate-family decomposition" in lowered)

    # Degree-12 scope sentence must be present.
    gate("degree-twelve scope is stated",
         "partial certified input" in lowered)

    # The draft banner must be present.
    gate("draft banner present",
         "DRAFT FOR MENTOR REVIEW" in text and "NOT FOR SUBMISSION" in text)
    gate("authorship marked unresolved",
         "Author list pending mentor review" in text)

    # No fabricated approval, licence, DOI or author.
    for label, pattern in [
        ("no licence asserted", r"licensed under|MIT License|Apache License|GPL"),
        ("no DOI asserted", r"doi:10\.5281/zenodo"),
        ("no arXiv id asserted", r"arXiv:\d{4}\.\d{4,5}\s*\[this work\]"),
    ]:
        gate(label, not re.search(pattern, text, re.I))

    # --- AI disclosure honesty -------------------------------------------
    gate("AI disclosure does not claim independent human verification",
         "not the case that the computations were verified by a human" in flat)
    gate("AI disclosure states no AI author",
         "no ai system is an author" in flat)

    # --- input manifest ---------------------------------------------------
    man = ROOT / "results" / "mentor_draft" / "scientific_input_manifest.json"
    if man.exists():
        data = json.loads(man.read_text())
        gate("scientific input manifest is clean", data.get("clean") is True,
             str(data.get("problems")))
    else:
        gate("scientific input manifest exists", False)

    # --- figures and tables present --------------------------------------
    figs = sorted((JHEP / "figures").glob("*.pdf"))
    tabs = sorted((JHEP / "tables").glob("*.tex"))
    gate("five figures generated", len(figs) == 5, f"found {len(figs)}")
    gate("thirteen tables generated", len(tabs) == 13, f"found {len(tabs)}")
    for f in figs:
        gate(f"figure referenced: {f.name}", f.name in text)
    for t in tabs:
        gate(f"table included: {t.name}", t.name in text)

    # Inclusion is not the same as being pointed at. A float that is \included
    # but never \ref'd is one the reader is never sent to: it sits wherever the
    # placement algorithm drops it, often pages from the prose it belongs to.
    # Five figures and eight tables were in exactly that state before this gate
    # existed, so it checks the cross-reference, not just the \input.
    label_re = re.compile(r"\\label\{((?:fig|tab):[^}]+)\}")
    ref_re = re.compile(r"\\(?:auto|c)?ref\{([^}]+)\}")
    float_labels = set(label_re.findall(text))
    for t in tabs:                      # table labels live in tables/*.tex
        float_labels |= set(label_re.findall(t.read_text()))
    referenced = set(ref_re.findall(text))
    for lab in sorted(float_labels):
        gate(f"float cross-referenced in prose: {lab}", lab in referenced)

    apps = sorted((JHEP / "appendices").glob("*.tex"))
    gate("twelve appendices present", len(apps) == 12, f"found {len(apps)}")

    # --- claim ledger points where it says it points ----------------------
    # The ledger is how a reviewer navigates from a claim to the place it is
    # made, so a wrong number there costs them real time. The numbers drifted
    # once already: theorems are numbered continuously, not by section, so
    # "theorem 9.2" never existed and "table 7" pointed at the wrong table.
    # Each ledger location now carries the LaTeX label in brackets, and this
    # gate resolves that label against main.aux rather than trusting the prose.
    # The same check covers the mentor review guide, whose page numbers moved
    # under an edit that added two lines of prose. Numbers a reviewer navigates
    # by are only useful if something recomputes them.
    aux_path = JHEP / "main.aux"
    targets = [("claim ledger", JHEP / "claim_ledger.md", 9),
               ("review guide", ROOT / "review" / "MENTOR_REVIEW_GUIDE.md", 12)]
    if aux_path.exists():
        aux_txt = aux_path.read_text()
        number_of = dict(re.findall(r"\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{[0-9]+\}", aux_txt))
        page_of = dict(re.findall(r"\\newlabel\{([^}]+)\}\{\{[^}]*\}\{([0-9]+)\}", aux_txt))
        for name, path, minimum in targets:
            if not path.exists():
                gate(f"{name} present for cross-check", False)
                continue
            txt = path.read_text()
            pairs = re.findall(r"(?:p\.\s*)?(\d+(?:\.\d+)?)\)?\s*\[`([^`]+)`\]", txt)
            gate(f"{name} has anchored locations", len(pairs) >= minimum,
                 f"found {len(pairs)}")
            for number, label in pairs:
                # An anchor written "p. 26 [`app:orientation`]" states a page;
                # "theorem 5 [`thm:reach`]" states the float/theorem number.
                ok = number in (number_of.get(label), page_of.get(label))
                gate(f"{name} location resolves: {label} -> {number}", ok,
                     f"aux: number={number_of.get(label)!r} page={page_of.get(label)!r}")
    else:
        gate("main.aux available for cross-check", False)

    # --- report -----------------------------------------------------------
    print(f"{len(passes)} gates passed, {len(failures)} failed")
    for f in failures:
        print("  FAIL:", f)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
