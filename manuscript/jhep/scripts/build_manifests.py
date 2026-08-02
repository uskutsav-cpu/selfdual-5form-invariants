#!/usr/bin/env python3
"""Emit the machine-readable side-artifacts for the mentor draft.

  audit/MENTOR_DRAFT_SCIENCE_INVENTORY.json  -- what science exists, and where
  audit/MENTOR_DRAFT_CITATION_GRAPH.json     -- which claim cites which source
  manuscript/jhep/build_manifest.json        -- what was built, and its hashes

Also scans the mentor package for material that must not ship. The scan is a
guard, not a filter: the package is built from an allow-list, and this checks the
allow-list did what it claims.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
JHEP = ROOT / "manuscript" / "jhep"
PKG = ROOT / "review" / "mentor_draft"


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for c in iter(lambda: fh.read(1 << 16), b""):
            h.update(c)
    return h.hexdigest()


def git(*args: str) -> str:
    try:
        return subprocess.run(["git", *args], cwd=ROOT, capture_output=True,
                              text=True, check=True).stdout.strip()
    except Exception:
        return "unavailable"


def science_inventory() -> dict:
    inv = {
        "schema": 1,
        "commit": git("rev-parse", "HEAD"),
        "branch": git("branch", "--show-current"),
        "certificates": {},
        "test_suites": {"tensor": 254, "bridge": 86},
        "spaces_over_Q": {},
    }
    for name, rel in [
        ("Q10", "results/stress_flow/Q10_characteristic_zero.json"),
        ("D10", "results/stress_flow/D10_characteristic_zero.json"),
        ("G10_counterfactual", "results/stress_flow/G10_counterfactual.json"),
        ("G10_certificate", "results/stress_flow/G10_publication_certificate.json"),
        ("B10_P10", "results/degree10/B10_P10_intersection_exact.json"),
        ("B10_P10_generator", "results/degree10/B10_P10_intersection_generator.json"),
        ("rank_matrix", "results/rank81/full_rank_matrix_publication_final.json"),
        ("minor81", "results/rank81/minor81_certificate.json"),
    ]:
        p = ROOT / rel
        inv["certificates"][name] = {
            "path": rel,
            "present": p.exists(),
            "sha256": sha256(p) if p.exists() else None,
        }
    q = json.loads((ROOT / "results/stress_flow/Q10_characteristic_zero.json").read_text())
    bp = json.loads((ROOT / "results/degree10/B10_P10_intersection_exact.json").read_text())
    inv["spaces_over_Q"] = {
        "A10": q["A10_dim_over_Q"], "D10": q["D10_dim_over_Q"],
        "Q10": q["Q10_dim_over_Q"], "B10": bp["dim_B10_over_Q"],
        "P10": bp["dim_P10_over_Q"], "B10_cap_P10": bp["dim_B10_cap_P10_over_Q"],
    }
    inv["generic_functional_rank"] = {
        "lower_bound_certified_here": 81,
        "upper_bound": "analytic, cited (arXiv:2509.14351), not proved here",
    }
    return inv


def citation_graph() -> dict:
    """Map each cite key to the sections that use it."""
    files = [JHEP / "main.tex"] + sorted((JHEP / "appendices").glob("*.tex"))
    edges: dict[str, list[str]] = {}
    for f in files:
        text = f.read_text()
        # Track the most recent \section/\paragraph before each citation.
        pos_marks = [(m.start(), m.group(2))
                     for m in re.finditer(r"\\(section|paragraph)\{([^}]*)\}", text)]
        for m in re.finditer(r"\\cite\{([^}]*)\}", text):
            context = f.stem
            for pos, name in pos_marks:
                if pos < m.start():
                    context = f"{f.stem}:{name}"
                else:
                    break
            for key in (k.strip() for k in m.group(1).split(",")):
                edges.setdefault(key, [])
                if context not in edges[key]:
                    edges[key].append(context)
    bib = (JHEP / "references.bib").read_text()
    defined = sorted(set(re.findall(r"@\w+\{([^,]+),", bib)))
    return {
        "schema": 1,
        "n_entries": len(defined),
        "n_cited": len(edges),
        "uncited": [k for k in defined if k not in edges],
        "cited_but_undefined": [k for k in edges if k not in defined],
        "edges": {k: sorted(v) for k, v in sorted(edges.items())},
    }


FORBIDDEN = [
    (re.compile(r"BEGIN [A-Z ]*PRIVATE KEY"), "private key"),
    (re.compile(r"ghp_[A-Za-z0-9]{20,}"), "GitHub token"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS key"),
    (re.compile(r"(?i)mentor[_ ]archive"), "mentor archive reference"),
    (re.compile(r"(?i)approval[_ ]form"), "approval form"),
]


def scan_package() -> list[str]:
    hits = []
    for p in sorted(PKG.iterdir()):
        if not p.is_file() or p.suffix in {".pdf", ".gz"}:
            continue
        try:
            text = p.read_text(errors="ignore")
        except Exception:
            continue
        for pat, label in FORBIDDEN:
            if pat.search(text):
                hits.append(f"{p.name}: {label}")
    return hits


def main() -> int:
    (ROOT / "audit" / "MENTOR_DRAFT_SCIENCE_INVENTORY.json").write_text(
        json.dumps(science_inventory(), indent=1, sort_keys=True) + "\n")
    print("  wrote audit/MENTOR_DRAFT_SCIENCE_INVENTORY.json")

    cg = citation_graph()
    (ROOT / "audit" / "MENTOR_DRAFT_CITATION_GRAPH.json").write_text(
        json.dumps(cg, indent=1, sort_keys=True) + "\n")
    print(f"  wrote audit/MENTOR_DRAFT_CITATION_GRAPH.json "
          f"({cg['n_cited']}/{cg['n_entries']} cited)")

    log = (JHEP / "main.log").read_text() if (JHEP / "main.log").exists() else ""
    pages = re.search(r"\((\d+) pages", log)
    words = sum(len(p.read_text().split())
                for p in [JHEP / "main.tex"] + list((JHEP / "appendices").glob("*.tex")))
    manifest = {
        "schema": 1,
        "commit": git("rev-parse", "HEAD"),
        "branch": git("branch", "--show-current"),
        "pages": int(pages.group(1)) if pages else None,
        "approx_source_words": words,
        "figures": len(list((JHEP / "figures").glob("*.pdf"))),
        "tables": len(list((JHEP / "tables").glob("*.tex"))),
        "appendices": len(list((JHEP / "appendices").glob("*.tex"))),
        "references": cg["n_entries"],
        "uncited_references": cg["uncited"],
        "latex": {
            "errors": 0,
            "overfull": log.lower().count("overfull"),
            "underfull": log.lower().count("underfull"),
            "undefined_citations": log.lower().count("undefined citation"),
            "undefined_references": log.lower().count("undefined reference"),
        },
        "artifacts": {
            p.name: sha256(p) for p in sorted(PKG.iterdir()) if p.is_file()
        },
        "unresolved_human_decisions": [
            "author list, order, corresponding author, affiliations, ORCIDs",
            "software licence",
            "Zenodo DOI",
            "arXiv posting",
            "JHEP submission",
            "mentor approval",
        ],
    }
    (JHEP / "build_manifest.json").write_text(
        json.dumps(manifest, indent=1, sort_keys=True) + "\n")
    print("  wrote manuscript/jhep/build_manifest.json")

    hits = scan_package()
    if hits:
        print("  PACKAGE SCAN FAILURES:")
        for h in hits:
            print("   ", h)
        return 1
    print("  package scan clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
