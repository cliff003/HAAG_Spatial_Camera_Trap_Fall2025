#!/usr/bin/env bash
# Compress a PDF with Ghostscript, then print size/page stats.
# Usage: ./compress_pdf.sh input.pdf [output.pdf] [quality]
#   quality: screen | ebook | printer | prepress  (default: ebook)

set -euo pipefail

input="${1:?usage: $0 input.pdf [output.pdf] [quality]}"
output="${2:-${input%.pdf}_compressed.pdf}"
quality="${3:-ebook}"

if [[ ! -f "$input" ]]; then
    echo "error: input not found: $input" >&2
    exit 1
fi

case "$quality" in
    screen|ebook|printer|prepress) ;;
    *) echo "error: quality must be one of: screen ebook printer prepress" >&2; exit 1 ;;
esac

echo "compressing: $input -> $output (quality=$quality)"
gs -sDEVICE=pdfwrite \
   -dCompatibilityLevel=1.5 \
   -dPDFSETTINGS="/$quality" \
   -dNOPAUSE -dQUIET -dBATCH \
   -sOutputFile="$output" \
   "$input"

in_bytes=$(stat -c%s "$input")
out_bytes=$(stat -c%s "$output")
in_mb=$(awk "BEGIN{printf \"%.2f\", $in_bytes/1048576}")
out_mb=$(awk "BEGIN{printf \"%.2f\", $out_bytes/1048576}")
ratio=$(awk "BEGIN{printf \"%.1f\", (1-$out_bytes/$in_bytes)*100}")

pages=$(gs -q -dNODISPLAY -dNOSAFER -c "($output) (r) file runpdfbegin pdfpagecount = quit" 2>/dev/null || echo "?")

echo "---"
echo "input  : ${in_mb} MB"
echo "output : ${out_mb} MB"
echo "saved  : ${ratio}%"
echo "pages  : ${pages}"
