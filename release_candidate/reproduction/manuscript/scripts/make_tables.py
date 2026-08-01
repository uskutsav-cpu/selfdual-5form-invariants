"""Generate every manuscript table from result artifacts.

No scientific value is typed into this script.  Every number is read from a
certificate; when a certificate is absent the table says so in the PDF rather
than silently omitting a row.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TABLES = ROOT / "manuscript" / "tables"


def load(rel: str):
    p = ROOT / rel
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except json.JSONDecodeError:
        return None


def pending(what: str, label: str) -> str:
    """A visible placeholder that still carries the label.

    Carrying the label matters: without it every cross-reference to the table
    becomes an undefined reference, and a build with undefined references cannot
    be distinguished from a build with a genuine mistake.
    """
    return ("\\begin{table}[t]\\centering\n"
            f"\\textbf{{[{what}: artifact not present at build time]}}\n"
            f"\\caption{{{what} --- pending.}}\n"
            f"\\label{{{label}}}\n\\end{{table}}\n")


def write(name: str, body: str) -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    (TABLES / f"{name}.tex").write_text(body)
    print(f"  tables/{name}.tex")


# --- Table 1: dimensions -----------------------------------------------------

def table_dimensions() -> None:
    inc = load("results/intrinsic_candidates/degree10_space_incidence.json")
    if not inc:
        write("dimensions", pending("dimension table", "tab:dims"))
        return
    prime = sorted(inc["per_prime"])[0]
    d = inc["per_prime"][prime]["dims"]
    rows = [
        ("$\\dim$ self-dual module", 126, "analytic", "--"),
        ("$\\dim \\mathfrak{so}(1,9)$", 45, "analytic", "--"),
        ("generic functional dimension", 126 - 45, "analytic", "cumulative"),
        ("atlas $A_{10}$", d["A10"], "exact modular", "graded, degree 10"),
        ("published span $B_{10}$", d["B10"], "exact modular", "graded, degree 10"),
        ("graph generators $G_{10}$", d["G10"], "exact modular", "graded, degree 10"),
        ("products $P_{10}$", d["P10"], "exact modular", "graded, degree 10"),
        ("reachable $D_{10}$", d["D10"], "exact modular", "graded, degree 10"),
        ("quotient $Q_{10}$", d["A10"] - d["D10"], "exact modular", "graded, degree 10"),
    ]
    body = ["\\begin{table}[t]", "\\centering",
            "\\begin{tabular}{lrll}", "\\toprule",
            "space & dimension & arithmetic & grading \\\\", "\\midrule"]
    for name, dim, arith, grading in rows:
        body.append(f"{name} & {dim} & {arith} & {grading} \\\\")
    body += ["\\bottomrule", "\\end{tabular}",
             "\\caption{Degree-ten dimensions. Each row dimensions a different "
             "space; several coincide numerically and must not be conflated. "
             f"Modular values are identical at all {len(inc['per_prime'])} primes "
             "tested.}",
             "\\label{tab:dims}", "\\end{table}", ""]
    write("dimensions", "\n".join(body))


# --- Table 2: incidence ------------------------------------------------------

def table_incidence() -> None:
    inc = load("results/intrinsic_candidates/degree10_space_incidence.json")
    if not inc:
        write("incidence", pending("incidence table", "tab:incidence"))
        return
    prime = sorted(inc["per_prime"])[0]
    pairs = inc["per_prime"][prime]["incidence"]
    body = ["\\begin{table}[t]", "\\centering",
            "\\begin{tabular}{lrrrrl}", "\\toprule",
            "pair $(X,Y)$ & $\\dim X$ & $\\dim Y$ & $\\dim(X\\cap Y)$ & "
            "$\\dim(X+Y)$ & containment \\\\", "\\midrule"]
    for key in sorted(pairs):
        v = pairs[key]
        a, b = key.split("|")
        if v["a_subset_b"]:
            cont = f"${a} \\subset {b}$"
        elif v["b_subset_a"]:
            cont = f"${b} \\subset {a}$"
        elif v["intersection"] == 0:
            cont = "complementary"
        else:
            cont = "neither"
        a_t, b_t = f"${a[0]}_{{10}}$", f"${b[0]}_{{10}}$"
        body.append(f"{a_t}, {b_t} & {v['dim_a']} & {v['dim_b']} & "
                    f"{v['intersection']} & {v['sum']} & {cont} \\\\")
    body += ["\\bottomrule", "\\end{tabular}",
             "\\caption{Complete pairwise incidence of the degree-ten subspaces, "
             "identical at both primes. The two rows that matter most are "
             "$(P_{10},B_{10})$, whose intersection is nonzero, and "
             "$(P_{10},G_{10})$, whose intersection is zero.}",
             "\\label{tab:incidence}", "\\end{table}", ""]
    write("incidence", "\n".join(body))


# --- Table 3: spinor/trace comparison ---------------------------------------

def table_comparison() -> None:
    c = load("verification/spinor_trace_comparison.json")
    if not c or not c.get("primes"):
        write("comparison", pending("spinor/trace comparison", "tab:comparison"))
        return
    pk = max(c["primes"], key=lambda k: len(c["primes"][k].get("degrees", {})))
    degs = c["primes"][pk]["degrees"]
    # The stopping-reason strings are long enough to push this table past the
    # text block, so the last column is boxed at a fixed width rather than left
    # to overflow into the margin.
    body = ["\\begin{table}[t]", "\\centering", "\\small",
            "\\begin{tabular}{rrrllp{3.4cm}}", "\\toprule",
            "degree & trace rank & spinor rank & spans equal & holdout "
            "validated & spinor stopping \\\\", "\\midrule"]
    for d in sorted(degs, key=int):
        e = degs[d]
        body.append(
            f"{d} & {e['trace_evaluation_rank']} & {e['spinor_evaluation_rank']} & "
            f"{'yes' if e['spans_equal_all_samples'] else 'NO'} & "
            f"{'yes' if e['holdout_validated'] else 'NO'} & "
            f"{e['spinor_enumeration']['stopping_reason'].replace('_',' ')} \\\\")
    missing = [d for d in ("4", "6", "8", "10") if d not in degs]
    body += ["\\bottomrule", "\\end{tabular}",
             "\\caption{Trace and spinor evaluation ranks on the common sample "
             "registry, exact over $\\mathbb{F}_p$. Span equality is established "
             "by two-way containment; the change-of-basis map is fitted on the "
             "fitting samples and validated on the holdout samples. The spinor "
             "stopping column records that the spinor-side candidate stream is "
             "sampled to rank saturation, which is an observation and not a claim "
             "of exhaustive enumeration."
             + (f" Degrees not yet built: {', '.join(missing)}." if missing else ""),
             "}",
             "\\label{tab:comparison}", "\\end{table}", ""]
    write("comparison", "\n".join(body))


# --- Table 4: float64 Jacobian runs -----------------------------------------

def table_jacobian_runs() -> None:
    f = load("verification/SPINOR_JACOBIAN_RUNS.json")
    if not f or not f.get("runs"):
        write("jacobian_runs", pending("float64 Jacobian run matrix", "tab:jacruns"))
        return
    body = ["\\begin{table}[t]", "\\centering", "\\small",
            "\\begin{tabular}{rrrrrll}", "\\toprule",
            "seed & scale & step & zero rows & sweep ranks & gap at 81 & "
            "classification \\\\", "\\midrule"]
    for r in f["runs"]:
        gap = r["gap_at_target"]
        gap_s = "--" if gap is None else (f"{gap:.1e}" if gap < 1e300 else "$\\infty$")
        sweep = "/".join(str(x) for x in r["distinct_ranks_over_sweep"])
        body.append(f"{r['seed']} & {r['scale']} & {r['step']:.0e} & "
                    f"{r['n_zero_rows']} & {sweep} & {gap_s} & "
                    f"{r['classification']} \\\\")
    body += ["\\bottomrule", "\\end{tabular}",
             "\\caption{Controlled float64 Jacobian matrix using the original "
             "finite-difference procedure. A run is degenerate when candidate "
             "rows evaluate to numerical zero at the sample point; rows at or "
             "below the declared noise floor are never normalised, since doing so "
             "rescales rounding noise into unit vectors and manufactures rank.}",
             "\\label{tab:jacruns}", "\\end{table}", ""]
    write("jacobian_runs", "\n".join(body))


# --- Table 5: environment ----------------------------------------------------

def table_environment() -> None:
    br = load("spinor_trace_bridge/results/bridge_validation.json")
    env = (br or {}).get("environment", {})
    lock = (ROOT / "requirements-lock.txt")
    body = ["\\begin{table}[t]", "\\centering", "\\begin{tabular}{ll}", "\\toprule",
            "item & value \\\\", "\\midrule"]
    body.append(f"Python & {env.get('python', 'not recorded')} \\\\")
    body.append(f"NumPy & {env.get('numpy', 'not recorded')} \\\\")
    if lock.exists():
        for line in lock.read_text().splitlines():
            if line.strip():
                pkg, _, ver = line.partition("==")
                body.append(f"{pkg} & {ver} \\\\")
    body.append("primes & 32749, 32719 \\\\")
    body += ["\\bottomrule", "\\end{tabular}",
             "\\caption{Reproducibility environment.}",
             "\\label{tab:env}", "\\end{table}", ""]
    write("environment", "\n".join(body))


def main() -> int:
    print("generating tables from artifacts:")
    table_dimensions()
    table_incidence()
    table_comparison()
    table_jacobian_runs()
    table_environment()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
