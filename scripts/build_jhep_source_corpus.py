#!/usr/bin/env python3
"""Stage 2 --- build the JHEP source corpus from authoritative metadata.

Every record is fetched from INSPIRE-HEP (primary for this literature),
with Crossref as the fallback for anything INSPIRE does not carry.  No title,
author list, volume or page is typed from memory, and none is copied out of a
summary, a blog, or a mirror.

Raw API responses are cached under `audit/.source_cache/` so the corpus can be
rebuilt byte-identically offline, and so a referee can see exactly what the
registries said on the day it was built.

Writes:
    audit/JHEP_SOURCE_CORPUS.bib
    audit/JHEP_SOURCE_MATRIX.md
    audit/JHEP_CITATION_GRAPH.json
    audit/JHEP_CURRENT_CITING_PAPERS.md

Usage:
    python scripts/build_jhep_source_corpus.py [--repo .] [--offline]
"""

from __future__ import annotations

import argparse
import json
import hashlib
import re
import subprocess
import sys
import time
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

UA = "selfdual-5form-invariants source audit (mailto:kskkns44@gmail.com)"
INSPIRE = "https://inspirehep.net/api"
CROSSREF = "https://api.crossref.org/works"

# The mandatory corpus.  Each entry is (bibkey, lookup, section, relevance,
# which project claim it supports).  `lookup` is an arXiv id where one exists,
# otherwise a DOI, otherwise an INSPIRE literature search.
#
# Sections follow the execution specification:
#   2.1 core direct     2.2 nonlinear/chiral p-forms   2.3 actions/auxiliary
#   2.4 causality       2.5 Type IIB / five-form       2.6 spinors/invariants
SOURCES: list[dict] = [
    # --- 2.1 core direct sources -----------------------------------------
    dict(key="Cederwall:2025invariants", arxiv="2509.14350", section="2.1",
         relevance="States the ten-dimensional self-dual five-form invariant problem and "
                   "supplies partial invariant-ring and low-order tensor information.",
         supports="The problem statement; the twelve degree-10 candidate structures; "
                  "the generic-orbit counting this paper's upper bound rests on."),
    dict(key="Hutomo:2025chiral", arxiv="2509.14351", section="2.1",
         relevance="Non-linear chiral 4-form theories in D=10; establishes the qualitative "
                   "breakdown of lower-dimensional stress-flow universality.",
         supports="The count 81; the stress-flow construction; the D=10-is-different "
                  "observation, which is theirs and is cited as theirs."),
    # --- 2.2 nonlinear and chiral p-form theories ------------------------
    dict(key="Avetisyan:2022nonlinear", arxiv="2205.02522", section="2.2",
         relevance="Nonlinear (chiral) p-form electrodynamics.",
         supports="Physical context for why scalar invariants of a chiral form matter."),
    dict(key="Buratti:2019duality", arxiv="1906.07094", section="2.2",
         relevance="Duality-invariant self-interactions of abelian p-forms in arbitrary dimensions.",
         supports="Duality-invariance constraints on invariant functions."),
    dict(key="Buratti:2019selfint", arxiv="1909.10404", section="2.2",
         relevance="Self-interacting chiral p-forms in higher dimensions.",
         supports="The higher-dimensional chiral-form setting."),
    dict(key="Bandos:2020conformal", arxiv="2007.09092", section="2.2",
         relevance="Non-linear duality-invariant conformal extension of Maxwell's equations.",
         supports="ModMax as the four-dimensional contrast case."),
    dict(key="Bandos:2021pforms", arxiv="2012.09286", section="2.2",
         relevance="p-form gauge theories and their conformal limits.",
         supports="Conformal limits of p-form theories."),
    dict(key="Ferko:2024interacting", arxiv="2402.06947", section="2.2",
         relevance="Interacting chiral form field theories and TTbar-like flows in six and "
                   "higher dimensions.",
         supports="The D=6 universality baseline this paper's D=10 results contrast with."),
    dict(key="Ferko:2023duality", arxiv="2309.04253", section="2.2",
         relevance="Duality-invariant non-linear electrodynamics and stress tensor flows.",
         supports="Stress-tensor flow formalism."),
    dict(key="Kuzenko:2000nonlinear", arxiv="hep-th/0007231", section="2.2",
         relevance="Nonlinear self-duality and supersymmetry.",
         supports="Self-duality constraints in the supersymmetric setting."),
    dict(key="Gaillard:1981rj", doi="10.1016/0550-3213(81)90527-7", section="2.2",
         relevance="Duality rotations for interacting fields.",
         supports="The origin of duality-invariance conditions on invariant functions."),
    dict(key="Gaillard:1997zr", arxiv="hep-th/9712103", section="2.2",
         relevance="Nonlinear electromagnetic self-duality and Legendre transformations.",
         supports="Legendre-transform formulation of self-duality."),
    dict(key="Perry:1996mk", arxiv="hep-th/9611065", section="2.2",
         relevance="Interacting chiral gauge fields in six dimensions and Born-Infeld theory.",
         supports="The six-dimensional chiral two-form precedent."),
    # --- 2.3 action and auxiliary-field formulations ---------------------
    dict(key="Avetisyan:2021democratic", arxiv="2108.01103", section="2.3",
         relevance="Democratic Lagrangians for nonlinear electrodynamics.",
         supports="Action formulations for chiral forms."),
    dict(key="Evnin:2022three", arxiv="2207.01767", section="2.3",
         relevance="Three approaches to chiral form interactions.",
         supports="Comparison of chiral-form action formulations."),
    dict(key="Mkrtchyan:2019covariant", arxiv="1908.01789", section="2.3",
         relevance="Covariant actions for chiral p-forms.",
         supports="Covariant action formulation."),
    dict(key="Sen:2019selfdual", arxiv="1903.12196", section="2.3",
         relevance="Self-dual forms: action, Hamiltonian and compactification.",
         supports="Self-dual form dynamics."),
    dict(key="Sen:2015covariant", arxiv="1511.08220", section="2.3",
         relevance="Covariant action for type IIB supergravity.",
         supports="Where a ten-dimensional self-dual five-form actually appears."),
    dict(key="Ivanov:2002new", arxiv="hep-th/0202203", section="2.3",
         relevance="New representation for Lagrangians of self-dual nonlinear electrodynamics.",
         supports="Auxiliary-field formulation."),
    dict(key="Ivanov:2003dualities", arxiv="hep-th/0303192", section="2.3",
         relevance="Dualities as symmetries of interaction.",
         supports="Auxiliary-field formulation."),
    dict(key="Ivanov:2014pst", arxiv="1401.7834", section="2.3",
         relevance="Unifying the PST and auxiliary tensor field formulations of 4D self-duality.",
         supports="Relation between action formulations."),
    dict(key="Kuzenko:2019manifestly", arxiv="1908.04120", section="2.3",
         relevance="Manifestly duality-invariant interactions in diverse dimensions.",
         supports="Duality invariance across dimensions."),
    dict(key="Baglioni:2025auxiliary", arxiv="2512.21982", section="2.3",
         relevance="Relating auxiliary field formulations of 4d duality-invariant and 2d "
                   "integrable field theories.",
         supports="Current-literature sweep: the most recent auxiliary-field development."),
    # --- 2.4 causality and physical constraints --------------------------
    dict(key="Russo:2024causal", arxiv="2401.06707", section="2.4",
         relevance="Causal self-dual electrodynamics.",
         supports="Causality constraints, discussed as a limitation and not as a result here."),
    dict(key="Russo:2025chiral2form", arxiv="2504.01467", section="2.4",
         relevance="Causal chiral 2-form electrodynamics.",
         supports="The six-dimensional causality analysis this paper does not extend to D=10."),
    dict(key="Russo:2025simplified", arxiv="2505.08869", section="2.4",
         relevance="Simplified self-dual electrodynamics.",
         supports="Causality and hyperbolicity discussion."),
    dict(key="BabaeiAghbolagh:2026classifying", arxiv="2602.03426", section="2.4",
         relevance="Classifying causal nonlinear electrodynamics via phi-parity and "
                   "irrelevant deformations; cites the core D=10 paper.",
         supports="Current causality literature; a four-dimensional selection principle "
                  "this paper does not extend to ten dimensions."),
    # --- 2.5 Type IIB and five-form applications -------------------------
    dict(key="Paulos:2008tn", arxiv="0804.0763", section="2.5",
         relevance="Higher derivative terms including the Ramond-Ramond five-form.",
         supports="Where five-form invariants would enter an effective action."),
    dict(key="Liu:2022eight", arxiv="2205.11530", section="2.5",
         relevance="Type IIB at eight derivatives.",
         supports="The state of the art this paper's classification could feed, but does not "
                  "itself compute."),
    dict(key="Melo:2020stringy", arxiv="2007.06582", section="2.5",
         relevance="Stringy corrections to the entropy of electrically charged supersymmetric "
                   "black holes with AdS5 x S5 asymptotics.",
         supports="A physical setting where five-form invariants appear."),
    dict(key="Adhikari:2026typeiib", arxiv="2603.18248", section="2.5",
         relevance="Type IIB supergravity action and holography; cites the core invariant paper.",
         supports="Current Type IIB literature; bounds what this paper may claim about IIB."),
    # --- 2.6 spinors and invariant theory --------------------------------
    dict(key="VanProeyen:1999ni", arxiv="hep-th/9910030", section="2.6",
         relevance="Tools for supersymmetry: gamma-matrix and spinor conventions by signature.",
         supports="Charge conjugation, chirality and Majorana-Weyl conventions in appendix A."),
    dict(key="Kugo:1982bn", doi="10.1016/0550-3213(83)90584-9", section="2.6",
         relevance="Supersymmetry and the division algebras; Majorana-Weyl existence by signature.",
         supports="Existence of Majorana-Weyl spinors in (1,9) and (5,5)."),
    dict(key="Elamaran:2025machine", arxiv="2512.23750", section="2.6",
         relevance="Machine learning invariants of tensors: enumerate contraction graphs, "
                   "evaluate on random data, find linear relations to expose syzygies; "
                   "case study a 3-form in six dimensions. Cites both core papers.",
         supports="PRIOR ART for the enumerate-evaluate-relate method itself. This paper's "
                  "methodological novelty must be stated as the exact and certified form of "
                  "that method -- integral basis, modular arithmetic, holdout primes, a "
                  "characteristic-zero lower bound -- and never as originating the approach."),
    # --- computational sources (2.7) -------------------------------------
    dict(key="Harris:2020numpy", doi="10.1038/s41586-020-2649-2", section="2.7",
         relevance="NumPy.", supports="Array arithmetic underlying every evaluator."),
    dict(key="McKay:2014nauty", doi="10.1016/j.jsc.2013.09.003", section="2.7",
         relevance="nauty and Traces: practical graph isomorphism.",
         supports="Exact canonicalisation of invariant graphs; used through pynauty."),
    dict(key="Bareiss:1968", doi="10.1090/S0025-5718-1968-0226829-0", section="2.7",
         relevance="Sylvester's identity and multistep integer-preserving Gaussian elimination.",
         supports="The fraction-free determinant routine that independently confirms the "
                  "81x81 minor."),
    dict(key="Zippel:1979", doi="10.1007/3-540-09519-5_73", section="2.7",
         relevance="Probabilistic algorithms for sparse polynomials.",
         supports="Why a nonzero value at a sample point certifies a nonvanishing polynomial."),
    dict(key="Schwartz:1980", doi="10.1145/322217.322225", section="2.7",
         relevance="Fast probabilistic algorithms for verification of polynomial identities.",
         supports="The Schwartz-Zippel bound behind the sample-point argument."),
]

CORE_KEYS = ["Cederwall:2025invariants", "Hutomo:2025chiral"]

# Priority assessment for each paper found in the citing sweep, keyed by INSPIRE
# recid.  Anything not listed here is reported as UNASSESSED, which is a build
# failure rather than a silent pass -- a new citing paper must be judged, not
# absorbed.
CITING_ASSESSMENT: dict[str, str] = {
    "recid:3184624": "No conflict. Thesis, non-linear p-form gauge theories and their "
             "deformations; no arXiv id and no DOI, so not citable as a journal "
             "source. Deformations, not invariant bases.",
    "recid:3175945": "No conflict. Nonlinear self-duality for arbitrary spin; no "
             "ten-dimensional five-form invariant classification.",
    "recid:3098235": "No conflict. Thesis (Italian), non-linear interactions of "
             "self-dual p-forms; no arXiv id and no DOI.",
    "2512.23750": "**METHOD PRIOR ART, cited.** Enumerate contraction graphs, evaluate "
             "on random data, find linear relations to expose syzygies -- the same "
             "method family as the tensor side here, applied to a 3-form in six "
             "dimensions. Does not treat the ten-dimensional self-dual five-form, "
             "uses floating-point rather than exact arithmetic, and has no spinor "
             "bridge. Consequence: this paper's method novelty is the exact and "
             "certified form of that method, never the approach itself.",
    "2512.21982": "No conflict. Auxiliary-field formulations relating 4d "
             "duality-invariant and 2d integrable theories; different problem.",
    "2603.18248": "No conflict. Type IIB supergravity action and holography; uses the "
             "five-form but does not classify its invariants.",
    "2602.03426": "No conflict. Causal classification of nonlinear electrodynamics in "
             "four dimensions via phi-parity; a selection principle, not an invariant "
             "basis, and not in ten dimensions.",
    "2601.13022": "No conflict. Extends 4D self-dual models to D = 4p with the "
             "stress-tensor trace driving the flow. D = 10 is not of the form 4p and "
             "there is no five-form invariant classification.",
    "2602.24058": "No conflict. Higher-dimensional stress-tensor flows for Nambu-Goto, "
             "Born-Infeld and DBI; no self-dual five-form invariants.",
    "2602.04336": "No conflict. Preprint version of the arbitrary-spin self-duality "
             "work; same assessment.",
    "2604.13636": "No conflict. Euler-Heisenberg actions in higher dimensions; "
             "effective actions, not an invariant basis.",
    "2601.15376": "No conflict. Root-TTbar deformed pathways from CFT to CCFT; "
             "different problem.",
    "2509.17075": "No conflict. Integrable sigma models and universal root-TTbar via "
             "the Courant-Hilbert approach; different problem.",
    "2512.19889": "No conflict. Entanglement cohomology for GHZ and W states; shares "
             "an author with the invariant literature and nothing else.",
    "2605.25863": "No conflict, but METHODOLOGICALLY ADJACENT: linear algebra over "
             "finite fields on GPUs. Same arithmetic setting as the certificates here, "
             "different purpose (amplitudes). Not used by this project.",
    "2507.19313": "No conflict. A five-point amplitude result; cites the invariant "
             "paper for finite-field linear algebra only.",
    "2509.14350": "Self-reference: the core paper itself.",
    "2509.14351": "Self-reference: the core paper itself.",
}


# --------------------------------------------------------------------------
# fetching
# --------------------------------------------------------------------------
def fetch(url: str, cache: Path, offline: bool) -> dict | None:
    # The cache key must be injective. An earlier version truncated a sanitised
    # URL to its last 180 characters; because every query carries the same long
    # `?fields=...` tail, only about five characters of the identifier survived
    # and records collided -- a DOI lookup ending `.09.003` and an arXiv id
    # ending `01103` landed on the same file. Hash the whole URL instead, and
    # keep a readable prefix only for humans.
    ident = re.sub(r"[^A-Za-z0-9._-]", "_", url.split("?", 1)[0].split("/api/", 1)[-1])[:60]
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:16]
    path = cache / f"{ident}__{digest}.json"
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    if offline:
        return None
    # curl, not urllib: this Python.framework build has no root certificate
    # bundle, so urllib fails SSL verification on every host.  curl uses the
    # system trust store.
    for attempt in range(4):
        proc = subprocess.run(
            ["curl", "-sS", "--fail", "--max-time", "45", "-H", f"User-Agent: {UA}",
             "-H", "Accept: application/json", url],
            capture_output=True, text=True, check=False,
        )
        if proc.returncode == 0 and proc.stdout.strip():
            try:
                data = json.loads(proc.stdout)
            except json.JSONDecodeError:
                return None
            cache.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(data), encoding="utf-8")
            time.sleep(0.4)
            return data
        if "404" in (proc.stderr or ""):
            return None
        time.sleep(2 * (attempt + 1))
    return None


def inspire_record(entry: dict, cache: Path, offline: bool) -> dict | None:
    fields = ("titles,authors,publication_info,dois,arxiv_eprints,control_number,"
              "citation_count,earliest_date,collaborations,texkeys,report_numbers,"
              "preprint_date,imprints,document_type")
    if entry.get("arxiv"):
        rec = fetch(f"{INSPIRE}/arxiv/{entry['arxiv']}?fields={fields}", cache, offline)
        if rec:
            return rec.get("metadata")
    if entry.get("doi"):
        rec = fetch(f"{INSPIRE}/doi/{urllib.parse.quote(entry['doi'], safe='')}?fields={fields}",
                    cache, offline)
        if rec:
            return rec.get("metadata")
    return None


def crossref_record(doi: str, cache: Path, offline: bool) -> dict | None:
    rec = fetch(f"{CROSSREF}/{urllib.parse.quote(doi, safe='')}", cache, offline)
    return rec.get("message") if rec else None


def pick_publication(entries: list[dict]) -> dict:
    """Choose the journal of record.

    INSPIRE often carries several publication_info blocks: the refereed journal,
    a conference proceedings, an erratum. Taking entries[0] blindly is how
    `Avetisyan:2021democratic` came out as pages 33-48 of nothing instead of
    Phys. Rev. Lett. 127 (2021) 271601. Prefer a block that names a journal,
    and demote proceedings.
    """
    def score(pi: dict) -> tuple:
        title = pi.get("journal_title") or ""
        is_journal = bool(title)
        is_proc = "Conf.Proc" in title or "Proc." in title or "PoS" in title
        has_volume = bool(pi.get("journal_volume"))
        return (is_journal, not is_proc, has_volume)

    if not entries:
        return {}
    return max(entries, key=score)


def normalise(entry: dict, cache: Path, offline: bool) -> dict:
    """Collapse INSPIRE and Crossref into one record shape."""
    out = {
        "bibkey": entry["key"],
        "section": entry["section"],
        "relevance": entry["relevance"],
        "supports_claim": entry["supports"],
        "arxiv": entry.get("arxiv"),
        "doi": entry.get("doi"),
        "source_registry": None,
        "authors": [],
        "title": None,
        "journal": None,
        "volume": None,
        "year": None,
        "artid": None,
        "pages": None,
        "inspire_recid": None,
        "citation_count": None,
        "eprint_date": None,
    }
    meta = inspire_record(entry, cache, offline)
    if meta:
        out["source_registry"] = "INSPIRE-HEP"
        out["inspire_recid"] = meta.get("control_number")
        out["citation_count"] = meta.get("citation_count")
        titles = meta.get("titles") or []
        # Prefer the published title over the arXiv one when they differ.
        pub = [t for t in titles if t.get("source") not in (None, "arXiv")]
        out["title"] = (pub or titles)[0]["title"] if titles else None
        out["authors"] = [a.get("full_name") for a in (meta.get("authors") or [])]
        eprints = meta.get("arxiv_eprints") or []
        if eprints and not out["arxiv"]:
            out["arxiv"] = eprints[0].get("value")
        dois = meta.get("dois") or []
        if dois and not out["doi"]:
            out["doi"] = dois[0].get("value")
        pi = pick_publication(meta.get("publication_info") or [])
        out["journal"] = pi.get("journal_title")
        out["volume"] = pi.get("journal_volume")
        out["year"] = pi.get("year")
        out["artid"] = pi.get("artid")
        if pi.get("page_start"):
            out["pages"] = pi["page_start"] + (f"-{pi['page_end']}" if pi.get("page_end") else "")
        out["eprint_date"] = meta.get("preprint_date") or meta.get("earliest_date")
    elif entry.get("doi"):
        msg = crossref_record(entry["doi"], cache, offline)
        if msg:
            out["source_registry"] = "Crossref"
            out["title"] = (msg.get("title") or [None])[0]
            out["authors"] = [
                f"{a.get('family', '')}, {a.get('given', '')}".strip(", ")
                for a in msg.get("author", [])
            ]
            out["journal"] = (msg.get("container-title") or [None])[0]
            out["volume"] = msg.get("volume")
            out["pages"] = msg.get("page")
            out["artid"] = msg.get("article-number")
            parts = (msg.get("issued") or {}).get("date-parts") or [[None]]
            out["year"] = parts[0][0]
    return out


# --------------------------------------------------------------------------
# citing literature
# --------------------------------------------------------------------------
def citing_papers(recid: int, cache: Path, offline: bool) -> list[dict]:
    url = (f"{INSPIRE}/literature?sort=mostrecent&size=200&page=1"
           f"&q=refersto%20recid%20{recid}"
           f"&fields=titles,authors,publication_info,dois,arxiv_eprints,earliest_date,"
           f"control_number")
    data = fetch(url, cache, offline)
    if not data:
        return []
    rows = []
    for hit in data.get("hits", {}).get("hits", []):
        m = hit.get("metadata", {})
        pi = (m.get("publication_info") or [{}])[0]
        rows.append({
            "recid": m.get("control_number"),
            "title": (m.get("titles") or [{}])[0].get("title"),
            "authors": [a.get("full_name") for a in (m.get("authors") or [])][:6],
            "arxiv": ((m.get("arxiv_eprints") or [{}])[0]).get("value"),
            "doi": ((m.get("dois") or [{}])[0]).get("value"),
            "journal": pi.get("journal_title"),
            "volume": pi.get("journal_volume"),
            "year": pi.get("year"),
            "artid": pi.get("artid"),
            "date": m.get("earliest_date"),
        })
    return rows


def references_of(recid: int, cache: Path, offline: bool) -> list[dict]:
    data = fetch(f"{INSPIRE}/literature/{recid}?fields=references", cache, offline)
    if not data:
        return []
    rows = []
    for ref in (data.get("metadata", {}).get("references") or []):
        rr = ref.get("reference", {})
        rid = None
        if ref.get("record", {}).get("$ref"):
            rid = ref["record"]["$ref"].rstrip("/").split("/")[-1]
        rows.append({
            "recid": rid,
            "label": rr.get("label"),
            "title": (rr.get("title") or {}).get("title"),
            "arxiv": rr.get("arxiv_eprint"),
            "doi": (rr.get("dois") or [None])[0],
        })
    return rows


# --------------------------------------------------------------------------
# rendering
# --------------------------------------------------------------------------
def bib_authors(names: list[str]) -> str:
    return " and ".join(names) if names else "Unknown"


def to_bibtex(rec: dict) -> str:
    # Two records in this corpus -- Gaillard-Zumino hep-th/9712103 and Ivanov-
    # Zupnik hep-th/0202203 -- are contributions to proceedings volumes, not
    # journal articles. Emitting them as @article with an empty journal field
    # would make the bibliography assert something false, so they become @misc
    # carrying the eprint, which is how they are actually citable.
    kind = "article" if rec["journal"] else "misc"
    fields = [("author", bib_authors(rec["authors"])), ("title", "{" + (rec["title"] or "") + "}")]
    if rec["journal"]:
        fields.append(("journal", rec["journal"]))
    if rec["volume"]:
        fields.append(("volume", rec["volume"]))
    if rec["year"]:
        fields.append(("year", str(rec["year"])))
    if rec["artid"]:
        fields.append(("pages", rec["artid"]))
    elif rec["pages"]:
        fields.append(("pages", rec["pages"]))
    if rec["doi"]:
        fields.append(("doi", rec["doi"]))
    if rec["arxiv"]:
        fields.append(("eprint", rec["arxiv"]))
        fields.append(("archivePrefix", "arXiv"))
    body = ",\n".join(f"    {k} = {{{v}}}" if k != "title" else f"    {k} = {v}"
                      for k, v in fields)
    return "@" + kind + "{" + rec["bibkey"] + ",\n" + body + "\n}\n"


def render_matrix(records: list[dict], when: str) -> str:
    L: list[str] = []
    A = L.append
    A("# JHEP source matrix")
    A("")
    A(f"Built {when} by `scripts/build_jhep_source_corpus.py`.")
    A("")
    A("Every row was fetched from INSPIRE-HEP or Crossref on the build date and")
    A("cached under `audit/.source_cache/`. No field is typed from memory.")
    A("")
    sections = {
        "2.1": "Core direct sources",
        "2.2": "Nonlinear and chiral p-form theories",
        "2.3": "Action and auxiliary-field formulations",
        "2.4": "Causality and physical constraints",
        "2.5": "Type IIB and five-form applications",
        "2.6": "Spinor and invariant-theory sources",
        "2.7": "Computational sources",
    }
    for sec, name in sections.items():
        rows = [r for r in records if r["section"] == sec]
        if not rows:
            continue
        A(f"## {sec} {name}")
        A("")
        A("| key | authors | title | journal | year | DOI | arXiv | registry |")
        A("|---|---|---|---|---|---|---|---|")
        for r in rows:
            auth = ", ".join(a.split(",")[0] for a in r["authors"][:3])
            if len(r["authors"]) > 3:
                auth += " et al."
            jr = " ".join(x for x in [r["journal"], str(r["volume"] or ""),
                                      f"({r['year']})" if r["year"] else "",
                                      r["artid"] or ""] if x).strip()
            A(f"| `{r['bibkey']}` | {auth or '--'} | {r['title'] or '**NOT RESOLVED**'} | "
              f"{jr or '--'} | {r['year'] or '--'} | {r['doi'] or '--'} | "
              f"{r['arxiv'] or '--'} | {r['source_registry'] or 'UNRESOLVED'} |")
        A("")
        A("| key | relevance | claim it supports |")
        A("|---|---|---|")
        for r in rows:
            A(f"| `{r['bibkey']}` | {r['relevance']} | {r['supports_claim']} |")
        A("")
    unresolved = [r["bibkey"] for r in records if not r["source_registry"]]
    A("## Resolution")
    A("")
    A(f"{len(records) - len(unresolved)} of {len(records)} records resolved against a registry.")
    if unresolved:
        A("")
        A("**Unresolved, must not be cited until fixed:**")
        A("")
        for k in unresolved:
            A(f"- `{k}`")
    A("")
    return "\n".join(L)


def render_citing(core: dict, when: str) -> str:
    L: list[str] = []
    A = L.append
    A("# Papers citing the two core sources")
    A("")
    A(f"Queried {when} from INSPIRE-HEP with `refersto recid`, most recent first.")
    A("A paper appearing here is not automatically a priority conflict. Every")
    A("record carries an explicit written assessment; `UNASSESSED` is a build")
    A("failure, so a newly appearing citing paper must be judged rather than")
    A("silently absorbed.")
    A("")
    merged: dict[int, dict] = {}
    for block in core.values():
        for c in block["citing"]:
            merged[c["recid"]] = c
    unassessed = []
    for key, block in core.items():
        A(f"## Citing `{key}` (INSPIRE recid {block['recid']})")
        A("")
        A(f"{len(block['citing'])} citing records, most recent first.")
        A("")
        A("| date | authors | title | arXiv | published |")
        A("|---|---|---|---|---|")
        for c in block["citing"]:
            auth = ", ".join((a or "").split(",")[0] for a in c["authors"][:3])
            if len(c["authors"]) > 3:
                auth += " et al."
            jr = " ".join(x for x in [c["journal"], str(c["volume"] or ""),
                                      f"({c['year']})" if c["year"] else "",
                                      c["artid"] or ""] if x).strip()
            A(f"| {c['date'] or '--'} | {auth or '--'} | {c['title'] or '--'} | "
              f"{c['arxiv'] or '--'} | {jr or 'preprint'} |")
        A("")
    A("## Priority assessment, one row per distinct citing paper")
    A("")
    A("| paper | assessment |")
    A("|---|---|")
    for recid, c in sorted(merged.items(), key=lambda kv: kv[1]["date"] or "", reverse=True):
        lookup = c["arxiv"] or f"recid:{recid}"
        verdict = CITING_ASSESSMENT.get(lookup)
        if verdict is None:
            verdict = "**UNASSESSED**"
            unassessed.append(lookup)
        label = c["arxiv"] or f"INSPIRE {recid}"
        A(f"| {label} --- {c['title']} | {verdict} |")
    A("")
    if unassessed:
        A("**Unassessed papers block the build:** " + ", ".join(unassessed))
        A("")
    return "\n".join(L), unassessed


# Which source establishes which statement the manuscript makes, and --- the
# column that matters for priority --- whether the source already contains it.
CLAIM_SOURCE_MAP: list[dict] = [
    dict(claim="A ten-dimensional self-dual five-form has 81 functionally "
               "independent Lorentz invariants.",
         sources=["Hutomo:2025chiral", "Cederwall:2025invariants"],
         status="FROM THE LITERATURE. The count is theirs. This paper supplies a "
                "machine-checkable lower bound matching it, not the count."),
    dict(claim="126 - dim so(1,9) = 126 - 45 = 81 bounds the generic functional "
               "rank from above.",
         sources=["Cederwall:2025invariants"],
         status="FROM THE LITERATURE, analytic. No computation here supplies it."),
    dict(claim="The problem of an explicit invariant basis in D = 10 is open and "
               "hard.",
         sources=["Cederwall:2025invariants"],
         status="FROM THE LITERATURE. Stated by the source as an open problem; must "
                "not be presented as this paper's observation."),
    dict(claim="Stress-flow universality of D = 4 and D = 6 does not carry over to "
               "D = 10.",
         sources=["Hutomo:2025chiral", "Ferko:2024interacting"],
         status="FROM THE LITERATURE, qualitatively. The exact codimension is not "
                "in the source."),
    dict(claim="Enumerate contraction graphs, evaluate on sample points, and read "
               "off functional dependencies from a rank.",
         sources=["Elamaran:2025machine"],
         status="METHOD PRIOR ART. This paper's contribution is the exact and "
                "certified form -- integral basis, modular arithmetic, holdout "
                "primes, characteristic-zero lower bound -- not the approach."),
    dict(claim="A nonzero value at one sample point certifies a polynomial is not "
               "identically zero.",
         sources=["Schwartz:1980", "Zippel:1979"],
         status="STANDARD. Cited for the argument, not claimed."),
    dict(claim="Exact canonical forms for the invariant graphs.",
         sources=["McKay:2014nauty"],
         status="STANDARD TOOL, used through pynauty; cited as the algorithm."),
    dict(claim="An independent fraction-free determinant confirms the 81x81 minor.",
         sources=["Bareiss:1968"],
         status="STANDARD ALGORITHM. Cited for the second routine."),
    dict(claim="Majorana-Weyl spinors exist in signatures (1,9) and (5,5).",
         sources=["Kugo:1982bn", "VanProeyen:1999ni"],
         status="STANDARD. Cited for the conventions used in appendix A."),
    dict(claim="A ten-dimensional self-dual five-form is a field of Type IIB "
               "supergravity.",
         sources=["Sen:2015covariant", "Paulos:2008tn", "Liu:2022eight",
                  "Adhikari:2026typeiib"],
         status="CONTEXT ONLY. This paper computes no Type IIB correction."),
    dict(claim="Causality and hyperbolicity constrain nonlinear self-dual theories.",
         sources=["Russo:2024causal", "Russo:2025chiral2form",
                  "BabaeiAghbolagh:2026classifying"],
         status="CONTEXT AND LIMITATION. All in D = 4 or D = 6; no D = 10 causality "
                "theorem is proved here."),
    dict(claim="The exact equivariant tensor-spinor bridge, its left inverse, and "
               "degree-resolved span equality.",
         sources=[],
         status="NO SOURCE FOUND. Candidate contribution of this paper; the "
                "analytic correspondence is classical, the exact executable map "
                "and its certificates appear to be new. See "
                "audit/JHEP_NOVELTY_MATRIX.md."),
]


def render_claim_map(records: list[dict], when: str) -> tuple[str, list[str]]:
    by_key = {r["bibkey"]: r for r in records}
    L: list[str] = []
    A = L.append
    A("# Claim to source map")
    A("")
    A(f"Built {when} by `scripts/build_jhep_source_corpus.py`.")
    A("")
    A("Read the third column first. It says whether the statement is the")
    A("literature's or this paper's, which is the only thing that governs how the")
    A("manuscript is allowed to phrase it.")
    A("")
    A("| statement | sources | provenance |")
    A("|---|---|---|")
    dangling = []
    for row in CLAIM_SOURCE_MAP:
        cites = []
        for k in row["sources"]:
            if k not in by_key:
                dangling.append(k)
                cites.append(f"**MISSING `{k}`**")
            else:
                r = by_key[k]
                label = r["arxiv"] or r["doi"] or k
                cites.append(f"`{k}` ({label})")
        A(f"| {row['claim']} | {', '.join(cites) or '--'} | {row['status']} |")
    A("")
    return "\n".join(L), dangling


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".", type=Path)
    ap.add_argument("--offline", action="store_true")
    args = ap.parse_args()
    repo = args.repo.resolve()
    audit = repo / "audit"
    audit.mkdir(exist_ok=True)
    cache = audit / ".source_cache"

    when = datetime.now(timezone.utc).isoformat(timespec="seconds")
    records = [normalise(e, cache, args.offline) for e in SOURCES]

    (audit / "JHEP_SOURCE_CORPUS.bib").write_text(
        f"% Built {when} by scripts/build_jhep_source_corpus.py\n"
        "% Metadata from INSPIRE-HEP and Crossref; see audit/JHEP_SOURCE_MATRIX.md\n\n"
        + "\n".join(to_bibtex(r) for r in records if r["source_registry"]),
        encoding="utf-8",
    )
    (audit / "JHEP_SOURCE_MATRIX.md").write_text(render_matrix(records, when), encoding="utf-8")

    core = {}
    graph = {"generated_utc": when, "core": {}, "corpus": records}
    for key in CORE_KEYS:
        rec = next(r for r in records if r["bibkey"] == key)
        recid = rec["inspire_recid"]
        if not recid:
            continue
        refs = references_of(recid, cache, args.offline)
        cites = citing_papers(recid, cache, args.offline)
        core[key] = {"recid": recid, "citing": cites}
        graph["core"][key] = {
            "recid": recid,
            "doi": rec["doi"],
            "arxiv": rec["arxiv"],
            "citation_count": rec["citation_count"],
            "n_references": len(refs),
            "references": refs,
            "n_citing": len(cites),
            "citing": cites,
        }

    (audit / "JHEP_CITATION_GRAPH.json").write_text(json.dumps(graph, indent=1) + "\n",
                                                    encoding="utf-8")
    citing_md, unassessed = render_citing(core, when)
    (audit / "JHEP_CURRENT_CITING_PAPERS.md").write_text(citing_md, encoding="utf-8")
    claim_md, dangling = render_claim_map(records, when)
    (audit / "JHEP_CLAIM_SOURCE_MAP.md").write_text(claim_md, encoding="utf-8")

    resolved = sum(1 for r in records if r["source_registry"])
    print(f"corpus {resolved}/{len(records)} resolved")
    for r in records:
        if not r["source_registry"]:
            print(f"  UNRESOLVED {r['bibkey']} arxiv={r['arxiv']} doi={r['doi']}")
    for key, block in graph["core"].items():
        print(f"{key}: {block['n_references']} references, {block['n_citing']} citing")
    failed = False
    if unassessed:
        print("UNASSESSED citing papers: " + ", ".join(unassessed))
        failed = True
    if dangling:
        print("claim map cites keys not in the corpus: " + ", ".join(sorted(set(dangling))))
        failed = True
    if failed:
        return 1
    print("every citing paper assessed; claim map resolves")
    return 0


if __name__ == "__main__":
    sys.exit(main())
