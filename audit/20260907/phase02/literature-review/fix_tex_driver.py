from pathlib import Path
root=Path(__file__).resolve().parents[1]/'repair-checkout'
for f in ['manuscript/main.tex','submission_candidate/main.tex']:
    p=root/f;s=p.read_text()
    a='\\pdfoutput=1\n'
    b='''\\pdfoutput=1
% Select the XeTeX hyperref driver when compiled with Tectonic/XeTeX.
\\ifdefined\\XeTeXversion
  \\PassOptionsToPackage{xetex}{hyperref}
\\fi
'''
    assert a in s
    p.write_text(s.replace(a,b,1))
print('Added engine-conditional hyperref driver selection to the two legacy JHEP-style sources.')
