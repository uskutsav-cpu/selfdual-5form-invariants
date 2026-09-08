from pathlib import Path
import hashlib,json

root=Path(__file__).resolve().parents[1]/'repair-checkout'
p=root/'manuscript/prd/build_prd.py'
before=s=p.read_text()
a=r'\title{Exact degree-ten invariants of a self-dual five-form'
b=r'\title{An archived degree-ten atlas of a self-dual five-form'
assert a in s
s=s.replace(a,b)
a='''    start = src.index(r"% ---------------------------------------------------------------- banner")
    body = src[start:]'''
b='''    start = src.index(r"% ---------------------------------------------------------------- banner")
    # Preserve the scientific audit scope immediately after the JHEP title.
    audit_scope = src.find(r"\\paragraph{Audit scope and inherited results.}")
    if 0 <= audit_scope < start:
        start = audit_scope
    body = src[start:]'''
assert a in s
s=s.replace(a,b)
p.write_text(s)
print(json.dumps({'path':str(p.relative_to(root)),'before_sha256':hashlib.sha256(before.encode()).hexdigest(),'after_sha256':hashlib.sha256(s.encode()).hexdigest()},indent=2))
