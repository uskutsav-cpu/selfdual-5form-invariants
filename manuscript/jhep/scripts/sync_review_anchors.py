#!/usr/bin/env python3
"""Rewrite the anchored locations in the review documents from main.aux.

The claim ledger and the mentor review guide tell a reviewer where to look:
"theorem 5", "appendix B, p. 26". Those numbers are produced by LaTeX, and every
edit that adds a paragraph can move them. Typing them by hand drifted twice in
one sitting -- once silently, before check_draft.py gained a gate for it, and
once while that gate was being written.

So they are generated. Each location carries its LaTeX label in brackets:

    theorem 5 [`thm:reach`]        <- a float or theorem number
    appendix B, p. 26 [`app:orientation`]   <- a page number

This script resolves each label against main.aux and rewrites the number in
front of it. A "p." immediately before the number means the page is wanted;
anything else means the number of the float, theorem or section. Labels that
main.aux does not know are an error rather than a silent skip, because a stale
label is exactly the failure this is meant to remove.

Run after compiling, before check_draft.py:

    python3 manuscript/jhep/scripts/sync_review_anchors.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
JHEP = ROOT / "manuscript" / "jhep"
AUX = JHEP / "main.aux"

TARGETS = [
    JHEP / "claim_ledger.md",
    ROOT / "review" / "MENTOR_REVIEW_GUIDE.md",
]

# "p. 26 [`app:orientation`]" or "theorem 5 [`thm:reach`]"
ANCHOR = re.compile(r"(p\.\s*)?(\d+(?:\.\d+)?)(\)?\s*\[`)([^`]+)(`\])")


def main() -> int:
    if not AUX.exists():
        raise SystemExit("main.aux not found; compile the manuscript first")
    aux = AUX.read_text()
    number_of = dict(re.findall(r"\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{[0-9]+\}", aux))
    page_of = dict(re.findall(r"\\newlabel\{([^}]+)\}\{\{[^}]*\}\{([0-9]+)\}", aux))

    unknown: list[str] = []
    total = changed = 0

    for path in TARGETS:
        if not path.exists():
            raise SystemExit(f"target missing: {path}")
        text = path.read_text()

        def repl(m: re.Match) -> str:
            nonlocal total, changed
            page_prefix, old, mid, label, tail = m.groups()
            total += 1
            want = page_of.get(label) if page_prefix else number_of.get(label)
            if want is None:
                unknown.append(label)
                return m.group(0)
            if want != old:
                changed += 1
            return f"{page_prefix or ''}{want}{mid}{label}{tail}"

        new = ANCHOR.sub(repl, text)
        if new != text:
            path.write_text(new)
        print(f"  {path.relative_to(ROOT)}")

    if unknown:
        raise SystemExit("labels absent from main.aux: " + ", ".join(sorted(set(unknown))))
    print(f"  {total} anchors resolved, {changed} rewritten")
    return 0


if __name__ == "__main__":
    sys.exit(main())
