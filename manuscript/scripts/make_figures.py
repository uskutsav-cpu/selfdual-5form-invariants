"""Generate every manuscript figure from result artifacts, as vector PDFs.

No scientific number is hard-coded.  Values come from the certificates; a figure
whose artifact is absent is emitted as a placeholder that says so, so that a
missing input is visible rather than silently stale.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt          # noqa: E402
from matplotlib.patches import FancyArrowPatch, Rectangle  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
FIG = ROOT / "figures"
FIG.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.size": 9, "axes.linewidth": 0.7, "pdf.fonttype": 42,
    "savefig.bbox": "tight", "savefig.pad_inches": 0.02,
})


def load(rel: str):
    p = ROOT / rel
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except json.JSONDecodeError:
        return None


def placeholder(name: str, why: str) -> None:
    fig, ax = plt.subplots(figsize=(5, 2))
    ax.axis("off")
    ax.text(0.5, 0.5, f"[{name}]\nartifact not present at build time\n{why}",
            ha="center", va="center", color="crimson", fontsize=9)
    fig.savefig(FIG / f"{name}.pdf")
    plt.close(fig)
    print(f"  {name}.pdf  (placeholder: {why})")


# --- 1. invariant space diagram ---------------------------------------------

def fig_spaces() -> None:
    inc = load("results/intrinsic_candidates/degree10_space_incidence.json")
    if not inc:
        placeholder("invariant_space_diagram", "incidence certificate missing")
        return
    prime = sorted(inc["per_prime"])[0]
    d = inc["per_prime"][prime]["dims"]
    pairs = inc["per_prime"][prime]["incidence"]
    capPB = pairs["P10|B10"]["intersection"]

    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")

    ax.add_patch(Rectangle((0.4, 0.5), 9.2, 5.0, fill=False, lw=1.4))
    ax.text(0.6, 5.15, f"$A_{{10}}$   dim {d['A10']}", fontsize=10, weight="bold")

    ax.add_patch(Rectangle((0.8, 2.9), 4.0, 1.7, fc="#d8e6f3", ec="#3b6ea5", lw=1.0))
    ax.text(1.0, 4.25, f"$G_{{10}}$  dim {d['G10']}", fontsize=9)
    ax.text(1.0, 3.85, "graph generators", fontsize=7.5, style="italic")

    ax.add_patch(Rectangle((5.2, 2.9), 4.0, 1.7, fc="#f6e3d8", ec="#b5713a", lw=1.0))
    ax.text(5.4, 4.25, f"$P_{{10}}$  dim {d['P10']}", fontsize=9)
    ax.text(5.4, 3.85, "products", fontsize=7.5, style="italic")
    ax.text(5.0, 2.55, r"$G_{10}\cap P_{10}=0$,   $G_{10}\oplus P_{10}=A_{10}$",
            ha="center", fontsize=8)

    ax.add_patch(Rectangle((0.8, 0.85), 5.6, 1.3, fc="#e6f3d8", ec="#5a8f3b", lw=1.0))
    ax.text(1.0, 1.75, f"$B_{{10}}$  dim {d['B10']}   (published span)", fontsize=9)
    ax.text(1.0, 1.2, f"meets $P_{{10}}$ in dim {capPB}: NOT a product complement",
            fontsize=7.5, color="#8b2d2d")

    ax.add_patch(Rectangle((6.8, 0.85), 2.4, 1.3, fc="#efe1f3", ec="#7a4d94", lw=1.0))
    ax.text(6.95, 1.75, f"$D_{{10}}$  dim {d['D10']}", fontsize=9)
    ax.text(6.95, 1.2, f"$Q_{{10}}=A_{{10}}/D_{{10}}$: {d['A10']-d['D10']}", fontsize=8)

    fig.savefig(FIG / "invariant_space_diagram.pdf")
    plt.close(fig)
    print("  invariant_space_diagram.pdf")


# --- 2/3. Jacobian spectra ---------------------------------------------------

def _spectrum(entry, name, title):
    import numpy as np
    vals = entry.get("singular_values_used_around_target")
    if not vals:
        placeholder(name, "no singular values recorded")
        return
    fig, ax = plt.subplots(figsize=(4.2, 2.8))
    target = entry.get("target", 81)
    x = list(range(target - 3, target - 3 + len(vals)))
    ax.semilogy(x, [abs(v) if v else 1e-300 for v in vals], "o-", ms=4, lw=1.0)
    ax.axvline(target - 0.5, color="crimson", ls="--", lw=0.9)
    ax.set_xlabel("singular value index")
    ax.set_ylabel(r"$\sigma_i$")
    ax.set_title(title, fontsize=9)
    gap = entry.get("gap_at_target")
    if gap:
        ax.text(0.03, 0.06, f"gap at {target}: {gap:.2e}", transform=ax.transAxes,
                fontsize=7.5)
    ax.text(0.03, 0.90, f"zero rows: {entry['n_zero_rows']}",
            transform=ax.transAxes, fontsize=7.5)
    fig.savefig(FIG / f"{name}.pdf")
    plt.close(fig)
    print(f"  {name}.pdf")


def fig_spectra() -> None:
    f = load("verification/SPINOR_JACOBIAN_RUNS.json")
    if not f or not f.get("runs"):
        placeholder("jacobian_spectrum_non_degenerate", "float64 run matrix missing")
        placeholder("jacobian_spectrum_degenerate", "float64 run matrix missing")
        return
    nd = next((r for r in f["runs"] if r["classification"] == "nondegenerate generic"), None)
    dg = next((r for r in f["runs"] if r["classification"] == "degenerate sample"), None)
    if nd:
        _spectrum(nd, "jacobian_spectrum_non_degenerate",
                  f"nondegenerate: seed {nd['seed']}, scale {nd['scale']}")
    else:
        placeholder("jacobian_spectrum_non_degenerate", "no nondegenerate run in matrix")
    if dg:
        _spectrum(dg, "jacobian_spectrum_degenerate",
                  f"degenerate: seed {dg['seed']}, scale {dg['scale']}")
    else:
        placeholder("jacobian_spectrum_degenerate", "no degenerate run in matrix")


# --- 4. rank stability grid --------------------------------------------------

def fig_rank_grid() -> None:
    import numpy as np
    f = load("verification/SPINOR_JACOBIAN_RUNS.json")
    if not f or not f.get("runs"):
        placeholder("rank_stability_grid", "float64 run matrix missing")
        return
    seeds = sorted({r["seed"] for r in f["runs"]})
    scales = sorted({r["scale"] for r in f["runs"]})
    grid = np.full((len(scales), len(seeds)), np.nan)
    for r in f["runs"]:
        i, j = scales.index(r["scale"]), seeds.index(r["seed"])
        v = r["observed_rank"]
        if v is not None:
            grid[i, j] = v if np.isnan(grid[i, j]) else min(grid[i, j], v)
    fig, ax = plt.subplots(figsize=(4.4, 2.6))
    im = ax.imshow(grid, aspect="auto", cmap="viridis")
    ax.set_xticks(range(len(seeds)), [str(s) for s in seeds])
    ax.set_yticks(range(len(scales)), [str(s) for s in scales])
    ax.set_xlabel("seed"); ax.set_ylabel("scale")
    for i in range(len(scales)):
        for j in range(len(seeds)):
            v = grid[i, j]
            ax.text(j, i, "--" if np.isnan(v) else f"{int(v)}",
                    ha="center", va="center", color="w", fontsize=7)
    fig.colorbar(im, ax=ax, label="tolerance-stable rank")
    ax.set_title("float64 rank stability", fontsize=9)
    fig.savefig(FIG / "rank_stability_grid.pdf")
    plt.close(fig)
    print("  rank_stability_grid.pdf")


# --- 5. spinor/trace dimension comparison ------------------------------------

def fig_comparison() -> None:
    import numpy as np
    c = load("verification/spinor_trace_comparison.json")
    if not c or not c.get("primes"):
        placeholder("spinor_trace_rank_comparison", "comparison certificate missing")
        return
    pk = max(c["primes"], key=lambda k: len(c["primes"][k].get("degrees", {})))
    degs = c["primes"][pk]["degrees"]
    ds = sorted(degs, key=int)
    tr = [degs[d]["trace_evaluation_rank"] for d in ds]
    sp = [degs[d]["spinor_evaluation_rank"] for d in ds]
    x = np.arange(len(ds))
    fig, ax = plt.subplots(figsize=(4.4, 2.6))
    ax.bar(x - 0.18, tr, 0.36, label="tensor side")
    ax.bar(x + 0.18, sp, 0.36, label="spinor side")
    for i, d in enumerate(ds):
        if degs[d]["spans_equal_all_samples"]:
            ax.text(i, max(tr[i], sp[i]) + 0.35, "spans equal", ha="center", fontsize=6.5)
    ax.set_xticks(x, [f"deg {d}" for d in ds])
    ax.set_ylabel("evaluation rank")
    ax.legend(fontsize=7.5, frameon=False)
    ax.set_title("evaluation rank on common samples", fontsize=9)
    fig.savefig(FIG / "spinor_trace_rank_comparison.pdf")
    plt.close(fig)
    print("  spinor_trace_rank_comparison.pdf")


# --- 6. pipelines ------------------------------------------------------------

def fig_pipeline() -> None:
    stages = [
        ("contraction\ngraphs", "#d8e6f3"),
        ("canonical\nform", "#d8e6f3"),
        ("modular\nevaluation", "#e6f3d8"),
        ("rank sieve\nover $\\mathbb{F}_p$", "#e6f3d8"),
        ("atlas +\nsubspaces", "#f6e3d8"),
        ("holdout\nvalidation", "#efe1f3"),
    ]
    fig, ax = plt.subplots(figsize=(6.4, 1.5))
    ax.set_xlim(0, len(stages) * 2); ax.set_ylim(0, 2); ax.axis("off")
    for i, (label, colour) in enumerate(stages):
        ax.add_patch(Rectangle((i * 2 + 0.1, 0.4), 1.6, 1.1, fc=colour, ec="0.3", lw=0.8))
        ax.text(i * 2 + 0.9, 0.95, label, ha="center", va="center", fontsize=7.5)
        if i < len(stages) - 1:
            ax.add_patch(FancyArrowPatch((i * 2 + 1.72, 0.95), (i * 2 + 2.06, 0.95),
                                         arrowstyle="->", mutation_scale=8, lw=0.8))
    fig.savefig(FIG / "trace_pipeline.pdf")
    plt.close(fig)
    print("  trace_pipeline.pdf")


def fig_bridge_diagram() -> None:
    br = load("spinor_trace_bridge/results/bridge_validation.json")
    if not br:
        placeholder("bridge_diagram", "bridge certificate missing")
        return
    one = br["primes"][sorted(br["primes"])[0]]["bridge"]
    fig, ax = plt.subplots(figsize=(6.0, 2.4))
    ax.set_xlim(0, 10); ax.set_ylim(0, 4); ax.axis("off")
    ax.add_patch(Rectangle((0.3, 2.1), 3.4, 1.3, fc="#d8e6f3", ec="#3b6ea5"))
    ax.text(2.0, 2.95, "self-dual five-forms", ha="center", fontsize=8.5)
    ax.text(2.0, 2.45, f"dim {one['selfdual_dim']}, Lorentzian frame",
            ha="center", fontsize=7)
    ax.add_patch(Rectangle((6.3, 2.1), 3.4, 1.3, fc="#f6e3d8", ec="#b5713a"))
    ax.text(8.0, 2.95, "gamma-traceless $\\mathrm{Sym}^2$", ha="center", fontsize=8.5)
    ax.text(8.0, 2.45, f"dim {one['image_dim']}, null frame (5,5)",
            ha="center", fontsize=7)
    ax.add_patch(FancyArrowPatch((3.8, 2.95), (6.2, 2.95), arrowstyle="->",
                                 mutation_scale=10, lw=1.0))
    ax.text(5.0, 3.15, r"$S_{ab}=\frac{1}{5!}F_{\mu_1\ldots\mu_5}"
                       r"\Gamma^{\mu_1\ldots\mu_5}_{ab}$", ha="center", fontsize=7.5)
    ax.add_patch(FancyArrowPatch((6.2, 2.35), (3.8, 2.35), arrowstyle="->",
                                 mutation_scale=10, lw=1.0, linestyle="dashed"))
    ax.text(5.0, 2.05, "verified left inverse", ha="center", fontsize=7)
    ax.add_patch(Rectangle((0.3, 0.3), 9.4, 1.3, fc="#f2f2f2", ec="0.6"))
    ax.text(5.0, 1.15, "anti-self-dual $\\to 0$ (kernel equals the "
                       f"{one['antiselfdual_dim']}, by span equality)",
            ha="center", fontsize=7.5)
    ax.text(5.0, 0.62, "exact over $\\mathbb{F}_p$; no tolerance anywhere",
            ha="center", fontsize=7.5, style="italic")
    fig.savefig(FIG / "bridge_diagram.pdf")
    plt.close(fig)
    print("  bridge_diagram.pdf")


def main() -> int:
    print("generating figures from artifacts:")
    fig_spaces()
    fig_spectra()
    fig_rank_grid()
    fig_comparison()
    fig_pipeline()
    fig_bridge_diagram()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
