from pathlib import Path
import re,json,hashlib
base=Path(__file__).resolve().parents[1]
root=base/'repair-checkout'
changes=[]
def save(rel,old,new,reason):
    assert old!=new,rel
    (root/rel).write_text(new)
    changes.append({'file':rel,'reason':reason,'before_sha256':hashlib.sha256(old.encode()).hexdigest(),'after_sha256':hashlib.sha256(new.encode()).hexdigest()})
p='manuscript/prd/main.tex';old=(root/p).read_text()
marker=r'\paragraph{Audit scope and inherited results.}'
positions=[m.start() for m in re.finditer(re.escape(marker),old)]
assert len(positions)==2
end=old.index(': revtex4-2 issues',positions[1])
new=old[:positions[1]]+old[end:]
new=new.replace('short resolves it. This has to come after \\maketitle\n\n: revtex4-2 issues','short resolves it. This has to come after \\maketitle: revtex4-2 issues')
assert new.count(marker)==1
save(p,old,new,'Remove duplicated audit paragraph inserted by matching a commented maketitle; restore the original comment.')
p='manuscript/prl/main.tex';old=(root/p).read_text()
new=old.replace('superscriptaddress,nofootinbib]','superscriptaddress,nofootinbib,floatfix]',1)
save(p,old,new,'Apply REVTeX floatfix option recommended by the compiler for a stuck float.')
p='manuscript/prd_letter/references.bib';old=(root/p).read_text();new=old
for key,journal,volume,pages,year,doi in [
    ('Hutomo:2025chiral','JHEP','02','147','2026','10.48550/arXiv.2509.14351'),
    ('Elamaran:2025mlinv','Phys. Rev. D','114','026016','2026','10.1103/ny3m-drnj')]:
    pat=r'@article\{'+re.escape(key)+r',[\s\S]*?\n\}'
    m=re.search(pat,new);assert m
    entry=m.group(0)
    entry=re.sub(r'\n  note\s*=\s*\{[\s\S]*?\}\n', '\n',entry)
    entry=re.sub(r'(year\s*=\s*)\{[^}]*\}',lambda m:m.group(1)+'{'+year+'}',entry)
    entry=re.sub(r'(doi\s*=\s*)\{[^}]*\}',lambda m:m.group(1)+'{'+doi+'}',entry)
    entry=entry[:-2]+f'\n  journal       = {{{journal}}},\n  volume        = {{{volume}}},\n  pages         = {{{pages}}}\n}}'
    new=new[:m.start()]+entry+new[m.end():]
save(p,old,new,'Fill verified publication metadata from the current primary-source literature ledger; remove stale no-journal note and eliminate BibTeX missing-field errors.')
(base/'literature-review/pdf-layout-changes.json').write_text(json.dumps(changes,indent=2)+'\n')
print(json.dumps(changes,indent=2))
