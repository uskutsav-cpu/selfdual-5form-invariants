#!/usr/bin/env python3
"""Emit the B10-cap-P10 generator as a LaTeX equation, from the artifact.

The identity is the concrete content of "the published span contains one product
direction". Its coefficients are large and specific, so it is generated rather
than typed.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "results" / "degree10" / "B10_P10_intersection_generator.json"
OUT = ROOT / "manuscript" / "generated" / "identity.tex"


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if not SRC.exists():
        OUT.write_text("\\ARTIFACTMISSING{B10capP10 generator}\n")
        print("artifact missing; emitted a loud marker")
        return 0
    g = json.loads(SRC.read_text())
    pub, atl = g["published_combination_integer"], g["atlas_combination_integer"]

    def signed(items, fmt):
        out = ""
        for i, (k, c) in enumerate(items):
            sign = "-" if c < 0 else ("+" if i else "")
            mag = "" if abs(c) == 1 else str(abs(c))
            out += f" {sign} {mag}\\,{fmt(k)}"
        return out.strip()

    def pubfmt(k):        # P10_05 -> I^{(5)}
        return f"I^{{({int(k.split('_')[1])})}}"

    def atlfmt(k):        # I4_1*I6_1 -> I^{(4)}_{1} I^{(6)}_{1}
        parts = k.split("*")
        return "".join("I^{(%s)}_{%s}" % tuple(p.replace("I", "").split("_"))
                       for p in parts)

    lhs = signed(list(pub.items()), pubfmt)
    rhs = signed(list(atl.items()), atlfmt)
    OUT.write_text(f"{lhs} \\;=\\; {rhs}\n")
    print(f"wrote {OUT.relative_to(ROOT)}: {lhs} = {rhs}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
