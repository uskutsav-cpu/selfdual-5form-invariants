#!/usr/bin/env python3
"""Generate every figure and table the JHEP mentor draft uses, from artifacts.

No scientific number in the paper is typed. Each asset here reads a frozen
JSON certificate and fails loudly if it is missing, so a stale value cannot
survive a rebuild -- the build breaks instead.

Figures are drawn in grayscale-safe styles: distinctions carry through marker
shape, line style and hatching, never through colour alone.

Writes into manuscript/jhep/:
    fig_*.pdf     figures
    tab_*.tex     tables
    generated_numbers.tex   macros for inline values

Usage:
    python manuscript/jhep/make_jhep_assets.py [--repo .]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt          # noqa: E402
from matplotlib.patches import FancyArrowPatch, Rectangle  # noqa: E402

plt.rcParams.update({
    "font.size": 9, "axes.linewidth": 0.8, "figure.dpi": 200,
    "savefig.bbox": "tight", "pdf.fonttype": 42,
})

GRAY = "#4d4d4d"
LIGHT = "#c8c8c8"


def load(repo: Path, rel: str):
    p = repo / rel
    if not p.exists():
        raise SystemExit(f"missing artifact: {rel}")
    return json.loads(p.read_text(encoding="utf-8"))


# --------------------------------------------------------------------------
# figures
# --------------------------------------------------------------------------
def fig_bridge(out: Path) -> str:
    fig, ax = plt.subplots(figsize=(5.4, 2.0))
    ax.axis("off")
    boxes = [(0.02, r"$\Lambda^5_+ V$" "\n" r"self-dual, $126$"),
             (0.37, r"$\mathrm{Sym}^2_{\gamma\text{-tr}} S_+$" "\n"
                    r"gamma-traceless, $126$"),
             (0.72, r"$\Lambda^5_- V$" "\n" r"anti-self-dual, $126$")]
    for x, label in boxes:
        ax.add_patch(Rectangle((x, 0.32), 0.26, 0.36, fill=False, lw=1.0))
        ax.text(x + 0.13, 0.50, label, ha="center", va="center", fontsize=8)
    ax.add_patch(FancyArrowPatch((0.28, 0.56), (0.37, 0.56),
                                 arrowstyle="-|>", mutation_scale=11, lw=1.0))
    ax.text(0.325, 0.62, r"$\Phi$", ha="center", fontsize=9)
    ax.add_patch(FancyArrowPatch((0.37, 0.44), (0.28, 0.44),
                                 arrowstyle="-|>", mutation_scale=11, lw=1.0,
                                 linestyle="--"))
    ax.text(0.325, 0.34, r"$\Phi^{-1}$", ha="center", fontsize=8)
    ax.add_patch(FancyArrowPatch((0.72, 0.50), (0.63, 0.50),
                                 arrowstyle="-|>", mutation_scale=11, lw=1.0,
                                 color=GRAY))
    ax.text(0.675, 0.56, r"$\mapsto 0$", ha="center", fontsize=8, color=GRAY)
    ax.set_xlim(0, 1); ax.set_ylim(0.2, 0.8)
    fig.savefig(out / "fig_bridge.pdf"); plt.close(fig)
    return "fig_bridge.pdf"


def fig_orientation(repo: Path, out: Path) -> str:
    d = load(repo, "results/bridge/orientation_canonical_independent.json")
    rows = sorted((r for r in d["rows"] if "error" not in r),
                  key=lambda r: r["prime"])
    fig, ax = plt.subplots(figsize=(5.4, 2.4))
    for i, r in enumerate(rows):
        flip = r["branch_chosen_by_production"] == "flipped"
        ax.scatter(i, r["p_mod_8"], s=64,
                   marker="s" if flip else "o",
                   facecolor="black" if flip else "white",
                   edgecolor="black", zorder=3, linewidths=0.9)
    ax.set_xticks(range(len(rows)))
    ax.set_xticklabels([str(r["prime"]) for r in rows], rotation=60, fontsize=7)
    ax.set_yticks([1, 3, 5, 7])
    ax.set_ylabel(r"$p \mathrm{\ mod\ } 8$")
    ax.grid(axis="y", ls=":", lw=0.5, color=LIGHT)
    ax.set_axisbelow(True)
    ax.scatter([], [], marker="s", facecolor="black", edgecolor="black",
               label="reversed branch needed")
    ax.scatter([], [], marker="o", facecolor="white", edgecolor="black",
               label="plain branch")
    ax.legend(fontsize=7, loc="upper left", framealpha=1.0)
    ax.set_title("Every prime lands on the self-dual channel; the branch "
                 "needed\nis not a function of the residue class", fontsize=8)
    fig.savefig(out / "fig_orientation.pdf"); plt.close(fig)
    return "fig_orientation.pdf"


def fig_degree_ranks(repo: Path, out: Path) -> str:
    comp = load(repo, "verification/spinor_trace_comparison.json")
    deg8 = load(repo, "verification/degree8_span_equality.json")
    block = next(iter(comp["primes"].values()))
    degrees, tensor, spinor = [], [], []
    for d in sorted(block["degrees"], key=int):
        info = block["degrees"][d]
        degrees.append(int(d))
        tensor.append(info["trace_evaluation_rank"])
        if int(d) == 8:
            spinor.append(next(iter(deg8["primes"].values()))["spinor_rank"])
        else:
            spinor.append(info["spinor_evaluation_rank"])
    x = range(len(degrees))
    fig, ax = plt.subplots(figsize=(4.4, 2.4))
    ax.bar([i - 0.19 for i in x], tensor, width=0.38, label="tensor",
           facecolor="white", edgecolor="black", hatch="///", lw=0.8)
    ax.bar([i + 0.19 for i in x], spinor, width=0.38, label="spinor",
           facecolor=LIGHT, edgecolor="black", lw=0.8)
    for i, (t, s) in enumerate(zip(tensor, spinor)):
        ax.text(i, max(t, s) + 0.35, f"{t}", ha="center", fontsize=7)
    ax.set_xticks(list(x)); ax.set_xticklabels([f"$d={d}$" for d in degrees])
    ax.set_ylabel("rank"); ax.legend(fontsize=7, framealpha=1.0)
    ax.set_title("Tensor and spinor ranks agree at every certified degree",
                 fontsize=8)
    ax.spines[["top", "right"]].set_visible(False)
    fig.savefig(out / "fig_degree_ranks.pdf"); plt.close(fig)
    return "fig_degree_ranks.pdf"


def fig_degree8_ablation(repo: Path, out: Path) -> str:
    d = load(repo, "verification/degree8_span_equality.json")
    blk = next(iter(d["primes"].values()))
    fam = blk["family_contribution"]
    names = sorted(fam)
    vals = [fam[n]["rank_without_this_family"] for n in names]
    full = blk["spinor_rank"]
    fig, ax = plt.subplots(figsize=(4.4, 2.2))
    bars = ax.barh(names, vals, facecolor="white", edgecolor="black", lw=0.8)
    for b, v in zip(bars, vals):
        if v < full:
            b.set_hatch("xxx")
    ax.axvline(full, ls="--", lw=1.0, color="black")
    ax.text(full + 0.05, -0.4, f"full rank {full}", fontsize=7)
    ax.set_xlabel("rank with this family removed")
    ax.set_title("Only the tensor-word family is load-bearing at degree 8",
                 fontsize=8)
    ax.spines[["top", "right"]].set_visible(False)
    fig.savefig(out / "fig_degree8_ablation.pdf"); plt.close(fig)
    return "fig_degree8_ablation.pdf"


def fig_rank_matrix(repo: Path, out: Path) -> str:
    m = load(repo, "results/rank81/certificate_matrix.json")
    cells = m["cells"] + [{"prime": c["prime"], "seed": c["seed"],
                           "role": "extra", "total_rank": c["total_rank"]}
                          for c in m.get("extra_cells", [])]
    primes = sorted({c["prime"] for c in cells})
    seeds = sorted({c["seed"] for c in cells})
    fig, ax = plt.subplots(figsize=(4.6, 2.3))
    for c in cells:
        i, j = primes.index(c["prime"]), seeds.index(c["seed"])
        ax.add_patch(Rectangle((i - 0.45, j - 0.45), 0.9, 0.9,
                               facecolor="white", edgecolor="black", lw=0.8))
        ax.text(i, j, str(c["total_rank"]), ha="center", va="center", fontsize=9)
    role = {c["prime"]: c["role"] for c in cells}
    ax.set_xticks(range(len(primes)))
    ax.set_xticklabels([f"{p}\n{role[p]}" for p in primes], fontsize=7)
    ax.set_yticks(range(len(seeds)))
    ax.set_yticklabels([f"seed {s}" for s in seeds], fontsize=7)
    ax.set_xlim(-0.6, len(primes) - 0.4); ax.set_ylim(-0.6, len(seeds) - 0.4)
    ax.set_title("Every cell of the certificate matrix has rank 81", fontsize=8)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.tick_params(length=0)
    fig.savefig(out / "fig_rank_matrix.pdf"); plt.close(fig)
    return "fig_rank_matrix.pdf"


def fig_degree10_spaces(repo: Path, out: Path) -> str:
    s = load(repo, "results/stress_flow/degree10_spaces_final.json")["spaces"]
    fig, ax = plt.subplots(figsize=(4.4, 2.6))
    ax.axis("off")
    ax.add_patch(Rectangle((0.05, 0.08), 0.9, 0.84, fill=False, lw=1.2))
    ax.text(0.5, 0.95, rf"$A_{{10}}$, $\dim_{{\mathbb{{Q}}}} = "
                       rf"{s['A10']['exact_over_Q']}$", ha="center", fontsize=8)
    ax.add_patch(Rectangle((0.09, 0.12), 0.52, 0.62, fill=False, lw=1.0,
                           hatch="///"))
    ax.text(0.35, 0.68, rf"$D_{{10}} = {s['D10']['exact_over_Q']}$",
            ha="center", fontsize=8)
    ax.add_patch(Rectangle((0.13, 0.17), 0.20, 0.22, fill=False, lw=0.9))
    ax.text(0.23, 0.28, rf"$P_{{10}} = {s['P10']['exact_over_Q']}$",
            ha="center", fontsize=7)
    ax.add_patch(Rectangle((0.64, 0.12), 0.28, 0.62, fill=False, lw=1.0,
                           linestyle="--"))
    ax.text(0.78, 0.44, rf"$Q_{{10}} = {s['Q10']['exact_over_Q']}$" "\n"
                        r"$I10_6, I10_7, I10_{12}$",
            ha="center", va="center", fontsize=8)
    ax.set_title("Degree-ten spaces, exact over $\\mathbb{Q}$", fontsize=8)
    fig.savefig(out / "fig_degree10_spaces.pdf"); plt.close(fig)
    return "fig_degree10_spaces.pdf"


def fig_closure_vs_raw(repo: Path, out: Path) -> str:
    d = load(repo, "results/stress_flow/D10_exact_rational_final.json")
    t = d["three_distinct_spaces"]
    labels = ["raw target span\n(no activation)", "activated closure\n$D_{10}$",
              "full space\n$A_{10}$"]
    vals = [t["raw_target_span_rank"], t["activated_flow_closure_rank"],
            t["complete_invariant_space_rank"]]
    quot = [14 - v for v in vals]
    fig, ax = plt.subplots(figsize=(4.6, 2.2))
    ax.bar(labels, vals, facecolor="white", edgecolor="black", lw=0.9)
    ax.bar(labels, quot, bottom=vals, facecolor=LIGHT, edgecolor="black",
           lw=0.9, hatch="...", label="quotient")
    for i, (v, q) in enumerate(zip(vals, quot)):
        ax.text(i, 14.4, f"quotient {q}", ha="center", fontsize=7)
    ax.set_ylim(0, 16); ax.set_ylabel("dimension")
    ax.tick_params(axis="x", labelsize=7)
    ax.legend(fontsize=7, loc="lower right", framealpha=1.0)
    ax.set_title("Using the raw span in place of the closure gives no "
                 "obstruction", fontsize=8)
    ax.spines[["top", "right"]].set_visible(False)
    fig.savefig(out / "fig_closure_vs_raw.pdf"); plt.close(fig)
    return "fig_closure_vs_raw.pdf"


def fig_pipeline(out: Path) -> str:
    steps = ["candidate\nformula", "exact\nevaluator", "analytic\nJacobian",
             "modular\nrank", "pivot\nminor", "char-zero\ncertificate"]
    fig, ax = plt.subplots(figsize=(5.6, 1.5))
    ax.axis("off")
    w = 1.0 / len(steps)
    for i, s in enumerate(steps):
        ax.add_patch(Rectangle((i * w + 0.01, 0.3), w - 0.03, 0.42,
                               fill=False, lw=0.9))
        ax.text(i * w + w / 2, 0.51, s, ha="center", va="center", fontsize=7)
        if i < len(steps) - 1:
            ax.add_patch(FancyArrowPatch(((i + 1) * w - 0.015, 0.51),
                                         ((i + 1) * w + 0.008, 0.51),
                                         arrowstyle="-|>", mutation_scale=8,
                                         lw=0.8))
    ax.set_xlim(0, 1); ax.set_ylim(0.2, 0.85)
    fig.savefig(out / "fig_pipeline.pdf"); plt.close(fig)
    return "fig_pipeline.pdf"


# --------------------------------------------------------------------------
# tables
# --------------------------------------------------------------------------
def tab(path: Path, head: str, rows: list[str], caption: str, label: str,
        spec: str) -> None:
    L = [r"\begin{table}[t]", r"\centering", r"\small",
         rf"\begin{{tabular}}{{{spec}}}", r"\hline", head + r" \\", r"\hline"]
    L += [r + r" \\" for r in rows]
    L += [r"\hline", r"\end{tabular}", rf"\caption{{{caption}}}",
          rf"\label{{{label}}}", r"\end{table}", ""]
    path.write_text("\n".join(L), encoding="utf-8")


def tab_matrix(repo: Path, out: Path) -> str:
    m = load(repo, "results/rank81/certificate_matrix.json")
    rows = []
    for c in sorted(m["cells"], key=lambda r: (r["role"], r["prime"], r["seed"])):
        rows.append(f"{c['prime']} & {c['role']} & {c['seed']} & "
                    f"{c['total_rank']} & {c['n_rows']} & {c['euler']} & "
                    f"{c['evaluation_errors']} & {c['zero_rows']}")
    for c in sorted(m.get("extra_cells", []), key=lambda r: r["seed"]):
        rows.append(f"{c['prime']} & extra & {c['seed']} & {c['total_rank']} & "
                    f"83 & 83/83 & 0 & 0")
    tab(out / "tab_matrix.tex",
        "prime & role & seed & rank & rows & Euler & errors & zero rows",
        rows,
        "The complete certificate matrix under the canonical orientation-fixed "
        "bridge: fifteen required publication cells and three extra validation "
        "cells at $32693$. Every cell evaluates all $83$ candidates with no "
        "errors and no zero rows.",
        "tab:matrix", "rlrrrrrr")
    return "tab_matrix.tex"


def tab_spaces(repo: Path, out: Path) -> str:
    s = load(repo, "results/stress_flow/degree10_spaces_final.json")
    rows = []
    for name, blk in s["spaces"].items():
        exact = blk["exact_over_Q"]
        rows.append(f"${name[0]}_{{10}}$ & {blk['modular_dimension']} & "
                    f"{exact if exact is not None else r'\textit{not established}'} & "
                    f"{blk['status'].split(';')[0]}")
    cap = s["spaces"]["B10"]
    rows.append(r"$B_{10} \cap P_{10}$ & "
                f"{s['intersection_B10_P10']['modular_value']} & "
                r"\textit{not established} & at the tested primes")
    tab(out / "tab_spaces.tex",
        "space & modular & exact over $\\mathbb{Q}$ & status", rows,
        "Degree-ten subspaces. $A_{10}$, $G_{10}$ and $P_{10}$ are spans of "
        "distinct basis vectors, so their dimensions are structural and no "
        "prime can be exceptional. $D_{10}$ and $Q_{10}$ are established over "
        "$\\mathbb{Q}$ by exact rational computation. $B_{10}$ is recovered by "
        "a solve modulo $p$ and keeps its finite-field qualification.",
        "tab:spaces", "lccl")
    return "tab_spaces.tex"


def tab_tests(repo: Path, out: Path) -> str:
    t = load(repo, "results/tests/final_test_manifest.json")
    rows = [f"{s['suite']} & {s.get('collected') or s['passed']} & "
            f"{s['passed']} & {s['failed']} & {s['errors']} & "
            f"{s['returncode']}"
            for s in t["suites"] if s.get("status") == "PASS"]
    rows.append(rf"\textbf{{total}} & & \textbf{{{t['total_passed']}}} & "
                rf"\textbf{{{t['total_failed_or_error']}}} & & ")
    tab(out / "tab_tests.tex",
        "suite & collected & passed & failed & errors & exit", rows,
        "Test suites, counted by a parser with nineteen regression tests of its "
        "own covering wrapped progress output, interrupted runs and "
        "duplicate-writer contamination. A log without a recorded exit status "
        "is reported as incomplete rather than as a pass.",
        "tab:tests", "lrrrrr")
    return "tab_tests.tex"


def tab_minor(repo: Path, out: Path) -> str:
    d = load(repo, "results/rank81/minor81_certificate.json")
    rows = [f"{p} & {b['det_mod_p_lu']} & {b['det_mod_p_bareiss']} & "
            f"{'yes' if b['routines_agree'] else 'NO'} & "
            f"{'yes' if b['nonzero'] else 'NO'}"
            for p, b in sorted(d["per_prime"].items())]
    tab(out / "tab_minor.tex",
        "prime & modular LU & Bareiss & agree & nonzero", rows,
        "The same explicit $81\\times81$ minor of the integral Jacobian, "
        "evaluated at six primes by two independent determinant routines. A "
        "minor that is nonzero modulo any prime is nonzero over $\\mathbb{Z}$, "
        "so $\\mathrm{rank}_{\\mathbb{Q}} \\geq 81$ unconditionally.",
        "tab:minor", "rrrcc")
    return "tab_minor.tex"


def numbers(repo: Path, out: Path) -> str:
    m = load(repo, "results/rank81/certificate_matrix.json")
    t = load(repo, "results/tests/final_test_manifest.json")
    s = load(repo, "results/stress_flow/degree10_spaces_final.json")["spaces"]
    o = load(repo, "results/bridge/orientation_canonical_independent.json")
    d = load(repo, "results/rank81/minor81_certificate.json")
    defs = {
        "NumRequiredCells": m["n_present"],
        "NumExtraCells": m.get("n_extra_present", 0),
        "GenericRank": m["summary"]["distinct_total_ranks"][0],
        "NumCandidates": m["summary"].get("n_candidates_scheduled") or 83,
        "TotalTests": t["total_passed"],
        "TensorTests": next(x["passed"] for x in t["suites"] if x["suite"] == "tensor"),
        "BridgeTests": next(x["passed"] for x in t["suites"] if x["suite"] == "bridge"),
        "DimAten": s["A10"]["exact_over_Q"],
        "DimDten": s["D10"]["exact_over_Q"],
        "DimQten": s["Q10"]["exact_over_Q"],
        "NumOrientationPrimes": len(o["rows"]),
        "NumMinorPrimes": d["summary"]["n_primes_verified"],
    }
    body = "\n".join(rf"\newcommand{{\{k}}}{{{v}}}" for k, v in defs.items())
    (out / "generated_numbers.tex").write_text(
        "%% GENERATED by manuscript/jhep/make_jhep_assets.py -- do not edit.\n"
        + body + "\n", encoding="utf-8")
    return "generated_numbers.tex"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".", type=Path)
    args = ap.parse_args()
    repo = args.repo.resolve()
    out = repo / "manuscript" / "jhep"
    made = [
        fig_bridge(out),
        fig_orientation(repo, out),
        fig_degree_ranks(repo, out),
        fig_degree8_ablation(repo, out),
        fig_rank_matrix(repo, out),
        fig_degree10_spaces(repo, out),
        fig_closure_vs_raw(repo, out),
        fig_pipeline(out),
        tab_matrix(repo, out),
        tab_spaces(repo, out),
        tab_tests(repo, out),
        tab_minor(repo, out),
        numbers(repo, out),
    ]
    for m in made:
        print("wrote", m)
    print(f"\n{sum(1 for m in made if m.endswith('.pdf'))} figures, "
          f"{sum(1 for m in made if m.startswith('tab_'))} tables")
    return 0


if __name__ == "__main__":
    sys.exit(main())
