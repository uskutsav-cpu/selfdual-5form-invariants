"""Assemble the arXiv and journal source archives, and verify they compile alone.

The archives must contain only what is needed to build the PDF.  This script
copies that set into a temporary tree, builds it there from scratch, and refuses
to produce the archives if the isolated build is not clean.  Building in place
would not catch a file that the manuscript needs but the archive omits.

Nothing is uploaded.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript"
OUT = ROOT / "submission_candidate"

#: Everything the PDF needs, and nothing else.
SOURCES = ["main.tex", "references.bib", "jheppub.sty", "JHEP.bst"]
DIRS = ["appendices", "generated", "tables"]

TEX = Path.home() / "Library" / "TinyTeX" / "bin" / "universal-darwin"


def figures_used() -> list[str]:
    """Only the figures actually included, so unused files are not shipped."""
    text = "\n".join(p.read_text() for p in MANUSCRIPT.rglob("*.tex"))
    return sorted(set(re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", text)))


def stage(tmp: Path) -> list[str]:
    staged = []
    for name in SOURCES:
        src = MANUSCRIPT / name
        if not src.exists():
            raise SystemExit(f"missing required source: {name}")
        shutil.copy2(src, tmp / name)
        staged.append(name)
    for d in DIRS:
        src = MANUSCRIPT / d
        if src.exists():
            shutil.copytree(src, tmp / d)
            staged += [str(p.relative_to(tmp)) for p in (tmp / d).rglob("*") if p.is_file()]
    figdir = tmp / "figures"
    figdir.mkdir(exist_ok=True)
    for f in figures_used():
        cand = (ROOT / "figures" / Path(f).name)
        if not cand.exists() and not cand.with_suffix(".pdf").exists():
            raise SystemExit(f"figure referenced but not found: {f}")
        src = cand if cand.exists() else cand.with_suffix(".pdf")
        shutil.copy2(src, figdir / src.name)
        staged.append(f"figures/{src.name}")
    return staged


def build(tmp: Path) -> tuple[bool, dict]:
    env = dict(os.environ)
    env["PATH"] = f"{TEX}:{env.get('PATH','')}"
    log = ""
    for i in range(3):
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "main.tex"],
                       cwd=tmp, env=env, capture_output=True, text=True)
        if i == 0:
            subprocess.run(["bibtex", "main"], cwd=tmp, env=env,
                           capture_output=True, text=True)
    logfile = tmp / "main.log"
    if logfile.exists():
        log = logfile.read_text(errors="replace")
    diag = {
        "errors": len(re.findall(r"^! ", log, re.MULTILINE)),
        "undefined_citations": len(re.findall(r"Citation.*undefined", log)),
        "undefined_references": len(re.findall(r"Reference.*undefined", log)),
        "overfull_boxes": len(re.findall(r"Overfull", log)),
        "pdf_produced": bool(re.search(r"Output written on main\.pdf", log)),
    }
    m = re.search(r"Output written on main\.pdf \((\d+) pages", log)
    diag["pages"] = int(m.group(1)) if m else None
    ok = (diag["errors"] == 0 and diag["undefined_citations"] == 0
          and diag["undefined_references"] == 0 and diag["pdf_produced"])
    return ok, diag


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--allow-dirty-build", action="store_true")
    args = ap.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        staged = stage(tmp)
        ok, diag = build(tmp)
        print("isolated build:", json.dumps(diag))
        if not ok and not args.allow_dirty_build:
            print("refusing to package: the isolated build is not clean")
            return 1

        shutil.copy2(tmp / "main.pdf", OUT / "compiled_manuscript.pdf")
        for name in SOURCES:
            shutil.copy2(tmp / name, OUT / name)
        for d in DIRS:
            if (tmp / d).exists():
                shutil.copytree(tmp / d, OUT / d, dirs_exist_ok=True)
        shutil.copytree(tmp / "figures", OUT / "figures", dirs_exist_ok=True)

        keep = set(staged) | {"main.bbl"}
        tarpath = OUT / "arxiv_source.tar.gz"
        with tarfile.open(tarpath, "w:gz") as tf:
            for rel in sorted(keep):
                p = tmp / rel
                if p.exists():
                    tf.add(p, arcname=rel)
        zippath = OUT / "jhep_source.zip"
        with zipfile.ZipFile(zippath, "w", zipfile.ZIP_DEFLATED) as zf:
            for rel in sorted(keep):
                p = tmp / rel
                if p.exists():
                    zf.write(p, arcname=rel)

    manifest = {
        "build": diag,
        "files": sorted(keep),
        "arxiv_source_sha256": sha256(OUT / "arxiv_source.tar.gz"),
        "jhep_source_sha256": sha256(OUT / "jhep_source.zip"),
        "pdf_sha256": sha256(OUT / "compiled_manuscript.pdf"),
        "contents_are_equivalent": True,
        "note": ("Both archives contain the identical file set; they differ only "
                 "in container format, as the two submission workflows require."),
        "uploaded": False,
    }
    (OUT / "package_manifest.json").write_text(json.dumps(manifest, indent=1))
    print(f"packaged -> {OUT.relative_to(ROOT)} "
          f"({len(keep)} files, {diag['pages']} pages)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
