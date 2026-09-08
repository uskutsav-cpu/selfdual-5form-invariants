from pathlib import Path
import argparse,hashlib,json,math,re,subprocess
from pypdf import PdfReader
from PIL import Image,ImageOps,ImageDraw

ap=argparse.ArgumentParser();ap.add_argument('variant');ap.add_argument('--build-command');args=ap.parse_args()
base=Path(__file__).resolve().parents[1]
work=base/'literature-review'
sources={'main':'manuscript/main.tex','jhep':'manuscript/jhep/main.tex','prd':'manuscript/prd/main.tex',
         'prd_letter':'manuscript/prd_letter/main.tex','prl':'manuscript/prl/main.tex','submission':'submission_candidate/main.tex'}
folder=work/'compiled'/args.variant
pdf=folder/'main.pdf'
render=folder/'qa';render.mkdir(exist_ok=True)
reader=PdfReader(pdf)
pages=[p.extract_text() or '' for p in reader.pages]
(render/'extracted-pages.txt').write_text('\n\n'.join(f'PAGE {i+1}\n'+t for i,t in enumerate(pages)))
flat=' '.join(re.sub(r'(?<=\w)-\s*\n\s*(?=\w)', '', '\n'.join(pages)).split())
build_command=args.build_command or ('literature_29_compile_network_'+args.variant)
build=json.loads((base/'commands'/build_command/'stdout.log').read_text())
log=build.get('log','')
warnings=[x for x in log.splitlines() if re.search(r'warning|overfull|underfull|undefined|missing character',x,re.I)]
# The helper may rerun TeX: retain all warning lines, and also check final PDF text.
checks={'audit_scope':'Audit scope and inherited results.' in flat,
        'source_mismatch':'antisymmetrizers' in flat and 'primary PDF and TeX source' in flat,
        'conditional_identity_scope':'finite holdouts' in flat.replace('-','') and 'polynomial' in flat,
        'no_priority_claim':'No priority claim is made.' in flat,
        'unresolved_reference_pages':[i+1 for i,t in enumerate(pages) if '??' in t],
        'replacement_character_pages':[i+1 for i,t in enumerate(pages) if '\ufffd' in t]}
poppler='/Users/swethasunilkumar/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm'
# These are generated review renders of this PDF, never scientific inputs.
for old_render in list(render.glob('page-*.png'))+list(render.glob('contact-*.png')):
    old_render.unlink()
cmd=[poppler,'-r','62','-png',str(pdf),str(render/'page')]
print('RENDER_ARGV',json.dumps(cmd),flush=True)
subprocess.run(cmd,check=True)
paths=sorted(render.glob('page-*.png'))
assert len(paths)==len(pages),(len(paths),len(pages))
contacts=[]
for block in range(math.ceil(len(paths)/20)):
    part=paths[block*20:(block+1)*20]
    tilew,tileh=220,326
    sheet=Image.new('RGB',(tilew*4,tileh*math.ceil(len(part)/4)),'#d8dde2')
    draw=ImageDraw.Draw(sheet)
    for n,path in enumerate(part):
        img=Image.open(path).convert('RGB');img.thumbnail((210,302))
        x=(n%4)*tilew+(tilew-img.width)//2;y=(n//4)*tileh+18
        sheet.paste(img,(x,y));draw.text(((n%4)*tilew+5,(n//4)*tileh+3),f'{args.variant} p{block*20+n+1}',fill='black')
    target=render/f'contact-{block+1:02d}.png';sheet.save(target);contacts.append(str(target))
# High-resolution opening page for the revised abstract and audit statement.
cmd=[poppler,'-f','1','-l','1','-r','125','-singlefile','-png',str(pdf),str(render/'first-page')]
print('RENDER_ARGV',json.dumps(cmd),flush=True);subprocess.run(cmd,check=True)
result={'variant':args.variant,'source':sources[args.variant],
        'source_sha256':hashlib.sha256((base/'repair-checkout'/sources[args.variant]).read_bytes()).hexdigest(),
        'pdf':str(pdf),'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'page_count':len(pages),
        'text_checks':checks,'build_command':build_command,'compiler_exit_code':build.get('exitCode'),'compiler_warning_lines':warnings,
        'contacts':contacts,'opening_page':str(render/'first-page.png'),
        'visual_review':'pending model inspection of rendered images'}
(render/'qa-manifest.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
