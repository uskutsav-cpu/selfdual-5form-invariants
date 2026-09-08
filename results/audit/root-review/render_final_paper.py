from pathlib import Path
import hashlib
import json
import subprocess
from PIL import Image, ImageDraw
import pdfplumber

A = Path(__file__).resolve().parents[1]
directory = A / "root-review/paper-final"
pdf = directory / "manuscript.pdf"
subprocess.run(["/opt/homebrew/bin/pdftoppm", "-r", "90", "-png", str(pdf), str(directory / "page")], check=True)
images = sorted(directory.glob("page-*.png"))
sheet = Image.new("RGB", (1400, ((len(images)+3)//4)*490), "#bbbbbb")
draw = ImageDraw.Draw(sheet)
for k, path in enumerate(images):
    with Image.open(path) as im:
        im.thumbnail((330,460))
        x,y = (k%4)*350+10,(k//4)*490+24
        sheet.paste(im,(x,y))
        draw.text((x,y-18),str(k+1),fill="black")
sheet.save(directory / "contact-sheet.png")
with pdfplumber.open(pdf) as doc:
    pages = [p.extract_text() or "" for p in doc.pages]
assert not any("??" in p or "\ufffd" in p for p in pages)
log = json.loads((A / "commands/compile-paper-final/stdout.log").read_text())["log"]
record = {"pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(), "pages": len(pages),
          "missing_reference_markers": 0, "compiler_log": log,
          "rendered_pages": list(range(1,len(pages)+1)), "visual_review": "pending"}
(directory / "text.txt").write_text("\n\f\n".join(pages))
(A / "root-review/final-paper-qa.json").write_text(json.dumps(record,indent=2)+"\n")
print(json.dumps({k:v for k,v in record.items() if k!='compiler_log'},indent=2))
