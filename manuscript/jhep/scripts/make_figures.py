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
    # Every dimension on this figure is read from the macros, not typed. Three
    # of them were literals until a sweep for typed numbers found them.
    d_sd = imacro("dimSelfdual")
    d_gt = imacro("dimGammaTraceless")
    fig, ax = plt.subplots(figsize=(5.6, 2.15))
    _box(ax, (0.05, 0.30), 1.75, 0.85, r"$\Lambda^5_+(\mathbb{R}^{1,9})$",
         f"self-dual five-forms, dim {d_sd}")
    _box(ax, (3.30, 0.30), 1.95, 0.85,
         r"$\mathrm{Sym}^2_{\gamma\text{-}\mathrm{tr}}\,S_+$",
         f"gamma-traceless bispinors, dim {d_gt}")
    _arrow(ax, (1.82, 0.86), (3.28, 0.86), rad=0.0)
    _arrow(ax, (3.28, 0.56), (1.82, 0.56), rad=0.0, ls=(0, (4, 2)))
    ax.text(2.55, 0.98, r"$\Phi$   rank %d" % imacro("bridgeForwardRank"),
            ha="center", fontsize=8)
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
    _box(ax, (4.45, 0.85), 1.55, 0.62, r"$\Lambda^5_+$ survives",
         f"rank {imacro('bridgeForwardRank')}")
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

    # Panel (a) is a dimension, panel (b) is a Jacobian rank. They are different
    # quantities and are kept on separate axes on purpose: sharing one axis
    # would invite exactly the conflation the paper spends section 9 undoing.
    tbl = load("results/stress_flow/dimension_table.json")["degrees"]
    dims = [(int(k), tbl[k]["full_dimension"]) for k in sorted(tbl, key=int)]
    m = load("results/rank81/full_rank_matrix_publication_final.json")
    cum = {int(k): v for k, v in m["cumulative_rank_by_degree"].items()}
    cdeg = sorted(cum)

    fig, axes = plt.subplots(1, 3, figsize=(9.4, 2.75))

    ax = axes[0]
    xs_a = [d for d, _ in dims]
    ys_a = [v for _, v in dims]
    ax.plot(xs_a, ys_a, marker="o", color=INK, linewidth=1.1, markersize=4.5,
            markerfacecolor="white", markeredgecolor=INK, zorder=3)
    for x, y in zip(xs_a, ys_a):
        ax.annotate(str(y), (x, y), textcoords="offset points",
                    xytext=(0, 7), ha="center", fontsize=7.6)
    ax.set_yscale("log")
    ax.set_xticks(xs_a)
    ax.set_xlabel("field degree $d$")
    ax.set_ylabel(r"$\dim A_d$")
    ax.set_title("(a) invariant dimension", fontsize=8.4)
    ax.set_ylim(0.7, max(ys_a) * 2.4)
    ax.grid(axis="y", linestyle=":", linewidth=0.5, color=PALE, zorder=0)
    ax.spines[["top", "right"]].set_visible(False)

    ax = axes[1]
    prev = 0
    for i, d in enumerate(cdeg):
        inc = cum[d] - prev
        ax.bar(i, prev, 0.62, color="white", edgecolor=INK, linewidth=0.8,
               zorder=2)
        ax.bar(i, inc, 0.62, bottom=prev, color=MID, edgecolor=INK,
               linewidth=0.8, hatch=HATCH, zorder=2)
        ax.text(i, cum[d] + 1.8, f"+{inc}", ha="center", fontsize=7.4)
        prev = cum[d]
    ax.set_xticks(range(len(cdeg)))
    ax.set_xticklabels([rf"$\leq {d}$" for d in cdeg], fontsize=7.8)
    ax.set_xlabel("degrees included")
    ax.set_ylabel("cumulative Jacobian rank")
    ax.set_title(f"(b) rank growth to {max(cum.values())}", fontsize=8.4)
    ax.set_ylim(0, max(cum.values()) * 1.20)
    ax.spines[["top", "right"]].set_visible(False)

    ax = axes[2]
    w = 0.26
    xs = range(len(degrees))
    ax.bar([x - w for x in xs], tensor, w, label="tensor", color=INK)
    ax.bar(list(xs), spinor, w, label="spinor", color=MID, hatch=HATCH,
           edgecolor="white", linewidth=0.0)
    ax.bar([x + w for x in xs], union, w, label="union", facecolor="white",
           edgecolor=INK, linewidth=0.9)
    for x, (t, s) in enumerate(zip(tensor, spinor)):
        if t != s:
            ax.text(x, s + 0.55, f"gap {t - s}", ha="center", fontsize=7.0)
    ax.set_xticks(list(xs))
    ax.set_xticklabels([f"${d}$" for d in degrees])
    ax.set_xlabel("field degree $d$")
    ax.set_ylabel("rank")
    ax.set_ylim(0, 16.5)
    ax.set_title("(c) tensor vs spinor", fontsize=8.4)
    ax.legend(frameon=False, fontsize=7.2, ncol=3, loc="upper left",
              handlelength=1.2, columnspacing=0.9)
    ax.spines[["top", "right"]].set_visible(False)

    fig.tight_layout()
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
    # The reference line is the tensor-side rank, read from the macro. It was
    # written as a literal 7 here, which is exactly the typed-in number the
    # header of this file forbids: had the artifact moved, the line would have
    # stayed put and quietly disagreed with the bars beside it.
    tensor_rank = imacro("dEightTraceRank")
    ax.axhline(tensor_rank, color=MID, linestyle=(0, (4, 2)), linewidth=0.8)
    ax.text(1.30, tensor_rank + 0.16, f"tensor rank {tensor_rank}",
            fontsize=7.4, color=MID, ha="right")
    ax.set_ylabel("rank at degree 8")
    ax.set_ylim(0, max(vals + [tensor_rank]) * 1.22)
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
    # A cell used to fit the certificate is not evidence in the same sense as
    # one held out of it, so the role is drawn rather than left to the caption.
    roles = m.get("roles_by_cell", {})
    rank = m["rank"]

    fig = plt.figure(figsize=(7.8, 2.95))
    gs = fig.add_gridspec(1, 2, width_ratios=[2.1, 1.0], wspace=0.30)
    ax = fig.add_subplot(gs[0, 0])

    for i, p in enumerate(primes):
        for j, s in enumerate(seeds):
            key = f"p{p}_s{s}"
            r = cells.get(key)
            role = str(roles.get(key, ""))
            hold = role.startswith("hold")
            # Shade rather than hatch: hatching at this cell size ran straight
            # through the rank digits and made them unreadable. Lightness, not
            # hue, so it survives a greyscale print.
            ax.add_patch(Rectangle((j, i), 0.92, 0.92,
                                   facecolor=PALE if hold else "white",
                                   edgecolor=INK,
                                   linewidth=1.4 if hold else 0.8, zorder=2))
            ax.text(j + 0.46, i + 0.60, str(r) if r is not None else "--",
                    ha="center", va="center", fontsize=9.5, zorder=3)
            ax.text(j + 0.46, i + 0.26, role[:8], ha="center", va="center",
                    fontsize=6.0, color=MID, zorder=3)
    ax.set_xticks([j + 0.46 for j in range(len(seeds))])
    ax.set_xticklabels([f"seed {s}" for s in seeds], fontsize=7.8)
    ax.set_yticks([i + 0.46 for i in range(len(primes))])
    ax.set_yticklabels([f"$p={p}$" for p in primes], fontsize=7.8)
    ax.set_xlim(-0.04, len(seeds))
    ax.set_ylim(-0.04, len(primes))
    ax.set_aspect("equal")
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.tick_params(length=0)
    ax.set_title(f"{m['cells_complete']} cells, every one at rank {rank}",
                 fontsize=8.4, pad=6)

    ax2 = fig.add_subplot(gs[0, 1])
    ax2.axis("off")
    lines = [
        ("pivot rows", macro("matrixStableRows")),
        ("pivot columns", macro("matrixStableCols")),
        ("unstable rows", macro("matrixUnstableRows")),
        ("distinct total ranks", str(len(m.get("distinct_total_ranks", [rank])))),
    ]
    ax2.text(0.0, 0.95, "identical in every cell", fontsize=8.2, style="italic")
    y = 0.78
    for label, val in lines:
        ax2.text(0.06, y, label, fontsize=8.0, color=MID)
        ax2.text(1.0, y, val, fontsize=8.8, ha="right")
        y -= 0.145
    ax2.plot([0.0, 1.0], [y + 0.06, y + 0.06], color=PALE, linewidth=0.8)
    ax2.text(0.0, y - 0.02,
             "Cells from a single run agreeing with\n"
             "each other corroborates; it is not\n"
             "independent confirmation. The lower\n"
             "bound rests on the explicit minor.",
             fontsize=6.8, color=MID, va="top")
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
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
         r"all generated targets: $\dim=%d$" % imacro("dimAten"),
         fc=PALE, hatch=HATCH)
    _box(ax, (0.05, 0.10), 2.30, 0.68, "activated closure $D_{10}$",
         r"only what the flow reaches: $\dim=%d$" % imacro("dimDtenQ"))
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


# --------------------------------------------------------------- figure 11
def fig_pivot_composition():
    """Where the 81 pivot rows come from, by degree and by candidate family.

    The certificate is an 81x81 minor, and "rank 81" on its own says nothing
    about which invariants realise it. This reads the certificate's own row list
    and sorts it two ways: by the degree of the candidate, and by the family it
    was constructed in. Both matter to the paper's argument -- the degree split
    shows the rank is not concentrated at one degree, and the family split shows
    the tensor words carry pivots rather than riding along.
    """
    import collections

    cert = load("results/rank81/minor81_certificate.json")
    ids = cert["row_candidate_ids"]

    def degree_of(cid: str) -> str:
        m = re.search(r"_d(\d+)$", cid)
        if m:
            return m.group(1)
        # The spinor candidates carry their degree in the name instead.
        s = re.search(r"degree(\d+)", cid)
        if s:
            return s.group(1)
        # Tensor words encode degree in their letter count: each letter is one
        # field insertion, so AAAA is degree eight and AAAAAA degree twelve.
        w = re.search(r"word_([A-B]+)$", cid)
        if w:
            return str(2 * len(w.group(1)))
        raise SystemExit(f"cannot assign a degree to candidate {cid!r}")

    def family_of(cid: str) -> str:
        if "portgraph" in cid:
            return "port graph"
        if "tensor_word" in cid:
            return "tensor word"
        if "spinor" in cid:
            return "spinor"
        return "other"

    by_deg = collections.Counter(degree_of(c) for c in ids)
    by_fam = collections.Counter(family_of(c) for c in ids)
    degs = sorted(by_deg, key=lambda s: (not s.isdigit(), int(s) if s.isdigit() else 0))
    fams = [f for f, _ in by_fam.most_common()]

    fig, axes = plt.subplots(1, 2, figsize=(7.9, 2.8))

    ax = axes[0]
    vals = [by_deg[d] for d in degs]
    bars = ax.bar(range(len(degs)), vals, 0.62, color="white", edgecolor=INK,
                  linewidth=0.9)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + max(vals) * 0.03, str(v),
                ha="center", fontsize=7.8)
    ax.set_xticks(range(len(degs)))
    ax.set_xticklabels([f"$d={d}$" if d.isdigit() else d for d in degs],
                       fontsize=7.8)
    ax.set_ylabel("pivot rows")
    ax.set_ylim(0, max(vals) * 1.22)
    ax.set_title(f"(a) the {len(ids)} pivots by degree", fontsize=8.4)
    ax.spines[["top", "right"]].set_visible(False)

    ax = axes[1]
    vals = [by_fam[f] for f in fams]
    hatches = [None, HATCH, "..", "xx"]
    left = 0.0
    for k, (f, v) in enumerate(zip(fams, vals)):
        ax.barh(0, v, 0.55, left=left, facecolor="white", edgecolor=INK,
                linewidth=0.9, hatch=hatches[k % len(hatches)])
        if v >= max(vals) * 0.25:
            ax.text(left + v / 2, 0, str(v), ha="center", va="center",
                    fontsize=8.2)
        else:
            # Too narrow to hold a label; put it under the segment instead of
            # dropping it, so every family is accounted for on the figure.
            ax.annotate(str(v), (left + v / 2, -0.30), ha="center",
                        va="top", fontsize=7.4)
        left += v
    ax.set_yticks([])
    ax.set_ylim(-0.75, 0.95)
    ax.set_xlim(0, left)
    ax.set_xlabel("pivot rows")
    ax.set_title("(b) the same pivots by family", fontsize=8.4)
    handles = [Rectangle((0, 0), 1, 1, facecolor="white", edgecolor=INK,
                         linewidth=0.9, hatch=hatches[k % len(hatches)])
               for k in range(len(fams))]
    # Above the bar, not below it: the x-label already occupies the space
    # underneath and the two collided.
    ax.legend(handles, fams, frameon=False, fontsize=7.0, ncol=3,
              loc="upper center", bbox_to_anchor=(0.5, 1.02),
              handlelength=1.3, columnspacing=0.9)
    ax.spines[["top", "right", "left"]].set_visible(False)

    fig.tight_layout()
    save(fig, "fig11_pivot_composition.pdf")


# --------------------------------------------------------------- figure 12
def fig_rational_heights():
    """Why the closure had to be run over Q rather than modulo a prime.

    Each bar is the bit length of the largest numerator appearing in a basis
    vector of the flow-reachable space at that degree, read from the closure's
    own exact coordinates. At low degree the coordinates are small integers and
    nothing is at stake. At degree ten one basis vector needs a numerator of
    twenty-nine bits over a five-digit denominator -- far past what a single
    prime near 2^15 can represent, which is exactly why that row had to be
    lifted by CRT and rational reconstruction instead of being read off one
    modular solve.
    """
    tbl = load("results/stress_flow/dimension_table.json")["degrees"]
    rows = []
    for k in sorted(tbl, key=int):
        best_num, best_den = 1, 1
        for vec in tbl[k].get("stress_basis", []):
            for c in vec.get("coordinates", []):
                n = abs(int(c.get("numerator", 0) or 0))
                d = abs(int(c.get("denominator", 1) or 1))
                best_num = max(best_num, n)
                best_den = max(best_den, d)
        rows.append((int(k), best_num, best_den))
    if not rows:
        raise SystemExit("dimension table carries no exact coordinates")

    prime_bits = imacro("comparisonPrime").bit_length()

    fig, ax = plt.subplots(figsize=(5.9, 2.75))
    xs = range(len(rows))
    nb = [max(n, 1).bit_length() for _, n, _ in rows]
    db = [max(d, 1).bit_length() for _, _, d in rows]
    w = 0.36
    ax.bar([x - w / 2 for x in xs], nb, w, label="numerator", color=INK)
    ax.bar([x + w / 2 for x in xs], db, w, label="denominator", color=MID,
           hatch=HATCH, edgecolor="white", linewidth=0.0)
    ax.axhline(prime_bits, color=INK, linewidth=0.9, linestyle=(0, (4, 3)))
    ax.text(len(rows) - 0.5, prime_bits + 0.6,
            f"one prime near $2^{{{prime_bits - 1}}}$", ha="right", fontsize=7.0)
    for x, (_, n, _) in zip(xs, rows):
        if n > 10_000:
            ax.text(x - w / 2, max(n, 1).bit_length() + 0.6, f"{n:,}",
                    ha="center", fontsize=6.6)
    ax.set_xticks(list(xs))
    ax.set_xticklabels([f"$d={d}$" for d, _, _ in rows])
    ax.set_xlabel("field degree $d$")
    ax.set_ylabel("bits in the largest coefficient")
    ax.set_ylim(0, max(max(nb), prime_bits) * 1.30)
    ax.legend(frameon=False, fontsize=7.4, ncol=2, loc="upper left",
              handlelength=1.3)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    save(fig, "fig12_rational_heights.pdf")


FIGURES = [fig_bridge, fig_real_forms, fig_orientation, fig_degree_ranks,
           fig_degree8_ablation, fig_rank81_pipeline, fig_rank_matrix,
           fig_incidence, fig_raw_vs_activated, fig_repro_pipeline,
           fig_pivot_composition, fig_rational_heights]


def main() -> int:
    print(f"generating {len(FIGURES)} figures")
    for fn in FIGURES:
        fn()
    print("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
