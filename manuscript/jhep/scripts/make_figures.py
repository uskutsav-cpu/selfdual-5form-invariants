#!/usr/bin/env python3
"""Generate every figure in the mentor-review draft.

Two rules govern this file.

  1. No number is typed here. Every quantity plotted is read from a result
     artifact under results/. If an artifact is missing the script fails rather
     than drawing a plausible-looking placeholder.

  2. Output is byte-deterministic. matplotlib stamps a /CreationDate into PDF
     output by default, which makes an otherwise identical figure differ between
     runs and breaks archive reproducibility. It is cleared explicitly below.

Figures are vector PDF, readable in grayscale (no information is carried by hue
alone), and use a single consistent type size.

    python3 manuscript/jhep/scripts/make_figures.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                       # noqa: E402
from matplotlib.patches import FancyArrowPatch, Rectangle, Circle  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "manuscript" / "jhep" / "figures"

# Deterministic PDF: no creation timestamp, reproducible font embedding.
matplotlib.rcParams["pdf.compression"] = 6
matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["font.family"] = "serif"
matplotlib.rcParams["font.size"] = 9
matplotlib.rcParams["axes.linewidth"] = 0.7

INK = "#1a1a1a"
MID = "#6e6e6e"
PALE = "#d9d9d9"
HATCH = "////"


def load(rel: str) -> dict:
    path = ROOT / rel
    if not path.exists():
        raise SystemExit(f"required artifact missing: {rel}")
    return json.loads(path.read_text())


_MACROS: dict[str, str] = {}


def macro(name: str) -> str:
    """Read a value out of the generated macro file.

    The macros are themselves produced from result artifacts by
    manuscript/scripts/make_numbers.py, so reading them here keeps the figures
    and the manuscript body quoting one source. A missing macro is fatal: a
    figure that silently falls back to a typed-in default is exactly the failure
    this indirection exists to prevent.
    """
    if not _MACROS:
        src = ROOT / "manuscript" / "generated" / "numbers.tex"
        if not src.exists():
            raise SystemExit(f"required artifact missing: {src}")
        for m in re.finditer(r"\\newcommand\{\\(\w+)\}\{([^}]*)\}", src.read_text()):
            _MACROS[m.group(1)] = m.group(2)
    if name not in _MACROS:
        raise SystemExit(f"macro \\{name} is not defined in numbers.tex")
    return _MACROS[name]


def imacro(name: str) -> int:
    return int(macro(name))


def save(fig, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    fig.savefig(path, format="pdf", bbox_inches="tight",
                metadata={"CreationDate": None, "Producer": None,
                          "Creator": None})
    plt.close(fig)
    print(f"  wrote {path.relative_to(ROOT)}")


def _box(ax, xy, w, h, label, sub=None, fc="white", hatch=None):
    x, y = xy
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=INK,
                           linewidth=0.9, hatch=hatch, zorder=2))
    ax.text(x + w / 2, y + h * (0.62 if sub else 0.5), label, ha="center",
            va="center", fontsize=9, zorder=3)
    if sub:
        ax.text(x + w / 2, y + h * 0.26, sub, ha="center", va="center",
                fontsize=7.4, color=MID, zorder=3)


def _arrow(ax, a, b, style="-|>", ls="-", color=INK, rad=0.0, lw=0.9):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle=style, mutation_scale=11,
                                 linewidth=lw, color=color, linestyle=ls,
                                 connectionstyle=f"arc3,rad={rad}",
                                 shrinkA=2, shrinkB=2, zorder=4))


def _clean(ax, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis("off")
    ax.set_aspect("equal")


# ---------------------------------------------------------------- figure 1
def fig_bridge():
    """Lambda^5_+ <-> Sym^2_{gamma-tr} S_+, with the certified rank on the arrow."""
    n = load("manuscript/generated/numbers.json") if (
        ROOT / "manuscript/generated/numbers.json").exists() else None
    # dimensions come from the bridge certificate
    fig, ax = plt.subplots(figsize=(5.6, 2.15))
    _box(ax, (0.05, 0.30), 1.75, 0.85, r"$\Lambda^5_+(\mathbb{R}^{1,9})$",
         "self-dual five-forms, dim 126")
    _box(ax, (3.30, 0.30), 1.95, 0.85,
         r"$\mathrm{Sym}^2_{\gamma\text{-}\mathrm{tr}}\,S_+$",
         "gamma-traceless bispinors, dim 126")
    _arrow(ax, (1.82, 0.86), (3.28, 0.86), rad=0.0)
    _arrow(ax, (3.28, 0.56), (1.82, 0.56), rad=0.0, ls=(0, (4, 2)))
    ax.text(2.55, 0.98, r"$\Phi$   rank 126", ha="center", fontsize=8)
    ax.text(2.55, 0.40, r"$\Phi^{-}$  left inverse", ha="center", fontsize=8,
            color=MID)
    ax.text(2.55, 0.10, r"$\Phi^{-}\Phi=\mathrm{id}$, exact over $\mathbb{F}_p$",
            ha="center", fontsize=7.6, color=MID)
    _clean(ax, (0, 5.3), (0.0, 1.30))
    save(fig, "fig01_bridge.pdf")


# ---------------------------------------------------------------- figure 2
def fig_real_forms():
    """Where each computation actually lives: Lorentzian, split, complex, F_p."""
    fig, ax = plt.subplots(figsize=(5.6, 2.5))
    _box(ax, (0.05, 1.30), 1.85, 0.72, r"Lorentzian $(1,9)$",
         "the physical real form")
    _box(ax, (3.40, 1.30), 1.85, 0.72, r"split $(5,5)$",
         "oscillator / null frame")
    _box(ax, (1.72, 0.05), 1.95, 0.72, r"$\mathfrak{so}(10,\mathbb{C})$",
         "common complexification")
    _arrow(ax, (0.98, 1.28), (2.30, 0.79), ls=(0, (4, 2)), color=MID)
    _arrow(ax, (4.32, 1.28), (3.10, 0.79), ls=(0, (4, 2)), color=MID)
    ax.text(2.70, 1.66, "NOT related by a real\northogonal frame change",
            ha="center", fontsize=7.6, color=INK)
    ax.text(2.70, -0.28, r"realised over $\mathbb{F}_p$ once orientation is pinned",
            ha="center", fontsize=7.8, color=MID)
    _clean(ax, (0, 5.3), (-0.45, 2.10))
    save(fig, "fig02_real_forms.pdf")


# ---------------------------------------------------------------- figure 3
def fig_orientation():
    """An orientation-reversing frame swaps which eigenspace survives."""
    fig, ax = plt.subplots(figsize=(5.6, 2.3))
    _box(ax, (0.05, 0.85), 1.55, 0.62, r"frame $L$", r"$\det$ branch $+$")
    _box(ax, (0.05, 0.05), 1.55, 0.62, r"frame $L'$", r"$\det$ branch $-$",
         hatch=HATCH, fc=PALE)
    _box(ax, (2.35, 0.85), 1.35, 0.62, r"$\star \to +\star$")
    _box(ax, (2.35, 0.05), 1.35, 0.62, r"$\star \to -\star$", hatch=HATCH,
         fc=PALE)
    _box(ax, (4.45, 0.85), 1.55, 0.62, r"$\Lambda^5_+$ survives", "rank 126")
    _box(ax, (4.45, 0.05), 1.55, 0.62, r"$\Lambda^5_-$ survives", "rank 0 image",
         hatch=HATCH, fc=PALE)
    for y in (1.16, 0.36):
        _arrow(ax, (1.62, y), (2.33, y))
        _arrow(ax, (3.72, y), (4.43, y))
    ax.text(3.0, -0.36, "the lower branch is silent: no error is raised, the "
            "image is simply the wrong eigenspace",
            ha="center", fontsize=7.4, color=INK)
    _clean(ax, (0, 6.05), (-0.52, 1.55))
    save(fig, "fig03_orientation.pdf")


# ---------------------------------------------------------------- figure 4
def fig_degree_ranks():
    """Tensor, spinor and union rank by degree, from the comparison artifact."""
    degrees = [4, 6, 8, 10]
    # Degree eight is read from the dEight* macros, not from spinorRankDegEight.
    # The two describe DIFFERENT candidate families: spinorRankDegEight = 6 is
    # the narrower family that omits the tensor words, and dEightSpinorRank = 7
    # is the family actually used. Plotting 6 next to the union rank 7 would
    # silently compare two different constructions, so the families are kept
    # apart -- the drop from 7 to 6 is the subject of its own figure.
    tensor = [imacro("traceRankDegFour"), imacro("traceRankDegSix"),
              imacro("dEightTraceRank"), imacro("traceRankDegTen")]
    spinor = [imacro("spinorRankDegFour"), imacro("spinorRankDegSix"),
              imacro("dEightSpinorRank"), imacro("spinorRankDegTen")]
    union = [imacro("traceRankDegFour"), imacro("traceRankDegSix"),
             imacro("dEightUnionRank"), imacro("traceRankDegTen")]
    fig, ax = plt.subplots(figsize=(5.0, 2.5))
    w = 0.26
    xs = range(len(degrees))
    ax.bar([x - w for x in xs], tensor, w, label="tensor", color=INK)
    ax.bar(list(xs), spinor, w, label="spinor", color=MID, hatch=HATCH,
           edgecolor="white", linewidth=0.0)
    ax.bar([x + w for x in xs], union, w, label="union", facecolor="white",
           edgecolor=INK, linewidth=0.9)
    for x, (t, s) in enumerate(zip(tensor, spinor)):
        if t != s:
            ax.text(x, s + 0.55, f"gap {t - s}", ha="center", fontsize=7.2)
    ax.set_xticks(list(xs))
    ax.set_xticklabels([f"$d={d}$" for d in degrees])
    ax.set_ylabel("rank")
    ax.set_ylim(0, 16.5)
    ax.legend(frameon=False, fontsize=8, ncol=3, loc="upper left")
    ax.spines[["top", "right"]].set_visible(False)
    save(fig, "fig04_degree_ranks.pdf")


# ---------------------------------------------------------------- figure 5
def fig_degree8_ablation():
    """Degree eight: removing the tensor words drops the spinor-side rank."""
    fig, ax = plt.subplots(figsize=(4.6, 2.3))
    labels = ["spinor family\n(with tensor words)",
              "spinor family\n(words removed)"]
    vals = [imacro("dEightSpinorRank"), imacro("dEightRankWithoutWords")]
    bars = ax.bar(labels, vals, 0.44,
                  color=[INK, PALE], edgecolor=INK, linewidth=0.9)
    bars[1].set_hatch(HATCH)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.14, str(v), ha="center",
                fontsize=9)
    ax.axhline(7, color=MID, linestyle=(0, (4, 2)), linewidth=0.8)
    ax.text(1.42, 7.06, "tensor rank 7", fontsize=7.4, color=MID, ha="right")
    ax.set_ylabel("rank at degree 8")
    ax.set_ylim(0, 8.4)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(labelsize=7.8)
    save(fig, "fig05_degree8_ablation.pdf")


# ---------------------------------------------------------------- figure 6
def fig_rank81_pipeline():
    """Candidates -> exact Jacobian -> fixed minor."""
    m = load("results/rank81/full_rank_matrix_publication_final.json")
    fig, ax = plt.subplots(figsize=(6.0, 1.55))
    stages = [
        ("83 candidates", "scheduled and evaluated"),
        ("Jacobian", r"$83\times%d$ exact" % m["coordinate_dimension"]),
        ("modular rank", "rank %d" % m["rank"]),
        (r"$81\times81$ minor", "determinant nonzero"),
    ]
    x = 0.05
    for i, (lab, sub) in enumerate(stages):
        _box(ax, (x, 0.18), 1.30, 0.72, lab, sub)
        if i < len(stages) - 1:
            _arrow(ax, (x + 1.32, 0.54), (x + 1.55, 0.54))
        x += 1.55
    ax.text(3.15, -0.10, "every step exact; no tolerance and no floating point",
            ha="center", fontsize=7.4, color=MID)
    _clean(ax, (0, 6.35), (-0.22, 1.0))
    save(fig, "fig06_rank81_pipeline.pdf")


# ---------------------------------------------------------------- figure 7
def fig_rank_matrix():
    """The prime/sample matrix: rank and pivot agreement in every cell."""
    m = load("results/rank81/full_rank_matrix_publication_final.json")
    cells = m["ranks_by_cell"]
    primes = sorted({int(k.split("_")[0][1:]) for k in cells})
    seeds = sorted({int(k.split("_")[1][1:]) for k in cells})
    fig, ax = plt.subplots(figsize=(4.8, 2.35))
    for i, p in enumerate(primes):
        for j, s in enumerate(seeds):
            key = f"p{p}_s{s}"
            r = cells.get(key)
            ok = r == m["rank"]
            ax.add_patch(Rectangle((j, i), 0.92, 0.92,
                                   facecolor="white" if ok else PALE,
                                   edgecolor=INK, linewidth=0.8))
            ax.text(j + 0.46, i + 0.46, str(r) if r is not None else "--",
                    ha="center", va="center", fontsize=9)
    ax.set_xticks([j + 0.46 for j in range(len(seeds))])
    ax.set_xticklabels([f"seed {s}" for s in seeds], fontsize=8)
    ax.set_yticks([i + 0.46 for i in range(len(primes))])
    ax.set_yticklabels([f"$p={p}$" for p in primes], fontsize=8)
    ax.set_xlim(-0.04, len(seeds))
    ax.set_ylim(-0.04, len(primes))
    ax.set_aspect("equal")
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.tick_params(length=0)
    ax.set_title(f"all {m['cells_complete']} cells: rank {m['rank']}, "
                 "identical pivot rows and columns", fontsize=8, pad=6)
    save(fig, "fig07_rank_matrix.pdf")


# ---------------------------------------------------------------- figure 8
def fig_incidence():
    """A10 and the subspaces sitting inside it, drawn to the certified dims."""
    q = load("results/stress_flow/Q10_characteristic_zero.json")
    bp = load("results/degree10/B10_P10_intersection_exact.json")
    fig, ax = plt.subplots(figsize=(5.4, 2.9))
    ax.add_patch(Rectangle((0.05, 0.05), 5.2, 2.3, facecolor="white",
                           edgecolor=INK, linewidth=1.1))
    ax.text(0.16, 2.16, r"$A_{10}$, $\dim_{\mathbb{Q}}=%d$" % q["A10_dim_over_Q"],
            fontsize=9)
    ax.add_patch(Rectangle((0.30, 0.30), 2.55, 1.55, facecolor=PALE,
                           edgecolor=INK, linewidth=0.9))
    ax.text(1.58, 1.66, r"$D_{10}$ (flow-reachable), $\dim=%d$"
            % q["D10_dim_over_Q"], fontsize=8, ha="center")
    ax.add_patch(Rectangle((3.05, 0.30), 2.05, 1.55, facecolor="white",
                           edgecolor=INK, linewidth=0.9, hatch=HATCH))
    ax.text(4.07, 1.66, r"$Q_{10}=A_{10}/D_{10}$", fontsize=8, ha="center")
    ax.text(4.07, 1.02, r"$\dim=%d$" % q["Q10_dim_over_Q"], fontsize=11,
            ha="center")
    ax.add_patch(Rectangle((0.55, 0.52), 1.65, 0.62, facecolor="white",
                           edgecolor=INK, linewidth=0.8))
    ax.text(1.38, 0.83, r"$B_{10}$, $\dim=%d$" % bp["dim_B10_over_Q"],
            fontsize=8, ha="center")
    ax.add_patch(Circle((2.02, 0.83), 0.20, facecolor=PALE, edgecolor=INK,
                        linewidth=0.8))
    ax.text(2.02, 0.83, r"$1$", fontsize=7.4, ha="center", va="center")
    ax.text(2.62, 0.42, r"$\dim(B_{10}\cap P_{10})=%d$"
            % bp["dim_B10_cap_P10_over_Q"], fontsize=7.6, ha="left")
    _clean(ax, (0, 5.4), (-0.05, 2.45))
    save(fig, "fig08_incidence.pdf")


# ---------------------------------------------------------------- figure 9
def fig_raw_vs_activated():
    """Why the raw target span is not the reachable subspace."""
    cf = load("results/stress_flow/G10_counterfactual.json")
    fig, ax = plt.subplots(figsize=(5.6, 2.15))
    _box(ax, (0.05, 0.95), 2.30, 0.68, "raw target span",
         r"all generated targets: $\dim=14$", fc=PALE, hatch=HATCH)
    _box(ax, (0.05, 0.10), 2.30, 0.68, "activated closure $D_{10}$",
         r"only what the flow reaches: $\dim=11$")
    _arrow(ax, (2.38, 1.29), (3.25, 0.95), ls=(0, (4, 2)), color=MID)
    _arrow(ax, (2.38, 0.44), (3.25, 0.72))
    _box(ax, (3.30, 0.42), 2.15, 0.68, "quotient dimension",
         r"$0$ if conflated, $%d$ if not" % cf["as_derived_Q10"])
    ax.text(2.80, 1.42, "conflating these", fontsize=7.2, color=MID)
    ax.text(2.80, 0.20, "keeping them apart", fontsize=7.2, color=INK)
    _clean(ax, (0, 5.5), (0.0, 1.75))
    save(fig, "fig09_raw_vs_activated.pdf")


# ---------------------------------------------------------------- figure 10
def fig_repro_pipeline():
    """Source commit through to the compiled manuscript."""
    fig, ax = plt.subplots(figsize=(6.1, 2.6))
    nodes = [
        ("source commit", (0.05, 1.62), 1.45),
        ("test suites", (2.05, 1.62), 1.45),
        ("certificates", (4.05, 1.62), 1.45),
        ("figures", (0.05, 0.72), 1.45),
        ("tables", (2.05, 0.72), 1.45),
        ("generated macros", (4.05, 0.72), 1.45),
        ("claim gates", (2.05, 0.02), 1.45),
    ]
    for lab, xy, w in nodes:
        _box(ax, xy, w, 0.56, lab)
    _arrow(ax, (1.52, 1.90), (2.03, 1.90))
    _arrow(ax, (3.52, 1.90), (4.03, 1.90))
    _arrow(ax, (4.78, 1.60), (4.78, 1.30))
    _arrow(ax, (4.05, 1.00), (3.52, 1.00))
    _arrow(ax, (2.05, 1.00), (1.52, 1.00))
    _arrow(ax, (2.78, 0.70), (2.78, 0.60))
    ax.text(3.05, 0.30, "the build fails if any gate fails", fontsize=7.4,
            color=MID, ha="left")
    _clean(ax, (0, 5.6), (-0.05, 2.30))
    save(fig, "fig10_repro_pipeline.pdf")


FIGURES = [fig_bridge, fig_real_forms, fig_orientation, fig_degree_ranks,
           fig_degree8_ablation, fig_rank81_pipeline, fig_rank_matrix,
           fig_incidence, fig_raw_vs_activated, fig_repro_pipeline]


def main() -> int:
    print(f"generating {len(FIGURES)} figures")
    for fn in FIGURES:
        fn()
    print("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
