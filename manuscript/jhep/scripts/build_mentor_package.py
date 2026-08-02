#!/usr/bin/env python3
"""Assemble the self-contained mentor-review package.

Produces review/mentor_draft/ containing the paper, a source tarball that
compiles on its own, the supporting documents as PDFs, a certificate manifest and
SHA256SUMS.

Two things this script deliberately does NOT do:

  * It does not include private correspondence, the mentor archive, credentials,
    caches, approval forms or unrelated logs. The source tarball is built from an
    explicit allow-list, not by excluding known-bad patterns, because an
    exclusion list silently ships anything nobody thought to exclude.

  * It does not invent a licence, DOI, author list or approval.

Archives are byte-reproducible: fixed epoch, normalised member metadata, gzip
without an embedded timestamp.

    python3 manuscript/jhep/scripts/build_mentor_package.py
"""

from __future__ import annotations

import gzip
import hashlib
import io
import json
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
JHEP = ROOT / "manuscript" / "jhep"
OUT = ROOT / "review" / "mentor_draft"

FIXED_EPOCH = 1735689600  # 2025-01-01T00:00:00Z, matching the project's archives

# Explicit allow-list for the source tarball. Everything shipped is named here.
SOURCE_MEMBERS = [
    "main.tex", "references.bib", "jheppub.sty", "JHEP.bst",
    "generated/numbers.tex", "generated/identity.tex",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def md_to_pdf(src: Path, dest: Path, title: str) -> None:
    """Render a markdown document to PDF via pandoc + tectonic."""
    subprocess.run(
        ["pandoc", str(src), "-o", str(dest),
         "--pdf-engine=tectonic",
         "-V", "geometry:margin=1in",
         "-V", "colorlinks=true",
         "-M", f"title={title}",
         "-M", "date=",
         "--toc" if src.stat().st_size > 6000 else "--standalone"],
        cwd=ROOT, check=True, capture_output=True, text=True)
    print(f"  wrote {dest.relative_to(ROOT)}")


def build_figure_book() -> Path:
    """One PDF containing every figure, for reading away from the paper."""
    tex = OUT / "_figure_book.tex"
    lines = [
        r"\PassOptionsToPackage{xetex}{hyperref}",
        r"\documentclass[11pt,a4paper]{article}",
        r"\usepackage[margin=1in]{geometry}",
        r"\usepackage{graphicx}\usepackage{hyperref}",
        r"\title{Figure book\\ \large Exact degree-ten invariants of a "
        r"self-dual five-form in ten dimensions}",
        r"\date{}", r"\begin{document}\maketitle",
        r"\begin{center}\fbox{\parbox{0.9\textwidth}{\centering\bfseries "
        r"DRAFT FOR MENTOR REVIEW --- NOT FOR SUBMISSION}}\end{center}",
        r"\vspace{1em}",
        r"\noindent Every figure is generated from a result artifact by "
        r"\texttt{manuscript/jhep/scripts/make\_figures.py}. Output is "
        r"byte-identical across runs.\par\vspace{1em}",
    ]
    for fig in sorted((JHEP / "figures").glob("*.pdf")):
        safe = fig.name.replace("_", r"\_")
        lines += [r"\begin{center}",
                  rf"\includegraphics[width=0.92\textwidth]{{{fig}}}",
                  r"\par\vspace{6pt}",
                  rf"\small\texttt{{{safe}}}",
                  r"\end{center}", r"\clearpage"]
    lines.append(r"\end{document}")
    tex.write_text("\n".join(lines))
    subprocess.run(["tectonic", "-X", "compile", str(tex), "--outdir", str(OUT)],
                   check=True, capture_output=True, text=True)
    produced = OUT / "_figure_book.pdf"
    dest = OUT / "figure_book.pdf"
    produced.replace(dest)
    tex.unlink(missing_ok=True)
    print(f"  wrote {dest.relative_to(ROOT)}")
    return dest


def build_source_tarball() -> Path:
    """A tarball that compiles on its own, from an explicit allow-list."""
    dest = OUT / "paper_source.tar.gz"
    members: list[tuple[str, Path]] = []
    for rel in SOURCE_MEMBERS:
        p = JHEP / rel
        if not p.exists():
            raise SystemExit(f"source member missing: {rel}")
        members.append((f"paper_source/{rel}", p))
    for sub in ("figures", "tables", "appendices"):
        for p in sorted((JHEP / sub).iterdir()):
            if p.is_file() and not p.name.startswith("."):
                members.append((f"paper_source/{sub}/{p.name}", p))

    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w") as tar:
        for arcname, path in sorted(members):
            info = tarfile.TarInfo(arcname)
            data = path.read_bytes()
            info.size = len(data)
            info.mtime = FIXED_EPOCH
            info.mode = 0o644
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            info.type = tarfile.REGTYPE
            tar.addfile(info, io.BytesIO(data))
    with open(dest, "wb") as fh:
        fh.write(gzip.compress(raw.getvalue(), mtime=0))
    print(f"  wrote {dest.relative_to(ROOT)} ({len(members)} members)")
    return dest


def certificate_manifest() -> Path:
    src = ROOT / "results" / "mentor_draft" / "scientific_input_manifest.json"
    data = json.loads(src.read_text())
    dest = OUT / "certificate_manifest.json"
    dest.write_text(json.dumps({
        "schema": 1,
        "note": "Certificates underlying the mentor-review draft. Hashes are of "
                "the artifacts as read during the build.",
        "commit": data.get("commit"),
        "n_inputs": data.get("n_inputs"),
        "clean": data.get("clean"),
        "inputs": data.get("inputs"),
    }, indent=1, sort_keys=True) + "\n")
    print(f"  wrote {dest.relative_to(ROOT)}")
    return dest


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    print("building mentor package")

    shutil.copy2(JHEP / "main.pdf", OUT / "paper.pdf")
    print(f"  wrote {(OUT / 'paper.pdf').relative_to(ROOT)}")

    md_to_pdf(JHEP / "claim_ledger.md", OUT / "claim_ledger.pdf",
              "Claim ledger --- mentor-review draft")
    md_to_pdf(ROOT / "review" / "MENTOR_REVIEW_GUIDE.md",
              OUT / "mentor_review_guide.pdf", "Mentor review guide")
    md_to_pdf(ROOT / "docs" / "MENTOR_DRAFT_QUICKSTART.md",
              OUT / "reproduction_quickstart.pdf", "Reproduction quickstart")

    build_figure_book()
    build_source_tarball()
    certificate_manifest()

    # SHA256SUMS last, over everything else in the directory.
    sums = OUT / "SHA256SUMS"
    lines = [f"{sha256(p)}  {p.name}"
             for p in sorted(OUT.iterdir())
             if p.is_file() and p.name != "SHA256SUMS"]
    sums.write_text("\n".join(lines) + "\n")
    print(f"  wrote {sums.relative_to(ROOT)} ({len(lines)} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
