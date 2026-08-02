#!/usr/bin/env python3
"""Assemble review/ferko_delivery/ — the directory Utsav sends to Christian Ferko.

This is the mentor package under delivery names, plus the two documents that
only make sense at delivery time: a one-page README_FIRST and a draft covering
message. It reuses the artifacts built by build_mentor_package.py rather than
recompiling them, so the two directories cannot disagree.

Nothing here decides authorship, licence, DOI or submission, and nothing is
sent. The covering message is a draft for a human to send.

Archives and the zip are byte-reproducible: fixed epoch, normalised member
metadata, gzip and zip without embedded timestamps.

    python3 manuscript/jhep/scripts/build_ferko_delivery.py
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
JHEP = ROOT / "manuscript" / "jhep"
SRC = ROOT / "review" / "mentor_draft"
OUT = ROOT / "review" / "ferko_delivery"

FIXED_DATE = (2025, 1, 1, 0, 0, 0)

# mentor_draft name -> delivery name
RENAMES = {
    "paper.pdf": "Ferko_mentor_review_draft.pdf",
    "paper_source.tar.gz": "Ferko_mentor_review_source.tar.gz",
    "mentor_review_guide.pdf": "Ferko_review_guide.pdf",
    "claim_ledger.pdf": "Ferko_claim_ledger.pdf",
    "figure_book.pdf": "Ferko_figure_book.pdf",
    "reproduction_quickstart.pdf": "Ferko_reproduction_quickstart.pdf",
    "certificate_manifest.json": "Ferko_certificate_manifest.json",
}

# Included in the Downloads zip, at its root.
ZIP_MEMBERS = list(RENAMES.values()) + [
    "README_FIRST.md", "message_to_Ferko.md", "SHA256SUMS",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True,
                          capture_output=True, text=True).stdout.strip()


LEAK_PATTERNS = (b"/Users/", b"/home/", b"swethasunilkumar", b"/private/tmp",
                 b"/Volumes/", b"Mobile Documents")


def strip_pdf_metadata(path: Path) -> None:
    """Strip private metadata from a PDF where possible, and always verify.

    exiftool is used when present, but it is not assumed: tectonic already emits
    PDFs with no Producer/Creator/Author/Title and no build paths. What matters
    for a document leaving the machine is the check, not the tool, so the scan
    below runs either way and raises rather than shipping a leak.
    """
    if shutil.which("exiftool") is not None:
        subprocess.run(
            ["exiftool", "-overwrite_original", "-quiet",
             "-Producer=", "-Creator=", "-Author=", "-Title=",
             "-CreatorTool=", "-DocumentID=", "-InstanceID=",
             str(path)],
            check=True, capture_output=True, text=True)

    blob = path.read_bytes()
    hits = sorted({pat.decode() for pat in LEAK_PATTERNS if pat in blob})
    if hits:
        raise SystemExit(
            f"{path.name} contains machine-specific strings {hits}; refusing to "
            f"ship it. Recompile with a relative \\graphicspath, or install "
            f"exiftool and rerun.")


def build_zip(dest: Path) -> Path:
    """A reproducible zip with the PDF at its root."""
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as zf:
        for name in sorted(ZIP_MEMBERS):
            p = OUT / name
            if not p.exists():
                raise SystemExit(f"zip member missing: {name}")
            info = zipfile.ZipInfo(name, date_time=FIXED_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, p.read_bytes())
    return dest


def main() -> int:
    if not SRC.exists():
        raise SystemExit("run build_mentor_package.py first")
    OUT.mkdir(parents=True, exist_ok=True)
    print("building ferko delivery")

    for src_name, dst_name in RENAMES.items():
        src = SRC / src_name
        if not src.exists():
            raise SystemExit(f"missing mentor-package artifact: {src_name}")
        shutil.copy2(src, OUT / dst_name)
    for name in RENAMES.values():
        if name.endswith(".pdf"):
            strip_pdf_metadata(OUT / name)
    print(f"  copied {len(RENAMES)} artifacts under delivery names")

    commit = git("rev-parse", "HEAD")
    branch = git("rev-parse", "--abbrev-ref", "HEAD")
    manifest = json.loads((OUT / "Ferko_certificate_manifest.json").read_text())

    (OUT / "README_FIRST.md").write_text(readme(commit, branch, manifest))
    (OUT / "message_to_Ferko.md").write_text(message())
    print("  wrote README_FIRST.md, message_to_Ferko.md")

    sums = OUT / "SHA256SUMS"
    lines = [f"{sha256(p)}  {p.name}"
             for p in sorted(OUT.iterdir())
             if p.is_file() and p.name not in {"SHA256SUMS",
                                               "Ferko_mentor_review_package.zip"}]
    sums.write_text("\n".join(lines) + "\n")
    print(f"  wrote SHA256SUMS ({len(lines)} files)")

    zpath = build_zip(OUT / "Ferko_mentor_review_package.zip")
    print(f"  wrote {zpath.name}")
    return 0


def readme(commit: str, branch: str, manifest: dict) -> str:
    return f"""# Read this first

**Exact degree-ten invariants of a self-dual five-form in ten dimensions**

Draft for mentor review. Not submitted anywhere.

- Repository: `github.com/uskutsav-cpu/selfdual-5form-invariants`
- Branch: `{branch}`
- Draft commit: `{commit}`
- Certificates behind the draft: {manifest.get('n_inputs', 'see manifest')},
  hashed in `Ferko_certificate_manifest.json`

## What is in this directory

| file | what it is |
|---|---|
| `Ferko_mentor_review_draft.pdf` | the paper |
| `Ferko_review_guide.pdf` | **start here** — ten questions, in priority order |
| `Ferko_claim_ledger.pdf` | every claim mapped to the certificate behind it |
| `Ferko_figure_book.pdf` | all figures, full page, for reading away from the paper |
| `Ferko_reproduction_quickstart.pdf` | how to re-run everything from a clean clone |
| `Ferko_certificate_manifest.json` | hashes of every certificate the draft rests on |
| `Ferko_mentor_review_source.tar.gz` | LaTeX source; compiles on its own |
| `SHA256SUMS` | hashes of all of the above |

## What to read first

The review guide, section "The ten questions, in priority order". It gives, for
each question, the section and page, the equation, the artifact behind it, what
breaks if it is wrong, and wording we would accept instead.

If you have time for one question only, make it **Q4**, the G-10 stress-tensor
trace. The counterfactual collapses the headline result to zero.

## Which results are exact

Exact over the rationals, not modulo a prime:

- `dim_Q A10 = 14`, `dim_Q D10 = 11`, `dim_Q Q10 = 3`
- `dim_Q(B10 ∩ P10) = 1`, with the explicit integer identity

Exact modulo a prime, carried to characteristic zero by an integer minor:

- generic functional rank **at least 81**, via an explicit 81×81 minor

**Cited, not ours:** the analytic generic upper bound that closes rank 81. We do
not claim all 83 candidates are algebraically independent.

## What needs your judgement

The spinor conventions behind the orientation-fixed bridge; the real-form
statements; whether `D10` is the physically right object; whether the G-10
derivation holds in the formulation the source intends; how `Q10` should be
read; and the framing questions — credit for rank 81, the fairness of the
`B10 ∩ P10` discussion, the title, and what belongs in the body.

## Authorship and submission

**Authorship is not decided.** The title page says so. You are not named as an
author, and nothing in the draft implies you have approved the manuscript, the
results, authorship, credit, submission, or release of the repository.

**Nothing has been submitted.** Not to arXiv, not to JHEP. No DOI, no licence
and no release has been created. Those are decisions for after your review.
"""


def message() -> str:
    return """# Draft message to Christian Ferko

*Not sent. For Utsav to edit and send.*

---

Subject: Draft for your review — exact degree-ten invariants of a self-dual
five-form in D=10

Dear Christian,

I have a complete technical draft I would value your review of, attached as
`Ferko_mentor_review_draft.pdf`.

The work extends the ten-dimensional invariant programme. It determines the
degree-ten Lorentz-invariant structure of a self-dual five-form exactly over the
rationals: the full invariant space has dimension 14, the subspace activated by
the stress-tensor flow has dimension 11, and the quotient is therefore
three-dimensional. It also gives an exact integer identity for the
one-dimensional overlap between the published degree-ten span and the product
sector, and certifies generic functional rank at least 81 with an explicit
81×81 minor. The enumerate–evaluate–relate workflow is prior work and the draft
says so; what is offered here is the exact ten-dimensional realisation, the
tensor–spinor bridge, and the characteristic-zero certificates.

There are four things I would most like your judgement on:

1. whether the orientation-fixed bridge matches the spinor conventions you would
   intend — a square-root branch was selecting the wrong projector at some
   primes, and I fixed the orientation rather than excluding the prime;
2. the G-10 stress-tensor trace argument, which everything at degree ten rests
   on: forcing a degree-two contribution takes the quotient from three to zero;
3. whether `D10` and `Q10` are the physically right objects, and are read
   correctly;
4. how the novelty and credit should be stated — particularly for rank 81, where
   the upper bound is not mine, and for the presentation of the `B10 ∩ P10`
   correction, which I have tried to keep structural rather than critical.

Included alongside the paper: a review guide that lists ten questions in
priority order with the section, equation and supporting artifact for each; a
claim ledger mapping every claim to its certificate; a figure book; and
instructions to reproduce everything from a clean clone.

To be clear about what I am *not* asking: I am making no assumption about
authorship, and nothing has been submitted anywhere. The draft names no authors
and carries a mentor-review banner. Whether you would want to be an author, an
acknowledged mentor, or neither is entirely your call, and I would rather
discuss it than presume it.

Comments directly in the PDF are perfectly fine, or we could work through the
priority list together, whichever is easier for you.

Thank you for taking the time.

Best regards,
Utsav
"""


if __name__ == "__main__":
    sys.exit(main())
