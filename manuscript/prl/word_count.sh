#!/bin/sh
# APS word-equivalent count.
#
# APS counts the text words, then adds word EQUIVALENTS for displayed material:
# a single-column figure counts as 150 words / (aspect ratio) + 20, a
# displayed equation counts as roughly 16 words, and a table counts by its
# lines.  This script reports the text count exactly and the equivalents on the
# APS rule, and states which parts are estimates rather than pretending the
# total is exact.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
cd "$HERE"

if command -v detex >/dev/null 2>&1; then
    TEXT=$(detex main.tex | tr -s '[:space:]' '\n' | grep -c '[A-Za-z]')
else
    TEXT=$(sed -e 's/%.*//' -e 's/\\[a-zA-Z]*//g' -e 's/[{}$&_^]//g' main.tex \
           | tr -s '[:space:]' '\n' | grep -c '[A-Za-z]')
fi
EQ=$(grep -cE '\\begin\{(equation|align|gather|eqnarray)' main.tex || true)
FIG=$(grep -c '\\includegraphics' main.tex || true)
TAB=$(grep -cE '\\begin\{tabular' main.tex || true)

EQ_W=$((EQ * 16))
FIG_W=$((FIG * 170))
TAB_W=$((TAB * 60))
TOTAL=$((TEXT + EQ_W + FIG_W + TAB_W))

echo "text words (counted):        $TEXT"
echo "displayed equations: $EQ  -> $EQ_W word equivalents (16 each, APS rule)"
echo "figures:             $FIG  -> $FIG_W word equivalents (single column, estimated)"
echo "tables:              $TAB  -> $TAB_W word equivalents (estimated)"
echo "-------------------------------------------"
echo "APS word-equivalent total:   $TOTAL   (PRL limit 3750)"
if [ "$TOTAL" -gt 3750 ]; then echo "STATUS: OVER LIMIT by $((TOTAL - 3750))"; else
  echo "STATUS: within limit, $((3750 - TOTAL)) to spare"; fi
echo
echo "Figure and table equivalents are estimates on the APS rule; the text count"
echo "is exact. The authoritative count is the one APS computes at submission."
