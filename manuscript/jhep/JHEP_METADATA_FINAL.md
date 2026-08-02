# JHEP submission metadata — PREPARED, NOT SUBMITTED

The journal requires an arXiv identifier first. Nothing here can proceed until
the arXiv posting has happened and every author has approved it.

## Identical version

The JHEP source archive and the arXiv source archive are built from the same
staged files and contain the **same 25-file set**; both are byte-reproducible.
`release/SUBMISSION_FREEZE.json` records the check.

## Keywords — two to four, from the journal's official list

    Extended Supersymmetry
    p-branes
    Differential and Algebraic Geometry

Confirm against the current official list at submission time; journals revise it.

## Archive requirements, each already satisfied

- master `main.tex` at the archive root;
- `main.bbl` included (BibTeX is used);
- only compilation-required files — 25, no more;
- **no cover letter inside the archive** (it is `manuscript/jhep/cover_letter_final.pdf`);
- archive well under any size limit at ~150 KB.

## Availability statements

    Data availability:  see submission_candidate/data_code_availability.md
    Code availability:  same
    Repository DOI:     [PENDING ZENODO DEPOSITION]

## AI-use declaration

`submission_candidate/ai_use_disclosure.md`. It distinguishes AI-assisted code
generation, debugging, literature discovery, drafting and script execution from
human scientific responsibility, and it does not list any AI system as an author.

## The exact manual sequence

1. Obtain all-author approval of the final PDF.
2. Choose the licence; insert it.
3. Deposit to Zenodo; obtain the version DOI and the concept DOI.
4. Insert the DOI into the manuscript; **rebuild both archives** and re-verify
   their hashes — the DOI changes the bytes.
5. Post to arXiv manually. Record the arXiv identifier.
6. At JHEP, enter the arXiv identifier.
7. Select the keywords above from the official list.
8. Select the data and code availability options.
9. Enter the repository DOI.
10. Upload or import the exact matching version.
11. Read the JHEP compilation report; it must be clean.
12. Confirm as corresponding author.

Steps 1–3 are human decisions. Steps 5, 6 and 12 are authenticated actions no
automation may take.
