#!/bin/sh
# Build the Letter, End Matter and Supplemental Material.
# Regenerates every number, table and figure from artifacts first, so a stale
# value cannot survive a build.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/../.." && pwd)
PY=${PYTHON:-python}

"$PY" "$ROOT/manuscript/scripts/make_numbers.py"
"$PY" "$ROOT/manuscript/scripts/make_tables.py"
"$PY" "$ROOT/manuscript/scripts/make_figures.py"

cd "$HERE"
for pass in 1 2 3; do
    pdflatex -interaction=nonstopmode main.tex >/dev/null 2>&1 || true
    [ "$pass" = 1 ] && (bibtex main >/dev/null 2>&1 || true)
done
pdflatex -interaction=nonstopmode supplemental.tex >/dev/null 2>&1 || true
pdflatex -interaction=nonstopmode supplemental.tex >/dev/null 2>&1 || true

echo "errors:            $(grep -cE '^! ' main.log || true)"
echo "undefined refs:    $(grep -cE 'Reference.*undefined' main.log || true)"
echo "undefined cites:   $(grep -cE 'Citation.*undefined' main.log || true)"
echo "overfull boxes:    $(grep -c Overfull main.log || true)"
grep -oE "Output written on main.pdf \([0-9]+ pages" main.log | tail -1 || true
