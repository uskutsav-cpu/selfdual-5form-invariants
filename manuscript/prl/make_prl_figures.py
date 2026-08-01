"""PRL figures, generated from result artifacts and readable in grayscale.

APS asks that figures not rely on colour alone.  Every distinction here is
carried by a label, a line style or a hatch as well as by fill, so the figures
survive a monochrome print.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                       # noqa: E402
from matplotlib.patches import FancyArrowPatch, Rectangle  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "manuscript" / "prl" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.size": 8, "axes.linewidth": 0.6, "pdf.fonttype": 42,
    "savefig.bbox": "tight", "savefig.pad_inches": 0.02,
    "text.usetex": False,
})

COL = 3.4          # single PRL column, inches


def load(rel: str):
    p = ROOT / rel
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except json.JSONDecodeError:
        return None


def missing(name: str, why: str) -> None:
    fig, ax = plt.subplots(figsize=(COL, 1.4))
    ax.axis("off")
    ax.text(0.5, 0.5, f"[{name}]\nartifact missing at build time\n{why}",
            ha="center", va="center", color="crimson", fontsize=7)
    fig.savefig(OUT / f"{name}.pdf")
    plt.close(fig)
    print(f"  {name}.pdf (placeholder: {why})")


def fig_spaces() -> None:
    inc = load("results/intrinsic_candidates/degree10_space_incidence.json")
    if not inc:
        missing("prl_spaces", "incidence certificate absent")
        return
    prime = sorted(inc["per_prime"])[0]
    d = inc["per_prime"][prime]["dims"]
    q = d["A10"] - d["D10"]

    fig, ax = plt.subplots(figsize=(COL, 2.05))
    ax.set_xlim(0, 10); ax.set_ylim(0, 6.2); ax.axis("off")

    # outer: the whole degree-ten space
    ax.add_patch(Rectangle((0.2, 0.35), 9.6, 5.5, fill=False, lw=1.3))
    ax.text(0.45, 5.42, rf"$\mathcal{{A}}_{{10}}$: all degree-10 invariants, dim {d['A10']}",
            fontsize=8, weight="bold")

    # reachable sector
    ax.add_patch(Rectangle((0.6, 0.75), 6.6, 4.2, fc="0.87", ec="k", lw=0.9))
    ax.text(0.85, 4.45, rf"$\mathcal{{D}}_{{10}}$ reachable by the stress flow, dim {d['D10']}",
            fontsize=7.5)

    # products, inside the reachable sector
    ax.add_patch(Rectangle((1.0, 1.15), 3.0, 1.5, fc="0.72", ec="k", lw=0.9,
                           hatch="///"))
    ax.text(1.2, 2.15, rf"$\mathcal{{P}}_{{10}}$ products", fontsize=7)
    ax.text(1.2, 1.6, rf"dim {d['P10']}", fontsize=7)
    ax.text(1.0, 0.95, r"$\mathcal{P}_{10}\subset\mathcal{D}_{10}$: every product is reachable",
            fontsize=6.5, style="italic")

    # the quotient
    ax.add_patch(Rectangle((7.6, 0.75), 2.0, 4.2, fc="w", ec="k", lw=1.2,
                           hatch="xxx"))
    ax.text(8.6, 3.5, rf"$\mathcal{{Q}}_{{10}}$", fontsize=9, ha="center")
    ax.text(8.6, 2.85, rf"dim {q}", fontsize=8, ha="center", weight="bold")
    ax.text(8.6, 2.1, "not\nreachable", fontsize=6.5, ha="center")

    ax.add_patch(FancyArrowPatch((7.2, 5.3), (7.9, 5.3), arrowstyle="->",
                                 mutation_scale=7, lw=0.8))
    ax.text(7.45, 5.5, "quotient", fontsize=6, ha="center")

    fig.savefig(OUT / "prl_spaces.pdf")
    plt.close(fig)
    print("  prl_spaces.pdf")


def fig_crossvalidation() -> None:
    cmp_ = load("verification/spinor_trace_comparison.json")
    br = load("spinor_trace_bridge/results/bridge_validation.json")
    inc = load("results/intrinsic_candidates/degree10_space_incidence.json")
    if not (inc and br):
        missing("prl_crossvalidation", "bridge or incidence certificate absent")
        return
    prime = sorted(inc["per_prime"])[0]
    d = inc["per_prime"][prime]["dims"]
    q = d["A10"] - d["D10"]
    bp = sorted(br["primes"])[0]
    img = br["primes"][bp]["bridge"]["image_dim"]

    deg10 = None
    if cmp_ and cmp_.get("primes"):
        pk = max(cmp_["primes"], key=lambda k: len(cmp_["primes"][k].get("degrees", {})))
        deg10 = cmp_["primes"][pk]["degrees"].get("10")

    fig, ax = plt.subplots(figsize=(COL, 2.0))
    ax.set_xlim(0, 10); ax.set_ylim(0, 5.6); ax.axis("off")

    boxes = [
        (0.2, "contraction\ngraphs", f"dim {d['A10']}"),
        (3.6, "block tensors\n$M$, $N$", f"dim {d['A10']}"),
        (7.0, "gamma-traceless\nbispinors", f"dim {img}"),
    ]
    for x, label, dim in boxes:
        ax.add_patch(Rectangle((x, 3.0), 2.8, 1.9, fc="0.93", ec="k", lw=0.9))
        ax.text(x + 1.4, 4.35, label, fontsize=7, ha="center")
        ax.text(x + 1.4, 3.35, dim, fontsize=7.5, ha="center", weight="bold")

    for x0, x1 in ((3.0, 3.55), (6.4, 6.95)):
        ax.add_patch(FancyArrowPatch((x0, 3.95), (x1, 3.95), arrowstyle="<->",
                                     mutation_scale=7, lw=0.9))
    ax.text(3.28, 4.15, "exact", fontsize=6, ha="center")
    ax.text(6.68, 4.15, "equivariant", fontsize=6, ha="center")

    ax.add_patch(Rectangle((0.2, 1.35), 9.6, 1.25, fc="w", ec="k", lw=1.0,
                           hatch="xxx"))
    ax.text(5.0, 2.15, rf"same quotient $\mathcal{{Q}}_{{10}}$, dim {q}, in all three",
            fontsize=7.5, ha="center")
    note = "spans compared by two-way containment on a common sample registry"
    if deg10 and deg10.get("spans_equal_all_samples"):
        note += f"; degree-10 ranks {deg10['trace_evaluation_rank']} = " \
                f"{deg10['spinor_evaluation_rank']}, holdout validated"
    ax.text(5.0, 1.62, note, fontsize=6, ha="center", style="italic")

    ax.text(5.0, 0.75, "exact arithmetic over $\\mathbb{F}_p$; no tolerance anywhere",
            fontsize=6.5, ha="center")
    fig.savefig(OUT / "prl_crossvalidation.pdf")
    plt.close(fig)
    print("  prl_crossvalidation.pdf")


def main() -> int:
    print("PRL figures:")
    fig_spaces()
    fig_crossvalidation()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
