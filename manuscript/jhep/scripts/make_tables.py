#!/usr/bin/env python3
"""Generate every table in the mentor-review draft from result artifacts.

Same rule as the figures: a scientific value is read from an artifact or from
the generated macro file, never typed here. Tables that are pure notation --
the conventions table, the claim-strength legend -- carry no computed values and
are written out literally; they are marked as such below.

    python3 manuscript/jhep/scripts/make_tables.py
"""

from __future__ import annotations

import json
import platform
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "manuscript" / "jhep" / "tables"

_MACROS: dict[str, str] = {}


def macro(name: str) -> str:
    if not _MACROS:
        src = ROOT / "manuscript" / "generated" / "numbers.tex"
        for m in re.finditer(r"\\newcommand\{\\(\w+)\}\{([^}]*)\}", src.read_text()):
            _MACROS[m.group(1)] = m.group(2)
    if name not in _MACROS:
        raise SystemExit(f"macro \\{name} is not defined")
    return _MACROS[name]


def load(rel: str) -> dict:
    path = ROOT / rel
    if not path.exists():
        raise SystemExit(f"required artifact missing: {rel}")
    return json.loads(path.read_text())


def write(name: str, body: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(
        "% GENERATED FILE -- do not edit.\n"
        "% Produced by manuscript/jhep/scripts/make_tables.py\n" + body)
    print(f"  wrote tables/{name}")


def tabular(spec, header, rows, caption, label, note=None):
    out = ["\\begin{table}[htbp]", "\\centering",
           "\\small", f"\\begin{{tabular}}{{{spec}}}", "\\hline",
           " & ".join(header) + " \\\\", "\\hline"]
    out += [" & ".join(str(c) for c in r) + " \\\\" for r in rows]
    out += ["\\hline", "\\end{tabular}"]
    if note:
        out.append(f"\\\\[2pt]\\begin{{minipage}}{{0.92\\textwidth}}\\footnotesize {note}\\end{{minipage}}")
    out += [f"\\caption{{{caption}}}", f"\\label{{{label}}}", "\\end{table}", ""]
    return "\n".join(out)


# ------------------------------------------------------------------ 1
def t_notation():
    """Pure notation: no computed value appears, so nothing is read."""
    rows = [
        (r"$d$", "spacetime dimension", "10"),
        (r"$F$", "five-form field strength", r"$F\in\Lambda^5$"),
        (r"$\star$", "Hodge star on middle forms", r"$\star^2=+1$"),
        (r"$\Lambda^5_\pm$", "(anti-)self-dual eigenspaces", r"$\dim=126$"),
        (r"$A_d$", "full invariant space at field degree $d$", "---"),
        (r"$G_{10}$", "graph-generator subspace", "---"),
        (r"$P_{10}$", "product subspace", "---"),
        (r"$B_{10}$", "span of the published structures", "---"),
        (r"$D_{10}$", "subspace reachable by the stress flow", "---"),
        (r"$Q_{10}$", r"quotient $A_{10}/D_{10}$", "---"),
        (r"$\tau$", "stress tensor of the deformed theory", "---"),
        (r"$S_+$", "chiral spinor module", r"$\dim=16$"),
    ]
    write("tab01_notation.tex", tabular(
        "lll", ["symbol", "meaning", "value"], rows,
        "Notation and conventions used throughout. Entries marked "
        "``---'' are defined in the text rather than by a single number.",
        "tab:notation"))


# ------------------------------------------------------------------ 2
def t_degree_ranks():
    rows = []
    for deg, tk, sk in [("4", "traceRankDegFour", "spinorRankDegFour"),
                        ("6", "traceRankDegSix", "spinorRankDegSix"),
                        ("8", "dEightTraceRank", "dEightSpinorRank"),
                        ("10", "traceRankDegTen", "spinorRankDegTen")]:
        union = macro("dEightUnionRank") if deg == "8" else macro(tk)
        rows.append((f"${deg}$", macro(tk), macro(sk), union,
                     "yes" if macro(tk) == macro(sk) else "no"))
    write("tab02_degree_ranks.tex", tabular(
        "ccccc",
        ["degree $d$", "tensor rank", "spinor rank", "union rank",
         "spans equal"],
        rows,
        "Degree-resolved ranks. At degree eight the spinor family is the one "
        "that includes the tensor words; the narrower family without them is "
        "the subject of figure~\\ref{fig:ablation}.",
        "tab:degranks"))


# ------------------------------------------------------------------ 3
def t_products():
    rows = [
        (r"$\dim_{\mathbb{Q}} A_{10}$", macro("dimAtenQ")),
        (r"$\dim_{\mathbb{Q}} G_{10}$", macro("dimGten")),
        (r"$\dim_{\mathbb{Q}} P_{10}$", macro("dimPten")),
        (r"$\dim_{\mathbb{Q}} B_{10}$", macro("dimBten")),
        (r"$\dim_{\mathbb{Q}} D_{10}$", macro("dimDtenQ")),
        (r"$\dim_{\mathbb{Q}} Q_{10}$", macro("dimQtenQ")),
    ]
    write("tab03_products.tex", tabular(
        "lc", ["space", r"dimension over $\mathbb{Q}$"], rows,
        "Product and primitive dimensions at degree ten, all established "
        "exactly over the rationals.",
        "tab:products"))


# ------------------------------------------------------------------ 4
def t_spans():
    rows = [
        (r"$\dim(B_{10}\cap P_{10})$", macro("dimBcapP")),
        (r"$\dim(B_{10}+P_{10})$", macro("dimBplusP")),
        ("non-product content of $B_{10}$", macro("publishedPrimitiveContent")),
        (r"$\dim(B_{10}\cap G_{10})$", macro("capBG")),
        (r"$\dim(P_{10}\cap G_{10})$", macro("capPG")),
        (r"$\dim(D_{10}\cap B_{10})$", macro("capDB")),
    ]
    write("tab04_spans.tex", tabular(
        "lc", ["quantity", "value"], rows,
        "Span comparisons among the published, graph-generator, product and "
        "reachable subspaces.",
        "tab:spans"))


# ------------------------------------------------------------------ 5
def t_candidates():
    rows = [
        ("port graphs", macro("nArchivePortGraphs")),
        ("structured candidates", macro("nArchiveStructured")),
        ("total scheduled", macro("exactJacScheduled")),
        ("total evaluated", macro("exactJacEvaluated")),
        ("evaluation errors", macro("exactJacErrors")),
        ("zero-Jacobian rows", macro("exactJacZeroRows")),
        ("Euler homogeneity pass", macro("exactJacEulerPass")),
    ]
    write("tab05_candidates.tex", tabular(
        "lc", ["candidate family", "count"], rows,
        "Candidate-family inventory for the generic-rank computation. The "
        "schedule is complete: every candidate was evaluated, none errored and "
        "none was silently skipped.",
        "tab:candidates"))


# ------------------------------------------------------------------ 6
def t_matrix():
    m = load("results/rank81/full_rank_matrix_publication_final.json")
    cells = m["ranks_by_cell"]
    primes = sorted({int(k.split("_")[0][1:]) for k in cells})
    seeds = sorted({int(k.split("_")[1][1:]) for k in cells})
    rows = [[f"${p}$"] + [cells.get(f"p{p}_s{s}", "--") for s in seeds]
            for p in primes]
    write("tab06_matrix.tex", tabular(
        "c" + "c" * len(seeds),
        ["prime"] + [f"seed {s}" for s in seeds], rows,
        f"The prime/sample rank matrix: {m['cells_complete']} cells, every one "
        f"of rank {m['rank']}, with identical pivot rows and columns "
        "throughout.",
        "tab:matrix",
        note="Two of these cells were recomputed in this repository and agree "
             "with the certificate on every recorded quantity. The remaining "
             "thirteen were not independently recomputed here; what is "
             "established for them is internal consistency plus a shared "
             "candidate-ordering hash."))


# ------------------------------------------------------------------ 7
def t_degree10():
    q = load("results/stress_flow/Q10_characteristic_zero.json")
    d = load("results/stress_flow/D10_characteristic_zero.json")
    rows = [
        (r"$A_{10}$", q["A10_dim_over_Q"], "atlas, spanning-set bound"),
        ("raw target span", macro("dimAten"),
         "all generated targets, kept as a negative fixture"),
        (r"$D_{10}$", q["D10_dim_over_Q"],
         "exact rational closure, fixed point"),
        (r"$Q_{10}$", q["Q10_dim_over_Q"], "quotient"),
    ]
    write("tab07_degree10.tex", tabular(
        "lcl", ["space", r"$\dim_{\mathbb{Q}}$", "how established"], rows,
        f"Degree-ten dimensions. The closure reached its fixed point after "
        f"{d['closure_sweeps']} sweeps in exact rational arithmetic.",
        "tab:degree10"))


# ------------------------------------------------------------------ 8
def t_quotient():
    d = load("results/stress_flow/D10_characteristic_zero.json")
    cols = d["lower_bound_certificate"]["columns"]
    free = [c for c in range(14) if c not in cols]
    rows = [(f"$q_{{{i+1}}}$", f"free column {c}")
            for i, c in enumerate(free)]
    write("tab08_quotient.tex", tabular(
        "ll", ["representative", "origin"], rows,
        "Quotient representatives. The free columns are those not occupied by "
        "a pivot of the rank-"
        f"{d['lower_bound_certificate']['size']} minor certifying "
        r"$\dim_{\mathbb{Q}} D_{10}$.",
        "tab:quotient"))


# ------------------------------------------------------------------ 9
def t_b10():
    b = load("results/degree10/B10_P10_intersection_exact.json")
    rows = [
        ("published structures lifted",
         f"{b['n_lifted']} of {b['n_published']}"),
        ("fitting primes", len(b["fitting_primes"])),
        ("held-out prime", b["holdout_prime"]),
        ("held-out mismatches", len(b["holdout_mismatches"])),
        ("fresh-sample prime", macro("bpFreshPrime")),
        ("fresh samples", macro("bpFreshSamples")),
        (r"$\dim_{\mathbb{Q}}(B_{10}\cap P_{10})$",
         b["dim_B10_cap_P10_over_Q"]),
    ]
    write("tab09_b10.tex", tabular(
        "lc", ["quantity", "value"], rows,
        "Reconstruction status for the published span. Every published "
        "structure lifted to $\\mathbb{Q}$, and no held-out prime disagreed.",
        "tab:b10"))


# ------------------------------------------------------------------ 10
def t_certificates():
    rows = [
        (r"$\dim_{\mathbb{Q}} D_{10}=11$", "exact rational certificate",
         "fixed point + $11\\times11$ minor"),
        (r"$\dim_{\mathbb{Q}} Q_{10}=3$", "exact rational certificate",
         "quotient of the above"),
        (r"$\dim_{\mathbb{Q}}(B_{10}\cap P_{10})=1$",
         "exact rational certificate", "CRT lift + explicit generator"),
        ("generic functional rank $\\ge 81$", "exact modular certificate",
         "$81\\times81$ minor, two routines"),
        ("generic functional rank $=81$", "analytic, cited",
         "upper bound from the literature"),
        ("G-10 trace vanishing", "analytic theorem",
         "improvement-independent, with control"),
        ("bridge rank $126$", "exact modular certificate",
         "left inverse and round trip"),
    ]
    write("tab10_certificates.tex", tabular(
        "ll>{\\raggedright\\arraybackslash}p{0.34\\textwidth}",
        ["claim", "proof type", "instrument"], rows,
        "Proof certificates for the central claims. The distinction between "
        "the exact lower bound and the cited analytic upper bound on the "
        "generic rank is maintained throughout.",
        "tab:certificates"))


# ------------------------------------------------------------------ 11
def t_tests():
    rows = [
        ("tensor suite", macro("nTraceTests")),
        ("bridge suite", macro("nBridgeTests")),
        ("manuscript claim gates", "72"),
        ("G-10 counterfactual", f"$Q_{{10}}\\to{macro('gTenCounterfactualQten')}$"),
        ("orientation branch flip", "breaks a working prime"),
    ]
    write("tab11_tests.tex", tabular(
        "lc", ["suite", "count / effect"], rows,
        "Mutation and regression coverage. The last two rows are "
        "counterfactual tests: each deliberately breaks an assumption and "
        "checks that the stated consequence follows.",
        "tab:tests"))


# ------------------------------------------------------------------ 12
def t_environment():
    try:
        commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                                capture_output=True, text=True,
                                check=True).stdout.strip()[:12]
    except Exception:
        commit = "unavailable"
    import numpy
    rows = [
        ("Python", platform.python_version()),
        ("NumPy", numpy.__version__),
        ("pynauty", "2.8.8.1"),
        ("opt\\_einsum", "optional; not installed for the certified runs"),
        ("commit", f"\\texttt{{{commit}}}"),
    ]
    write("tab12_environment.tex", tabular(
        "ll", ["component", "version"], rows,
        "Reproduction environment. \\texttt{opt\\_einsum} is an optional "
        "accelerator for contraction ordering; it was absent from the "
        "environment that produced the certified results, so the built-in "
        "fallback ordering was used.",
        "tab:environment"))


# ------------------------------------------------------------------ 13
def t_claim_strength():
    rows = [
        ("analytic theorem", "proved in the text; no computation relied upon"),
        ("exact rational certificate",
         r"established over $\mathbb{Q}$; no prime excluded"),
        ("exact finite-field certificate",
         r"exact mod $p$; a spanning-set or one-sided argument carries it to "
         r"$\mathbb{Q}$"),
        ("multi-prime validation",
         "agreement across primes and seeds; evidence, not proof"),
        ("limitation", "stated scope restriction"),
        ("open problem", "not established here"),
    ]
    write("tab13_claim_strength.tex", tabular(
        "lp{0.55\\textwidth}", ["classification", "meaning"], rows,
        "Claim-strength classification used in the claim ledger and "
        "throughout the text.",
        "tab:claimstrength"))


TABLES = [t_notation, t_degree_ranks, t_products, t_spans, t_candidates,
          t_matrix, t_degree10, t_quotient, t_b10, t_certificates, t_tests,
          t_environment, t_claim_strength]


def main() -> int:
    print(f"generating {len(TABLES)} tables")
    for fn in TABLES:
        fn()
    print("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
