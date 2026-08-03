#!/usr/bin/env python3
"""Generate the PRD (REVTeX 4.2) manuscript from the JHEP source.

There is one copy of the prose, the mathematics and the appendices, and it lives
in manuscript/jhep/. This script rewrites that source into the two-column APS
form rather than forking it, because two hand-maintained copies of a 45-page
argument diverge silently and the whole point of the surrounding machinery is
that nothing important is maintained twice.

What actually differs between the two journals is small and mechanical:

  * the class and preamble (revtex4-2 with aps,prd,reprint);
  * the abstract, which REVTeX takes as an environment rather than a macro;
  * float widths, since a 0.95-textwidth figure does not fit a PRD column --
    every float is promoted to the full-width starred form and re-scaled;
  * the bibliography style;
  * theorem environments, which REVTeX does not provide.

Everything else -- every section, equation, theorem, table and appendix -- is
carried across verbatim.

    python3 manuscript/prd/build_prd.py
"""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
JHEP = ROOT / "manuscript" / "jhep"
PRD = ROOT / "manuscript" / "prd"

# Displays that cannot be narrowed without losing their point, and so are set
# across both columns. Keep this list short: an equation that fits belongs in a
# column, and the reflex to widen everything produces a two-column paper that
# reads like a one-column paper with gaps in it.
WIDE = [
    "eq:bridgerank",       # three certified identities, aligned in two columns
    "eq:leadingdegree",    # a cases block beside a summation rule
    "eq:closureoperator",  # set-builder with a degree condition
    "eq:rawvsactivated",   # an equality and a strict inclusion, side by side
    "eq:equivariance",     # carries the character and its value
    "eq:jacobian",         # matrix with both index ranges spelled out
    "eq:generators",       # ten trace monomials in a two-row block
]

# eq:sdprojector, eq:bridge and eq:bpidentity were on this list until they were
# rewritten across two lines in the shared source. Narrowing the display is
# always better than widening the page: it costs nothing in the single-column
# version and removes a column break from the two-column one.

PREAMBLE = r"""% ===========================================================================
% DRAFT FOR MENTOR REVIEW -- NOT FOR SUBMISSION
%
% GENERATED FILE. Do not edit: this file is produced from manuscript/jhep by
% manuscript/prd/build_prd.py. Edit the source there and rebuild.
%
% Physical Review D format, REVTeX 4.2, two-column reprint.
% Authorship, affiliations, corresponding author, ORCIDs, licence, DOI and
% arXiv identifier are deliberately unresolved. They are human decisions and
% nothing in this file may be read as having made them.
% ===========================================================================

\documentclass[
  aps,prd,
  reprint,
  amsmath,amssymb,
  nofootinbib,
  longbibliography
]{revtex4-2}

% A PRD column is about 3.4 inches. Long unbreakable technical tokens --
% \texttt{} paths, index-laden symbols -- leave TeX stretching interword space
% past its tolerance, which it reports as an underfull box. A little emergency
% stretch lets it find an acceptable break instead of a badness-10000 line.
\emergencystretch=1.2em

\usepackage{amsthm}
\usepackage{booktabs}
\usepackage{array}
\usepackage{xcolor}
\usepackage{graphicx}
\usepackage{bm}

% REVTeX provides no theorem environments of its own.
\theoremstyle{plain}
\newtheorem{theorem}{Theorem}
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{lemma}[theorem]{Lemma}
\theoremstyle{definition}
\newtheorem{definition}[theorem]{Definition}
\theoremstyle{remark}
\newtheorem{remark}[theorem]{Remark}

\input{generated/numbers.tex}

\newcommand{\Ften}{A_{10}}
\newcommand{\Dten}{D_{10}}
\newcommand{\Qten}{Q_{10}}
\newcommand{\Bten}{B_{10}}
\newcommand{\Pten}{P_{10}}
\newcommand{\Gten}{G_{10}}
\newcommand{\Fp}{\mathbb{F}_p}
\newcommand{\Q}{\mathbb{Q}}
\newcommand{\pending}[1]{\textcolor{red}{\textbf{[#1]}}}

\begin{document}

\title{Exact degree-ten invariants of a self-dual five-form\\
       in ten dimensions}

\author{\pending{Author list pending mentor review}}
\affiliation{\pending{Affiliations pending mentor review}}

\date{\today}
"""

BANNER = r"""
\maketitle

% widetext breaks the two-column flow to set a display across the page, and the
% page builder must then balance the remaining columns. With a rigid bottom it
% cannot, and the horizontal overruns reappear as "Overfull \vbox ... while
% \output is active" -- the same complaint on the other axis. Letting pages end
% short resolves it. This has to come after \maketitle: revtex4-2 issues
% \flushbottom itself, so setting it in the preamble is silently undone.
\raggedbottom

% ---------------------------------------------------------------- banner
\begin{center}
\fcolorbox{red}{yellow!12}{%
\begin{minipage}{0.94\columnwidth}
\centering\vspace{3pt}
{\bfseries\footnotesize DRAFT FOR MENTOR REVIEW --- NOT FOR SUBMISSION}\\[2pt]
{\bfseries\footnotesize AUTHORSHIP AND AFFILIATIONS NOT YET FINALIZED}\\[3pt]
\scriptsize
The author list, author order, corresponding author, affiliations and ORCIDs
are unresolved. No licence has been selected, no DOI has been minted, and
nothing here has been submitted to arXiv or to a journal. Items marked in
\textcolor{red}{\textbf{red}} throughout are pending human decisions.
\vspace{3pt}
\end{minipage}}
\end{center}
\vspace{4pt}
"""


def convert_shared(text: str) -> str:
    """Two-column adjustments applied to appendices and generated tables alike.

    Verbatim is the awkward case: a shell command cannot be hyphenated or
    reflowed, so a clone URL that fits a 6-inch measure simply will not fit a
    3.4-inch column. Setting it smaller is the only honest option short of
    editing the command, and the command has to stay copy-pasteable.
    """
    text = text.replace(r"\begin{verbatim}",
                        "\\begingroup\\scriptsize\n\\begin{verbatim}")
    text = text.replace(r"\end{verbatim}",
                        "\\end{verbatim}\n\\endgroup")
    # Generated tables are sized for a single-column page. Reducing the type
    # size fixes most of them; the widest still overrun. An unconditional
    # \resizebox is the wrong tool -- it scales every table to exactly the text
    # width, which blows a three-row table up into a billboard. The conditional
    # form below shrinks a table only when it is genuinely too wide and leaves
    # the rest at their natural size.
    text = text.replace(
        r"\begin{tabular}",
        "\\footnotesize\n"
        "\\resizebox{\\ifdim\\width>\\linewidth \\linewidth\\else\\width\\fi}{!}{%\n"
        "\\begin{tabular}")
    text = text.replace(r"\end{tabular}", "\\end{tabular}}")
    # The tables declare their own float, so the single- to two-column
    # promotion has to happen here and not only in main.tex. Missing this left
    # every generated table as a single-column float and produced one 223pt
    # overrun that looked, from the log, like a runaway equation.
    text = re.sub(r"\\begin\{table\}(\[[^\]]*\])?", r"\\begin{table*}[tbp]", text)
    text = text.replace(r"\end{table}", r"\end{table*}")

    # Appendix displays are reference material and several are genuinely wider
    # than a column. Promoting *all* of them was tried and is wrong: widetext
    # interrupts column balancing, and a page of short widened displays
    # overflows vertically instead of horizontally -- the same defect moved to
    # the other axis. Only displays with a long source line are promoted, which
    # is a crude proxy for typeset width but errs on the side of leaving things
    # in the column where they belong.
    def widen_if_wide(m: re.Match) -> str:
        block = m.group(1)
        longest = max((len(ln) for ln in block.splitlines()), default=0)
        # Source line length alone is a poor proxy and produced a false
        # negative: a list of ten trace monomials, one short line each, sets as
        # a single very wide row. Horizontal separators are the better signal,
        # since each one is an item continuing on the same typeset line.
        separators = block.count(r"\;") + block.count(r"\quad") \
                   + block.count(r"\qquad") + block.count("&")
        if longest <= 78 and separators < 4:
            return block
        return "\\begin{widetext}\n" + block + "\n\\end{widetext}"

    text = re.sub(r"(\\begin\{equation\}.*?\\end\{equation\})",
                  widen_if_wide, text, flags=re.S)
    return text


def convert(src: str) -> str:
    # --- abstract: macro form -> environment form -------------------------
    m = re.search(r"\\abstract\{%?\n(.*?)\n\}\n\n\\begin\{document\}",
                  src, re.S)
    if not m:
        raise SystemExit("could not locate the JHEP \\abstract{...} block")
    abstract = m.group(1).rstrip().rstrip("%").rstrip()

    # --- body: everything from the banner to \end{document} ---------------
    start = src.index(r"% ---------------------------------------------------------------- banner")
    body = src[start:]
    # Drop the JHEP banner block; the REVTeX one is inserted separately.
    body = re.sub(
        r"% -+ banner\n\\begin\{center\}.*?\\end\{center\}\n\\vspace\{6pt\}\n",
        "", body, count=1, flags=re.S)

    # --- floats: PRD is two-column, so every float goes full width --------
    # A 0.95-textwidth figure is wider than a PRD column. Promoting to the
    # starred form and rescaling is the honest fix; shrinking the figures to
    # column width would make the axis labels unreadable.
    body = body.replace(r"\begin{figure}[htbp]", r"\begin{figure*}[tbp]")
    body = body.replace(r"\end{figure}", r"\end{figure*}")
    body = re.sub(r"\\includegraphics\[width=[0-9.]+\\textwidth\]",
                  r"\\includegraphics[width=0.86\\textwidth]", body)

    # Tables are generated with \begin{table}; the wide ones need table*.
    body = body.replace(r"\begin{table}[", r"\begin{table*}[")
    body = body.replace(r"\end{table}", r"\end{table*}")

    # --- wide displays ----------------------------------------------------
    # A few equations are genuinely wider than a PRD column and cannot be
    # broken without obscuring what they say -- a multi-case grading rule, an
    # aligned block of certified identities. REVTeX's widetext is the intended
    # mechanism: the display spans both columns and the text flows around it.
    # Equations that were merely several short statements strung onto one line
    # were rewritten in the shared source instead, since that improves the
    # single-column version too.
    for label in WIDE:
        pat = re.compile(
            r"(\\begin\{(equation|align)\}(?:(?!\\end\{\2\}).)*?"
            r"\\label\{" + re.escape(label) + r"\}"
            r"(?:(?!\\end\{\2\}).)*?\\end\{\2\})", re.S)
        m = pat.search(body)
        if not m:
            raise SystemExit(f"widetext target not found: {label}")
        body = body[:m.start()] + "\\begin{widetext}\n" + m.group(1) \
             + "\n\\end{widetext}" + body[m.end():]

    # --- bibliography -----------------------------------------------------
    body = body.replace(r"\bibliographystyle{JHEP}",
                        r"\bibliographystyle{apsrev4-2}")

    return (PREAMBLE
            + "\n\\begin{abstract}\n" + abstract + "\n\\end{abstract}\n"
            + BANNER + "\n" + body)


def main() -> int:
    PRD.mkdir(parents=True, exist_ok=True)
    src = (JHEP / "main.tex").read_text()
    (PRD / "main.tex").write_text(convert(src))
    print(f"  wrote {(PRD / 'main.tex').relative_to(ROOT)}")

    # Shared assets are copied, not symlinked, so the directory tars cleanly.
    for sub in ("figures", "tables", "appendices", "generated"):
        dst = PRD / sub
        if dst.is_symlink():
            dst.unlink()
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(JHEP / sub if (JHEP / sub).exists()
                        else ROOT / "manuscript" / sub, dst)
        if sub in ("appendices", "tables"):
            for f in sorted(dst.glob("*.tex")):
                f.write_text(convert_shared(f.read_text()))
    for f in ("references.bib",):
        d = PRD / f
        if d.is_symlink():
            d.unlink()
        shutil.copy2(JHEP / f, d)
    print("  copied figures, tables, appendices, generated, references.bib")
    return 0


if __name__ == "__main__":
    sys.exit(main())
